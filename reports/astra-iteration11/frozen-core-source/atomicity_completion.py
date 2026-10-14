"""Source-derived conditional deduplication judgments, never runtime races.

This adapter connects the existing region/predicate extractor with default
dependency assembly, logical resources and guarded writes.  The small solver
consumes only extracted operations; policy may select source and register
models/invariants, but cannot provide paths, predicates, states or schedules.
"""
from __future__ import annotations

from collections import deque
from copy import deepcopy
import hashlib
import json
import posixpath
from typing import Any

from . import atomicity_analysis as aa
from .semantic_sources import SemanticSources
from .models import GraphSnapshot
from .models import Evidence, Finding

VERSION = "source-derived-atomicity-completion-1"
MODEL_IDS = (
    "ecmascript-literal-module-import-v1",
    "ecmascript-plain-json-record-array-v1",
    "ecmascript-source-closed-instance-v1",
    "node-logical-path-identity-v1",
    "directory-owner-lock-normal-operation-v1",
    "atomic-file-normal-publish-v1",
    "finite-queue-interleaving-v1",
    "node-source-hash-key-v1",
)
_MAX_STATES = 4096
_MAX_AST_NODES = 100_000
_ALLOWED_BINDINGS = {"snapshot_resolved", "source_lexical_declaration_relation"}


def unwrap(node: Any) -> Any:
    """Source normal-completion expression; awaiting is recorded separately."""
    return aa._unwrap(node)


def _dense_members(node: Any) -> list[Any] | None:
    if node is None or node.type not in {"array","array_pattern"}:return None
    members=aa._children(node)
    if not members or any(item.type in {"spread_element","rest_pattern","assignment_pattern"} for item in members):return None
    tokens=[child for child in node.children if child.type!="comment" and child.type not in {"[","]"}]
    expect_item=True;seen=0
    for token in tokens:
        if expect_item:
            if not token.is_named or token.type==",":return None
            seen+=1;expect_item=False
        else:
            if token.type!=",":return None
            expect_item=True
    return members if seen==len(members) else None


def _render_key_model(document:Any,function:Any,context:aa._Analysis,record:dict)->str|None:
    """Interpret only captured data reads/||/string templates in our model.

    No target Python/JS function is executed; this is the analyzer's finite
    standard-data expression domain, used to exhibit a predicate distinction.
    """
    formal=aa._param_node(function,0);environment={context.identity(document,formal).get("declaration_id"):record}
    unknown=object();steps=0
    def value(node:Any)->Any:
        nonlocal steps
        steps+=1
        if steps>128:return unknown
        node=unwrap(node)
        if node is None:return unknown
        if node.type in {"identifier","shorthand_property_identifier"}:return environment.get(context.identity(document,node).get("declaration_id"),unknown)
        if node.type=="member_expression":
            base=value(node.child_by_field_name("object"));key=document.text(node.child_by_field_name("property"))
            return base.get(key,None) if isinstance(base,dict) else None if base is None and any(child.type=="optional_chain" for child in node.children) else unknown
        if node.type=="binary_expression" and aa._op(document,node)=="||":
            left=value(node.child_by_field_name("left"))
            return unknown if left is unknown else left if left else value(node.child_by_field_name("right"))
        if node.type=="template_string":
            parts=[]
            for child in aa._children(node):
                if child.type=="string_fragment":
                    fragment=document.text(child)
                    if "\\" in fragment:return unknown
                    parts.append(fragment)
                elif child.type=="template_substitution" and len(aa._children(child))==1:
                    selected=value(aa._children(child)[0])
                    if not isinstance(selected,str):return unknown
                    parts.append(selected)
                else:return unknown
            return "".join(parts)
        literal=aa._literal(document,node)
        return literal if isinstance(literal,str) else unknown
    returned=None
    for statement in aa._children(function.child_by_field_name("body")):
        if statement.type=="lexical_declaration":
            for declaration in aa._children(statement):
                if declaration.type!="variable_declarator":return None
                environment[context.identity(document,declaration.child_by_field_name("name")).get("declaration_id")]=value(declaration.child_by_field_name("value"))
        elif statement.type=="return_statement":returned=value(_return_expr(statement))
        else:return None
    return returned if isinstance(returned,str) else None


def _digest(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=True,
        separators=(",", ":"), allow_nan=False).encode()).hexdigest()


def validate_completion(value: Any) -> None:
    if not isinstance(value, dict) or set(value) != {"models", "invariant"}:
        raise ValueError("atomicity completion accepts only models and invariant; source selectors remain in the atomicity rule")
    models = value["models"]
    if not isinstance(models, list) or len(models) != len(MODEL_IDS) or set(models) != set(MODEL_IDS):
        raise ValueError("atomicity completion requires the exact registered, versioned models")
    invariant = value["invariant"]
    if not isinstance(invariant, dict) or set(invariant) != {"kind", "project_path", "key_path"}:
        raise ValueError("invariant cannot contain extracted predicates, status literals, transitions or precomputed interleavings")
    if invariant["kind"] != "reuse_nonterminal_same_project_key":
        raise ValueError("unregistered product invariant")
    for name in ("project_path", "key_path"):
        path = invariant[name]
        if not isinstance(path, list) or not path or len(path) > 8 or any(not isinstance(key, str) or not key.isidentifier() for key in path):
            raise ValueError("invariant paths must be finite data-property paths")


def _node_at(document: Any, location: dict | None) -> Any:
    if not isinstance(location, dict) or location.get("file") != document.source.path or location.get("source_hash") != document.source.hash:
        return None
    lo, hi = location.get("start_byte"), location.get("end_byte")
    return next((node for node in aa._walk(document.tree.root_node)
        if node.start_byte == lo and node.end_byte == hi and node.type == location.get("node_type", node.type)), None)


def _returns(function: Any) -> list[Any]:
    return [node for node in aa._walk(function.child_by_field_name("body"), skip_functions=True) if node.type == "return_statement"]


def _return_expr(statement: Any) -> Any:
    values = aa._children(statement)
    return unwrap(values[0]) if len(values) == 1 else None


def _pairs(document: Any, obj: Any, *, members: list[Any] | None = None) -> tuple[dict[str, Any], bool]:
    obj = unwrap(obj)
    if obj is None or obj.type != "object":
        return {}, False
    fields: dict[str, Any] = {}
    closed = True
    for child in aa._children(obj) if members is None else members:
        if child.type == "shorthand_property_identifier":
            key, value = document.text(child), child
        elif child.type == "pair":
            key_node = child.child_by_field_name("key")
            key = document.text(key_node) if key_node is not None and key_node.type in {"property_identifier", "identifier"} else aa._literal(document, key_node)
            value = child.child_by_field_name("value")
        else:
            closed = False
            continue
        if not isinstance(key, str) or key == "__proto__" or key in fields or value is None:
            closed = False
            continue
        fields[key] = unwrap(value)
    return fields, closed


def _same_path(context: aa._Analysis, document: Any, value: Any, root: Any, keys: list[str]) -> bool:
    path = aa._path_of(document, value)
    return bool(path is not None and path[1:] == list(keys) and context.same(document, value, root))


def _inside_argument(call: Any, index: int, node: Any) -> bool:
    argument=aa._argument(call,index)
    return bool(argument is not None and node is not None and argument.start_byte<=node.start_byte and node.end_byte<=argument.end_byte)


def _ordinary_return_copy(document: Any, statement: Any, formal: Any, context: aa._Analysis, protected_keys: set[str]) -> dict:
    expression=_return_expr(statement)
    result={"state":"unknown", "return":document.location(statement), "kind":None, "suffix_keys":[]}
    if expression is not None and context.exact(document,expression,formal):
        result.update(state="source_current_formal_reference",kind="reference")
        return result
    if expression is None or expression.type!="object":
        return result
    children=aa._children(expression)
    if not children or children[0].type!="spread_element" or len(aa._children(children[0]))!=1 or not context.exact(document,aa._children(children[0])[0],formal):
        return result
    keys=[]
    for child in children[1:]:
        if child.type!="pair":
            return result
        key_node=child.child_by_field_name("key")
        if key_node is None or key_node.type not in {"property_identifier","identifier"}:
            return result
        key=document.text(key_node)
        if key=="__proto__" or key in protected_keys:
            return result
        keys.append(key)
    result.update(state="source_ordered_disjoint_return_copy",kind="copy",suffix_keys=keys,
        spread=document.location(children[0]),copy_expression=document.location(expression))
    return result


def _excluded_helper_copy(document: Any, assignment: Any, entrypoint: Any) -> bool:
    if assignment is None:return False
    owner=next((node for node in aa._ancestors(assignment) if node.type=="method_definition"),None)
    if owner is None or owner is entrypoint:return False
    name=document.text(owner.child_by_field_name("name"))
    cls=next((node for node in aa._ancestors(owner) if node.type=="class_declaration"),None)
    calls=[call for call in aa._calls(document,cls.child_by_field_name("body"),nested=True)
        if aa._path_of(document,call.child_by_field_name("function"))==["this",name]] if cls is not None else []
    if not calls:return False
    for call in calls:
        statement=next((node for node in aa._ancestors(call) if node.parent is not None and node.parent.type=="statement_block"),None)
        if statement is None:return False
        siblings=aa._children(statement.parent)
        position=next((index for index,node in enumerate(siblings) if node.id==statement.id),None)
        if position is None or position+1>=len(siblings) or siblings[position+1].type!="continue_statement":return False
    return True


def _search_transitions(operations: list[dict], terminal: list[str], *, descriptions_equal: bool,
        include_scheduler: bool, include_rollback: bool = True) -> dict:
    """Breadth-first exploration of extracted finite operations, not target execution.

    Queue rows = (abstract request id, status, version). A request may perform
    facade precheck then a protected authoritative check/commit.  Scheduler
    captures an existing row and applies exactly the extracted status/version
    guard.  Transition labels always contain authenticated operation IDs.
    """
    bykind: dict[str,list[dict]]={}
    for operation in operations:bykind.setdefault(operation["kind"],[]).append(operation)
    needed=("facade_active_precheck","protected_find_or_insert")
    if any(len(bykind.get(kind,[]))!=1 for kind in needed):
        return {"state":"unknown","gap":"required extracted operation is missing or ambiguous"}
    precheck=bykind[needed[0]][0];authority=bykind[needed[1]][0]
    scheduler=bykind.get("guarded_status_update",[])
    capture=bykind.get("scheduler_candidate_selection",[])
    if include_scheduler and (len(scheduler)!=1 or len(capture)!=1):return {"state":"unknown","gap":"scheduler operation/candidate selection is missing or ambiguous"}
    update=scheduler[0] if include_scheduler else None
    rollbacks=bykind.get("conditional_rollback_status",[])
    initial_status=authority["initial_status"]
    allowed_inner=set(authority["matching_statuses"])
    initial=((),(0,0),None,0)
    pending=deque([(initial,[])])
    visited={initial}
    duplicate=None;reuse_paths=[];guard_rejections=[];rollback_paths=[]
    terminal_set=set(terminal)
    truncated=False

    def push(state: tuple,trace: list[dict],event: dict) -> None:
        nonlocal truncated
        if state in visited:return
        if len(visited)>=_MAX_STATES:truncated=True;return
        visited.add(state);pending.append((state,[*trace,event]))

    while pending:
        state,trace=pending.popleft()
        rows,pcs,candidate,scheduler_pc=state
        active=[row for row in rows if row[1] not in terminal_set]
        if len(active)>1 and duplicate is None:
            duplicate={"steps":trace,"resulting_rows":[{"request":row[0],"status":row[1],"abstract_version":row[2]} for row in rows],
                "violated_invariant":"more than one nonterminal row with the same project and idempotency key"}
        for request in (0,1):
            if pcs[request]==0:
                reuse=next((row for row in rows if row[1] not in terminal_set),None)
                stage=2 if reuse is not None else 1
                newpcs=tuple(stage if index==request else value for index,value in enumerate(pcs))
                event={"actor":"request-"+str(request),"operation_id":precheck["operation_id"],"operation":"facade_precheck",
                    "outcome":"reuse_existing_nonterminal" if reuse is not None else "continue_to_authority","observed_rows":len(rows)}
                if reuse is not None and len(reuse_paths)<8:reuse_paths.append({"category":"facade_sees_nonterminal_reuses","steps":[*trace,event]})
                push((rows,newpcs,candidate,scheduler_pc),trace,event)
            elif pcs[request]==1:
                reusable=next((row for row in rows if row[1] in allowed_inner and (descriptions_equal or row[0]==request)),None)
                newrows=rows if reusable is not None else (*rows,(request,initial_status,0))
                newpcs=tuple(2 if index==request else value for index,value in enumerate(pcs))
                event={"actor":"request-"+str(request),"operation_id":authority["operation_id"],"operation":"protected_check_and_normal_commit",
                    "outcome":"reuse_matching_pending" if reusable is not None else "insert_new_row","inner_matching_statuses":sorted(allowed_inner),
                    "compound_key_relation":"same" if descriptions_equal else "description_distinct"}
                if reusable is not None and len(reuse_paths)<8:reuse_paths.append({"category":"authority_pending_compound_key_reuses","steps":[*trace,event]})
                push((newrows,newpcs,candidate,scheduler_pc),trace,event)
        if update is not None and scheduler_pc==0:
            for row in rows:
                if row[1]!=update["from_status"]:continue
                event={"actor":"scheduler","operation_id":capture[0]["operation_id"],"operation":"capture_eligible_pending_candidate",
                    "request":row[0],"captured_status":row[1],"captured_version":row[2],
                    "condition":"actual readiness/capacity/leader gates admit this captured candidate"}
                push((rows,pcs,(row[0],row[1],row[2]),1),trace,event)
        elif update is not None and scheduler_pc==1 and candidate is not None:
            row=next((value for value in rows if value[0]==candidate[0]),None)
            if row is not None and row[1]==update["from_status"] and row[2]==candidate[2]:
                newrows=tuple((value[0],update["to_status"],value[2]+1) if value[0]==candidate[0] else value for value in rows)
                event={"actor":"scheduler","operation_id":update["operation_id"],"operation":"guarded_status_normal_commit",
                    "from_status":row[1],"to_status":update["to_status"],"request":row[0],"version_guard":"matched"}
                push((newrows,pcs,(row[0],update["to_status"],row[2]+1),2),trace,event)
            else:
                event={"actor":"scheduler","operation_id":update["operation_id"],"operation":"guarded_status_update_rejected",
                    "reason":"status/version no longer matches captured candidate"}
                if len(guard_rejections)<8:guard_rejections.append({"steps":[*trace,event]})
                push((rows,pcs,candidate,4),trace,event)
        elif update is not None and scheduler_pc==2 and candidate is not None and include_rollback:
            for rollback in rollbacks:
                row=next((value for value in rows if value[0]==candidate[0]),None)
                if row is None or row[1]!=update["to_status"] or row[2]!=candidate[2]:continue
                newrows=tuple((value[0],rollback["to_status"],value[2]+1) if value[0]==candidate[0] else value for value in rows)
                event={"actor":"scheduler","operation_id":rollback["operation_id"],"operation":"conditional_dispatch_failure_rollback",
                    "request":row[0],"to_status":rollback["to_status"],"condition":"dispatch fails before inbox is published and rollback guard still matches"}
                if len(rollback_paths)<8:rollback_paths.append({"steps":[*trace,event]})
                push((newrows,pcs,candidate,3),trace,event)
    return {"state":"bounded_source_transition_exploration_complete" if not truncated else "unknown_budget_exceeded",
        "states_explored":len(visited),"state_budget":_MAX_STATES,"truncated":truncated,"duplicate_witness":duplicate,
        "refutations":{"observed_reuse_paths":reuse_paths,"guard_rejection_paths":guard_rejections,"rollback_paths":rollback_paths},
        "value_assignment":{"same_project":True,"same_idempotency_key":True,"descriptions_equal":descriptions_equal,
            "ids_distinct":"successful generated IDs are distinct; an explicit runtime condition"},
        "scheduler_enabled":include_scheduler,"target_code_executed":False,
        "scope":"finite abstract transition system under registered normal read/lock/commit semantics; not actual concurrency, reachability of environment gates or all-writer analysis"}


class _CollectionOrigins:
    """Finite AST membership provenance through real filters, helpers and pushes.

    This computes possible element origins, not values, eligibility or timing.
    An arbitrary helper return cannot be accepted as a source collection.
    """
    def __init__(self, adapter: Any, document: Any, class_name: str, fresh_source: dict):
        self.adapter,self.ctx,self.doc,self.class_name=adapter,adapter.context,document,class_name
        self.fresh_source=fresh_source;self.relations=[];self.gaps=[];self.steps=0;self.active=[]

    def key(self,node:Any)->str|None:
        identity=self.ctx.lexical(self.doc).resolve(node) if node is not None and node.type in {"identifier","shorthand_property_identifier","shorthand_property_identifier_pattern"} else self.ctx.identity(self.doc,node)
        return identity.get("declaration_id") if identity.get("state")=="unique" and identity.get("identity_complete") else None

    @staticmethod
    def unknown()->dict:return {"kind":"unknown"}

    @staticmethod
    def item()->dict:return {"kind":"item","origins":["captured-logical-queue-entry"]}

    def collection(self,element:dict|None=None)->dict:
        return {"kind":"collection","element":element or {"kind":"empty"}}

    def join(self,left:dict,right:dict)->dict:
        if left==right:return left
        if left.get("kind")=="empty":return right
        if right.get("kind")=="empty":return left
        if left.get("kind")!=right.get("kind"):return self.unknown()
        if left.get("kind")=="item":return {"kind":"item","origins":sorted(set(left["origins"]+right["origins"]))}
        if left.get("kind")=="collection":return self.collection(self.join(left["element"],right["element"]))
        if left.get("kind")=="record":return {"kind":"record","fields":{key:self.join(left["fields"].get(key,self.unknown()),right["fields"].get(key,self.unknown())) for key in set(left["fields"])|set(right["fields"])}}
        return self.unknown()

    def merge(self,*envs:dict)->dict:
        result={}
        for env in envs:
            for key,value in env.items():result[key]=self.join(result.get(key,value),value)
        return result

    def bind(self,pattern:Any,value:dict,env:dict)->None:
        if pattern is None:return
        if pattern.type in {"required_parameter","optional_parameter"}:pattern=pattern.child_by_field_name("pattern") or pattern.child_by_field_name("name")
        if pattern is None:return
        if pattern.type in {"identifier","shorthand_property_identifier_pattern","shorthand_property_identifier"}:
            key=self.key(pattern)
            if key:env[key]=value
        elif pattern.type=="object_pattern":
            for part in aa._children(pattern):
                if part.type=="shorthand_property_identifier_pattern":name=self.doc.text(part);target=part
                elif part.type=="pair_pattern":name=self.doc.text(part.child_by_field_name("key"));target=part.child_by_field_name("value")
                else:continue
                self.bind(target,value.get("fields",{}).get(name,self.unknown()),env)
        elif pattern.type in {"lexical_declaration","variable_declaration"}:
            declarations=[part for part in aa._children(pattern) if part.type=="variable_declarator"]
            if len(declarations)==1:self.bind(declarations[0].child_by_field_name("name"),value,env)

    def evaluate(self,node:Any,env:dict,depth:int=0)->dict:
        self.steps+=1
        if self.steps>8192 or depth>48:
            self.gaps.append("collection_origin_budget_exceeded");return self.unknown()
        node=unwrap(node)
        if node is None:return self.unknown()
        kind=node.type
        if kind in {"identifier","shorthand_property_identifier","shorthand_property_identifier_pattern"}:return env.get(self.key(node),self.unknown())
        if kind=="array":
            if not aa._children(node):return self.collection()
            element={"kind":"empty"}
            for child in aa._children(node):element=self.join(element,self.evaluate(child,env,depth+1))
            return self.collection(element)
        if kind=="object":
            fields,closed=_pairs(self.doc,node)
            return {"kind":"record","fields":{key:self.evaluate(value,env,depth+1) for key,value in fields.items()}} if closed else self.unknown()
        if kind=="member_expression":
            value=self.evaluate(node.child_by_field_name("object"),env,depth+1)
            prop=self.doc.text(node.child_by_field_name("property"))
            return value.get("fields",{}).get(prop,self.unknown()) if value.get("kind")=="record" else self.unknown()
        if kind=="subscript_expression":
            receiver=self.evaluate(node.child_by_field_name("object"),env,depth+1)
            return receiver["element"] if receiver.get("kind")=="collection" else self.unknown()
        if kind=="ternary_expression":return self.join(self.evaluate(node.child_by_field_name("consequence"),env,depth+1),self.evaluate(node.child_by_field_name("alternative"),env,depth+1))
        if kind=="binary_expression" and aa._op(self.doc,node) in {"||","??"}:
            return self.join(self.evaluate(node.child_by_field_name("left"),env,depth+1),self.evaluate(node.child_by_field_name("right"),env,depth+1))
        if kind=="assignment_expression":
            value=self.evaluate(node.child_by_field_name("right"),env,depth+1)
            left=node.child_by_field_name("left")
            if left is not None and left.type=="identifier":self.bind(left,value,env)
            return value
        if kind!="call_expression":return self.unknown()
        function=unwrap(node.child_by_field_name("function"));path=aa._path_of(self.doc,function) or []
        if function is not None and function.type=="member_expression":
            receiver_node=function.child_by_field_name("object");receiver=self.evaluate(receiver_node,env,depth+1)
            method=self.doc.text(function.child_by_field_name("property"))
            if receiver.get("kind")=="collection" and method in {"filter","sort","slice"}:
                self.relations.append({"kind":"standard_array_preserves_element_origins","method":method,"location":self.adapter.ref(self.doc,node),"element":receiver["element"]})
                return receiver
            if receiver.get("kind")=="collection" and method=="push":
                element=receiver["element"]
                for arg in aa._args(node):element=self.join(element,self.evaluate(arg,env,depth+1))
                result=self.collection(element);self.bind(receiver_node,result,env)
                self.relations.append({"kind":"explicit_element_append","location":self.adapter.ref(self.doc,node),"element":element})
                return self.unknown()
            if receiver.get("kind")=="collection" and method=="map":
                callback=unwrap(aa._argument(node,0))
                if callback is None or callback.type not in aa._FUNCTIONS:return self.unknown()
                value=self.function(callback,[receiver["element"]],env,depth+1)
                self.relations.append({"kind":"map_callback_return_origin","location":self.adapter.ref(self.doc,node),"return":value})
                return self.collection(value)
        if len(path)==2 and path[0]=="this":
            target={"file":self.doc.source.path,"symbol":self.class_name+"."+path[1]}
            document,_,function=self.adapter.select(target)
            if function is None or document is not self.doc:return self.unknown()
            args=[self.evaluate(arg,env,depth+1) for arg in aa._args(node)]
            value=self.function(function,args,env,depth+1)
            self.relations.append({"kind":"actual_class_helper_return","call":self.adapter.ref(self.doc,node),"target":self.adapter.ref(self.doc,function),"return":value})
            return value
        # Only the actual fresh queue provider can introduce the original element domain.
        source=self.fresh_source.get("call")
        if source and node.start_byte==source.get("start_byte") and node.end_byte==source.get("end_byte"):
            self.relations.append({"kind":"actual_fresh_queue_source","location":self.adapter.ref(self.doc,node)})
            return self.collection(self.item())
        return self.unknown()

    def statements(self,node:Any,env:dict,returns:list,depth:int)->dict|None:
        if node is None:return env
        kind=node.type
        if kind in {"statement_block","else_clause","catch_clause"}:
            for child in aa._children(node):
                env=self.statements(child,env,returns,depth+1)
                if env is None:break
            return env
        if kind in {"lexical_declaration","variable_declaration"}:
            for child in aa._children(node):
                if child.type=="variable_declarator":self.bind(child.child_by_field_name("name"),self.evaluate(child.child_by_field_name("value"),env,depth+1),env)
            return env
        if kind=="expression_statement":
            for child in aa._children(node):self.evaluate(child,env,depth+1)
            return env
        if kind=="return_statement":returns.append(self.evaluate(_return_expr(node),env,depth+1));return None
        if kind in {"continue_statement","break_statement","throw_statement"}:return None
        if kind=="if_statement":
            yes=self.statements(node.child_by_field_name("consequence"),dict(env),returns,depth+1)
            alternative=node.child_by_field_name("alternative")
            no=self.statements(alternative,dict(env),returns,depth+1) if alternative is not None else dict(env)
            return self.merge(*[branch for branch in (yes,no) if branch is not None]) if yes is not None or no is not None else None
        if kind=="for_in_statement" and aa._op(self.doc,node)=="of":
            collection=self.evaluate(node.child_by_field_name("right"),env,depth+1)
            loop_env=dict(env);self.bind(node.child_by_field_name("left"),collection.get("element",self.unknown()),loop_env)
            after=self.statements(node.child_by_field_name("body"),loop_env,returns,depth+1)
            return self.merge(env,after or {})
        if kind=="try_statement":
            normal=self.statements(node.child_by_field_name("body"),dict(env),returns,depth+1)
            caught=self.statements(node.child_by_field_name("handler"),dict(env),returns,depth+1)
            result=self.merge(*[branch for branch in (normal,caught) if branch is not None])
            return self.statements(node.child_by_field_name("finalizer"),result,returns,depth+1)
        return env

    def function(self,function:Any,args:list[dict],outer:dict|None=None,depth:int=0)->dict:
        identity=(function.start_byte,function.end_byte)
        if identity in self.active or depth>48:
            self.gaps.append("recursive_collection_helper_unknown");return self.unknown()
        self.active.append(identity)
        env=dict(outer or {})
        for index,param in enumerate(aa._parameters(function)):self.bind(param,args[index] if index<len(args) else self.unknown(),env)
        body=function.child_by_field_name("body");returns=[]
        if body is not None and body.type!="statement_block":returns=[self.evaluate(body,env,depth+1)];normal=None
        else:normal=self.statements(body,env,returns,depth+1)
        self.active.pop()
        if normal is not None:returns.append(self.unknown())
        value={"kind":"empty"}
        for item in returns:value=self.join(value,item)
        return value


def _module_path(snapshot: GraphSnapshot, current: str, literal: str) -> str | None:
    if not literal.startswith(".") or "\\" in literal or "\x00" in literal:
        return None
    candidate = posixpath.normpath(posixpath.join(posixpath.dirname(current), literal))
    if candidate.startswith("../") or candidate.startswith("/"):
        return None
    paths = {source.path for source in snapshot.files}
    options = [candidate]
    if candidate.endswith(".js"):
        options += [candidate[:-3] + ".ts", candidate[:-3] + ".tsx"]
    elif not posixpath.splitext(candidate)[1]:
        options += [candidate + ".ts", candidate + ".tsx", candidate + "/index.ts"]
    matches = [path for path in options if path in paths]
    return matches[0] if len(matches) == 1 else None


class _Completion:
    def __init__(self, snapshot: GraphSnapshot, rule: dict):
        self.snapshot, self.rule = snapshot, rule
        self.context = aa._Analysis(snapshot, SemanticSources(snapshot))
        self.gaps: list[dict] = []
        self.operations: list[dict] = []
        self.models: list[dict] = []

    def ref(self, document: Any, node: Any) -> dict | None:
        if document is None or node is None:
            return None
        record = self.context.ref(document, node)
        record["owner"] = document.call_owner(node)
        record["extractor_version"] = VERSION
        return record

    def gap(self, code: str, message: str, document: Any = None, node: Any = None) -> dict:
        result = {"code": code, "message": message, "location": self.ref(document, node)}
        self.gaps.append(result)
        return result

    def model(self, name: str, applicable: bool, evidence: list[dict | None], conditions: list[str], **details: Any) -> dict:
        result = {"id": name, "state": "source_applicability_supported" if applicable else "unknown",
            "evidence": [value for value in evidence if value is not None], "conditions": conditions,
            "runtime_provider_verified": False, **details}
        result["model_application_id"] = _digest({"version": VERSION, "snapshot": self.snapshot.id, **result})[:24]
        self.models.append(result)
        return result

    def op(self, kind: str, document: Any, node: Any, **details: Any) -> dict:
        record = {"kind": kind, "location": self.ref(document, node), **details}
        record["operation_id"] = _digest({"version": VERSION, "snapshot": self.snapshot.id, **record})[:24]
        self.operations.append(record)
        return record

    def select(self, selector: dict) -> tuple[Any, Any, Any]:
        return self.context.select(selector)

    def import_member(self, document: Any, expression: Any) -> dict:
        """Literal import/Promise.all/destructure is a relation, not a CALLS edge."""
        expression = unwrap(expression)
        root = aa._root_identifier(expression)
        identity = self.context.identity(document, root)
        result = {"state": "unknown", "expression": self.ref(document, expression), "binding_identity": identity,
            "existing_calls_unchanged": True, "runtime_module_load_verified": False}
        if identity.get("state") != "unique" or not identity.get("identity_complete") or root is None:
            return result
        declaration = self.context.lexical(document).declaration_for(identity)
        initializer = unwrap(self.context.lexical(document).initializer_for(identity))
        if not self.context.stable(document, document.tree.root_node, root):
            return result
        imported = identity.get("import") or {}
        path = aa._path_of(document, expression)
        export_name = None
        literal = None
        evidence = [self.ref(document, declaration)]
        promise_guard = None
        if imported and imported.get("module") and not imported.get("type_only"):
            literal = imported["module"]
            export_name = imported.get("imported_name")
            if export_name == "*" and path and len(path) == 2:
                export_name = path[1]
        elif declaration is not None and declaration.type == "variable_declarator":
            pattern = declaration.child_by_field_name("name")
            if initializer is not None and initializer.type == "call_expression" and aa._path_of(document, initializer.child_by_field_name("function")) == ["Promise", "all"]:
                promise_guard = self.context.environment(document).audit("Promise", initializer, "all")
                array = unwrap(aa._argument(initializer, 0))
                array_members=_dense_members(array);pattern_members=_dense_members(pattern)
                positions = identity.get("pattern_path", [])
                indexes = [item["index"] for item in positions if item.get("kind") == "array_index"]
                if (pattern is not None and pattern.type == "array_pattern" and array is not None and array.type == "array"
                        and array_members is not None and pattern_members is not None and len(array_members)==len(pattern_members)
                        and len(indexes) == 1 and indexes[0] < len(array_members) and len(aa._args(initializer)) == 1
                        and promise_guard.get("supported")):
                    initializer = unwrap(array_members[indexes[0]])
                    evidence.append(self.ref(document, array))
                else:
                    initializer = None
            if initializer is not None and initializer.type == "call_expression" and document.text(initializer.child_by_field_name("function")) == "import" and len(aa._args(initializer)) == 1:
                literal = aa._literal(document, aa._argument(initializer, 0))
                positions = identity.get("pattern_path", [])
                properties = [item["name"] for item in positions if item.get("kind") == "object_property"]
                if len(properties) == 1 and path and len(path) == 1:
                    export_name = properties[0]
                elif not properties and path and len(path) == 2:
                    export_name = path[1]
                evidence.append(self.ref(document, initializer))
        target_file = _module_path(self.snapshot, document.source.path, literal) if isinstance(literal, str) else None
        if target_file is None or not isinstance(export_name, str) or export_name in {"*", "default"}:
            return result
        target_document, definition, target_function = self.select({"file": target_file, "symbol": export_name})
        if definition is None:
            # Classes are indexed by their constructor/method, not as a callable class.
            target_document, definition, target_function = self.select({"file": target_file, "symbol": export_name + ".constructor"})
        if definition is None or target_document is None or target_function is None:
            return result
        enclosing_export = next((node for node in aa._ancestors(definition.node) if node.type == "export_statement"), None)
        if enclosing_export is None:
            return result
        result.update(state="source_literal_module_member", module_literal=literal, export_name=export_name,
            target={"file": target_file, "symbol": definition.symbol}, declaration=self.ref(target_document, definition.node),
            source_relation_evidence=evidence, promise_all_environment=promise_guard,
            scope="captured local ESM module provider, after successful standard loading; no dynamic edge promotion")
        result["relation_id"] = _digest({"version": VERSION, "snapshot": self.snapshot.id, **result})[:24]
        return result

    def call_target(self, document: Any, call: Any, expected: dict | None = None) -> tuple[dict, Any, Any]:
        record, target_document, target_function = self.context.source_callee(document, call, expected)
        if record.get("state") in _ALLOWED_BINDINGS:
            return record, target_document, target_function
        relation = self.import_member(document, call.child_by_field_name("function"))
        if relation.get("state") == "source_literal_module_member" and (expected is None or relation["target"] == expected):
            target_document, _, target_function = self.select(relation["target"])
            return relation, target_document, target_function
        return record, target_document, target_function

    def queue_entries_provider(self,document:Any,function:Any)->dict:
        ctx=self.context;wanted=self.rule["facade"]["read"]["implementation"]
        result={"state":"unknown","definition":self.ref(document,function)}
        calls=aa._calls(document,function.child_by_field_name("body"))
        selected=[]
        for call in calls:
            binding,doc,fn=self.call_target(document,call,wanted)
            if fn is not None and binding.get("state") in _ALLOWED_BINDINGS:selected.append((call,binding))
        returns=_returns(function)
        expression=_return_expr(returns[0]) if len(returns)==1 else None
        if len(selected)!=1 or expression is None or expression.type!="call_expression":return result
        call,binding=selected[0];declaration=aa._bound_call(call);binder=declaration.child_by_field_name("name") if declaration is not None else None
        path=aa._path_of(document,expression.child_by_field_name("function"))
        supported=bool(path is not None and path[1:]==["entries","filter"] and ctx.same(document,expression.child_by_field_name("function"),binder)
            and ctx.exact(document,aa._argument(call,0),aa._param_node(function,0)) and ctx.stable(document,function,binder)
            and ctx.stable(document,function,aa._param_node(function,0)))
        result.update(state="source_loaded_queue_entries_subset" if supported else "unknown",load_binding=binding,load_call=self.ref(document,call),
            actual_entries_filter=self.ref(document,expression),normal_array_model="filter selects original parsed queue entries without constructing replacements")
        return result

    def assembly(self) -> dict:
        rule, ctx = self.rule, self.context
        doc, _, fn = self.select(rule.get("dependency_assembly", {}))
        result = {"state": "unknown", "defaults": [], "overrides": [], "run_binding": None}
        if fn is None:
            return result
        returns = _returns(fn)
        statements=aa._children(fn.child_by_field_name("body"))
        returned = _return_expr(returns[0]) if len(returns) == 1 and statements and statements[-1].id==returns[0].id and returns[0].parent==fn.child_by_field_name("body") else None
        fields, closed = _pairs(doc, returned)
        ctx_param = aa._param_node(fn, 0)
        for role in ("read", "write"):
            field = rule["facade"][role]["callee"].split(".")[-1]
            value = fields.get(field)
            item = {"role": role, "field": field, "state": "unknown"}
            if value is not None and value.type == "binary_expression" and aa._op(doc, value) == "??":
                override, default = value.child_by_field_name("left"), value.child_by_field_name("right")
                binding = self.import_member(doc, default)
                wanted = rule["authority"] if role == "write" else rule["facade"][role].get("implementation")
                override_root = aa._root_identifier(override)
                override_identity = ctx.identity(doc, override_root)
                override_init = unwrap(ctx.lexical(doc).initializer_for(override_identity))
                override_proven = bool(override_init is not None and override_init.type == "binary_expression"
                    and aa._op(doc, override_init) == "??" and _same_path(ctx, doc, override_init.child_by_field_name("left"), ctx_param, ["deps"])
                    and unwrap(override_init.child_by_field_name("right")).type == "object"
                    and not aa._children(unwrap(override_init.child_by_field_name("right"))) and ctx.stable(doc, fn, override_root)
                    and aa._path_of(doc, override)[1:] == [field])
                supported = bool(closed and override_proven and binding.get("state") == "source_literal_module_member" and binding.get("target") == wanted)
                item.update(state="source_default_assembly_supported" if supported else "unknown", operator="??",
                    override_source=self.ref(doc, override), override_root_initializer=self.ref(doc, override_init),
                    default_binding=binding, default_condition="selected ctx.deps member is null or undefined",
                    ctx_parameter_identity=ctx.identity(doc, ctx_param), override_possible=True)
                result["overrides"].append({"role": role, "location": self.ref(doc, override), "selection":"a non-nullish injected member selects the override and is outside the default-provider proof"})
            result["defaults"].append(item)
        facade_doc, _, facade_fn = self.select(rule["facade"]["owner"])
        if facade_fn is not None:
            calls = aa._calls(facade_doc, facade_fn.child_by_field_name("body"), rule["dependency_assembly"]["symbol"].split(".")[-1])
            call = calls[0] if len(calls) == 1 else None
            decl = aa._bound_call(call) if call is not None else None
            binder = decl.child_by_field_name("name") if decl is not None else None
            actual_ctx = aa._argument(call, 0) if call is not None else None
            relation, _, _ = self.call_target(facade_doc, call, rule["dependency_assembly"]) if call is not None else ({}, None, None)
            uses = {}
            for role in ("read", "write"):
                selected = aa._calls(facade_doc, facade_fn.child_by_field_name("body"), rule["facade"][role]["callee"])
                selected_call = selected[0] if len(selected) == 1 else None
                uses[role] = bool(selected_call is not None and binder is not None
                    and ctx.same(facade_doc, selected_call.child_by_field_name("function"), binder)
                    and ctx.stable(facade_doc, facade_fn, binder))
            supported = bool(call is not None and ctx.exact(facade_doc, actual_ctx, aa._param_node(facade_fn, 1))
                and relation.get("state") in _ALLOWED_BINDINGS and decl is not None and ctx.directly_awaited(facade_doc, call)
                and all(uses.values()))
            result["run_binding"] = {"state":"source_factory_result_receiver_supported" if supported else "unknown",
                "call":self.ref(facade_doc, call), "declaration":self.ref(facade_doc, decl), "actual_ctx":self.ref(facade_doc,actual_ctx),
                "binding":relation, "receiver_identity":ctx.identity(facade_doc,binder), "selected_member_uses":uses}
        complete = bool(len(result["defaults"]) == 2 and all(item["state"] == "source_default_assembly_supported" for item in result["defaults"])
            and (result["run_binding"] or {}).get("state") == "source_factory_result_receiver_supported")
        result["state"] = "source_default_execution_chain_supported" if complete else "unknown"
        self.model(MODEL_IDS[0],complete,[self.ref(doc,fn)], ["Standard ESM loading and Promise.all succeed", "ctx.deps selected members are nullish; overrides are separate"])
        if not complete:
            self.gap("atomicity_default_assembly_incomplete","Actual dynamic module provider, factory result or facade receiver is not closed",doc,fn)
        return result

    def resources(self, facade: dict, lifecycle: dict) -> dict:
        ctx, rule = self.context, self.rule
        life_doc, _, life_fn = self.select(rule["protection"]["lifecycle"]["owner"])
        facade_doc, _, facade_fn = self.select(rule["facade"]["owner"])
        load_doc, _, load_fn = self.select(rule["facade"]["read"]["implementation"])
        result = {"state":"unknown", "physical_resource_identity_verified":False,
            "identity_scope":"same logical input root under registered Node path semantics; symlinks, mount aliases and deployment identity are conditions",
            "mapping":[], "path_constructor":None, "atomic_publish":None}
        if any(value is None for value in (life_fn, facade_fn, load_fn)):
            return result
        names = rule["protection"]["lifecycle"]
        local_docs: dict[str, tuple[Any,Any]] = {}
        for role in ("fresh_read","persist"):
            calls = aa._calls(life_doc,life_fn.child_by_field_name("body"),names[role]["callee"])
            call = calls[0] if len(calls)==1 else None
            binding, doc, fn = self.call_target(life_doc,call) if call is not None else ({},None,None)
            if fn is not None and binding.get("state") in _ALLOWED_BINDINGS:
                local_docs[role]=(doc,fn)
                result["mapping"].append({"role":role,"binding":binding,"call":self.ref(life_doc,call),"actual_root":self.ref(life_doc,aa._argument(call,names[role]["resource_argument_index"]))})
        load_returns=_returns(load_fn)
        load_call=_return_expr(load_returns[0]) if len(load_returns)==1 else None
        load_binding, delegated_doc, delegated_fn = self.call_target(load_doc,load_call) if load_call is not None and load_call.type=="call_expression" else ({},None,None)
        loader_mapped=bool(local_docs.get("fresh_read") and delegated_fn is local_docs["fresh_read"][1]
            and ctx.exact(load_doc,aa._argument(load_call,0),aa._param_node(load_fn,0))
            and ctx.stable(load_doc,load_fn,aa._param_node(load_fn,0)))
        result["facade_load_delegate"]={"state":"source_root_forwarded" if loader_mapped else "unknown", "binding":load_binding,
            "return":self.ref(load_doc,load_returns[0]) if load_returns else None}
        # Identify the shared path function by actual call binding and its argument.
        constructors=[]
        for role,doc,fn in [("lock",life_doc,life_fn)]+[(role,*value) for role,value in local_docs.items()]:
            param=aa._param_node(fn,0)
            for call in aa._calls(doc,fn.child_by_field_name("body")):
                if len(aa._args(call))!=1 or not ctx.exact(doc,aa._argument(call,0),param):
                    continue
                relation,pdoc,pfn=self.call_target(doc,call)
                if pfn is None or relation.get("state") not in _ALLOWED_BINDINGS:
                    continue
                returns=_returns(pfn)
                expression=_return_expr(returns[0]) if len(returns)==1 else None
                if expression is None or expression.type!="call_expression":
                    continue
                path=aa._path_of(pdoc,expression.child_by_field_name("function"))
                if path is None or path[-1:]!=["join"]:
                    continue
                receiver=aa._root_identifier(expression.child_by_field_name("function"))
                imported=ctx.identity(pdoc,receiver).get("import") or {}
                args=aa._args(expression)
                first=unwrap(args[0]) if args else None
                resolver=aa._path_of(pdoc,first.child_by_field_name("function")) if first is not None and first.type=="call_expression" else None
                fixed=[aa._literal(pdoc,item) for item in args[1:]]
                supported=bool(imported.get("module") in {"node:path","path"} and resolver==[path[0],"resolve"]
                    and len(aa._args(first))==1 and ctx.exact(pdoc,aa._argument(first,0),aa._param_node(pfn,0))
                    and ctx.same(pdoc,first.child_by_field_name("function"),receiver) and fixed and all(isinstance(item,str) for item in fixed)
                    and ctx.stable(pdoc,pfn,aa._param_node(pfn,0)) and ctx.stable(pdoc,pdoc.tree.root_node,receiver))
                if supported:
                    constructors.append({"role":role,"target":self.ref(pdoc,pfn),"call":self.ref(doc,call),
                        "parameter_mapping":self.ref(doc,aa._argument(call,0)),"path_components":fixed,"import_binding":ctx.identity(pdoc,receiver)})
        identities={(item["target"]["file"],item["target"]["start_byte"],item["target"]["end_byte"]) for item in constructors}
        roles={item["role"] for item in constructors}
        path_closed=bool(len(identities)==1 and roles=={"lock","fresh_read","persist"} and loader_mapped)
        result["path_constructor"]={"state":"source_same_logical_path_supported" if path_closed else "unknown", "applications":constructors}
        # A successful selected save publishes exactly the argument path through rename.
        publish_closed=False
        if "persist" in local_docs:
            sdoc,sfn=local_docs["persist"]
            path_calls=[_node_at(sdoc,item["call"]) for item in constructors if item["role"]=="persist"]
            publish_calls=[node for node in aa._calls(sdoc,sfn.child_by_field_name("body"))
                if any(_inside_argument(node,0,p) for p in path_calls if p is not None)]
            publish_call=publish_calls[0] if len(publish_calls)==1 else None
            binding,wdoc,wfn=self.call_target(sdoc,publish_call) if publish_call is not None else ({},None,None)
            if wfn is not None:
                renames=[]
                for call in aa._calls(wdoc,wfn.child_by_field_name("body")):
                    function=call.child_by_field_name("function")
                    info=ctx.identity(wdoc,function)
                    imported=info.get("import") or {}
                    if imported.get("module") in {"node:fs/promises","fs/promises"} and imported.get("imported_name")=="rename":
                        if len(aa._args(call))==2 and ctx.exact(wdoc,aa._argument(call,1),aa._param_node(wfn,0)):
                            renames.append(call)
                json_calls=[node for node in aa._walk(aa._argument(publish_call,1)) if node.type=="call_expression" and aa._path_of(sdoc,node.child_by_field_name("function"))==["JSON","stringify"]]
                json_call=json_calls[0] if len(json_calls)==1 else None
                serialized=unwrap(aa._argument(json_call,0)) if json_call is not None else None
                serialized_init=unwrap(ctx.lexical(sdoc).initializer_for(ctx.identity(sdoc,serialized)))
                serialized_fields,serialized_closed=_pairs(sdoc,serialized_init)
                selected_entries=serialized_fields.get("entries")
                queue_parameter=aa._param_node(sfn,1)
                serialization_closed=bool(serialized_closed and _same_path(ctx,sdoc,selected_entries,queue_parameter,["entries"])
                    and ctx.stable(sdoc,sfn,serialized) and ctx.lexical(sdoc).unbound("JSON",json_call).get("local_declaration_absent"))
                writes=[node for node in aa._calls(wdoc,wfn.child_by_field_name("body")) if node.child_by_field_name("function") is not None
                    and node.child_by_field_name("function").type=="member_expression"
                    and wdoc.text(node.child_by_field_name("function").child_by_field_name("property"))=="writeFile"
                    and ctx.exact(wdoc,aa._argument(node,0),aa._param_node(wfn,1)) and aa._literal(wdoc,aa._argument(node,1))=="utf8"]
                content_write=writes[0] if len(writes)==1 else None
                handle=content_write.child_by_field_name("function").child_by_field_name("object") if content_write is not None else None
                handle_writes,handle_complete=ctx.writes(wdoc,wfn,handle)
                opens=[]
                for mutation in handle_writes:
                    if mutation.type!="assignment_expression" or content_write is None or mutation.start_byte>content_write.start_byte:continue
                    opening=unwrap(mutation.child_by_field_name("right"))
                    if opening is None or opening.type!="call_expression":continue
                    imported=ctx.identity(wdoc,opening.child_by_field_name("function")).get("import") or {}
                    if imported.get("module") in {"node:fs/promises","fs/promises"} and imported.get("imported_name")=="open":opens.append((mutation,opening))
                opened=opens[0][1] if len(opens)==1 else None
                temp=unwrap(aa._argument(opened,0)) if opened is not None else None
                temp_initializer=unwrap(ctx.lexical(wdoc).initializer_for(ctx.identity(wdoc,temp)))
                rename=renames[0] if len(renames)==1 else None
                content_closed=bool(content_write is not None and handle_complete and len(opens)==1 and rename is not None
                    and ctx.exact(wdoc,aa._argument(rename,0),temp) and ctx.stable(wdoc,wfn,temp)
                    and ctx.stable(wdoc,wfn,aa._param_node(wfn,1)) and ctx.directly_awaited(wdoc,content_write)
                    and opens[0][0].end_byte<content_write.start_byte<rename.start_byte
                    and temp_initializer is not None and temp_initializer.type=="template_string"
                    and any(ctx.exact(wdoc,node,aa._param_node(wfn,0)) for node in aa._walk(temp_initializer)))
                publish_closed=bool(len(renames)==1 and ctx.stable(wdoc,wfn,aa._param_node(wfn,0))
                    and ctx.directly_awaited(sdoc,publish_call) and ctx.directly_awaited(wdoc,renames[0]) and serialization_closed and content_closed)
                result["atomic_publish"]={"state":"source_normal_rename_to_argument_supported" if publish_closed else "unknown",
                    "save_call":self.ref(sdoc,publish_call),"binding":binding,"definition":self.ref(wdoc,wfn),
                    "rename_calls":[self.ref(wdoc,node) for node in renames],
                    "content_flow":{"state":"source_queue_json_content_temp_rename_connected" if serialization_closed and content_closed else "unknown",
                        "queue_entries":self.ref(sdoc,selected_entries),"serialization_record":self.ref(sdoc,serialized_init),"json_stringify":self.ref(sdoc,json_call),
                        "actual_content":self.ref(sdoc,aa._argument(publish_call,1)),"content_formal":self.ref(wdoc,aa._param_node(wfn,1)),
                        "temp_declaration":self.ref(wdoc,temp_initializer),"open_assignment":self.ref(wdoc,opens[0][0]) if len(opens)==1 else None,
                        "content_write":self.ref(wdoc,content_write),"same_temp_as_rename":content_closed,"serialization_connected":serialization_closed},
                    "failures":{"before_publish":"no selected successful commit", "after_publish":"durability/release error may be committed; no automatic rollback claim"}}
        facade_mapped=bool(facade.get("resource",{}).get("same_stable_lexical_candidate") and lifecycle.get("fresh_queue_callback_save_mapping"))
        complete=bool(path_closed and facade_mapped and publish_closed)
        result["state"]="source_logical_resource_chain_supported" if complete else "unknown"
        self.model(MODEL_IDS[3],path_closed,[item["target"] for item in constructors],
            ["Compared invocations supply the same logical hubRoot", "Node path.join/resolve have registered standard semantics; physical aliases are not proved"])
        self.model(MODEL_IDS[5],publish_closed,[result.get("atomic_publish",{}).get("definition") if result.get("atomic_publish") else None],
            ["Only the successful normal publish is represented as commit", "Atomic rename and file-system visibility implement the declared model", "Post-publish durability and release failures may leave a committed update"])
        if not complete:
            self.gap("atomicity_resource_chain_incomplete","Root forwarding, shared queuePath or normal publish is not closed")
        return result

    def input_keys(self) -> dict:
        """Actual facade request fields and authority normalization, not names alone."""
        ctx,rule=self.context,self.rule
        invariant=rule["completion"]["invariant"]
        project_path,key_path=invariant["project_path"],invariant["key_path"]
        result={"state":"unknown","producer":{},"normalization":{},"parameter_fields_preserved_under_model":False}
        if len(project_path)!=1 or len(key_path)!=2:
            self.gap("atomicity_key_path_model_unsupported","First completion adapter supports a scalar project and a one-level metadata key")
            return result
        fdoc,_,ffn=self.select(rule["facade"]["owner"])
        adoc,_,afn=self.select(rule["authority"])
        if ffn is None or afn is None:
            return result
        calls=aa._calls(fdoc,ffn.child_by_field_name("body"),rule["facade"]["write"]["callee"])
        write=calls[0] if len(calls)==1 else None
        actual=unwrap(aa._argument(write,1)) if write is not None else None
        identity=ctx.identity(fdoc,actual)
        builder_call=unwrap(ctx.lexical(fdoc).initializer_for(identity))
        bbind,bdoc,bfn=self.call_target(fdoc,builder_call) if builder_call is not None and builder_call.type=="call_expression" else ({},None,None)
        producer_complete=False
        if bfn is not None and ctx.stable(fdoc,ffn,actual):
            returns=_returns(bfn)
            obj=_return_expr(returns[0]) if len(returns)==1 else None
            fields,closed=_pairs(bdoc,obj)
            project_value=fields.get(project_path[0])
            metadata=fields.get(key_path[0])
            meta_identity=ctx.identity(bdoc,metadata)
            meta_initializer=unwrap(ctx.lexical(bdoc).initializer_for(meta_identity))
            meta_fields,meta_closed=_pairs(bdoc,meta_initializer)
            writes,write_complete=ctx.writes(bdoc,bfn,metadata,members=True)
            selected_writes=[]
            for node in writes:
                left=node.child_by_field_name("left") if node.type in {"assignment_expression","augmented_assignment_expression"} else None
                if left is not None and _same_path(ctx,bdoc,left,metadata,[key_path[1]]):
                    selected_writes.append(node)
            project_index=ctx.identity(bdoc,project_value).get("parameter_index")
            selected=selected_writes[0] if len(selected_writes)==1 else None
            key_value=selected.child_by_field_name("right") if selected is not None else None
            key_index=ctx.identity(bdoc,key_value).get("parameter_index")
            project_actual=aa._argument(builder_call,project_index) if isinstance(project_index,int) else None
            key_actual=aa._argument(builder_call,key_index) if isinstance(key_index,int) else None
            select_calls=aa._calls(fdoc,ffn.child_by_field_name("body"),rule["facade"]["select"]["callee"])
            select=select_calls[0] if len(select_calls)==1 else None
            same_key=bool(select is not None and ctx.exact(fdoc,key_actual,aa._argument(select,1)))
            hash_writes,hash_write_complete=ctx.writes(fdoc,ffn,key_actual)
            hash_assignments=[node for node in hash_writes if node.type=="assignment_expression" and ctx.exact(fdoc,node.child_by_field_name("left"),key_actual)]
            hash_call=unwrap(hash_assignments[0].child_by_field_name("right")) if len(hash_assignments)==1 else None
            hash_binding,hash_doc,hash_fn=self.call_target(fdoc,hash_call) if hash_call is not None and hash_call.type=="call_expression" else ({},None,None)
            hash_shape=False;hash_evidence=[]
            if hash_fn is not None:
                hash_returns=_returns(hash_fn);hash_expr=_return_expr(hash_returns[0]) if len(hash_returns)==1 else None
                if hash_expr is not None and hash_expr.type=="template_string":
                    constructors=[node for node in aa._calls(hash_doc,hash_fn.child_by_field_name("body")) if len(aa._args(node))==1
                        and aa._literal(hash_doc,aa._argument(node,0))=="sha256"]
                    constructor=constructors[0] if len(constructors)==1 else None
                    imported=ctx.identity(hash_doc,constructor.child_by_field_name("function")).get("import") or {} if constructor is not None else {}
                    updates=[node for node in aa._calls(hash_doc,hash_fn.child_by_field_name("body")) if (aa._path_of(hash_doc,node.child_by_field_name("function")) or [])[-1:]==["update"]]
                    # Chained member receivers are call expressions, so inspect their genuine property token too.
                    updates=[node for node in aa._calls(hash_doc,hash_fn.child_by_field_name("body")) if node.child_by_field_name("function") is not None
                        and node.child_by_field_name("function").type=="member_expression" and hash_doc.text(node.child_by_field_name("function").child_by_field_name("property"))=="update"]
                    digests=[node for node in aa._calls(hash_doc,hash_fn.child_by_field_name("body")) if node.child_by_field_name("function") is not None
                        and node.child_by_field_name("function").type=="member_expression" and hash_doc.text(node.child_by_field_name("function").child_by_field_name("property"))=="digest"]
                    update=updates[0] if len(updates)==1 else None;digest=digests[0] if len(digests)==1 else None
                    hash_shape=bool(imported.get("module")=="node:crypto" and imported.get("imported_name")=="createHash" and constructor is not None
                        and update is not None and digest is not None and ctx.exact(hash_doc,aa._argument(update,0),aa._param_node(hash_fn,0))
                        and aa._literal(hash_doc,aa._argument(update,1))=="utf8" and aa._literal(hash_doc,aa._argument(digest,0))=="hex"
                        and unwrap(update.child_by_field_name("function").child_by_field_name("object")).id==constructor.id
                        and unwrap(digest.child_by_field_name("function").child_by_field_name("object")).id==update.id
                        and any(node.type=="string_fragment" and hash_doc.text(node)=="sha256:" for node in aa._children(hash_expr)))
                    hash_evidence=[self.ref(hash_doc,node) for node in (hash_expr,constructor,update,digest)]
            self.model(MODEL_IDS[7],bool(hash_shape and hash_write_complete),hash_evidence,
                ["The actual node:crypto createHash provider retains standard sha256/UTF8/hex behavior", "Only deterministic source hashing form is modeled; no collision or actual runtime value is proved"])
            # Same declaration as the equality RHS in the real project filter.
            same_project=False
            comparisons=[]
            for call in aa._calls(fdoc,ffn.child_by_field_name("body")):
                if aa._path_of(fdoc,call.child_by_field_name("function")) and aa._path_of(fdoc,call.child_by_field_name("function"))[-1]=="filter":
                    callback=unwrap(aa._argument(call,0))
                    if callback is None or callback.type not in aa._FUNCTIONS:
                        continue
                    formal=aa._param_node(callback,0)
                    for term in aa._walk(callback.child_by_field_name("body"),skip_functions=True):
                        if term.type=="binary_expression" and aa._op(fdoc,term)=="===":
                            for side,other in (("left","right"),("right","left")):
                                if _same_path(ctx,fdoc,term.child_by_field_name(side),formal,project_path) and ctx.exact(fdoc,term.child_by_field_name(other),project_actual):
                                    comparisons.append(self.ref(fdoc,term));same_project=True
            # The input key must be guarded by the same formal, not unconditional arbitrary input.
            key_guard=next((parent for parent in aa._ancestors(selected) if parent.type=="if_statement"),None) if selected is not None else None
            guarded_key=bool(key_guard is not None and ctx.exact(bdoc,key_guard.child_by_field_name("condition"),key_value)
                and aa._inside(key_guard.child_by_field_name("consequence"),selected) and key_guard.child_by_field_name("alternative") is None)
            producer_complete=bool(closed and meta_closed and write_complete and len(selected_writes)==1 and guarded_key and same_key and same_project and hash_shape and hash_write_complete
                and key_path[1] not in meta_fields and isinstance(project_index,int) and isinstance(key_index,int)
                and ctx.exact(bdoc,project_value,aa._param_node(bfn,project_index)) and ctx.exact(bdoc,key_value,aa._param_node(bfn,key_index)))
            result["producer"]={"state":"source_request_identity_fields_supported" if producer_complete else "unknown",
                "builder_binding":bbind,"call":self.ref(fdoc,builder_call),"return":self.ref(bdoc,obj),
                "selected_key_write":self.ref(bdoc,selected),"key_guard":self.ref(bdoc,key_guard),
                "key_argument":self.ref(fdoc,key_actual),"project_argument":self.ref(fdoc,project_actual),
                "project_filter_comparisons":comparisons,"same_selected_hashed_key_binding":same_key,"same_project_binding":same_project,
                "hash_assignment":self.ref(fdoc,hash_assignments[0]) if len(hash_assignments)==1 else None,"hash_binding":hash_binding,"hash_shape_supported":hash_shape,"hash_evidence":hash_evidence,
                "metadata_literal":self.ref(bdoc,meta_initializer),"selected_key_initializer_absent":key_path[1] not in meta_fields}
        # Normalization starts at the actual writer input; expand the metadata helper's real return paths.
        input_param=aa._param_node(afn,1)
        candidate_literals=[]
        for node in aa._walk(afn.child_by_field_name("body"),skip_functions=True):
            if node.type!="variable_declarator":continue
            value=unwrap(node.child_by_field_name("value"))
            children=aa._children(value) if value is not None and value.type=="object" else []
            if children and children[0].type=="spread_element" and len(aa._children(children[0]))==1 and ctx.exact(adoc,aa._children(children[0])[0],input_param):
                candidate_literals.append(node)
        normalization_complete=False
        if len(candidate_literals)==1:
            normalized=candidate_literals[0]
            binder=normalized.child_by_field_name("name")
            value=unwrap(normalized.child_by_field_name("value"))
            suffix=aa._children(value)[1:]
            suffix_fields,suffix_closed=_pairs(adoc,value,members=suffix)
            key_doc,_,key_fn=self.select(rule["predicate_sources"]["key"])
            key_returns=_returns(key_fn) if key_fn is not None else []
            key_fields,_=aa._return_fields(ctx,key_doc,key_fn,_return_expr(key_returns[0]),aa._param_node(key_fn,0)) if len(key_returns)==1 else ([],False)
            protected_root={key_path[0]}|{record["field_path"][0] for record in key_fields if len(record.get("field_path",[]))==1 and record["field_path"]!=project_path}
            root_unchanged=bool(suffix_closed and protected_root.isdisjoint(suffix_fields))
            # Project is rewritten from the same input property through a simple immutable alias.
            project_written=suffix_fields.get(project_path[0])
            project_origin=unwrap(ctx.lexical(adoc).initializer_for(ctx.identity(adoc,project_written))) if project_written is not None else None
            project_retained=bool(project_origin is not None and _same_path(ctx,adoc,project_origin,input_param,project_path))
            mutations,mutation_complete=ctx.writes(adoc,afn,binder,members=True)
            replacement=[];disjoint=[];unknown=[]
            for mutation in mutations:
                left=mutation.child_by_field_name("left") if mutation.type=="assignment_expression" else None
                if left is None:
                    unknown.append(self.ref(adoc,mutation));continue
                path=aa._path_of(adoc,left)
                keys=path[1:] if path is not None and ctx.same(adoc,left,binder) else None
                if keys==key_path[:1]:replacement.append(mutation)
                elif keys is not None and (keys[:1]!=key_path[:1] or keys[1:]!=key_path[1:]):disjoint.append(self.ref(adoc,mutation))
                else:unknown.append(self.ref(adoc,mutation))
            helper_facts=[]
            # One optional missing-metadata {} fallback and one call result replacement.
            normal_replacements=[];fallbacks=[]
            for assignment in replacement:
                right=unwrap(assignment.child_by_field_name("right"))
                if right is not None and right.type=="object" and not aa._children(right):
                    parent=next((item for item in aa._ancestors(assignment) if item.type=="if_statement"),None)
                    condition=unwrap(parent.child_by_field_name("condition")) if parent is not None else None
                    safe_missing=bool(condition is not None and condition.type=="unary_expression" and aa._op(adoc,condition)=="!"
                        and _same_path(ctx,adoc,condition.child_by_field_name("argument"),binder,key_path[:1]))
                    fallbacks.append({"location":self.ref(adoc,assignment),"missing_only":safe_missing,"selected_producer_branch":"metadata object was constructed, so fallback is not selected"})
                else:
                    initializer=unwrap(ctx.lexical(adoc).initializer_for(ctx.identity(adoc,right)))
                    if initializer is not None and initializer.type=="call_expression":normal_replacements.append((assignment,initializer))
                    else:unknown.append(self.ref(adoc,assignment))
            if len(normal_replacements)==1:
                assignment,helper_call=normal_replacements[0]
                hbind,hdoc,hfn=self.call_target(adoc,helper_call)
                if hfn is not None:
                    indexes=[index for index,arg in enumerate(aa._args(helper_call)) if _same_path(ctx,adoc,arg,binder,key_path[:1])]
                    formal=aa._param_node(hfn,indexes[0]) if len(indexes)==1 else None
                    returns=_returns(hfn)
                    returns_facts=[_ordinary_return_copy(hdoc,item,formal,ctx,{key_path[1]}) for item in returns] if formal is not None else []
                    aliases=[formal] if formal is not None else []
                    for node in aa._walk(hfn.child_by_field_name("body"),skip_functions=True):
                        if node.type=="variable_declarator" and any(ctx.exact(hdoc,unwrap(node.child_by_field_name("value")),origin) for origin in aliases):
                            aliases.append(node.child_by_field_name("name"))
                    root_writes=[];passed_roots=[]
                    for origin in aliases:
                        writes,complete=ctx.writes(hdoc,hfn,origin,members=True)
                        if not complete:root_writes.append({"reason":"incomplete_write_enumeration"})
                        for mutation in writes:
                            left=mutation.child_by_field_name("left") if mutation.type=="assignment_expression" else None
                            if left is None or _same_path(ctx,hdoc,left,origin,[key_path[1]]) or aa._path_of(hdoc,left)==[hdoc.text(origin)]:root_writes.append(self.ref(hdoc,mutation))
                    for call in aa._calls(hdoc,hfn.child_by_field_name("body")):
                        for arg in aa._args(call):
                            if any(ctx.exact(hdoc,arg,origin) for origin in aliases):passed_roots.append(self.ref(hdoc,call))
                    supported=bool(returns_facts and all(item["state"] in {"source_current_formal_reference","source_ordered_disjoint_return_copy"} for item in returns_facts)
                        and not root_writes and not passed_roots and all(ctx.stable(hdoc,hfn,origin) for origin in aliases))
                    helper_facts.append({"state":"source_selected_key_return_preserved_under_plain_record_model" if supported else "unknown",
                        "binding":hbind,"call":self.ref(adoc,helper_call),"replacement":self.ref(adoc,assignment),
                        "metadata_formal":self.ref(hdoc,formal),"return_paths":returns_facts,"root_write_barriers":root_writes,"root_escape_calls":passed_roots,
                        "model_scope":"primitive own-data selected key in a finite acyclic JSON record; external readers receive disjoint child records and do not concurrently mutate the invocation input"})
            normalization_complete=bool(root_unchanged and project_retained and mutation_complete and not unknown and len(helper_facts)==1
                and helper_facts[0]["state"]=="source_selected_key_return_preserved_under_plain_record_model" and all(item["missing_only"] for item in fallbacks))
            result["normalization"]={"state":"source_request_fields_preserved_under_model" if normalization_complete else "unknown",
                "initial_spread":self.ref(adoc,value),"protected_root_field_not_redefined":root_unchanged,"project_same_input_source":project_retained,
                "disjoint_explicit_writes":disjoint,"missing_metadata_fallbacks":fallbacks,"metadata_replacement_helpers":helper_facts,"unknown_writes":unknown,
                "write_enumeration_complete":mutation_complete}
        complete=producer_complete and normalization_complete
        result.update(state="source_request_identity_fields_connected_under_model" if complete else "unknown",parameter_fields_preserved_under_model=complete)
        self.model(MODEL_IDS[1],complete,[result["producer"].get("return"),result["normalization"].get("initial_spread")],
            ["Input and persisted queue records are finite acyclic JSON data records with standard Array methods", "Selected key/project/description are ordinary scalar data values",
             "No accessor, Proxy, customized prototype, child-to-parent alias or concurrent external mutation of the invocation input is admitted", "JSON and object copy use registered standard data semantics"])
        if not complete:self.gap("atomicity_input_identity_incomplete","Actual producer or queue normalization fields are not connected in the registered record model")
        return result

    def instance_member(self, document: Any, method: Any, member: str, invoked: str) -> dict:
        """A constructor-created receiver and source class method, with no edge upgrade."""
        ctx=self.context
        cls=next((node for node in aa._ancestors(method) if node.type=="class_declaration"),None)
        result={"state":"unknown","member":member,"method":invoked,"runtime_object_identity_verified":False}
        body=cls.child_by_field_name("body") if cls is not None else None
        constructors=[node for node in aa._children(body) if node.type=="method_definition" and document.text(node.child_by_field_name("name"))=="constructor"]
        constructor=constructors[0] if len(constructors)==1 else None
        assignments=[]
        for node in aa._walk(body):
            if node.type=="assignment_expression" and aa._path_of(document,node.child_by_field_name("left"))==["this",member]:assignments.append(node)
        if constructor is None or len(assignments)!=1 or not aa._inside(constructor,assignments[0]):return result
        new=unwrap(assignments[0].child_by_field_name("right"))
        if new is None or new.type!="new_expression":return result
        provider=self.import_member(document,new.child_by_field_name("constructor"))
        if provider.get("state")!="source_literal_module_member":return result
        cdoc,_,cfn=self.select(provider["target"])
        class_name=provider["target"]["symbol"].rsplit(".",1)[0]
        target={"file":provider["target"]["file"],"symbol":class_name+"."+invoked}
        mdoc,_,mfn=self.select(target)
        root_arg=aa._argument(new,0)
        root_member_assignments=[node for node in aa._walk(body) if node.type=="assignment_expression"
            and aa._path_of(document,node.child_by_field_name("left"))==["this","hubRoot"]]
        captured_root=bool(len(root_member_assignments)==1 and ctx.exact(document,root_member_assignments[0].child_by_field_name("right"),aa._param_node(constructor,0))
            and ctx.exact(document,root_arg,aa._param_node(constructor,0)))
        child_cls=next((node for node in aa._ancestors(cfn) if node.type=="class_declaration"),None) if cfn is not None else None
        child_body=child_cls.child_by_field_name("body") if child_cls is not None else None
        child_root_assignments=[node for node in aa._walk(child_body) if node.type=="assignment_expression" and aa._path_of(cdoc,node.child_by_field_name("left"))==["this","hubRoot"]] if cdoc is not None else []
        child_captures=bool(len(child_root_assignments)==1 and cfn is not None
            and aa._inside(cfn,child_root_assignments[0]) and ctx.exact(cdoc,child_root_assignments[0].child_by_field_name("right"),aa._param_node(cfn,0)))
        if captured_root and child_captures and mfn is not None:
            result.update(state="source_constructor_member_provider_supported",constructor=self.ref(document,constructor),member_assignment=self.ref(document,assignments[0]),
                provider=provider,root_argument=self.ref(document,root_arg),root_capture=self.ref(document,root_member_assignments[0]),
                child_root_capture=self.ref(cdoc,child_root_assignments[0]),target=target,target_definition=self.ref(mdoc,mfn),
                model_scope="normal source-created instances and unmodified class methods, excluding injected or reflectively replaced receivers")
        return result

    def guarded_update(self, document: Any, function: Any) -> dict:
        ctx=self.context
        result={"state":"unknown","identity_select":None,"rejection_guards":[],"writes":[]}
        wrapper=self.rule["protection"]["wrappers"][0]
        calls=aa._calls(document,function.child_by_field_name("body"),wrapper["owner"]["symbol"].split(".")[-1])
        call=calls[0] if len(calls)==1 else None
        callback=unwrap(aa._argument(call,wrapper["callback_argument_index"])) if call is not None else None
        binding,_,_=self.call_target(document,call,wrapper["owner"]) if call is not None else ({},None,None)
        if callback is None or callback.type not in aa._FUNCTIONS or binding.get("state") not in _ALLOWED_BINDINGS:return result
        body=callback.child_by_field_name("body")
        formal=aa._param_node(callback,0)
        finds=[node for node in aa._calls(document,body) if _same_path(ctx,document,node.child_by_field_name("function"),formal,["entries","find"])]
        find=finds[0] if len(finds)==1 else None
        predicate=unwrap(aa._argument(find,0)) if find is not None else None
        predicate_body=unwrap(predicate.child_by_field_name("body")) if predicate is not None and predicate.type in aa._FUNCTIONS else None
        finder=aa._bound_call(find) if find is not None else None
        entry=finder.child_by_field_name("name") if finder is not None else None
        entry_id=aa._param_node(function,1)
        identity_closed=bool(predicate_body is not None and predicate_body.type=="binary_expression" and aa._op(document,predicate_body)=="==="
            and any(_same_path(ctx,document,predicate_body.child_by_field_name(side),aa._param_node(predicate,0),["id"])
                and ctx.exact(document,predicate_body.child_by_field_name(other),entry_id) for side,other in (("left","right"),("right","left"))))
        status_writes=[];updated_writes=[];rejections=[]
        for node in aa._walk(body,skip_functions=True):
            if node.type=="assignment_expression":
                left,right=node.child_by_field_name("left"),node.child_by_field_name("right")
                if _same_path(ctx,document,left,entry,["status"]):status_writes.append(node)
                if _same_path(ctx,document,left,entry,["updatedAt"]):updated_writes.append(node)
            if node.type=="if_statement" and node.parent==body and node.child_by_field_name("alternative") is None:
                consequence=node.child_by_field_name("consequence")
                statements=aa._children(consequence) if consequence is not None and consequence.type=="statement_block" else [consequence]
                if len(statements)==1 and statements[0] is not None and statements[0].type=="return_statement" and aa._literal(document,_return_expr(statements[0])) is None and document.text(_return_expr(statements[0]))=="null":
                    rejections.append(node)
        patch=aa._param_node(function,self.rule["transition"]["patch_argument_index"])
        guard=aa._param_node(function,self.rule["transition"]["guard_argument_index"])
        write=status_writes[0] if len(status_writes)==1 else None
        write_if=write.parent.parent if write is not None and write.parent is not None and write.parent.type=="expression_statement" else None
        write_condition=unwrap(write_if.child_by_field_name("condition")) if write_if is not None and write_if.type=="if_statement" else None
        guarded_write=bool(write is not None and _same_path(ctx,document,write.child_by_field_name("right"),patch,["status"])
            and write_condition is not None and write_condition.type=="binary_expression" and aa._op(document,write_condition)=="!=="
            and _same_path(ctx,document,write_condition.child_by_field_name("left"),patch,["status"])
            and document.text(write_condition.child_by_field_name("right"))=="undefined")
        status_guard=None;version_guard=None;missing_guard=None
        for rejected in rejections:
            condition=unwrap(rejected.child_by_field_name("condition"))
            if condition is None:continue
            if condition.type=="unary_expression" and aa._op(document,condition)=="!" and ctx.exact(document,condition.child_by_field_name("argument"),entry):missing_guard=rejected
            has_status=False;has_version=False
            terms=aa._conjuncts(document,condition)
            if len(terms)==2:
                first,second=unwrap(terms[0]),unwrap(terms[1])
                includes=unwrap(second.child_by_field_name("argument")) if second is not None and second.type=="unary_expression" and aa._op(document,second)=="!" else None
                if includes is not None and includes.type=="call_expression" and (aa._path_of(document,includes.child_by_field_name("function")) or [])[-1:]==["includes"]:
                    receiver=includes.child_by_field_name("function").child_by_field_name("object")
                    argument=unwrap(aa._argument(includes,0))
                    if argument is not None and argument.type=="call_expression" and document.text(argument.child_by_field_name("function"))=="String":
                        selected=unwrap(aa._argument(argument,0))
                        has_status=bool(ctx.exact(document,first,receiver) and len(aa._args(includes))==1 and len(aa._args(argument))==1
                            and selected is not None and selected.type=="binary_expression" and aa._op(document,selected)=="||"
                            and _same_path(ctx,document,selected.child_by_field_name("left"),entry,["status"])
                            and aa._literal(document,selected.child_by_field_name("right"))==""
                            and ctx.lexical(document).unbound("String",argument).get("local_declaration_absent"))
                if first is not None and first.type=="call_expression" and second is not None and second.type=="binary_expression" and aa._op(document,second)=="!==":
                    hasown=aa._path_of(document,first.child_by_field_name("function"))
                    left,right=unwrap(second.child_by_field_name("left")),unwrap(second.child_by_field_name("right"))
                    has_version=bool(hasown==["Object","prototype","hasOwnProperty","call"] and len(aa._args(first))==2
                        and ctx.exact(document,aa._argument(first,0),guard) and aa._literal(document,aa._argument(first,1))=="expectedUpdatedAt"
                        and left is not None and left.type=="binary_expression" and aa._op(document,left)=="??"
                        and _same_path(ctx,document,left.child_by_field_name("left"),entry,["updatedAt"])
                        and document.text(unwrap(left.child_by_field_name("right")))=="null"
                        and _same_path(ctx,document,right,guard,["expectedUpdatedAt"])
                        and ctx.environment(document).audit("Object",first,"prototype").get("supported"))
            if has_status:status_guard=rejected
            if has_version:version_guard=rejected
        # Trace includes receiver to the actual expectedStatus construction, rather than name matching.
        receiver_verified=False
        expected_declarations=[]
        if status_guard is not None:
            includes=[item for item in aa._walk(status_guard.child_by_field_name("condition")) if item.type=="call_expression"
                and (aa._path_of(document,item.child_by_field_name("function")) or [])[-1:]==["includes"]]
            receiver=includes[0].child_by_field_name("function").child_by_field_name("object") if len(includes)==1 else None
            init=unwrap(ctx.lexical(document).initializer_for(ctx.identity(document,receiver)))
            if init is not None:
                expected_declarations=[self.ref(document,init)]
                condition=unwrap(init.child_by_field_name("condition")) if init.type=="ternary_expression" else None
                consequence=unwrap(init.child_by_field_name("consequence")) if init.type=="ternary_expression" else None
                alternative=unwrap(init.child_by_field_name("alternative")) if init.type=="ternary_expression" else None
                second_condition=unwrap(alternative.child_by_field_name("condition")) if alternative is not None and alternative.type=="ternary_expression" else None
                missing=unwrap(alternative.child_by_field_name("consequence")) if alternative is not None and alternative.type=="ternary_expression" else None
                singleton=unwrap(alternative.child_by_field_name("alternative")) if alternative is not None and alternative.type=="ternary_expression" else None
                receiver_verified=bool(condition is not None and condition.type=="call_expression" and aa._path_of(document,condition.child_by_field_name("function"))==["Array","isArray"]
                    and len(aa._args(condition))==1 and _same_path(ctx,document,aa._argument(condition,0),guard,["expectedStatus"])
                    and _same_path(ctx,document,consequence,guard,["expectedStatus"])
                    and second_condition is not None and second_condition.type=="binary_expression" and aa._op(document,second_condition)=="==="
                    and _same_path(ctx,document,second_condition.child_by_field_name("left"),guard,["expectedStatus"])
                    and document.text(unwrap(second_condition.child_by_field_name("right")))=="undefined"
                    and document.text(missing)=="null" and singleton is not None and singleton.type=="array" and len(aa._children(singleton))==1
                    and _same_path(ctx,document,aa._children(singleton)[0],guard,["expectedStatus"])
                    and ctx.lexical(document).unbound("Array",condition).get("local_declaration_absent") and ctx.stable(document,callback,receiver))
        returns=_returns(callback)
        last=aa._children(body)[-1] if aa._children(body) else None
        return_entry=bool(last is not None and last.type=="return_statement" and ctx.exact(document,_return_expr(last),entry))
        precede=bool(write is not None and all(node.end_byte<write.start_byte for node in (missing_guard,status_guard,version_guard) if node is not None))
        synchronous_body=not any(item.type in {"await_expression","yield_expression"} for item in aa._walk(body,skip_functions=True))
        complete=bool(identity_closed and guarded_write and missing_guard is not None and status_guard is not None and version_guard is not None
            and receiver_verified and precede and return_entry and synchronous_body and len(updated_writes)==1
            and ctx.exact(document,aa._argument(call,wrapper["resource_argument_index"]),aa._param_node(function,0)))
        result.update(state="source_identity_status_version_guarded_write_supported" if complete else "unknown",
            identity_select=self.ref(document,find),predicate=self.ref(document,predicate_body),entry_binding=ctx.identity(document,entry),
            wrapper_binding=binding,wrapper_call=self.ref(document,call),queue_callback=self.ref(document,callback),
            rejection_guards=[{"kind":kind,"location":self.ref(document,node)} for kind,node in (("entry_absent",missing_guard),("expected_status_mismatch",status_guard),("expected_version_mismatch",version_guard)) if node is not None],
            expected_status_receiver_sources=expected_declarations,writes=[self.ref(document,node) for node in status_writes+updated_writes],
            direct_status_transfer=guarded_write,guards_before_write=precede,return_entry=return_entry,no_callback_await=synchronous_body)
        return result

    def scheduler(self) -> dict:
        ctx,rule=self.context,self.rule
        doc,_,fn=self.select(rule["transition"]["owner"])
        result={"state":"unknown","writes":[],"rollback":None,"assembly":None,"candidate_flow":{},"guarded_writer":None}
        if fn is None:return result
        candidate_calls=[call for call in aa._calls(doc,fn.child_by_field_name("body"))
            if aa._path_of(doc,call.child_by_field_name("function"))==["this","scheduler","nextCandidates"]]
        candidate_call=candidate_calls[0] if len(candidate_calls)==1 else None
        receiver=self.instance_member(doc,fn,"scheduler","nextCandidates")
        result["assembly"]=receiver
        cdoc=cfn=None
        if receiver.get("state")=="source_constructor_member_provider_supported":
            cdoc,_,cfn=self.select(receiver["target"])
        candidate_decl=aa._bound_call(candidate_call) if candidate_call is not None else None
        candidate_binder=candidate_decl.child_by_field_name("name") if candidate_decl is not None else None
        loops=[node for node in aa._walk(fn.child_by_field_name("body"),skip_functions=True) if node.type=="for_in_statement"
            and aa._op(doc,node)=="of" and ctx.exact(doc,node.child_by_field_name("right"),candidate_binder)]
        loop=loops[0] if len(loops)==1 else None
        item=loop.child_by_field_name("left") if loop is not None else None
        # for-of lexical declarations have a declarator binder under `left`.
        if item is not None and item.type in {"lexical_declaration","variable_declaration"}:
            declarations=[node for node in aa._children(item) if node.type=="variable_declarator"]
            item=declarations[0].child_by_field_name("name") if len(declarations)==1 else None
        updates=aa._calls(doc,fn.child_by_field_name("body"),rule["transition"]["callee"])
        resolved_targets=[]
        reservation=None
        for call in updates:
            binding,wdoc,wfn=self.call_target(doc,call)
            patch=unwrap(aa._argument(call,rule["transition"]["patch_argument_index"]))
            guard=unwrap(aa._argument(call,rule["transition"]["guard_argument_index"]))
            pfields,pclosed=_pairs(doc,patch);gfields,gclosed=_pairs(doc,guard)
            status=aa._literal(doc,pfields.get("status"));expected=aa._literal(doc,gfields.get("expectedStatus"))
            mapped=bool(item is not None and _same_path(ctx,doc,aa._argument(call,1),item,["id"])
                and aa._path_of(doc,aa._argument(call,0))==["this","hubRoot"])
            version=gfields.get("expectedUpdatedAt")
            version_candidate=bool(version is not None and any(_same_path(ctx,doc,node,item,["updatedAt"]) for node in aa._walk(version)))
            if wfn is not None:resolved_targets.append((wdoc,wfn,binding))
            record={"call":self.ref(doc,call),"binding":binding,"patch_closed":pclosed,"guard_closed":gclosed,
                "status":status if isinstance(status,str) else None,"expected_status":expected if isinstance(expected,str) else None,
                "same_candidate_id_and_resource":mapped,"candidate_version_guard":version_candidate,"guard_version":self.ref(doc,version),
                "conditions":aa._conditions(doc,call,fn),"runtime_transition_success_verified":False}
            result["writes"].append(record)
            if isinstance(status,str) and isinstance(expected,str) and status!=expected and pclosed and gclosed and mapped and version_candidate:
                if reservation is None:reservation=(call,record)
                else:reservation=False
        writer=None;writer_closed=False
        targets={(value[0].source.path,value[1].start_byte,value[1].end_byte) for value in resolved_targets}
        if len(targets)==1 and resolved_targets:
            writer=self.guarded_update(resolved_targets[0][0],resolved_targets[0][1]);writer_closed=writer["state"]=="source_identity_status_version_guarded_write_supported"
        result["guarded_writer"]=writer
        candidate_closed=False
        if cfn is not None:
            class_name=receiver["target"]["symbol"].rsplit(".",1)[0]
            # Capture the selected pending filter, actual successful outputs, and all rejection/capacity conditions.
            pending_filters=[];helper_calls=[];helper_outputs=[];all_guards=[]
            for call in aa._calls(cdoc,cfn.child_by_field_name("body")):
                path=aa._path_of(cdoc,call.child_by_field_name("function")) or []
                if path[-1:]==["filter"]:
                    callback=unwrap(aa._argument(call,0))
                    if callback is not None and callback.type in aa._FUNCTIONS:
                        body=unwrap(callback.child_by_field_name("body"))
                        if body is not None and body.type=="binary_expression" and aa._op(cdoc,body)=="===" and _same_path(ctx,cdoc,body.child_by_field_name("left"),aa._param_node(callback,0),["status"]):
                            status=aa._literal(cdoc,body.child_by_field_name("right"))
                            if isinstance(status,str):pending_filters.append({"status":status,"filter":self.ref(cdoc,call),"predicate":self.ref(cdoc,body)})
                if len(path)==2 and path[0]=="this":
                    selector={"file":cdoc.source.path,"symbol":class_name+"."+path[1]}
                    hdoc,_,hfn=self.select(selector)
                    if hfn is not None:
                        helper_calls.append({"call":self.ref(cdoc,call),"target":self.ref(hdoc,hfn),"callee":path[1]})
                        for node in aa._walk(hfn.child_by_field_name("body")):
                            if node.type=="if_statement":all_guards.append({"location":self.ref(hdoc,node.child_by_field_name("condition")),
                                "early_exits":[self.ref(hdoc,child) for child in aa._walk(node.child_by_field_name("consequence"),skip_functions=True) if child.type in {"return_statement","continue_statement","throw_statement"}]})
                            if node.type=="call_expression" and (aa._path_of(hdoc,node.child_by_field_name("function")) or [])[-1:]==["push"]:
                                arg=unwrap(aa._argument(node,0))
                                if arg is not None and arg.type=="identifier":helper_outputs.append({"append":self.ref(hdoc,node),"item_binding":ctx.identity(hdoc,arg)})
                        if path[1]=="_preparePendingPool":
                            last=aa._children(hfn.child_by_field_name("body"))[-1]
                            reread=_return_expr(last) if last.type=="return_statement" else None
                            load_binding,ldoc,lfn=self.call_target(hdoc,reread) if reread is not None and reread.type=="call_expression" else ({},None,None)
                            provider=self.queue_entries_provider(ldoc,lfn) if lfn is not None else {"state":"unknown"}
                            result["candidate_flow"]["fresh_read"]={"binding":load_binding,"call":self.ref(hdoc,reread),
                                "same_logical_root":aa._path_of(hdoc,aa._argument(reread,0))==["this","hubRoot"] if reread is not None else False,
                                "return_definition":self.ref(ldoc,lfn),"provider_relation":provider}
            # Root identities are never rewritten in the scheduler; selected metadata copies are explicitly audited.
            selected_key=rule["completion"]["invariant"]["key_path"][1]
            key_writes=[];root_writes=[];metadata_copies=[]
            class_node=next((node for node in aa._ancestors(cfn) if node.type=="class_declaration"),None)
            for node in aa._walk(class_node):
                if node.type!="assignment_expression":continue
                left=node.child_by_field_name("left");path=aa._path_of(cdoc,left)
                if path is None:continue
                if path[-1:] in [["id"],rule["completion"]["invariant"]["project_path"]]:root_writes.append(self.ref(cdoc,node))
                if path[-2:]==rule["completion"]["invariant"]["key_path"]:key_writes.append(self.ref(cdoc,node))
                if path[-1:]==[rule["completion"]["invariant"]["key_path"][0]]:
                    right=unwrap(node.child_by_field_name("right"))
                    if right is not None and right.type=="identifier":right=unwrap(ctx.lexical(cdoc).initializer_for(ctx.identity(cdoc,right)))
                    parts=aa._children(right) if right is not None and right.type=="object" else []
                    first=unwrap(aa._children(parts[0])[0]) if parts and parts[0].type=="spread_element" and len(aa._children(parts[0]))==1 else None
                    if first is not None and first.type=="binary_expression" and aa._op(cdoc,first)=="||":first=unwrap(first.child_by_field_name("left"))
                    fields,closed=_pairs(cdoc,right,members=parts[1:]) if right is not None and right.type=="object" else ({},False)
                    metadata_copies.append({"assignment":self.ref(cdoc,node),"first_copy":self.ref(cdoc,first),"suffix_keys":sorted(fields),
                        "selected_key_disjoint":bool(closed and selected_key not in fields and first is not None and aa._path_of(cdoc,first)==path),
                        "unknown_suffix_spread":any(part.type=="spread_element" for part in parts[1:])})
            fresh=result["candidate_flow"].get("fresh_read",{})
            origin_reader=_CollectionOrigins(self,cdoc,class_name,fresh)
            origin=origin_reader.function(cfn,[])
            origin_supported=bool(origin.get("kind")=="collection" and origin.get("element",{}).get("kind")=="item"
                and origin["element"].get("origins")==["captured-logical-queue-entry"] and not origin_reader.gaps)
            supported_copies=[record for record in metadata_copies if record["selected_key_disjoint"]]
            # The unavailable branch's metadataPatch spread cannot reach eligible append: keep it as a refutation, never certify it.
            unsupported_copies=[record for record in metadata_copies if not record["selected_key_disjoint"]]
            candidate_closed=bool(len(pending_filters)==1 and fresh.get("binding",{}).get("state") in {"source_literal_module_member",*_ALLOWED_BINDINGS}
                and fresh.get("same_logical_root") and fresh.get("provider_relation",{}).get("state")=="source_loaded_queue_entries_subset"
                and origin_supported and not root_writes and not key_writes and helper_outputs and supported_copies
                and all(_excluded_helper_copy(cdoc,_node_at(cdoc,record["assignment"]),cfn) for record in unsupported_copies))
            result["candidate_flow"].update(state="source_pending_candidates_under_successful_gates" if candidate_closed else "unknown",
                membership_provenance={"state":"source_collection_return_origins_connected" if origin_supported else "unknown",
                    "return_origin":origin,"relations":origin_reader.relations,"gaps":origin_reader.gaps,"operations_reviewed":origin_reader.steps,
                    "scope":"actual initializer/assignments, class helper returns, Array filter/sort/slice, loop appends and map/destructure returns; membership and source identities, not runtime eligibility"},
                pending_filters=pending_filters,helper_bindings=helper_calls,successful_item_appends=helper_outputs,
                eligibility_conditions=all_guards,selected_root_field_writes=root_writes,selected_key_writes=key_writes,
                metadata_copies=metadata_copies,exclusion_scope="copies in a called rejection helper are outside eligible outputs only when the caller branch immediately continues")
        reservation_closed=False
        if reservation and candidate_call is not None and loop is not None:
            call,record=reservation
            decl=aa._bound_call(call)
            assigned=call.parent
            while assigned is not None and assigned.type not in {"assignment_expression","expression_statement","statement_block"}:assigned=assigned.parent
            reservation_binder=assigned.child_by_field_name("left") if assigned is not None and assigned.type=="assignment_expression" else decl.child_by_field_name("name") if decl is not None else None
            skips=[node for node in aa._walk(loop.child_by_field_name("body"),skip_functions=True) if node.type=="if_statement"
                and call.end_byte<node.start_byte and (lambda condition: condition is not None and condition.type=="unary_expression" and aa._op(doc,condition)=="!" and ctx.exact(doc,condition.child_by_field_name("argument"),reservation_binder))(unwrap(node.child_by_field_name("condition")))
                and any(child.type=="continue_statement" for child in aa._walk(node.child_by_field_name("consequence"),skip_functions=True))]
            waits=[node for node in aa._walk(loop.child_by_field_name("body"),skip_functions=True) if node.type=="await_expression" and node.start_byte>call.end_byte]
            leader_guards=[]
            for node in aa._walk(fn.child_by_field_name("body"),skip_functions=True):
                if node.type=="if_statement" and node.start_byte<call.start_byte and any(aa._path_of(doc,item.child_by_field_name("function"))==["this","leaderLock","stillHeld"] for item in aa._calls(doc,node.child_by_field_name("condition"))):
                    exits=[item for item in aa._walk(node.child_by_field_name("consequence"),skip_functions=True) if item.type=="return_statement"]
                    if exits:leader_guards.append({"guard":self.ref(doc,node.child_by_field_name("condition")),"returns":[self.ref(doc,item) for item in exits]})
            reservation_closed=bool(skips and waits and leader_guards and ctx.directly_awaited(doc,call))
            result["reservation"]={"state":"source_guarded_pending_reservation_supported" if reservation_closed else "unknown",**record,
                "reject_continue":[self.ref(doc,node) for node in skips],"leader_stop_guards":leader_guards,
                "subsequent_await_windows":[self.ref(doc,node) for node in waits],"candidate_call":self.ref(doc,candidate_call),"candidate_loop":self.ref(doc,loop)}
            self.op("scheduler_candidate_selection",doc,candidate_call,
                source_receiver=receiver,candidate_flow=result["candidate_flow"],candidate_loop=self.ref(doc,loop),
                scope="actual captured queue-entry members returned by the source scheduler")
            self.op("guarded_status_update",doc,call,from_status=record["expected_status"],to_status=record["status"],
                entry_identity="candidate.id",version_guard="candidate.updatedAt",resource="same constructor-captured logical hubRoot",
                eligibility="source pending filter and actual successful readiness/capacity/leader/version gates",guarded_writer=writer)
        # Rollback is extracted from the catch-local conditional object spread.
        rollbacks=[]
        for call in updates:
            patch=unwrap(aa._argument(call,rule["transition"]["patch_argument_index"]))
            parts=aa._children(patch) if patch is not None and patch.type=="object" else []
            if not parts or parts[0].type!="spread_element" or len(aa._children(parts[0]))!=1:continue
            variable=unwrap(aa._children(parts[0])[0]);initial=unwrap(ctx.lexical(doc).initializer_for(ctx.identity(doc,variable)))
            if initial is None or initial.type!="ternary_expression":continue
            for branch,field_name in (("consequence","true"),("alternative","false")):
                fields,closed=_pairs(doc,initial.child_by_field_name(branch));status=aa._literal(doc,fields.get("status"))
                if not closed or not isinstance(status,str):continue
                handler=next((node for node in aa._ancestors(call) if node.type=="catch_clause"),None)
                if handler is not None:
                    record={"call":self.ref(doc,call),"handler":self.ref(doc,handler),"conditional_patch":self.ref(doc,initial),
                        "patch_condition":self.ref(doc,initial.child_by_field_name("condition")),"selected_condition_value":field_name,"status":status,
                        "guard":self.ref(doc,aa._argument(call,rule["transition"]["guard_argument_index"])),"runtime_rollback_success_verified":False}
                    rollbacks.append(record);self.op("conditional_rollback_status",doc,call,to_status=status,condition=record["patch_condition"],condition_value=field_name)
        result["rollback"]={"state":"source_conditional_best_effort_rollback" if rollbacks else "unknown","paths":rollbacks,
            "limitation":"rollback requires dispatch failure before inboxWritten plus matching expected status/version; failure is caught, and published inbox is not unconditionally reset"}
        complete=bool(receiver.get("state")=="source_constructor_member_provider_supported" and candidate_closed and reservation_closed and writer_closed and rollbacks)
        result["state"]="source_guarded_scheduler_transition_supported" if complete else "unknown"
        self.model(MODEL_IDS[2],receiver.get("state")=="source_constructor_member_provider_supported",[receiver.get("constructor"),receiver.get("member_assignment")],
            ["Normal source-created orchestrator/scheduler instances retain their captured methods and receiver fields", "Injected or reflectively overwritten members are excluded and not inferred as default providers"])
        if not complete:self.gap("atomicity_scheduler_transition_incomplete","Actual candidate provider, queue identity, guarded writer or rollback is not fully connected")
        return result

    def operations_from_sources(self, facade: dict, authority: dict, predicates: dict, lifecycle_complete: bool,
            wrappers_complete: bool, resources: dict, inputs: dict) -> dict:
        ctx,rule=self.context,self.rule
        result={"state":"unknown","facade_operation":None,"authority_operation":None,"compound_key_equality":{},"counterevidence":[]}
        fdoc,_,ffn=self.select(rule["facade"]["owner"])
        adoc,_,afn=self.select(rule["authority"])
        if ffn is None or afn is None:return result
        outer_closed=bool(predicates.get("state")=="source_backed_standard_set_model" and predicates.get("outer_control_pattern_closed")
            and facade.get("syntax_order")=="read_select_write" and facade.get("existing_guard_early_exit")
            and all(record.get("all_guard_paths_return") for record in facade.get("existing_guard_early_exit",[])))
        read=_node_at(fdoc,facade.get("calls",{}).get("read",{}).get("location"))
        if outer_closed and read is not None:
            result["facade_operation"]=self.op("facade_active_precheck",fdoc,read,
                project_path=rule["completion"]["invariant"]["project_path"],key_path=rule["completion"]["invariant"]["key_path"],
                excluded_statuses=predicates["terminal_initializer"]["members"],
                selector_evidence=predicates["outer_terminal_rejection"],existing_guard=facade["existing_guard_early_exit"],
                order="successful selected read and active selection precede the authority call; read errors have an explicit empty fallback")
        wrapper=rule["protection"]["wrappers"][0]
        calls=aa._calls(adoc,afn.child_by_field_name("body"),wrapper["owner"]["symbol"].split(".")[-1])
        call=calls[0] if len(calls)==1 else None
        callback=unwrap(aa._argument(call,wrapper["callback_argument_index"])) if call is not None else None
        body=callback.child_by_field_name("body") if callback is not None else None
        push=_node_at(adoc,authority.get("insertion_location"))
        inserted=unwrap(aa._argument(push,0)) if push is not None else None
        init=unwrap(ctx.lexical(adoc).initializer_for(ctx.identity(adoc,inserted)))
        fields,closed=_pairs(adoc,init)
        initial_status=aa._literal(adoc,fields.get("status"))
        inner_statuses=authority.get("predicate_model",{}).get("status_equality_literals",[])
        find=_node_at(adoc,authority.get("find_location"))
        pred=unwrap(aa._argument(find,0)) if find is not None else None
        pred_body=pred.child_by_field_name("body") if pred is not None else None
        key_selector=rule["predicate_sources"]["key"]
        key_calls=aa._calls(adoc,pred_body,key_selector["symbol"].split(".")[-1])
        key_call=key_calls[0] if len(key_calls)==1 else None
        equality=key_call.parent if key_call is not None else None
        while equality is not None and equality.type in {"parenthesized_expression","as_expression","non_null_expression"}:equality=equality.parent
        other=None
        if equality is not None and equality.type=="binary_expression" and aa._op(adoc,equality)=="===":
            left,right=unwrap(equality.child_by_field_name("left")),unwrap(equality.child_by_field_name("right"))
            other=right if left is not None and left.id==key_call.id else left if right is not None and right.id==key_call.id else None
        current_key=unwrap(ctx.lexical(adoc).initializer_for(ctx.identity(adoc,other)))
        current_binding,kdoc,kfn=self.call_target(adoc,current_key,key_selector) if current_key is not None and current_key.type=="call_expression" else ({},None,None)
        normalized=unwrap(aa._argument(current_key,0)) if current_key is not None else None
        normalized_init=unwrap(ctx.lexical(adoc).initializer_for(ctx.identity(adoc,normalized)))
        input_param=aa._param_node(afn,1)
        starts=aa._children(normalized_init) if normalized_init is not None and normalized_init.type=="object" else []
        actual_input_origin=bool(starts and starts[0].type=="spread_element" and len(aa._children(starts[0]))==1
            and ctx.exact(adoc,aa._children(starts[0])[0],input_param))
        meta=fields.get(rule["completion"]["invariant"]["key_path"][0]);meta=unwrap(meta)
        if meta is not None and meta.type=="binary_expression" and aa._op(adoc,meta)=="||":meta=unwrap(meta.child_by_field_name("left"))
        inserted_metadata_same=bool(meta is not None and _same_path(ctx,adoc,meta,normalized,rule["completion"]["invariant"]["key_path"][:1]))
        normal_fields,normal_closed=_pairs(adoc,normalized_init,members=starts[1:]) if starts else ({},False)
        actual_key_fields_match=inserted_metadata_same and normal_closed
        key_field_connections=[]
        for field_path in predicates.get("authority_key_source",{}).get("field_paths",[]):
            if len(field_path)!=1:continue
            value=unwrap(fields.get(field_path[0]))
            if value is not None and value.type=="binary_expression" and aa._op(adoc,value)=="||":value=unwrap(value.child_by_field_name("left"))
            matched=bool(_same_path(ctx,adoc,value,normalized,field_path)
                or field_path[0] in normal_fields and value is not None and normal_fields[field_path[0]] is not None
                    and value.type in {"identifier","shorthand_property_identifier"} and normal_fields[field_path[0]].type in {"identifier","shorthand_property_identifier"}
                    and ctx.same(adoc,value,normal_fields[field_path[0]]))
            actual_key_fields_match=actual_key_fields_match and matched
            key_field_connections.append({"field_path":field_path,"entry_source":self.ref(adoc,value),"matches_incoming_source":matched})
        kreturns=_returns(kfn) if kfn is not None else []
        kexpr=_return_expr(kreturns[0]) if len(kreturns)==1 else None
        literal_constructor=bool(kexpr is not None and kexpr.type=="template_string" and len(aa._children(kexpr))>=3)
        result["compound_key_equality"]={"state":"source_same_key_function_on_existing_and_normalized_input" if current_binding.get("state") in _ALLOWED_BINDINGS and actual_input_origin and literal_constructor else "unknown",
            "existing_key_call":self.ref(adoc,key_call),"incoming_key_call":self.ref(adoc,current_key),"incoming_key_binding":current_binding,
            "incoming_input_origin":self.ref(adoc,normalized_init),"key_constructor":self.ref(kdoc,kexpr),
            "field_paths":predicates.get("authority_key_source",{}).get("field_paths",[]),
            "inserted_key_field_connections":key_field_connections,"inserted_key_matches_current_incoming":actual_key_fields_match,
            "structural_equality_scope":"equal selected scalar values render the same captured template; arbitrary distinct tuples are not claimed injective"}
        outer_paths={tuple(path) for path in predicates.get("outer_key_field_paths",[])}
        outer_paths.update(tuple(path) for path in facade.get("preselection_field_paths",[]))
        extras=[list(path) for path in predicates.get("authority_key_source",{}).get("field_paths",[]) if tuple(path) not in outer_paths]
        different=None
        for extra in extras:
            if len(extra)!=1 or kfn is None:continue
            project_path=rule["completion"]["invariant"]["project_path"];key_path=rule["completion"]["invariant"]["key_path"]
            first={project_path[0]:"<same project>",key_path[0]:{key_path[1]:"<same non-empty hashed key>"},extra[0]:"alpha"}
            second=deepcopy(first);second[extra[0]]="beta"
            first_key=_render_key_model(kdoc,kfn,ctx,first);second_key=_render_key_model(kdoc,kfn,ctx,second)
            if first_key is not None and second_key is not None and first_key!=second_key:
                different={"state":"source_template_predicate_difference_witness","varying_field_path":extra,
                    "common_project_key":"symbolic common non-empty scalar project/hash; the display tokens are not asserted runtime values",
                    "different_scalar_values":["alpha","beta"],"rendered_source_model_keys":[first_key,second_key],
                    "key_constructor":self.ref(kdoc,kexpr),"target_code_executed":False,
                    "scope":"finite registered string/data model; no arbitrary tuple injectivity or SHA preimage is claimed"}
                break
        result["compound_key_equality"]["different_description_witness"]=different
        no_await=bool(body is not None and not any(node.type in {"await_expression","yield_expression"} for node in aa._walk(body,skip_functions=True)))
        protected=bool(lifecycle_complete and wrappers_complete and authority.get("resource_forwarded")
            and resources.get("state")=="source_logical_resource_chain_supported")
        inner_closed=bool(authority.get("predicate_model",{}).get("state")=="source_closed_conjunction" and authority.get("early_existing_reuse")
            and authority.get("check_before_insert") and authority.get("find_push_same_member_path") and authority.get("queue_formal_stable")
            and closed and isinstance(initial_status,str) and len(inner_statuses)==1 and no_await and actual_key_fields_match
            and result["compound_key_equality"]["state"]=="source_same_key_function_on_existing_and_normalized_input"
            and inputs.get("state")=="source_request_identity_fields_connected_under_model" and protected)
        if inner_closed:
            result["authority_operation"]=self.op("protected_find_or_insert",adoc,push,initial_status=initial_status,
                matching_statuses=inner_statuses,key_field_paths=predicates["authority_key_source"]["field_paths"],
                find=authority["find_location"],reuse_guards=authority["early_existing_reuse"],entry_literal=self.ref(adoc,init),
                protection="acquire -> fresh queue -> actual callback -> changed queue normal publish -> release attempt",
                independent_process_fence="process fence covers acquisition and release, not the whole facade read",
                field_model=inputs,no_callback_await=no_await,entry_then_key_absent="then" not in fields)
        result["state"]="source_operations_connected" if outer_closed and inner_closed else "unknown"
        result["counterevidence"]=[{"kind":"facade_existing_nonterminal_reuse","evidence":facade.get("existing_guard_early_exit",[])},
            {"kind":"authority_has_locked_pending_recheck","evidence":authority.get("early_existing_reuse",[])},
            {"kind":"read_failure_empty_fallback","evidence":facade.get("read_catch_fallback",[])},
            {"kind":"normal_publish_not_guaranteed","evidence":resources.get("atomic_publish"),"condition":"acquire/read/callback/pre-publish failures can prevent selected commit; post-publish failures may be committed"}]
        self.model(MODEL_IDS[4],protected,[self.ref(adoc,call)],
            ["Successful directory owner-lock acquisition excludes concurrent selected queue mutations until release attempt", "The checked source acquire/fresh-read/callback/save/release lifecycle applies",
             "Directory lock safety, recovery, crash behavior and physical file-system correctness are trusted conditions, not statically certified", "A process fence is a narrower acquisition/release guard, not facade-wide serialization"])
        if not outer_closed:self.gap("atomicity_outer_operation_incomplete","Outer select/early reuse and order are not closed")
        if not inner_closed:self.gap("atomicity_authority_operation_incomplete","Authoritative key, ordinary collection, insertion or protected lifecycle relation is not closed")
        return result


def validate_atomicity_completion_rule(rule: Any) -> None:
    if not isinstance(rule,dict) or "completion" not in rule:
        raise ValueError("a full atomicity contract requires completion models and product invariant")
    base={key:value for key,value in rule.items() if key!="completion"}
    aa.validate_atomicity_rule(base)
    if "dependency_assembly" not in rule or "transition" not in rule:
        raise ValueError("full atomicity requires actual dependency assembly and transition source selectors")
    validate_completion(rule["completion"])


def complete_atomicity(snapshot: GraphSnapshot, rule: dict, *, prior_facts: Any = None) -> dict:
    """Compute all A1..A7 from authenticated saved source; prior facts are not authority."""
    if not isinstance(snapshot,GraphSnapshot):raise ValueError("atomicity completion requires a captured GraphSnapshot")
    validate_atomicity_completion_rule(rule)
    adapter=_Completion(snapshot,rule);ctx=adapter.context
    # Recompute the existing source summaries so externally supplied JSON cannot pre-certify relations.
    facade=aa._facade(ctx,rule)
    assembly=adapter.assembly()
    wrappers,wrappers_complete=aa._wrappers(ctx,rule)
    lifecycle,lifecycle_complete=aa._lifecycle(ctx,rule)
    authority=aa._authority(ctx,rule)
    predicates=aa._predicates(ctx,rule)
    resources=adapter.resources(facade,lifecycle)
    inputs=adapter.input_keys()
    scheduler=adapter.scheduler()
    source_ops=adapter.operations_from_sources(facade,authority,predicates,lifecycle_complete,wrappers_complete,resources,inputs)
    comparison=aa._compare(facade,authority,predicates,lifecycle_complete,wrappers_complete,{},assembly)
    critical_scans=[]
    for path,document in sorted(ctx.documents.items()):
        count=0
        for _ in aa._walk(document.tree.root_node):
            count+=1
            if count>_MAX_AST_NODES:break
        complete=count<=_MAX_AST_NODES and not document.tree.root_node.has_error and document.source.status=="parsed"
        critical_scans.append({"file":path,"source_hash":document.source.hash,"parser_version":document.parser_version,
            "ast_nodes_reviewed":count,"node_budget":_MAX_AST_NODES,"source_scan_complete":complete})
        if not complete:adapter.gap("atomicity_source_scan_incomplete","Selected source document is invalid, partial or over the AST budget",document,document.tree.root_node)
    source_complete=all(item["source_scan_complete"] for item in critical_scans)
    searches=[]
    operations_ready=source_ops["state"]=="source_operations_connected" and scheduler["state"]=="source_guarded_scheduler_transition_supported"
    if operations_ready and source_complete:
        excluded=predicates["terminal_initializer"]["members"]
        searches.append({"case":"same_description_with_scheduler",**_search_transitions(adapter.operations,excluded,descriptions_equal=True,include_scheduler=True)})
        searches.append({"case":"same_description_without_scheduler",**_search_transitions(adapter.operations,excluded,descriptions_equal=True,include_scheduler=False)})
        different=source_ops.get("compound_key_equality",{}).get("different_description_witness")
        if different:
            searches.append({"case":"same_product_key_different_description_without_scheduler","predicate_difference":different,
                **_search_transitions(adapter.operations,excluded,descriptions_equal=False,include_scheduler=False)})
    searches_complete=bool(searches and all(item["state"]=="bounded_source_transition_exploration_complete" for item in searches))
    witness=next((item["duplicate_witness"] for item in searches if item.get("duplicate_witness")),None)
    no_scheduler_case=next((item for item in searches if item["case"]=="same_description_without_scheduler"),{})
    solver_supported=bool(searches_complete and witness is not None and no_scheduler_case.get("duplicate_witness") is None)
    adapter.model(MODEL_IDS[6],solver_supported,[operation["location"] for operation in adapter.operations],
        ["Two selected default facade invocations share a logical queue/project/key and can overlap without extra external facade serialization",
         "Selected lock/read/normal-publish operations obey their independently applicable models",
         "Successful requests generate distinct entry IDs", "A real scheduler candidate passes captured readiness/capacity/leader/status/version guards",
         "The finite search is an existential conditional schedule; it does not prove that actual requests or scheduler timing take these steps"],
        states_explored=sum(item.get("states_explored",0) for item in searches),state_budget_per_case=_MAX_STATES,
        transition_ids=[operation["operation_id"] for operation in adapter.operations],interleaving_supplied_by_policy=False)
    if not solver_supported:adapter.gap("atomicity_interleaving_incomplete","No complete source/model-derived guarded transition exploration supports the conditional invariant violation")
    protection_supported=bool(lifecycle_complete and wrappers_complete and resources["state"]=="source_logical_resource_chain_supported")
    checks={
        "A1":assembly["state"]=="source_default_execution_chain_supported",
        "A2":bool(facade.get("syntax_order")=="read_select_write" and predicates.get("state")=="source_backed_standard_set_model"
            and source_ops.get("facade_operation") and inputs.get("producer",{}).get("state")=="source_request_identity_fields_supported"),
        "A3":resources["state"]=="source_logical_resource_chain_supported" and inputs["state"]=="source_request_identity_fields_connected_under_model"
            and scheduler.get("assembly",{}).get("state")=="source_constructor_member_provider_supported",
        "A4":protection_supported,
        "A5":bool(source_ops.get("authority_operation") and authority.get("early_existing_reuse")),
        "A6":scheduler["state"]=="source_guarded_scheduler_transition_supported",
        "A7":solver_supported,
    }
    evidence_by_id={"A1":assembly,"A2":{"facade":facade,"predicates":predicates,"producer":inputs.get("producer")},
        "A3":{"resources":resources,"inputs":inputs,"scheduler_receiver":scheduler.get("assembly")},
        "A4":{"wrapper_forwarding":wrappers,"lifecycle":lifecycle},"A5":{"authority":authority,"operation":source_ops.get("authority_operation"),"operation_derivation":source_ops},
        "A6":scheduler,"A7":{"searches":searches,"source_predicate_comparison":comparison,"operations":adapter.operations}}
    obligations=[{"id":name,"status":"supported" if supported and source_complete else "unknown", "evidence":evidence_by_id[name],
        "gaps":[] if supported and source_complete else [{"code":"necessary_source_relation_incomplete","obligation":name}],
        "source_category":"source-derived and independently applicable trusted models","runtime_result_verified":False}
        for name,supported in checks.items()]
    models_complete=bool(len(adapter.models)==len(MODEL_IDS) and {item["id"] for item in adapter.models}==set(MODEL_IDS)
        and all(item["state"]=="source_applicability_supported" for item in adapter.models))
    full=bool(all(item["status"]=="supported" for item in obligations) and models_complete and not adapter.gaps and witness is not None)
    conditions=[]
    for model in adapter.models:
        for condition in model["conditions"]:
            if condition not in conditions:conditions.append(condition)
    refutations={"source":source_ops.get("counterevidence",[]),"dependency_overrides":assembly.get("overrides",[]),
        "scheduler_rejection_and_rollback":scheduler,"bounded_cases":[{"case":item["case"],"duplicate_witness":item.get("duplicate_witness"),"refutations":item.get("refutations",{})} for item in searches],
        "runtime_limits":["A sequential facade that already sees scheduled/in_progress/nonterminal reuses the existing id",
            "The writer has a lock and a second check; an equal compound key still pending is reused",
            "Actual scheduler gates may prevent reservation; matching rollback may restore pending before the second authority check",
            "Read, lock, callback or pre-publish failure can prevent the selected commit; an error after rename may be committed",
            "The complete judgment is conditional and existential, never a claim that any pair of submissions duplicates or that all writers were analyzed"]}
    result={"schema":"callscope.atomicity-completion.v1","analyzer_version":VERSION,"snapshot_id":snapshot.id,"source_hash":snapshot.source_hash,
        "policy_hash":snapshot.policy_hash,"contract_hash":_digest(rule),"prior_facts_consumed_as_authority":False,
        "original_claim":"Same-key product reuse checks outside the queue authority and a narrower pending-only inner check admit a conditional duplicate across an actual guarded nonterminal scheduler transition",
        "derived_judgment":"Two same-project/key/description default submissions can both observe no row; the first protected insert can be guardedly scheduled before the second protected check; the pending-only inner check then inserts a second nonterminal row" if full else "Only supported source/model obligations are available; necessary relations remain unknown",
        "assessment":"scoped_static_judgment_reproduced" if full else "partial_obligations_supported" if any(checks.values()) else "unknown_or_source_invalid",
        "complete_assessment":full,"full_goal_supported":full,"obligations":obligations,"necessary_gaps":adapter.gaps,
        "source":{"captured_inputs":critical_scans,"source_scan_complete":source_complete,"selection_issues":ctx.issues,
            "node_ids":sorted(ctx.node_ids),"edge_ids":sorted(ctx.edge_ids),"facts_recomputed_from_saved_ast":True},
        "model":{"applications":adapter.models,"all_applications_supported":models_complete,"versioned_registry":list(MODEL_IDS)},
        "policy":{"invariant":deepcopy(rule["completion"]["invariant"]),"provenance":deepcopy(rule.get("provenance",{})),
            "policy_supplied_intermediate_relations":False,"policy_supplied_interleaving":False},
        "conditions":conditions,"refutations":refutations,"conditional_witness":witness,
        "analysis_scope":{"pure_static":True,"target_code_executed":False,"target_tests_run":False,"target_build_run":False,
            "runtime_duplicate_proof":False,"lock_correctness_verified":False,"physical_identity_verified":False,"all_writers_scope_closed":False,
            "bounded_source_model_interleaving_computed":bool(searches)},
        "coverage":{"obligation_count":7,"supported_obligation_count":sum(item["status"]=="supported" for item in obligations),
            "operation_count":len(adapter.operations),"search_count":len(searches),"incomplete":not source_complete,"truncated":False,"exhausted":False,
            "fact_count_is_not_runtime_or_business_coverage":True}}
    result["assessment_id"]=_digest({"version":VERSION,"snapshot":snapshot.id,"contract":_digest(rule),"assessment":result})[:24]
    return result


def analyze_atomicity_completions(snapshot: GraphSnapshot, rules: list[dict]) -> list[Finding]:
    if not isinstance(snapshot,GraphSnapshot):raise ValueError("atomicity completion requires a captured GraphSnapshot")
    if not isinstance(rules,list) or len(rules)>256:raise ValueError("atomicity completion rules must be a finite list")
    findings=[]
    ids=[rule.get("id") for rule in rules if isinstance(rule,dict)]
    for index,rule in enumerate(rules):
        try:
            validate_atomicity_completion_rule(rule)
            if ids.count(rule["id"])!=1:raise ValueError("duplicate completion contract identity")
            details=complete_atomicity(snapshot,rule)
        except (ValueError,TypeError,RecursionError,OverflowError) as exc:
            details={"schema":"callscope.atomicity-completion.v1","analyzer_version":VERSION,"snapshot_id":snapshot.id,"source_hash":snapshot.source_hash,
                "assessment":"unknown_or_source_invalid","complete_assessment":False,"full_goal_supported":False,
                "obligations":[{"id":"A"+str(i),"status":"unknown","evidence":{}} for i in range(1,8)],
                "necessary_gaps":[{"code":"atomicity_completion_invalid","message":str(exc)[:1000]}],"source":{},"model":{},"policy":{},"conditions":[],"refutations":{},
                "analysis_scope":{"pure_static":True,"target_code_executed":False,"target_tests_run":False,"target_build_run":False}}
        identity=rule.get("id",f"invalid-atomicity-completion-{index}") if isinstance(rule,dict) else f"invalid-atomicity-completion-{index}"
        fingerprint=_digest({"project":snapshot.project_id,"version":VERSION,"contract":rule})
        description=details.get("derived_judgment","Full static atomicity judgment remains unknown")
        locations=[operation["location"] for obligation in details.get("obligations",[]) if obligation.get("id")=="A7"
            for operation in obligation.get("evidence",{}).get("operations",[])]
        evidence=Evidence(id=_digest({"snapshot":snapshot.id,"fingerprint":fingerprint,"details":details})[:24],
            kind="static_atomicity_completion",message=description,locations=locations,
            node_ids=details.get("source",{}).get("node_ids",[]),edge_ids=details.get("source",{}).get("edge_ids",[]),details=details)
        findings.append(Finding(id=_digest({"snapshot":snapshot.id,"fingerprint":fingerprint})[:24],type="static_atomicity_completion",
            severity=rule.get("severity","medium") if isinstance(rule,dict) else "info",status="confirmed" if details["full_goal_supported"] else "uncertain",
            title="同键复用在受保护状态转换之间存在条件风险" if details["full_goal_supported"] else "同键复用完整静态义务尚未闭合",
            description=description,evidence=[evidence],rule_id=identity,node_ids=evidence.node_ids,edge_ids=evidence.edge_ids,
            fingerprint=fingerprint,snapshot_id=snapshot.id,
            metadata={"atomicity_completion_version":VERSION,"goal_id":"CPB-03","assessment":details["assessment"],
                "complete_assessment":details["complete_assessment"],"full_goal_supported":details["full_goal_supported"],"runtime_proof":False}))
    return findings
