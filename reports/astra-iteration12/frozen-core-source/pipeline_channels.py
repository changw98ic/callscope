"""Source-authenticated JSON/file/broker seams for finite pipeline reports.

No target is imported or executed.  This module connects actual operands,
declaration identities, path constructors, codecs and return projections under
explicit normal-channel models; it does not mint ordinary CALLS edges.
"""
from __future__ import annotations

from dataclasses import asdict
import hashlib
import json
from typing import Any

from . import atomicity_analysis as aa

VERSION="captured-pipeline-json-channels-1"
_MODEL_RECORD="ordinary-record-tree-flow-v1"
_MODEL_JSON="standard-json-record-codec-v1"
_MODEL_ASYNC="normal-async-callback-transfer-v1"
_MODEL_CHANNEL="normal-durable-record-channel-v1"
_MODEL_BROKER="normal-authenticated-json-broker-channel-v1"


def _digest(value:Any)->str:
    return hashlib.sha256(json.dumps(value,sort_keys=True,ensure_ascii=True,separators=(",",":"),allow_nan=False).encode()).hexdigest()


def _u(node:Any)->Any:return aa._unwrap(node)


def _returns(function:Any,*,nested:bool=False)->list[Any]:
    return [node for node in aa._walk(function.child_by_field_name("body"),skip_functions=not nested) if node.type=="return_statement"]


def _expression(returned:Any)->Any:
    children=aa._children(returned)
    return _u(children[0]) if len(children)==1 else None


def _path(document:Any,node:Any)->list[str]|None:
    node=_u(node)
    if node is None:return None
    if node.type in {"identifier","shorthand_property_identifier","shorthand_property_identifier_pattern","this"}:return [document.text(node)]
    if node.type in {"member_expression","subscript_expression"}:
        root=_path(document,node.child_by_field_name("object"))
        key=node.child_by_field_name("property") if node.type=="member_expression" else node.child_by_field_name("index")
        value=document.text(key) if key is not None and key.type in {"identifier","property_identifier","private_property_identifier"} else aa._literal(document,key)
        return [*root,value] if root is not None and isinstance(value,str) else None
    return None


def _pairs(document:Any,node:Any)->tuple[dict[str,Any],bool]:
    node=_u(node);fields={};closed=node is not None and node.type=="object"
    for child in aa._children(node) if closed else []:
        if child.type=="pair":
            key=child.child_by_field_name("key");name=document.text(key) if key is not None and key.type in {"identifier","property_identifier"} else aa._literal(document,key)
            value=_u(child.child_by_field_name("value"))
        elif child.type=="shorthand_property_identifier":name=document.text(child);value=child
        else:closed=False;continue
        if not isinstance(name,str) or name in fields or name=="__proto__" or value is None:closed=False;continue
        fields[name]=value
    return fields,closed


class _Channels:
    def __init__(self,analysis:Any):
        self.analysis=analysis;self.snapshot=analysis.snapshot;self.rule=analysis.rule
        self.context=aa._Analysis(self.snapshot,analysis.sources)
        self.gaps=[];self.relations=[];self.models=[];self.steps=0

    def ref(self,document:Any,definition:Any,node:Any)->dict|None:
        if document is None or node is None:return None
        result=document.location(node);result.update(anchor=asdict(self.analysis.anchor(document,definition,node)),extractor_version=VERSION)
        return result

    def gap(self,code:str,document:Any=None,definition:Any=None,node:Any=None,**details:Any)->None:
        value={"code":code,**details,"location":self.ref(document,definition,node)}
        if value not in self.gaps:self.gaps.append(value)

    def relation(self,relation_kind:str,source_document:Any,source_definition:Any,source_node:Any,**details:Any)->dict:
        self.steps+=1
        value={"relation_kind":relation_kind,"location":self.ref(source_document,source_definition,source_node),"conditions":list(self.analysis.conditions(source_document,source_definition,source_node)),
            "target_code_executed":False,"creates_calls_edge":False,**details}
        value["relation_id"]=_digest({"version":VERSION,"snapshot":self.snapshot.id,**value})[:24]
        self.relations.append(value)
        return value

    def role(self,symbol:str,*,file:str|None=None)->tuple[Any,Any,Any]|None:
        selectors=[candidate for candidate in self.rule.get("sources",[]) if candidate.get("symbol")==symbol and (file is None or candidate.get("file")==file)]
        if len(selectors)!=1:
            self.gap("pipeline_channel_source_locator_not_unique",symbol=symbol,file=file,count=len(selectors));return None
        result=self.analysis.component(selectors[0])
        if result is None:self.gap("pipeline_channel_source_invalid",selector=selectors[0])
        return result

    def target(self,document:Any,definition:Any,call:Any)->tuple[dict,tuple[Any,Any,Any]|None]:
        edge,issues=self.analysis.sources.call_binding(call,document,definition.node)
        relation={"state":"unknown","location":self.ref(document,definition,call),"binding_issues":issues,"creates_calls_edge":False}
        if edge is not None:
            nodes=[node for node in self.snapshot.nodes if node.id==edge.target]
            if len(nodes)==1:
                target_doc,target_def,gaps=self.analysis.sources.definition_for_node(nodes[0])
                if target_doc is not None and target_def is not None and not gaps:
                    target=self.analysis.component({"file":target_doc.source.path,"symbol":target_def.symbol})
                    if target is not None:relation.update(state="existing_snapshot_binding",edge_id=edge.id,target={"file":target_doc.source.path,"symbol":target_def.symbol});return relation,target
        path=_path(document,call.child_by_field_name("function"))
        if path is not None and len(path)==2 and path[0]=="this" and "." in definition.symbol:
            cls=definition.symbol.rsplit(".",1)[0]
            selector={"file":document.source.path,"symbol":cls+"."+path[1]}
            target=self.analysis.component(selector)
            if target is not None:
                relation.update(state="same_source_class_member_relation",target=selector,scope="normal source-created receiver retains captured class methods; no CALLS promotion")
                return relation,target
        imported=self.analysis.dynamic_import_binding(document,definition,call.child_by_field_name("function"))
        if imported.get("supported"):
            target=self.analysis.component(imported["target_selector"])
            relation.update(state="source_literal_module_member",target=imported["target_selector"],source_relation=imported)
            return relation,target
        # Existing same-file unique lexical declarations are an independent source relation.
        fallback,doc,fn=self.context.source_callee(document,call)
        if fallback.get("state") in {"snapshot_resolved","source_lexical_declaration_relation"} and doc is not None:
            target_def=doc.definition_for_ast(fn)
            if target_def is not None:
                target=self.analysis.component({"file":doc.source.path,"symbol":target_def.symbol})
                relation.update(state=fallback["state"],source_relation=fallback,target={"file":doc.source.path,"symbol":target_def.symbol})
                return relation,target
        return relation,None

    def same(self,document:Any,left:Any,right:Any)->bool:
        lpath,rpath=_path(document,left),_path(document,right)
        if not lpath or not rpath or lpath[1:]!=rpath[1:]:return False
        if lpath[0]==rpath[0]=="this":return True
        lroot=left;rroot=right
        while lroot is not None and _u(lroot).type in {"member_expression","subscript_expression"}:lroot=_u(lroot).child_by_field_name("object")
        while rroot is not None and _u(rroot).type in {"member_expression","subscript_expression"}:rroot=_u(rroot).child_by_field_name("object")
        # Equality here authenticates declaration identity only.  It does not
        # establish a stable current value; codec/alias/provider gates review
        # their actual source operations separately.
        li=self.analysis.reader(document).resolve_identity(_u(lroot));ri=self.analysis.reader(document).resolve_identity(_u(rroot))
        return bool(li.get("state")==ri.get("state")=="unique" and li.get("declaration_id")==ri.get("declaration_id"))

    def initializer(self,document:Any,node:Any)->Any:
        info=self.analysis.reader(document).resolve(_u(node)) if node is not None else {}
        return _u(self.analysis.reader(document).initializer_for(info))

    def model(self,name:str,supported:bool,evidence:list[dict|None],conditions:list[str])->dict:
        enabled=name in self.rule.get("models",[])
        value={"id":name,"enabled":enabled,"supported":bool(enabled and supported),"evidence":[item for item in evidence if item],
            "conditions":conditions,"runtime_provider_verified":False}
        value["model_application_id"]=_digest({"version":VERSION,"snapshot":self.snapshot.id,**value})[:24]
        self.models.append(value)
        return value

    def codec_normalizer(self,component:tuple)->dict:
        doc,definition,fn=component;formal=aa._param_node(fn,0)
        calls=aa._calls(doc,fn.child_by_field_name("body"))
        clones=[call for call in calls if _path(doc,call.child_by_field_name("function"))==["structuredClone"] and self.same(doc,aa._argument(call,0),formal)]
        clone=clones[0] if len(clones)==1 else None
        assignments=[node for node in aa._walk(fn.child_by_field_name("body"),skip_functions=True) if node.type=="assignment_expression"]
        clone_bindings=[node.child_by_field_name("left") for node in assignments if clone is not None and _u(node.child_by_field_name("right")).id==clone.id]
        strings=[call for call in calls if _path(doc,call.child_by_field_name("function"))==["JSON","stringify"] and any(self.same(doc,aa._argument(call,0),binder) for binder in clone_bindings)]
        stringify=strings[0] if len(strings)==1 else None
        string_bindings=[node.child_by_field_name("left") for node in assignments if stringify is not None and _u(node.child_by_field_name("right")).id==stringify.id]
        parses=[call for call in calls if _path(doc,call.child_by_field_name("function"))==["JSON","parse"] and any(self.same(doc,aa._argument(call,0),binder) for binder in string_bindings)]
        parse=parses[0] if len(parses)==1 else None
        parse_decl=aa._bound_call(parse) if parse is not None else None
        parsed=parse_decl.child_by_field_name("name") if parse_decl is not None else None
        returns=[node for node in _returns(fn) if self.same(doc,_expression(node),parsed)]
        guards=[node for node in aa._walk(fn.child_by_field_name("body"),skip_functions=True) if node.type=="if_statement" and parse is not None and node.start_byte>parse.end_byte
            and any(child.type=="throw_statement" for child in aa._walk(node.child_by_field_name("consequence"),skip_functions=True))]
        environment=bool(parse is not None and self.analysis.reader(doc).unbound("JSON",parse).get("local_declaration_absent")
            and clone is not None and self.analysis.reader(doc).unbound("structuredClone",clone).get("local_declaration_absent"))
        supported=bool(clone is not None and stringify is not None and parse is not None and returns and guards and environment
            and clone.start_byte<stringify.start_byte<parse.start_byte<returns[-1].start_byte)
        result={"supported":supported,"input":self.ref(doc,definition,formal),"structured_clone":self.ref(doc,definition,clone),
            "json_encode":self.ref(doc,definition,stringify),"json_decode":self.ref(doc,definition,parse),"returned_record":[self.ref(doc,definition,node) for node in returns],
            "object_guard":[self.ref(doc,definition,node) for node in guards],"record_scope":"finite acyclic plain JSON record, finite ordinary scalar fields; codec errors, undefined/nonfinite/custom providers are separate"}
        self.relation("clone_json_encode_decode_return",doc,definition,fn,**result)
        self.model(_MODEL_JSON,supported,[result["json_encode"],result["json_decode"]],
            ["Standard structuredClone/JSON providers retain registered semantics", "The selected payload is a finite ordinary JSON object with finite scalar maxRetries; unsupported values or codec failures are not preservation claims"])
        return result

    def data_file_writer(self,component:tuple)->dict:
        doc,definition,fn=component;file_formal=aa._param_node(fn,0);data_formal=aa._param_node(fn,1)
        calls=aa._calls(doc,fn.child_by_field_name("body"));result={"supported":False,"definition":self.ref(doc,definition,fn)}
        contents=[]
        for call in calls:
            if self.same(doc,aa._argument(call,0),data_formal):
                binding,target=self.target(doc,definition,call)
                if target is not None:
                    cdoc,cdef,cfn=target;json_calls=[node for node in aa._calls(cdoc,cfn.child_by_field_name("body")) if _path(cdoc,node.child_by_field_name("function"))==["JSON","stringify"]
                        and self.same(cdoc,aa._argument(node,0),aa._param_node(cfn,0))]
                    if json_calls:contents.append((call,binding,target,json_calls[0]))
        content=contents[0] if len(contents)==1 else None;content_decl=aa._bound_call(content[0]) if content is not None else None
        content_binder=content_decl.child_by_field_name("name") if content_decl is not None else None
        writes=[call for call in calls if (_path(doc,call.child_by_field_name("function")) or [])[-1:]==["writeFile"]
            and self.same(doc,aa._argument(call,0),content_binder) and aa._literal(doc,aa._argument(call,1))=="utf8"]
        write=writes[0] if len(writes)==1 else None;handle=write.child_by_field_name("function").child_by_field_name("object") if write is not None else None
        assignments=[node for node in aa._walk(fn.child_by_field_name("body"),skip_functions=True) if node.type=="assignment_expression" and self.same(doc,node.child_by_field_name("left"),handle)]
        opens=[]
        for mutation in assignments:
            call=_u(mutation.child_by_field_name("right"))
            if call is not None and call.type=="call_expression" and (_path(doc,call.child_by_field_name("function")) or [])[-1:]==["open"] and write is not None and call.end_byte<write.start_byte:opens.append(call)
        opening=opens[0] if len(opens)==1 else None;temp=aa._argument(opening,0) if opening is not None else None
        renames=[call for call in calls if (_path(doc,call.child_by_field_name("function")) or [])[-1:]==["rename"]
            and self.same(doc,aa._argument(call,0),temp) and self.same(doc,aa._argument(call,1),file_formal)]
        rename=renames[0] if len(renames)==1 else None
        hooks=opening.child_by_field_name("function").child_by_field_name("object") if opening is not None else None
        hook_initializer=self.initializer(doc,hooks);hbind,htarget=self.target(doc,definition,hook_initializer) if hook_initializer is not None and hook_initializer.type=="call_expression" else ({},None)
        default_hooks={};hook_choice=None
        if htarget is not None:
            hdoc,hdef,hfn=htarget
            returns=_returns(hfn);expression=_expression(returns[0]) if len(returns)==1 else None
            if expression is not None and expression.type=="binary_expression" and aa._op(hdoc,expression)=="??":
                default=_u(expression.child_by_field_name("right"));default_init=self.initializer(hdoc,default)
                default_fields,closed=_pairs(hdoc,default_init)
                if closed:
                    for name in ("open","rename"):
                        info=self.analysis.reader(hdoc).resolve(default_fields.get(name));imported=info.get("import") or {}
                        default_hooks[name]={"supported":imported.get("module") in {"node:fs/promises","fs/promises"} and imported.get("imported_name")==name,
                            "location":self.ref(hdoc,hdef,default_fields.get(name)),"binding_identity":info}
                hook_choice=self.ref(hdoc,hdef,expression)
        same_hooks=bool(opening is not None and rename is not None and self.same(doc,opening.child_by_field_name("function").child_by_field_name("object"),rename.child_by_field_name("function").child_by_field_name("object")))
        supported=bool(content is not None and write is not None and opening is not None and rename is not None and same_hooks
            and all(default_hooks.get(name,{}).get("supported") for name in ("open","rename")) and write.end_byte<rename.start_byte)
        result.update(supported=supported,data_argument=self.ref(doc,definition,data_formal),file_argument=self.ref(doc,definition,file_formal),
            json_content_call=self.ref(doc,definition,content[0]) if content else None,json_content_binding=content[1] if content else None,
            json_encode=self.ref(content[2][0],content[2][1],content[3]) if content else None,
            open_temp=self.ref(doc,definition,opening),write_content=self.ref(doc,definition,write),rename_same_temp=self.ref(doc,definition,rename),
            hooks_binding=hbind,default_hooks=default_hooks,hook_choice=hook_choice,
            provider_condition="currentHooks selects captured default node fs providers; injected test hooks are a separate source branch",
            error_scope="pre-publish failure, ambiguous publication and post-rename durability errors are not a guaranteed successful commit")
        self.relation("actual_json_content_handle_temp_rename",doc,definition,fn,**result)
        return result

    def data_file_reader(self,component:tuple)->dict:
        doc,definition,fn=component;result={"supported":False,"definition":self.ref(doc,definition,fn)}
        returns=_returns(fn);expression=_expression(returns[0]) if len(returns)==1 else None
        # _readLocalInboxJson directly delegates; then optional .record projection is followed.
        if expression is not None and expression.type=="call_expression":
            binding,target=self.target(doc,definition,expression)
            if target is not None:
                tdoc,tdef,tfn=target;next_returns=_returns(tfn);project=_expression(next_returns[0]) if len(next_returns)==1 else None
                if project is not None and project.type=="binary_expression" and aa._op(tdoc,project)=="??":project=_u(project.child_by_field_name("left"))
                projected_call=_u(project.child_by_field_name("object")) if project is not None and project.type=="member_expression" and tdoc.text(project.child_by_field_name("property"))=="record" else None
                if projected_call is not None and projected_call.type=="call_expression":
                    second_binding,authority=self.target(tdoc,tdef,projected_call)
                    if authority is not None:
                        adoc,adef,afn=authority;calls=aa._calls(adoc,afn.child_by_field_name("body"));parses=[call for call in calls if _path(adoc,call.child_by_field_name("function"))==["JSON","parse"]]
                        parse=parses[0] if len(parses)==1 else None;raw=aa._argument(parse,0) if parse is not None else None
                        raw_assignments=[node for node in aa._walk(afn.child_by_field_name("body"),skip_functions=True) if node.type=="assignment_expression" and self.same(adoc,node.child_by_field_name("left"),raw)]
                        reader=_u(raw_assignments[0].child_by_field_name("right")) if len(raw_assignments)==1 else None
                        parsed_decl=aa._bound_call(parse) if parse is not None else None;parsed=parsed_decl.child_by_field_name("name") if parsed_decl is not None else None
                        returned_records=[]
                        for returned in _returns(afn):
                            fields,closed=_pairs(adoc,_expression(returned))
                            if closed and self.same(adoc,fields.get("record"),parsed):returned_records.append(returned)
                        same_path=bool(reader is not None and reader.type=="call_expression" and self.same(adoc,aa._argument(reader,0),aa._param_node(afn,0))
                            and self.same(tdoc,aa._argument(projected_call,0),aa._param_node(tfn,0)) and self.same(doc,aa._argument(expression,0),aa._param_node(fn,0)))
                        supported=bool(same_path and parse is not None and returned_records and self.analysis.reader(adoc).unbound("JSON",parse).get("local_declaration_absent"))
                        result.update(supported=supported,path_forwarding=same_path,delegation=binding,record_projection=self.ref(tdoc,tdef,project),authority_binding=second_binding,
                            read_bytes=self.ref(adoc,adef,reader),json_decode=self.ref(adoc,adef,parse),returned_records=[self.ref(adoc,adef,node) for node in returned_records],
                            guards=[self.ref(adoc,adef,node) for node in aa._walk(afn.child_by_field_name("body"),skip_functions=True) if node.type=="if_statement" and any(child.type in {"throw_statement","return_statement"} for child in aa._walk(node.child_by_field_name("consequence"),skip_functions=True))],
                            error_scope="missing/malformed/not-object/generation-change outcomes are preserved; only selected successful pinned read returns a decoded record")
        self.relation("actual_file_read_decode_record_projection",doc,definition,fn,**result)
        return result

    def callback_result(self,component:tuple,parameter_index:int)->dict:
        """Follow an actual callback completion operand, without running it."""
        doc,definition,fn=component;formal=aa._param_node(fn,parameter_index)
        calls=[call for call in aa._calls(doc,fn.child_by_field_name("body"))
            if self.same(doc,call.child_by_field_name("function"),formal)]
        call=calls[0] if len(calls)==1 else None
        assignments=[node for node in aa._walk(fn.child_by_field_name("body"),skip_functions=True)
            if node.type=="assignment_expression" and call is not None and _u(node.child_by_field_name("right")).id==call.id]
        assignment=assignments[0] if len(assignments)==1 else None
        operand=assignment.child_by_field_name("left") if assignment is not None else None
        returns=[node for node in _returns(fn) if self.same(doc,_expression(node),operand)
            and assignment is not None and node.start_byte>assignment.end_byte]
        changed_after=[node for node in aa._walk(fn.child_by_field_name("body"),skip_functions=True)
            if node.type=="assignment_expression" and assignment is not None and node.start_byte>assignment.end_byte
            and self.same(doc,node.child_by_field_name("left"),operand)]
        guards=[node for node in aa._walk(fn.child_by_field_name("body"),skip_functions=True)
            if node.type=="if_statement" and assignment is not None and node.start_byte>assignment.end_byte
            and any(child.type=="throw_statement" for child in aa._walk(node.child_by_field_name("consequence"),skip_functions=True))]
        result={"supported":bool(call is not None and assignment is not None and returns and not changed_after),
            "callback_parameter_index":parameter_index,"actual_callback_call":self.ref(doc,definition,call),
            "captured_result_assignment":self.ref(doc,definition,assignment),
            "returned_same_result":[self.ref(doc,definition,node) for node in returns],
            "normal_completion_guards":[self.ref(doc,definition,node) for node in guards],
            "later_result_reassignments":[self.ref(doc,definition,node) for node in changed_after],
            "model_scope":"selected normal async callback completion; callback/lock/release failures are preserved alternate outcomes"}
        self.relation("actual_callback_completion_assignment_return",doc,definition,fn,**result)
        return result

    def inbox(self)->dict:
        write=self.role("WorkerStore.writeInboxWithReceipt");read=self.role("WorkerStore.claimInboxEntries");constructor=self.role("WorkerStore.constructor")
        result={"supported":False,"kind":"worker_inbox_file_record","writer":{},"reader":{},"record_identity":{},"branches":[]}
        if any(component is None for component in (write,read,constructor)):return result
        doc,definition,fn=write;rdoc,rdef,rfn=read;c_doc,c_def,c_fn=constructor
        normalized_calls=[call for call in aa._calls(doc,fn.child_by_field_name("body")) if _path(doc,call.child_by_field_name("function"))==["normalizeJsonRecord"] and self.same(doc,aa._argument(call,0),aa._param_node(fn,1))]
        normal=normalized_calls[0] if len(normalized_calls)==1 else None
        binding,normal_target=self.target(doc,definition,normal) if normal is not None else ({},None)
        codec=self.codec_normalizer(normal_target) if normal_target is not None else {"supported":False}
        normal_decl=aa._bound_call(normal) if normal is not None else None;payload=normal_decl.child_by_field_name("name") if normal_decl is not None else None
        declarations=[node for node in aa._walk(fn.child_by_field_name("body")) if node.type=="variable_declarator"]
        files=[node for node in declarations if (lambda initial: initial is not None and initial.type=="call_expression" and _path(doc,initial.child_by_field_name("function"))==["path","join"]
            and _path(doc,aa._argument(initial,0))==["this","inboxDir"])(self.initializer(doc,node.child_by_field_name("name")))]
        file_decl=files[0] if len(files)==1 else None;file_binder=file_decl.child_by_field_name("name") if file_decl is not None else None;file_call=_u(file_decl.child_by_field_name("value")) if file_decl is not None else None
        file_id=None
        if file_call is not None:
            template=_u(aa._argument(file_call,2));substitutions=[child for child in aa._children(template) if child.type=="template_substitution"] if template is not None and template.type=="template_string" else []
            file_id=_u(aa._children(substitutions[0])[0]) if len(substitutions)==1 and len(aa._children(substitutions[0]))==1 else None
        identity_initial=self.initializer(doc,file_id);identity_source=_u(aa._argument(identity_initial,0)) if identity_initial is not None and identity_initial.type=="call_expression" else None
        identity_source=_u(identity_source.child_by_field_name("left")) if identity_source is not None and identity_source.type=="binary_expression" and aa._op(doc,identity_source)=="||" else identity_source
        id_from_payload=bool(identity_source is not None and _path(doc,identity_source)[-1:]==["assignmentId"] and self.same(doc,identity_source.child_by_field_name("object"),payload)) if _path(doc,identity_source) else False
        stage_writes=[];published=[];receipts=[]
        for call in aa._calls(doc,fn.child_by_field_name("body"),nested=True):
            if _path(doc,call.child_by_field_name("function"))==["writeJsonAtomic"] and self.same(doc,aa._argument(call,1),payload):stage_writes.append(call)
            if _path(doc,call.child_by_field_name("function"))==["rename"] and self.same(doc,aa._argument(call,1),file_binder):published.append(call)
            if _path(doc,call.child_by_field_name("function"))==["inboxReceipt"]:
                fields,closed=_pairs(doc,aa._argument(call,0))
                if closed and self.same(doc,fields.get("committedRecord"),payload) and self.same(doc,fields.get("assignmentId"),file_id):receipts.append((call,fields))
        stage=stage_writes[0] if len(stage_writes)==1 else None;publication=published[0] if len(published)==1 else None
        same_staging=bool(stage is not None and publication is not None and self.same(doc,aa._argument(stage,0),aa._argument(publication,0)) and stage.end_byte<publication.start_byte)
        filesystem_binding,filesystem=self.target(doc,definition,stage) if stage is not None else ({},None)
        atomic=self.data_file_writer(filesystem) if filesystem is not None else {"supported":False}
        result["writer"]={"supported":bool(codec["supported"] and same_staging and atomic["supported"] and id_from_payload and receipts),
            "normalize_call":self.ref(doc,definition,normal),"normalization_binding":binding,"codec":codec,
            "file_construction":self.ref(doc,definition,file_call),"assignment_id_source":self.ref(doc,definition,identity_initial),"id_from_committed_payload":id_from_payload,
            "staging_write":self.ref(doc,definition,stage),"publication_rename":self.ref(doc,definition,publication),"same_staging_path":same_staging,
            "fs_binding":filesystem_binding,"atomic_json_writer":atomic,"committed_record_receipts":[self.ref(doc,definition,call) for call,_ in receipts],
            "receipt_keys":sorted(receipts[0][1]) if receipts else [],
            "guards":[self.ref(doc,definition,node) for node in aa._walk(fn.child_by_field_name("body"),skip_functions=False) if node.type=="if_statement" and any(child.type=="throw_statement" for child in aa._walk(node.child_by_field_name("consequence"),skip_functions=True))]}
        receipt_projection={"supported":False}
        if receipts:
            receipt_call=receipts[0][0];receipt_binding,receipt_target=self.target(doc,definition,receipt_call)
            if receipt_target is not None:
                tdoc,tdef,tfn=receipt_target;returns=_returns(tfn);returned=_expression(returns[0]) if len(returns)==1 else None
                record=aa._argument(returned,0) if returned is not None and returned.type=="call_expression" else None;fields,_=_pairs(tdoc,record)
                cloning=_u(fields.get("committedRecord"));clone_binding,clone_target=self.target(tdoc,tdef,cloning) if cloning is not None and cloning.type=="call_expression" else ({},None)
                source=_u(aa._argument(cloning,0)) if cloning is not None else None
                selected_source=bool(source is not None and (_path(tdoc,source) or [])[1:]==["committedRecord"] and self.same(tdoc,source.child_by_field_name("object"),aa._param_node(tfn,0)))
                clone_supported=False
                if clone_target is not None:
                    cdoc,cdef,cfn=clone_target;c_returns=_returns(cfn);value=_expression(c_returns[0]) if len(c_returns)==1 else None
                    clone_expr=_u(value.child_by_field_name("alternative")) if value is not None and value.type=="ternary_expression" else None
                    clone_supported=bool(clone_expr is not None and clone_expr.type=="call_expression" and _path(cdoc,clone_expr.child_by_field_name("function"))==["structuredClone"]
                        and self.same(cdoc,aa._argument(clone_expr,0),aa._param_node(cfn,0)) and self.same(cdoc,value.child_by_field_name("consequence"),aa._param_node(cfn,0)))
                freezer_binding,freezer_target=self.target(tdoc,tdef,returned) if returned is not None and returned.type=="call_expression" else ({},None)
                freezer_supported=False
                if freezer_target is not None:
                    fdoc,fdef,ffn=freezer_target;f_returns=_returns(ffn);last=f_returns[-1] if f_returns else None
                    freezer_supported=bool(last is not None and self.same(fdoc,_expression(last),aa._param_node(ffn,0)))
                receipt_projection={"supported":selected_source and clone_supported and freezer_supported,"receipt_binding":receipt_binding,
                    "committed_record_clone":self.ref(tdoc,tdef,cloning),"clone_binding":clone_binding,"clone_supported":clone_supported,
                    "freezer_binding":freezer_binding,"returns_same_freeze_operand":freezer_supported,"model_scope":"finite ordinary JSON records; structuredClone preserves data and standard Object.freeze changes mutability rather than selected fields"}
        result["writer"]["receipt_projection"]=receipt_projection
        result["writer"]["supported"]=result["writer"]["supported"] and receipt_projection["supported"]
        read_calls=aa._calls(rdoc,rfn.child_by_field_name("body"),nested=True)
        read_publications=[];decoders=[]
        for call in read_calls:
            if _path(rdoc,call.child_by_field_name("function"))==["rename"]:
                source,claimed=aa._argument(call,0),aa._argument(call,1)
                sinit,cinit=self.initializer(rdoc,source),self.initializer(rdoc,claimed)
                if sinit is not None and cinit is not None and _path(rdoc,sinit.child_by_field_name("function"))==["path","join"] and _path(rdoc,cinit.child_by_field_name("function"))==["path","join"]:
                    if self.same(rdoc,aa._argument(sinit,1),aa._argument(cinit,1)):read_publications.append((call,source,claimed,sinit,cinit))
            if _path(rdoc,call.child_by_field_name("function"))==["this","_readLocalInboxJson"]:decoders.append(call)
        # Select the payload rename whose claimed destination is actually decoded, excluding owner/rollback rename.
        candidates=[record for record in read_publications if any(self.same(rdoc,record[2],aa._argument(call,0)) for call in decoders)]
        moved=candidates[0] if len(candidates)==1 else None;decode=next((call for call in decoders if moved is not None and self.same(rdoc,moved[2],aa._argument(call,0))),None)
        dbind,dtarget=self.target(rdoc,rdef,decode) if decode is not None else ({},None)
        reader=self.data_file_reader(dtarget) if dtarget is not None else {"supported":False}
        decode_decl=aa._bound_call(decode) if decode is not None else None;assignment=decode_decl.child_by_field_name("name") if decode_decl is not None else None
        returned=[];malformed=[]
        for statement in _returns(rfn,nested=True):
            fields,closed=_pairs(rdoc,_expression(statement))
            if closed and self.same(rdoc,fields.get("assignment"),assignment):returned.append(statement)
            if fields.get("assignment") is not None and _u(fields["assignment"]).type=="object":malformed.append(self.ref(rdoc,rdef,statement))
        callback=next((node for node in aa._ancestors(returned[0]) if node.type in aa._FUNCTIONS),None) if returned else None
        lock_calls=[call for call in read_calls if _path(rdoc,call.child_by_field_name("function"))==["this","_withLocalInboxLock"]
            and callback is not None and _u(aa._argument(call,2)).id==callback.id]
        lock_call=lock_calls[0] if len(lock_calls)==1 else None
        lock_decl=aa._bound_call(lock_call) if lock_call is not None else None
        claim=lock_decl.child_by_field_name("name") if lock_decl is not None else None
        lock_binding,lock_target=self.target(rdoc,rdef,lock_call) if lock_call is not None else ({},None)
        lock_result=self.callback_result(lock_target,2) if lock_target is not None else {"supported":False}
        pushed=[call for call in read_calls if (_path(rdoc,call.child_by_field_name("function")) or [])[-1:]==["push"]
            and self.same(rdoc,aa._argument(call,0),claim)]
        collection=pushed[0].child_by_field_name("function").child_by_field_name("object") if len(pushed)==1 else None
        collection_initial=self.initializer(rdoc,collection)
        collection_returns=[node for node in _returns(rfn) if self.same(rdoc,_expression(node),collection)]
        claims_flow=bool(collection_initial is not None and collection_initial.type=="array" and not aa._children(collection_initial)
            and collection_returns and lock_result["supported"])
        result["reader"]={"supported":bool(moved is not None and decode is not None and reader["supported"] and returned and pushed and claims_flow),
            "payload_rename":self.ref(rdoc,rdef,moved[0]) if moved else None,"source_file":self.ref(rdoc,rdef,moved[3]) if moved else None,"processing_file":self.ref(rdoc,rdef,moved[4]) if moved else None,
            "decode_claimed_path":self.ref(rdoc,rdef,decode),"decoder_binding":dbind,"file_reader":reader,
            "assignment_return":[self.ref(rdoc,rdef,node) for node in returned],"malformed_assignment_returns":malformed,"claim_appends":[self.ref(rdoc,rdef,node) for node in pushed],
            "lock_callback_return_flow":lock_result,"lock_binding":lock_binding,"claim_result_binding":self.ref(rdoc,rdef,claim),
            "fresh_claims_array":self.ref(rdoc,rdef,collection_initial),"returned_same_claims":[self.ref(rdoc,rdef,node) for node in collection_returns],
            "claims_collection_flow_supported":claims_flow}
        # Match actual directory terms: writer inboxDir/workerId/id.json and reader inboxDir/workerId/file, processing/file.
        source_dir=self.initializer(rdoc,aa._argument(moved[3],0)) if moved else None
        processing_dir=self.initializer(rdoc,aa._argument(moved[4],0)) if moved else None
        constructor_assignments=[node for node in aa._walk(c_fn.child_by_field_name("body"),skip_functions=True) if node.type=="assignment_expression"]
        inbox_assignments=[node for node in constructor_assignments if _path(c_doc,node.child_by_field_name("left"))==["this","inboxDir"]]
        same_dir=bool(file_call is not None and source_dir is not None and _path(rdoc,source_dir.child_by_field_name("function"))==["path","join"]
            and _path(rdoc,aa._argument(source_dir,0))==["this","inboxDir"] and self.same(rdoc,aa._argument(source_dir,1),aa._param_node(rfn,0))
            and self.same(doc,aa._argument(file_call,1),aa._param_node(fn,0)) and processing_dir is not None
            and self.same(rdoc,aa._argument(processing_dir,0),aa._argument(moved[3],0)) and aa._literal(rdoc,aa._argument(processing_dir,1))=="processing"
            and len(inbox_assignments)==1 and c_doc is doc is rdoc)
        suffix=bool(file_call is not None and any(child.type=="string_fragment" and doc.text(child)==".json" for child in aa._children(_u(aa._argument(file_call,2)))))
        filenames=[call for call in read_calls if (_path(rdoc,call.child_by_field_name("function")) or [])[-1:]==["endsWith"] and aa._literal(rdoc,aa._argument(call,0))==".json"]
        slices=[call for call in read_calls if (_path(rdoc,call.child_by_field_name("function")) or [])[-1:]==["slice"] and rdoc.text(aa._argument(call,0))=="0" and rdoc.text(aa._argument(call,1))=="-5"]
        result["record_identity"]={"supported":bool(same_dir and suffix and filenames and slices and id_from_payload),
            "constructor_inbox_assignment":self.ref(c_doc,c_def,inbox_assignments[0]) if inbox_assignments else None,
            "same_inbox_receiver_directory":same_dir,"writer_suffix":suffix,"reader_file_filter":[self.ref(rdoc,rdef,node) for node in filenames],"reader_assignment_id_slice":[self.ref(rdoc,rdef,node) for node in slices],
            "identity_fields":["hubRoot","workerId","assignmentId","attempt","attemptToken"],
            "environment_seam":"the compared writer and claimant have the same production logical hubRoot/workerId and claim the selected committed assignment filename; physical aliasing and successful timing are conditional"}
        result["branches"]=[{"kind":"malformed_or_missing_claim","evidence":malformed,"record_correspondence_supported":False},
            {"kind":"writer_attempt_idempotency_conflict","evidence":result["writer"]["guards"],"success_is_not_guaranteed":True}]
        result["supported"]=all(result[key]["supported"] for key in ("writer","reader","record_identity"))
        self.model(_MODEL_CHANNEL,result["supported"],[result["writer"].get("publication_rename"),result["reader"].get("payload_rename")],
            ["Selected normal atomic JSON write and pinned read obey the registered filesystem provider model", "The selected payload/worker/assignment identities correspond; concurrent replacement, compensation, lock or durability failure and malformed claims are separate branches"])
        self.relation("worker_inbox_committed_file_processing_claim",doc,definition,fn,**result)
        if not result["supported"]:self.gap("pipeline_inbox_record_channel_incomplete",doc,definition,fn,states={key:result[key].get("supported") for key in ("writer","reader","record_identity")})
        return result

    def queue(self)->dict:
        mutation=self.role("withQueueMutation");life=self.role("withQueueLock");load=self.role("loadLocalQueue");save=self.role("saveLocalQueue")
        result={"supported":False,"kind":"protected_queue_json_record","callback":{},"codec":{},"path":{},"lifecycle":{}}
        if any(component is None for component in (mutation,life,load,save)):return result
        mdoc,mdef,mfn=mutation;ldoc,ldef,lfn=life;r_doc,rdef,rfn=load;sdoc,sdef,sfn=save
        calls=aa._calls(mdoc,mfn.child_by_field_name("body"),mdef.symbol.replace("withQueueMutation","withQueueLock"))
        call=calls[0] if len(calls)==1 else None
        callback=_u(aa._argument(call,1)) if call is not None else None
        original_callback=aa._param_node(mfn,1)
        callback_calls=[node for node in aa._calls(mdoc,callback.child_by_field_name("body")) if self.same(mdoc,node.child_by_field_name("function"),original_callback)] if callback is not None and callback.type in aa._FUNCTIONS else []
        cb_call=callback_calls[0] if len(callback_calls)==1 else None
        forward=bool(call is not None and self.same(mdoc,aa._argument(call,0),aa._param_node(mfn,0)) and cb_call is not None
            and self.same(mdoc,cb_call.child_by_field_name("function"),original_callback) and self.same(mdoc,aa._argument(cb_call,0),aa._param_node(callback,0)))
        binding,target=self.target(mdoc,mdef,call) if call is not None else ({},None)
        forward=bool(forward and target is not None and target[1].symbol==ldef.symbol and target[0] is ldoc)
        result["callback"]={"supported":forward,"wrapper_call":self.ref(mdoc,mdef,call),"binding":binding,"forwarded_callback_call":self.ref(mdoc,mdef,cb_call)}
        # Register the directory protocol using actual captured binder names; region facts are recomputed.
        life_calls=aa._calls(ldoc,lfn.child_by_field_name("body"),nested=True)
        acquire_candidates=[node for node in life_calls if _path(ldoc,node.child_by_field_name("function"))==["mkdir"] and _u(aa._argument(node,0)) is not None and _u(aa._argument(node,0)).type=="identifier"]
        acquire=acquire_candidates[0] if len(acquire_candidates)==1 else None
        lock_name=ldoc.text(aa._argument(acquire,0)) if acquire is not None else ""
        false_bindings=[node for node in aa._walk(lfn.child_by_field_name("body"),skip_functions=True) if node.type=="variable_declarator" and ldoc.text(_u(node.child_by_field_name("value")))=="false"]
        flags=[]
        for declaration in false_bindings:
            binder=declaration.child_by_field_name("name")
            if any(node.type=="if_statement" and (lambda cond:cond is not None and cond.type=="unary_expression" and aa._op(ldoc,cond)=="!" and self.same(ldoc,cond.child_by_field_name("argument"),binder))(_u(node.child_by_field_name("condition")))
                and any(child.type=="throw_statement" for child in aa._walk(node.child_by_field_name("consequence"),skip_functions=True)) for node in aa._walk(lfn.child_by_field_name("body"),skip_functions=True)):
                flags.append(binder)
        if acquire is not None and len(flags)==1:
            temporary_rule={"protection":{"lifecycle":{"owner":{"file":ldoc.source.path,"symbol":ldef.symbol},"callback_parameter_index":1,"resource_parameter_index":0,
                "acquire":{"callee":ldoc.text(acquire.child_by_field_name("function")),"resource_argument_index":0,"resource_binding":lock_name},
                "fresh_read":{"callee":rdef.symbol,"resource_argument_index":0},"persist":{"callee":sdef.symbol,"resource_argument_index":0},
                "release":{"callee":"releaseQueueLockExact","resource_argument_index":0},"acquired_binding":ldoc.text(flags[0]),
                "process_fence":{"callee":"withQueueProcessFence","implementation":{"file":ldoc.source.path,"symbol":"withQueueProcessFence"},"callback_argument_index":1}}}}
            protocol,protocol_supported=aa._lifecycle(self.context,temporary_rule)
            result["lifecycle"]={"supported":protocol_supported,"source_protocol":protocol,"protocol_descriptor_scope":"registered directory-owner lock callback protocol; binder/guard/region facts were extracted, not supplied by product policy"}
        source_calls=aa._calls(r_doc,rfn.child_by_field_name("body"));save_calls=aa._calls(sdoc,sfn.child_by_field_name("body"))
        read_paths=[node for node in source_calls if _path(r_doc,node.child_by_field_name("function"))==["queuePath"] and self.same(r_doc,aa._argument(node,0),aa._param_node(rfn,0))]
        save_paths=[node for node in save_calls if _path(sdoc,node.child_by_field_name("function"))==["queuePath"] and self.same(sdoc,aa._argument(node,0),aa._param_node(sfn,0))]
        read_path=read_paths[0] if read_paths else None;save_path=save_paths[0] if len(save_paths)==1 else None
        rb,rpt=self.target(r_doc,rdef,read_path) if read_path is not None else ({},None);sb,spt=self.target(sdoc,sdef,save_path) if save_path is not None else ({},None)
        same_path=bool(rpt is not None and spt is not None and rpt[0] is spt[0] and rpt[1] is spt[1])
        result["path"]={"supported":same_path,"read_applications":[self.ref(r_doc,rdef,node) for node in read_paths],"save_application":self.ref(sdoc,sdef,save_path),
            "read_binding":rb,"save_binding":sb,"logical_identity_condition":"same caller logical hubRoot; no physical symlink/mount/deployment identity proof"}
        parses=[node for node in source_calls if _path(r_doc,node.child_by_field_name("function"))==["JSON","parse"]]
        parse=parses[0] if len(parses)==1 else None;raw=aa._argument(parse,0) if parse is not None else None;raw_init=self.initializer(r_doc,raw)
        bounded_from_path=bool(raw_init is not None and raw_init.type=="call_expression" and any(aa._argument(raw_init,0).start_byte==node.start_byte for node in read_paths))
        stringify=[node for node in save_calls if _path(sdoc,node.child_by_field_name("function"))==["JSON","stringify"]]
        encoded=stringify[0] if len(stringify)==1 else None;record=aa._argument(encoded,0) if encoded is not None else None
        fields,closed=_pairs(sdoc,self.initializer(sdoc,record));entries=fields.get("entries")
        entries_forwarded=bool(entries is not None and _path(sdoc,entries)[-1:]==["entries"] and self.same(sdoc,entries.child_by_field_name("object"),aa._param_node(sfn,1))) if _path(sdoc,entries) else False
        saves=[node for node in save_calls if _path(sdoc,node.child_by_field_name("function"))==["writeAtomic"] and save_path is not None and aa._argument(node,0).start_byte==save_path.start_byte]
        write=saves[0] if len(saves)==1 else None;write_body=aa._argument(write,1) if write is not None else None
        code_connected=bool(write_body is not None and encoded is not None and write_body.start_byte<=encoded.start_byte<encoded.end_byte<=write_body.end_byte)
        result["codec"]={"supported":bool(parse is not None and bounded_from_path and encoded is not None and closed and entries_forwarded and code_connected),
            "read_bytes":self.ref(r_doc,rdef,raw_init),"json_decode":self.ref(r_doc,rdef,parse),"save_entries":self.ref(sdoc,sdef,entries),
            "json_encode":self.ref(sdoc,sdef,encoded),"actual_save":self.ref(sdoc,sdef,write),
            "record_scope":"successful normal queue format load/save; root version/entries shape and selected nested scalar fields use the explicit finite JSON model"}
        result["supported"]=forward and result["lifecycle"].get("supported",False) and same_path and result["codec"]["supported"]
        self.relation("actual_locked_queue_callback_json_read_save",mdoc,mdef,mfn,**result)
        if not result["supported"]:self.gap("pipeline_queue_record_channel_incomplete",mdoc,mdef,mfn,states={key:result[key].get("supported") for key in ("callback","lifecycle","path","codec")})
        return result

    def broker(self)->dict:
        client=self.role("WorkerBrokerClient.claimInboxEntries");call_role=self.role("WorkerBrokerClient.#call");server=self.role("handleWorkerStateBroker");constructor=self.role("WorkerBrokerClient.constructor")
        http=self.role("startHubServer");serializer=self.role("sendJson");result_validator=self.role("brokerResult");claims_validator=self.role("inboxClaimsResult")
        result={"supported":False,"kind":"authenticated_worker_broker_json","operation":{},"request":{},"dispatch":{},"response":{},"credentials":{}}
        if any(component is None for component in (client,call_role,server,http,serializer,result_validator,claims_validator,constructor)):return result
        doc,definition,fn=client;cdoc,cdef,cfn=call_role;sdoc,sdef,sfn=server;hdoc,hdef,hfn=http;jdoc,jdef,jfn=serializer
        calls=aa._calls(doc,fn.child_by_field_name("body"),nested=True)
        request_calls=[node for node in calls if (_path(doc,node.child_by_field_name("function")) or [])[-1:]==["#call"]]
        request_call=request_calls[0] if len(request_calls)==1 else None;operation=aa._literal(doc,aa._argument(request_call,0)) if request_call is not None else None
        validators=[node for node in calls if _path(doc,node.child_by_field_name("function"))==["inboxClaimsResult"] and aa._literal(doc,aa._argument(node,1))==operation]
        # The receiver is an expression (this.#call(...)), so a complete
        # identifier-root member path cannot represent this .then call.
        # Authenticate its actual static member and exact request operand.
        then_calls=[]
        for node in calls:
            callee=_u(node.child_by_field_name("function"))
            if callee is None or callee.type!="member_expression":continue
            property_node=callee.child_by_field_name("property");receiver=_u(callee.child_by_field_name("object"))
            if property_node is not None and doc.text(property_node)=="then" and request_call is not None and receiver is not None and receiver.id==request_call.id:then_calls.append(node)
        callback=_u(aa._argument(then_calls[0],0)) if len(then_calls)==1 else None
        then_returns=[node for node in _returns(fn) if len(then_calls)==1 and _expression(node) is not None and _expression(node).id==then_calls[0].id]
        callback_body=_u(callback.child_by_field_name("body")) if callback is not None else None
        direct_validation=bool(len(validators)==1 and callback_body is not None and callback_body.id==validators[0].id)
        result["operation"]={"supported":bool(isinstance(operation,str) and request_call is not None and len(validators)==1 and callback is not None and then_returns and direct_validation
            and self.same(doc,aa._argument(validators[0],0),aa._param_node(callback,0))),"literal":operation,
            "actual_request":self.ref(doc,definition,request_call),"then_callback":self.ref(doc,definition,callback),"actual_then_call":self.ref(doc,definition,then_calls[0]) if then_calls else None,
            "returned_request_then":[self.ref(doc,definition,node) for node in then_returns],"callback_returns_actual_validator":direct_validation,
            "result_validation":self.ref(doc,definition,validators[0]) if validators else None}
        ccalls=aa._calls(cdoc,cfn.child_by_field_name("body"),nested=True)
        json=[node for node in ccalls if _path(cdoc,node.child_by_field_name("function"))==["JSON","stringify"]]
        encoded=json[0] if len(json)==1 else None;fields,closed=_pairs(cdoc,aa._argument(encoded,0)) if encoded is not None else ({},False)
        fetches=[node for node in ccalls if _path(cdoc,node.child_by_field_name("function"))==["this","#fetch"]]
        fetch=fetches[0] if len(fetches)==1 else None;opts,opt_closed=_pairs(cdoc,aa._argument(fetch,1)) if fetch is not None else ({},False)
        actual_body=_u(opts.get("body"));actual_op=fields.get("op")
        req_supported=bool(closed and opt_closed and set(fields)=={"workerId","incarnationToken","op","args"}
            and actual_body is not None and encoded is not None and actual_body.id==encoded.id and aa._literal(cdoc,opts.get("method"))=="POST"
            and self.same(cdoc,actual_op,aa._param_node(cfn,0)) and self.same(cdoc,fields.get("args"),aa._param_node(cfn,1)))
        headers,_=_pairs(cdoc,opts.get("headers"))
        req_supported=req_supported and _path(cdoc,fields.get("workerId"))==["this","#workerId"] and _path(cdoc,fields.get("incarnationToken"))==["this","#incarnationToken"]
        result["request"]={"supported":req_supported,"json_encode":self.ref(cdoc,cdef,encoded),"fetch":self.ref(cdoc,cdef,fetch),"request_fields":sorted(fields),
            "credential_fields":{key:self.ref(cdoc,cdef,fields.get(key)) for key in ("workerId","incarnationToken")},"authorization":self.ref(cdoc,cdef,headers.get("authorization")),
            "provider_scope":"constructor default fetch posts captured JSON; an injected options.fetch is an explicit alternate provider"}
        # Authenticated server switch maps the actual body.op binding to a source-created WorkerStore receiver.
        switches=[node for node in aa._walk(sfn.child_by_field_name("body"),skip_functions=True) if node.type=="switch_statement"]
        case=None;dispatched=None
        for switch in switches:
            for child in aa._walk(switch):
                if child.type=="switch_case" and aa._literal(sdoc,child.child_by_field_name("value"))==operation:
                    case=child
                    cs=[node for node in aa._calls(sdoc,child) if (_path(sdoc,node.child_by_field_name("function")) or [])[-1:]==["claimInboxEntries"]]
                    dispatched=cs[0] if len(cs)==1 else None
        receiver=dispatched.child_by_field_name("function").child_by_field_name("object") if dispatched is not None else None
        receiver_init=self.initializer(sdoc,receiver)
        nominal=self.analysis.nominal_call_binding(sdoc,sdef,dispatched) if dispatched is not None else {"supported":False}
        switch_node=next((node for node in aa._ancestors(case) if node.type=="switch_statement"),None) if case is not None else None
        op_binding=_u(switch_node.child_by_field_name("value")) if switch_node is not None else None
        if op_binding is None and switch_node is not None:op_binding=_u(switch_node.child_by_field_name("condition"))
        op_initial=self.initializer(sdoc,op_binding)
        op_sources=[node for node in aa._walk(op_initial) if (_path(sdoc,node) or [])[1:]==["op"]] if op_initial is not None else []
        worker_arg=aa._argument(dispatched,0) if dispatched is not None else None;incarnation_arg=aa._argument(dispatched,1) if dispatched is not None else None
        worker_initial=self.initializer(sdoc,worker_arg);incarnation_initial=self.initializer(sdoc,incarnation_arg)
        id_sources=[node for node in aa._walk(worker_initial) if (_path(sdoc,node) or [])[1:]==["workerId"]] if worker_initial is not None else []
        incarnation_sources=[node for node in aa._walk(incarnation_initial) if (_path(sdoc,node) or [])[1:]==["incarnationToken"]] if incarnation_initial is not None else []
        early_guards=[node for node in aa._walk(sfn.child_by_field_name("body"),skip_functions=True) if node.type=="if_statement" and case is not None and node.end_byte<case.start_byte
            and any(child.type=="throw_statement" for child in aa._walk(node.child_by_field_name("consequence"),skip_functions=True))]
        token_guards=[node for node in early_guards if any(((_path(sdoc,child) or [])[-1:]==["incarnationToken"] or child.type=="call_expression" and _path(sdoc,child.child_by_field_name("function"))==["timingSafeEqual"]) for child in aa._walk(node.child_by_field_name("condition")))]
        result["dispatch"]={"supported":bool(case is not None and dispatched is not None and nominal.get("supported") and op_sources and id_sources and incarnation_sources and token_guards
            and receiver_init is not None and receiver_init.type=="new_expression"),"case":self.ref(sdoc,sdef,case),"call":self.ref(sdoc,sdef,dispatched),"receiver":self.ref(sdoc,sdef,receiver_init),
            "actual_receiver_binding":nominal,"op_binding":self.ref(sdoc,sdef,op_initial),"worker_binding":self.ref(sdoc,sdef,worker_initial),"incarnation_binding":self.ref(sdoc,sdef,incarnation_initial),
            "credential_rejection_guards":[self.ref(sdoc,sdef,node) for node in token_guards],"actual_execution_verified":False}
        # HTTP success envelope carries precisely the handler result, and sendJson serializes its payload argument.
        hcalls=aa._calls(hdoc,hfn.child_by_field_name("body"),nested=True)
        handles=[node for node in hcalls if _path(hdoc,node.child_by_field_name("function"))==["handleWorkerStateBroker"]]
        handle=handles[0] if len(handles)==1 else None;handle_decl=aa._bound_call(handle) if handle is not None else None;handler_result=handle_decl.child_by_field_name("name") if handle_decl is not None else None
        handler_fields,handler_closed=_pairs(hdoc,aa._argument(handle,0)) if handle is not None else ({},False)
        body_reader=self.initializer(hdoc,handler_fields.get("body"));breader_binding,breader_target=self.target(hdoc,hdef,body_reader) if body_reader is not None and body_reader.type=="call_expression" else ({},None)
        body_decode=None
        if breader_target is not None:
            bdoc,bdef,bfn=breader_target;parses=[node for node in aa._calls(bdoc,bfn.child_by_field_name("body"),nested=True) if _path(bdoc,node.child_by_field_name("function"))==["JSON","parse"]]
            body_decode=self.ref(bdoc,bdef,parses[0]) if len(parses)==1 else None
        envelopes=[]
        for node in aa._walk(hfn.child_by_field_name("body"),skip_functions=False):
            if node.type!="assignment_expression":continue
            outer,closed=_pairs(hdoc,node.child_by_field_name("right"));payload,pclosed=_pairs(hdoc,outer.get("payload"))
            carried=_u(payload.get("result"));carried=_u(carried.child_by_field_name("left")) if carried is not None and carried.type=="binary_expression" and aa._op(hdoc,carried)=="??" else carried
            if closed and pclosed and aa._literal(hdoc,payload.get("ok")) is True and self.same(hdoc,carried,handler_result):envelopes.append((node,outer,payload))
        send_calls=[node for node in hcalls if _path(hdoc,node.child_by_field_name("function"))==["sendJson"]]
        send=send_calls[0] if len(send_calls)==1 else None;sent=aa._argument(send,2) if send is not None else None
        send_to_envelope=bool(sent is not None and (_path(hdoc,sent) or [])[-1:]==["payload"] and envelopes
            and self.same(hdoc,sent.child_by_field_name("object"),envelopes[0][0].child_by_field_name("left")))
        jcalls=aa._calls(jdoc,jfn.child_by_field_name("body"));serialized=[node for node in jcalls if _path(jdoc,node.child_by_field_name("function"))==["JSON","stringify"] and self.same(jdoc,aa._argument(node,0),aa._param_node(jfn,2))]
        vcalls=aa._calls(cdoc,cfn.child_by_field_name("body"));json_responses=[node for node in vcalls if (_path(cdoc,node.child_by_field_name("function")) or [])[-1:]==["json"]]
        extracting=[node for node in vcalls if _path(cdoc,node.child_by_field_name("function"))==["brokerResult"]]
        fetch_decl=aa._bound_call(fetch) if fetch is not None else None
        response=fetch_decl.child_by_field_name("name") if fetch_decl is not None else None
        decoded=json_responses[0] if len(json_responses)==1 else None
        decoded_decl=aa._bound_call(decoded) if decoded is not None else None
        decoded_binder=decoded_decl.child_by_field_name("name") if decoded_decl is not None else None
        extraction=extracting[0] if len(extracting)==1 else None
        payload_arg=aa._argument(extraction,0) if extraction is not None else None
        payload_choice=self.initializer(cdoc,payload_arg)
        payload_check=_u(payload_choice.child_by_field_name("condition")) if payload_choice is not None and payload_choice.type=="ternary_expression" else None
        payload_preserved=bool(payload_check is not None and payload_check.type=="call_expression" and _path(cdoc,payload_check.child_by_field_name("function"))==["isRecord"]
            and self.same(cdoc,aa._argument(payload_check,0),decoded_binder)
            and self.same(cdoc,payload_choice.child_by_field_name("consequence"),decoded_binder)
            and _u(payload_choice.child_by_field_name("alternative")).type=="object" and not aa._children(_u(payload_choice.child_by_field_name("alternative"))))
        extracting_returns=[node for node in _returns(cfn) if extraction is not None and _expression(node) is not None and _expression(node).id==extraction.id]
        client_response_flow=bool(decoded is not None and self.same(cdoc,decoded.child_by_field_name("function").child_by_field_name("object"),response)
            and payload_preserved and extraction is not None and self.same(cdoc,aa._argument(extraction,1),aa._param_node(cfn,0)) and extracting_returns)
        vdoc,vdef,vfn=result_validator;v_returns=_returns(vfn);v_expression=_expression(v_returns[-1]) if v_returns else None
        extracts_result=bool(v_expression is not None and (_path(vdoc,v_expression) or [])[1:]==["result"] and self.same(vdoc,v_expression.child_by_field_name("object"),aa._param_node(vfn,0)))
        v_guards=[node for node in aa._walk(vfn.child_by_field_name("body"),skip_functions=True) if node.type=="if_statement" and any(child.type=="throw_statement" for child in aa._walk(node.child_by_field_name("consequence"),skip_functions=True))]
        success_guard=False;presence_guard=False
        for guard in v_guards:
            condition=_u(guard.child_by_field_name("condition"))
            if condition is not None and condition.type=="binary_expression" and aa._op(vdoc,condition)=="!==":
                left,right=condition.child_by_field_name("left"),condition.child_by_field_name("right")
                success_guard=success_guard or bool((_path(vdoc,left) or [])[1:]==["ok"] and self.same(vdoc,left.child_by_field_name("object"),aa._param_node(vfn,0)) and aa._literal(vdoc,right) is True)
            if condition is not None and condition.type=="unary_expression" and aa._op(vdoc,condition)=="!":
                check=_u(condition.child_by_field_name("argument"))
                presence_guard=presence_guard or bool(check is not None and check.type=="call_expression" and _path(vdoc,check.child_by_field_name("function"))==["Object","hasOwn"]
                    and self.same(vdoc,aa._argument(check,0),aa._param_node(vfn,0)) and aa._literal(vdoc,aa._argument(check,1))=="result")
        result["response"]={"supported":bool(handler_closed and body_decode and envelopes and send_to_envelope and serialized and client_response_flow and extracts_result and success_guard and presence_guard),
            "handler_call":self.ref(hdoc,hdef,handle),"handler_fields":sorted(handler_fields),"body_reader_binding":breader_binding,"request_json_decode":body_decode,
            "success_envelope":[self.ref(hdoc,hdef,node) for node,_,_ in envelopes],"send_payload":self.ref(hdoc,hdef,sent),"send_json_encode":[self.ref(jdoc,jdef,node) for node in serialized],
            "client_response_json":[self.ref(cdoc,cdef,node) for node in json_responses],"broker_result_projection":self.ref(vdoc,vdef,v_expression),"success_envelope_guards":[self.ref(vdoc,vdef,node) for node in v_guards],
            "client_payload_choice":self.ref(cdoc,cdef,payload_choice),"client_actual_result_extraction":self.ref(cdoc,cdef,extraction),
            "client_returned_extraction":[self.ref(cdoc,cdef,node) for node in extracting_returns],"client_response_operand_flow_supported":client_response_flow,
            "ok_true_required":success_guard,"result_own_presence_required":presence_guard,
            "decode_fallback_scope":"response.json rejection and non-record payload select an empty error envelope; only the actual successful ordinary-record branch carries server result"}
        tdoc,tdef,tfn=claims_validator;maps=[node for node in aa._calls(tdoc,tfn.child_by_field_name("body")) if (_path(tdoc,node.child_by_field_name("function")) or [])[-1:]==["map"]]
        mapper=_u(aa._argument(maps[0],0)) if len(maps)==1 else None;mapper_returns=_returns(mapper) if mapper is not None else []
        claim_expr=_expression(mapper_returns[-1]) if mapper_returns else None;claim_init=self.initializer(tdoc,claim_expr)
        candidate_arg=aa._argument(claim_init,0) if claim_init is not None and claim_init.type=="call_expression" else None
        claim_preserved=bool(mapper is not None and claim_init is not None and _path(tdoc,claim_init.child_by_field_name("function"))==["recordResult"]
            and self.same(tdoc,candidate_arg,aa._param_node(mapper,0)))
        map_call=maps[0] if len(maps)==1 else None
        map_returns=[node for node in _returns(tfn) if map_call is not None and _expression(node) is not None and _expression(node).id==map_call.id]
        map_source=map_call.child_by_field_name("function").child_by_field_name("object") if map_call is not None else None
        record_binding,record_target=self.target(tdoc,tdef,claim_init) if claim_init is not None and claim_init.type=="call_expression" else ({},None)
        record_preserved=False;record_returns=[]
        if record_target is not None:
            rdoc,rdef,rfn=record_target
            record_returns=[self.ref(rdoc,rdef,node) for node in _returns(rfn) if self.same(rdoc,_expression(node),aa._param_node(rfn,0))]
            record_preserved=bool(record_returns)
        map_flow=bool(map_call is not None and self.same(tdoc,map_source,aa._param_node(tfn,0)) and map_returns and record_preserved)
        result["claims_validation"]={"supported":claim_preserved and map_flow,"map":self.ref(tdoc,tdef,map_call),"record_result":self.ref(tdoc,tdef,claim_init),
            "returns_actual_map":[self.ref(tdoc,tdef,node) for node in map_returns],"map_source_is_result_formal":map_flow,
            "record_result_binding":record_binding,"record_result_same_operand_return":record_returns,
            "returns_same_claim_record":self.ref(tdoc,tdef,claim_expr),"guards":[self.ref(tdoc,tdef,node) for node in aa._walk(tfn.child_by_field_name("body"),skip_functions=False) if node.type=="if_statement"]}
        qdoc,qdef,qfn=constructor;assignments=[node for node in aa._walk(qfn.child_by_field_name("body"),skip_functions=True) if node.type=="assignment_expression"]
        fields_from_credentials=[]
        for property_name in ("workerId","incarnationToken","token"):
            values=[node for node in assignments if _path(qdoc,node.child_by_field_name("left"))==["this","#"+property_name]]
            mapped=bool(len(values)==1 and (_path(qdoc,values[0].child_by_field_name("right")) or [])[1:]==[property_name]
                and self.same(qdoc,values[0].child_by_field_name("right").child_by_field_name("object"),aa._param_node(qfn,0)))
            fields_from_credentials.append({"field":property_name,"supported":mapped,"assignment":self.ref(qdoc,qdef,values[0]) if values else None})
        fetch_fields=[node for node in assignments if _path(qdoc,node.child_by_field_name("left"))==["this","#fetch"]]
        fetch_choice=_u(fetch_fields[0].child_by_field_name("right")) if len(fetch_fields)==1 else None
        default_fetch=bool(fetch_choice is not None and fetch_choice.type=="binary_expression" and aa._op(qdoc,fetch_choice)=="??"
            and _path(qdoc,fetch_choice.child_by_field_name("right"))==["globalThis","fetch"]
            and (_path(qdoc,fetch_choice.child_by_field_name("left")) or [])[1:]==["fetch"]
            and self.same(qdoc,fetch_choice.child_by_field_name("left").child_by_field_name("object"),aa._param_node(qfn,1)))
        pathname=[node for node in assignments if (_path(qdoc,node.child_by_field_name("left")) or [])[-1:]==["pathname"] and isinstance(aa._literal(qdoc,node.child_by_field_name("right")),str)]
        route_literal=aa._literal(qdoc,pathname[0].child_by_field_name("right")) if len(pathname)==1 else None
        route_guards=[]
        for parent in aa._ancestors(handle):
            if parent.type!="if_statement":continue
            condition=parent.child_by_field_name("condition")
            literals=[aa._literal(hdoc,node) for node in aa._walk(condition) if node.type=="string"]
            if route_literal in literals and "POST" in literals:route_guards.append(self.ref(hdoc,hdef,condition))
        authorization=headers.get("authorization");bearer=bool(authorization is not None and authorization.type=="template_string"
            and any(node.type=="string_fragment" and cdoc.text(node)=="Bearer " for node in aa._children(authorization))
            and any(_path(cdoc,node)==["this","#token"] for node in aa._walk(authorization)))
        result["credentials"]={"supported":all(item["supported"] for item in fields_from_credentials) and default_fetch and bool(route_guards) and bearer,
            "constructor_field_sources":fields_from_credentials,"default_fetch_and_override":self.ref(qdoc,qdef,fetch_choice),"default_fetch_source_supported":default_fetch,
            "client_endpoint_path":self.ref(qdoc,qdef,pathname[0]) if pathname else None,"server_matching_post_route":route_guards,"authorization_source":self.ref(cdoc,cdef,authorization),
            "runtime_credentials_or_endpoint_availability_proven":False}
        result["supported"]=all(result[key].get("supported") for key in ("operation","request","dispatch","response","claims_validation","credentials"))
        broker_model=_MODEL_BROKER if _MODEL_BROKER in self.rule.get("models",[]) else _MODEL_CHANNEL
        self.model(broker_model,result["supported"],[result["operation"]["actual_request"],result["dispatch"]["call"],result["response"]["handler_call"]],
            ["The selected production fetch/HTTP/JSON provider reaches the captured Hub internal worker-state endpoint and receives its normal success response",
             "WorkerId/incarnation/token credentials pass the actual pre-dispatch checks; HTTP failure, invalid envelope/result and fetch overrides are separate outcomes",
             "JSON preserves selected finite ordinary record fields; operation names are protocol relations, not forged CALLS"])
        self.relation("actual_authenticated_broker_claim_request_response",doc,definition,fn,**result)
        if not result["supported"]:self.gap("pipeline_broker_claim_channel_incomplete",doc,definition,fn,states={key:result[key].get("supported") for key in ("operation","request","dispatch","response","claims_validation","credentials")})
        return result

    def plain_reader(self,component:tuple)->dict:
        doc,definition,fn=component;calls=aa._calls(doc,fn.child_by_field_name("body"),nested=True)
        parses=[node for node in calls if _path(doc,node.child_by_field_name("function"))==["JSON","parse"]]
        parse=parses[0] if len(parses)==1 else None;raw=aa._argument(parse,0) if parse is not None else None
        raw_init=self.initializer(doc,raw)
        if raw_init is None:
            mutations=[node for node in aa._walk(fn.child_by_field_name("body"),skip_functions=True) if node.type=="assignment_expression" and self.same(doc,node.child_by_field_name("left"),raw)]
            raw_init=_u(mutations[0].child_by_field_name("right")) if len(mutations)==1 else None
        parse_decl=aa._bound_call(parse) if parse is not None else None;parsed=parse_decl.child_by_field_name("name") if parse_decl is not None else None
        returns=[node for node in _returns(fn) if self.same(doc,_expression(node),parsed)]
        supported=bool(raw_init is not None and raw_init.type=="call_expression" and self.same(doc,aa._argument(raw_init,0),aa._param_node(fn,0)) and returns)
        return {"supported":supported,"actual_read":self.ref(doc,definition,raw_init),"json_decode":self.ref(doc,definition,parse),"returns_decoded_object":[self.ref(doc,definition,node) for node in returns]}

    def counter(self)->dict:
        create=self.role("AssignmentStore.createAttempt");read=self.role("AssignmentStore._readStateFile");save=self.role("AssignmentStore._writeState")
        listing=self.role("AssignmentStore.listAssignments");reconcile=self.role("Reconciler.reconcileAssignments");finalize=self.role("Reconciler._finalizeQueue")
        result={"supported":False,"kind":"persisted_assignment_attempt_counter","writer":{},"reader":{},"consumer":{},"branches":[]}
        if any(component is None for component in (create,read,save,listing,reconcile,finalize)):return result
        doc,definition,fn=create;rdoc,rdef,rfn=read;sdoc,sdef,sfn=save;ldoc,ldef,lfn=listing;cdoc,cdef,cfn=reconcile;fdoc,fdef,ffn=finalize
        calls=aa._calls(doc,fn.child_by_field_name("body"),nested=True)
        reads=[node for node in calls if _path(doc,node.child_by_field_name("function"))==["this","_readStateFile"] and self.same(doc,aa._argument(node,0),aa._param_node(fn,0))]
        state_call=reads[0] if len(reads)==1 else None;state_decl=aa._bound_call(state_call) if state_call is not None else None;state=state_decl.child_by_field_name("name") if state_decl is not None else None
        mutations=[node for node in aa._walk(fn.child_by_field_name("body")) if node.type=="assignment_expression" and (_path(doc,node.child_by_field_name("left")) or [])[1:]==["attempts"]
            and self.same(doc,node.child_by_field_name("left").child_by_field_name("object"),state)]
        change=mutations[0] if len(mutations)==1 else None;counter=change.child_by_field_name("right") if change is not None else None;increment=self.initializer(doc,counter)
        prior=increment.child_by_field_name("left") if increment is not None and increment.type=="binary_expression" and aa._op(doc,increment)=="+" else None
        prior_initializer=self.initializer(doc,prior);prior_source=_u(prior_initializer.child_by_field_name("consequence")) if prior_initializer is not None and prior_initializer.type=="ternary_expression" else None
        increment_connected=bool(increment is not None and increment.type=="binary_expression" and aa._op(doc,increment)=="+" and doc.text(increment.child_by_field_name("right"))=="1"
            and prior_source is not None and (_path(doc,prior_source) or [])[1:]==["attempts"] and self.same(doc,prior_source.child_by_field_name("object"),state))
        persists=[node for node in calls if _path(doc,node.child_by_field_name("function"))==["this","_writeState"]
            and self.same(doc,aa._argument(node,0),aa._param_node(fn,0)) and self.same(doc,aa._argument(node,1),state)]
        persist=persists[0] if len(persists)==1 else None
        result["writer"]={"supported":bool(state_call is not None and change is not None and increment_connected and persist is not None and change.end_byte<persist.start_byte),
            "read_state":self.ref(doc,definition,state_call),"previous_attempts":self.ref(doc,definition,prior_initializer),"increment":self.ref(doc,definition,increment),
            "write_counter":self.ref(doc,definition,change),"persist_same_state_id":self.ref(doc,definition,persist),"runtime_count_verified":False}
        r_calls=aa._calls(rdoc,rfn.child_by_field_name("body"));s_calls=aa._calls(sdoc,sfn.child_by_field_name("body"))
        r_paths=[node for node in r_calls if _path(rdoc,node.child_by_field_name("function"))==["path","join"] and _path(rdoc,aa._argument(node,0))==["this","baseDir"]
            and self.same(rdoc,aa._argument(node,1),aa._param_node(rfn,0)) and aa._literal(rdoc,aa._argument(node,2))=="state.json"]
        s_paths=[node for node in s_calls if _path(sdoc,node.child_by_field_name("function"))==["path","join"] and _path(sdoc,aa._argument(node,0))==["this","baseDir"]
            and self.same(sdoc,aa._argument(node,1),aa._param_node(sfn,0)) and aa._literal(sdoc,aa._argument(node,2))=="state.json"]
        local_reads=[node for node in r_calls if _path(rdoc,node.child_by_field_name("function"))==["this","_readLocalJsonObject"]]
        r_binding,r_target=self.target(rdoc,rdef,local_reads[0]) if len(local_reads)==1 else ({},None);decoder=self.plain_reader(r_target) if r_target is not None else {"supported":False}
        local_saves=[node for node in s_calls if _path(sdoc,node.child_by_field_name("function"))==["writeJsonAtomic"] and self.same(sdoc,aa._argument(node,1),aa._param_node(sfn,1))]
        w_binding,w_target=self.target(sdoc,sdef,local_saves[0]) if len(local_saves)==1 else ({},None);writer=self.data_file_writer(w_target) if w_target is not None else {"supported":False}
        result["reader"]={"supported":bool(len(r_paths)==len(s_paths)==1 and decoder["supported"] and writer["supported"]),
            "read_path":self.ref(rdoc,rdef,r_paths[0]) if r_paths else None,"write_path":self.ref(sdoc,sdef,s_paths[0]) if s_paths else None,
            "actual_decoder_binding":r_binding,"decoder":decoder,"actual_writer_binding":w_binding,"writer":writer,
            "resource_scope":"same source-created AssignmentStore baseDir, actual assignmentId parameter and state.json suffix"}
        listed_reads=[node for node in aa._calls(ldoc,lfn.child_by_field_name("body"),nested=True) if _path(ldoc,node.child_by_field_name("function"))==["this","_readState"]]
        listed=listed_reads[0] if len(listed_reads)==1 else None;listed_decl=aa._bound_call(listed) if listed is not None else None;listed_state=listed_decl.child_by_field_name("name") if listed_decl is not None else None
        appends=[node for node in aa._calls(ldoc,lfn.child_by_field_name("body"),nested=True) if (_path(ldoc,node.child_by_field_name("function")) or [])[-1:]==["push"] and self.same(ldoc,aa._argument(node,0),listed_state)]
        list_array=appends[0].child_by_field_name("function").child_by_field_name("object") if len(appends)==1 else None
        list_initial=self.initializer(ldoc,list_array)
        list_returns=[node for node in _returns(lfn) if self.same(ldoc,_expression(node),list_array)]
        list_output=bool(list_initial is not None and list_initial.type=="array" and not aa._children(list_initial) and list_returns)
        reader_binding,read_state=self.target(ldoc,ldef,listed) if listed is not None else ({},None)
        state_forward=False;state_forward_call=None
        if read_state is not None:
            d,ddef,dfn=read_state
            forwarded=[node for node in aa._calls(d,dfn.child_by_field_name("body")) if _path(d,node.child_by_field_name("function"))==["this","_readStateFile"] and self.same(d,aa._argument(node,0),aa._param_node(dfn,0))]
            state_returns=[node for node in _returns(dfn) if len(forwarded)==1 and _expression(node) is not None and _expression(node).id==forwarded[0].id]
            state_forward=bool(len(forwarded)==1 and state_returns);state_forward_call=self.ref(d,ddef,forwarded[0]) if forwarded else None
        reconcile_calls=aa._calls(cdoc,cfn.child_by_field_name("body"),nested=True)
        collections=[node for node in reconcile_calls if (_path(cdoc,node.child_by_field_name("function")) or [])[-1:]==["listAssignments"]]
        collection=collections[0] if len(collections)==1 else None;col_decl=aa._bound_call(collection) if collection is not None else None;col=col_decl.child_by_field_name("name") if col_decl is not None else None
        loops=[node for node in aa._walk(cfn.child_by_field_name("body"),skip_functions=True) if node.type=="for_in_statement" and aa._op(cdoc,node)=="of" and self.same(cdoc,node.child_by_field_name("right"),col)]
        loop=loops[0] if len(loops)==1 else None;item=loop.child_by_field_name("left") if loop is not None else None
        if item is not None and item.type in {"lexical_declaration","variable_declaration"}:
            children=[node for node in aa._children(item) if node.type=="variable_declarator"];item=children[0].child_by_field_name("name") if len(children)==1 else None
        forwards=[node for node in reconcile_calls if (_path(cdoc,node.child_by_field_name("function")) or [])[-1:] in [["_finalizeAssignment"],["_compensateFinalization"]] and self.same(cdoc,aa._argument(node,0),item)]
        forwarding=[]
        for forwarded in forwards:
            f_binding,target=self.target(cdoc,cdef,forwarded)
            if target is None:continue
            tdoc,tdef,tfn=target
            queue_calls=[node for node in aa._calls(tdoc,tfn.child_by_field_name("body"),nested=True) if (_path(tdoc,node.child_by_field_name("function")) or [])[-1:]==["_finalizeQueue"] and self.same(tdoc,aa._argument(node,0),aa._param_node(tfn,0))]
            if queue_calls:forwarding.append({"caller":self.ref(cdoc,cdef,forwarded),"binding":f_binding,"queue_calls":[self.ref(tdoc,tdef,node) for node in queue_calls]})
        routes=[node for node in aa._calls(fdoc,ffn.child_by_field_name("body"),nested=True) if _path(fdoc,node.child_by_field_name("function"))==["this","failureRouter","route"]]
        routed=[]
        for route in routes:
            fields,closed=_pairs(fdoc,aa._argument(route,0))
            if closed and self.same(fdoc,fields.get("assignment"),aa._param_node(ffn,0)):routed.append(route)
        result["consumer"]={"supported":bool(listed is not None and appends and list_output and state_forward and collection is not None and loop is not None and forwarding and routed),
            "list_state_read":self.ref(ldoc,ldef,listed),"state_read_binding":reader_binding,"read_state_file_forward":state_forward_call,
            "append_read_state":[self.ref(ldoc,ldef,node) for node in appends],"fresh_list_array":self.ref(ldoc,ldef,list_initial),
            "returned_same_state_list":[self.ref(ldoc,ldef,node) for node in list_returns],"list_output_supported":list_output,
            "reconcile_actual_list":self.ref(cdoc,cdef,collection),"assignment_loop":self.ref(cdoc,cdef,loop),
            "finalization_forwarding":forwarding,"failure_route_same_assignment":[self.ref(fdoc,fdef,node) for node in routed],
            "record_scope":"matching persisted assignment state, filtered list and actual loop item; no request maxRetries/queue/phase budgets are merged"}
        result["supported"]=all(result[key]["supported"] for key in ("writer","reader","consumer"))
        self.relation("actual_persisted_assignment_attempts_to_failure_route",doc,definition,fn,**result)
        if not result["supported"]:self.gap("pipeline_attempt_counter_channel_incomplete",doc,definition,fn,states={key:result[key].get("supported") for key in ("writer","reader","consumer")})
        return result


def analyze_pipeline_channels(analysis:Any)->dict:
    adapter=_Channels(analysis)
    queue=adapter.queue();inbox=adapter.inbox();broker=adapter.broker();counter=adapter.counter()
    enabled=set(analysis.rule.get("models",[]))
    required={_MODEL_RECORD,_MODEL_JSON,_MODEL_ASYNC,_MODEL_CHANNEL}
    if not required<=enabled:adapter.gap("pipeline_channel_models_not_registered",required_models=sorted(required-enabled))
    supported=bool(queue["supported"] and inbox["supported"] and broker["supported"] and counter["supported"] and not adapter.gaps)
    return {"version":VERSION,"snapshot_id":analysis.snapshot.id,"source_hash":analysis.snapshot.source_hash,"policy_hash":analysis.snapshot.policy_hash,
        "supported":supported,"gaps":adapter.gaps,"channels":[queue,inbox],"queue":queue,"inbox":inbox,"broker":broker,"counter_transport":counter,
        "source_relations":adapter.relations,"models":adapter.models,"source_only":True,"target_code_executed":False,"target_tests_run":False,
        "runtime_transport_verified":False,"creates_calls_edges":False,"operations_reviewed":adapter.steps,
        "conditions":["Actual selected default providers, corresponding logical roots/record keys and successful normal commits/reads/responses are required",
            "Existing/current/new records, compensation, malformed claims, codec failures, credential rejection and provider overrides are distinct source outcomes",
            "Finite ordinary JSON fields are preserved only inside their registered scalar/record codec domain"]}
