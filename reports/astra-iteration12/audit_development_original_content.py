"""Reconcile original finite report content with saved development prose.

Only saved artifact content is read; this is not a new target-code review,
analysis run, detector policy, semantic coverage score, or formal acceptance.
"""
from pathlib import Path
import hashlib
import json

HERE=Path(__file__).resolve().parent
EXISTING=HERE/'REPORT_COMPLETION_LAST_DEVELOPMENT_SEMANTIC_AUDIT.json'
if EXISTING.exists() and json.loads(EXISTING.read_text()).get('current_followup_state'):
    raise SystemExit('Refusing to replace actual later-scope resolutions with the initial development audit.')
contract=json.loads((HERE/'REPORT_COMPLETION_CONTRACT.json').read_text())
index=json.loads((HERE/'RESPONSIBILITY_ACTUAL_BODY_DEVELOPMENT_INDEX.json').read_text())

def artifact(name):
    p=HERE/name;b=p.read_bytes()
    return {'file':str(p),'sha256':hashlib.sha256(b).hexdigest()}

def actual(repo,symbol,terms=(),file=None,limit=2):
    result=[]
    for d in index['actual_declarations']:
        if d['repository']!=repo or d['actual_owner_symbol']!=symbol or (file and d['actual_owner_file']!=file):continue
        for statement in d['actual_statement_bodies']:
            if terms and not any(t.lower() in statement['text'].lower() for t in terms):continue
            result.append({'file':d['actual_owner_file'],'actual_owner':symbol,**statement})
            if len(result)>=limit:return result
    return result

# Declaration names locate existing prose only. Actual statement text/operation
# pointers, not these locators or the reference-report labels, supply evidence.
E={
'dynamic':actual('codepatchbay','main',('COMMANDS[cmd]',),file='cli/cpb.ts'),
'root':actual('codepatchbay','resolveExecutorRoot',('CPB_EXECUTOR_ROOT',)),
'fix':actual('codepatchbay','run',('readiness','enqueue','entry'),file='cli/commands/fix.ts',limit=3),
'queue':actual('codepatchbay','HubOrchestrator.tick',('assignment','inbox','worker'),limit=3),
'worker':actual('codepatchbay','main.processInbox',('assignment','bridge','runJobWithServices'),limit=3),
'ports':actual('codepatchbay','buildServices',('createJob','appendEvent','broker'),limit=3),
'engine':actual('codepatchbay','runJobInner',('createJobAndHandleBlocked','runHighAssurancePlanning','freezeChecklistAndMaterializeDag','executeWorkflowDag'),limit=5),
'audit':actual('codepatchbay','runJob',('finalizeAuditTrail','handleRunJobPanic'),limit=3),
'agent':actual('codepatchbay','runAgent',('allowedAgents','execPool','readOnlyMutationViolation'),limit=3),
'probe':actual('codepatchbay','runDeclaredCommandOnce',('execFile','shell','command'),limit=3),
'scope':actual('codepatchbay','scopeMatches',('count','changed.some'),limit=4),
'gate':actual('codepatchbay','evaluateCompletionGate',('checklist','mutating','verdict'),limit=3),
'event':actual('codepatchbay','appendEvent',('index','appendSerializedEvent','terminal','superseded'),limit=3),
'rebuild':actual('codepatchbay','rebuildJobsIndex',('rebuildJobsIndexLocked',)),
'doctor':actual('codepatchbay','checkRuntimeHealth',('collectRuntimeHealth',)),
'finalize':actual('codepatchbay','finalizeAndWriteSuccessfulResult',('finaliz','autoFinalize','result'),limit=3),
'common':actual('codepatchbay','writeJsonAtomic',('rename','writeFile','temporary','tmp'),limit=3)+actual('codepatchbay','WorkerBrokerClient.#call',('fetch','JSON','Authorization'),limit=3),
'browser':actual('winwincode','mountWinWinCodeClient.diagnosticScope',('resolveScopeContext',),limit=2)+actual('winwincode','mountWinWinCodeClient.performRender',('generation','abort','signal'),limit=2),
'client':actual('winwincode','createControlPlaneClient.<object@1149:9>.command',limit=2)+actual('winwincode','createControlPlaneClient.<object@1149:9>.query',limit=1)+actual('winwincode','createControlPlaneClient.<object@1149:9>.subscribe',limit=2),
'dispatcher':actual('winwincode','<GeneratedContractDispatcher as ControlPlaneApiPort>.command',('validate_actor','decode','authorize_scope','typed'),limit=5),
'chat':actual('winwincode','createChatDeliveryCreator.create',('Delivery','WorkRun','requestId','verificationCommand'),limit=3),
'authority':actual('winwincode','<LocalDeliveryAuthority as DeliveryAuthorityPort>.specification',('device','verification','repository','scope'),limit=4),
'workrun':actual('winwincode','WorkRunAggregate.start_item',('validate','find','WorkRunStart'),limit=3),
'identity':actual('winwincode','session_identity',('codex_thread_id','product_session_id'),limit=2)+actual('winwincode','CodexRunKey.from_dispatch',('fencing_token','payload_digest'),limit=2),
'worker_boot':actual('winwincode','run_managed',('WorkerSessionCredential','config.worker_credential_path'),limit=2)+actual('winwincode','run_worker',('RemoteWorkerPort','WorkerMain','codex'),limit=3),
'worker_dispatch':actual('winwincode','WorkerMain.accept_control',('accept_dispatch','replay'),limit=2)+actual('winwincode','WorkerMain.accept_dispatch',('from_dispatch','start_dispatch','max_concurrent'),limit=3),
'adapter':actual('winwincode','ProductionCodexAdapter.open',('seal_helper','Kernel','ExecutionOutbox','AdapterStore'),limit=4),
'intent':actual('winwincode','<ProductionCodexAdapter as CodexCoreAdapter>.submit_turn',('persist_run','reconcile_turn_exact','submission_digest','goal !='),limit=4),
'kernel':actual('winwincode','Kernel.create_session',('start_thread','manager'),limit=1)+actual('winwincode','Kernel.submit_turn',('start_or_steer_turn',),limit=1)+actual('winwincode','Kernel.reconcile_turn_exact',('inspect_durable_turn',),limit=1),
'outbox':actual('winwincode','ExecutionOutbox.retain_in_transaction',('INSERT INTO execution_outbox','metadata.delivery_id'),limit=2)+actual('winwincode','ExecutionOutbox.acknowledge_response',('response','delivery','state'),limit=2),
'device':actual('winwincode','WorkerMain.with_device_providers',limit=1)+actual('winwincode','DeviceModels.send',('consumer','transport'),limit=2)+actual('winwincode','ResolvedSecret.from_bytes',limit=1),
}

DOMAIN_CONTENT={
'cpb-command-queue':(['dynamic','root','fix','queue','worker'],'有限动态命令/环境覆盖、readiness和队列/assignment/inbox/worker来源有正文；CPB-01/03及既有production_assembly/channels保留字段预算/原子窗口与持久进程接缝，不用普通CALLS替代。'),
'cpb-engine-audit':(['ports','engine','audit'],'正文给出broker/local字段构造、ctx实际接口实参、create/规划/冻结/DAG及blocked返回；正常和panic audit调用由旧best-effort及access-audit不同模型保持对象分离。'),
'cpb-probe-gates':(['agent','probe','scope','gate'],'allowlist/pool/readonly、可信命令/execFile参数、scope count初始化/更新/返回和completion guards均有真实正文；trusted lineage/unsupported retention/hardGate有限反证由既有实际pattern保存，不把范围计量当业务语义或沙箱实效。'),
'cpb-events-delivery':(['event','rebuild','doctor','finalize'],'旧record投影模型及正文保留event/index/rebuild/doctor和finalizer/reconciler分离；新增state-lineage开发statement保留FIXED/job_superseded/同源queue字段与模式/opt-in/早退，不承诺必然入队或远端成功。'),
'wwc-browser-protocol':(['browser','client','dispatcher'],'浏览器scope/continuation正文与旧lifecycle模型保留generation/abort条件。boot无fake虽无通用boot正文，旧WWC-01 navigation_source.port_wiring有实际boot分支事实。D3既有真实生成JSON/Serde/route/typed模型现有窄seam开发正文；原语法/hash映射由冻结观察保存。'),
'wwc-chat-workrun':(['chat','authority','workrun','identity'],'独立Chat请求和保留身份、条件authority以及WorkRun候选/依赖/活动排除/重查已有有限pattern与实际正文，身份record分列。没有要求所有create/update/所有角色均成功。'),
'wwc-worker':(['worker_boot','worker_dispatch','identity'],'两入口/credential path/run_worker及typed dispatch真实正文与旧construction/message模型相互对应；保留generic候选，未把生产装配改成全局唯一边或所有故障收尾保证。'),
'wwc-kernel':(['adapter','intent','kernel'],'open的helper/store/outbox/Kernel调用、digest/persist/exact接口及三个独立Kernel API有实际正文和旧normal-order/source-join模型。部分SubmissionIntent写未被24句展示选中，完整源操作与旧actual message pattern保留，不将展示cap当source缺失。'),
'wwc-evidence-delivery':(['identity','workrun','outbox'],'WorkRun/lease/fencing/worker/session/outbox/ack已有有限身份/记录正文；原句冻结提交、角色、evidence source纳入交付合同尚无对应选中声明/有限fact/解释，保留该子句待来源定位。外部真实性及未审adapter仍排除。'),
'wwc-device':(['device'],'新增实际三项文档比较有literal/heading/scope与source fact refs，旧Device provider模型保留unsupported反证；实际比较限定Control Plane内部口径、凭据长期性unknown、protocol_bypass=false，不要求推翻全局Kernel原则。'),
}
ROWS={
('codepatchbay',34):(['dynamic','root','fix'],'CLI选择/提交正文可用，但task主要读取这一原句缺实际选中body，整行不能关闭。'),
('codepatchbay',35):(['queue'],'队列/assignment/attempt/inbox及旧权威原子/fencing/channel来源可用；不是全生命周期运行验证。'),
('codepatchbay',36):(['worker'],'workspace/inbox/bridge正文与真实Node process和持久channel seam可用；没有虚构普通跨进程调用。'),
('codepatchbay',37):(['ports','engine','gate'],'ctx/分支服务record、准备/规划/冻结/DAG/完成门有源码正文；注入目标与源码依赖方向不混为全局唯一实现。'),
('codepatchbay',38):(['probe','scope','gate'],'probe计量与可信输入、失败证据、completion/额外hardGate条件有有限内容；不声称结构范围证明业务需求。'),
('codepatchbay',39):(['event','rebuild','audit','finalize'],'服务写入/投影/audit/finalizer正文与新publication/lineage有限来源可用；外部效果未知保持。'),
('codepatchbay',40):(['common'],'公共文件/JSON/消息接口和已认证复用可见；原God-object/按耦合判断句是限制，不新增全项目所有权/复杂度证明。'),
('winwincode',34):(['browser','chat'],'页面、scope/request/port和旧真实导航拒绝模型可用；不把页面存在当上下文已接线。'),
('winwincode',35):(['client','dispatcher'],'command/query/subscribe有真实正文；所选D3生成JSON/Serde命令接缝有真实模型，不扩大所有query/WS codec。'),
('winwincode',36):(['dispatcher'],'公开解析/版本/actor/scope/typed dispatcher正文与有限D3模型可用；没有按模块大小评分或全权限定理。'),
('winwincode',37):(['authority','workrun','identity'],'产品authority/WorkRun来源已有；原候选/证据字段合同盘点中的冻结提交/角色/evidence-source子句待补选中来源。'),
('winwincode',38):(['worker_boot','worker_dispatch','identity'],'Job/lease/fencing/typed消息和generic生产装配的有限正文可用，不证明所有注入目标或故障资源回收。'),
('winwincode',39):(['adapter','intent','kernel'],'adapter/Kernel独立接口、helper调用与persist/exact来源可用；不假设安装的Codex CLI或声称完整helper算法安全证明。'),
('winwincode',40):(['device'],'Device/本地provider来源与文档3方面实际比较可用；没有把内部唯一改写成全局唯一或推断凭据长期性。'),
}

gaps=[{
'id':'original-cpb-task-read-source','repository':'codepatchbay','original_line':34,
'original_clause':'task 主要读取，不等于其所有传递依赖均无副作用',
'affected_units':['codepatchbay-responsibility-row-34'],
'actual_artifact_observation':'没有cli/commands/task.ts选中声明/正文；旧26引用也只有COMMANDS的task候选字符串。',
'needed_source_scope':{'file':'cli/commands/task.ts','symbol_locator_candidate':'run','actual_declaration_and_relevant_branch_authentication_required':True,'symbol_not_yet_verified_by_this_artifact_only_agent':True},
'finite_expected_content':'从真实选中task入口/分支的读取调用、投影字段/返回值解释所读职责；完整传递副作用未知保留。',
'not_required':['all CLI commands','full task purity','all transitive side effects'],
'formal_completion':None},
{'id':'original-wwc-selected-delivery-evidence-contract-inventory','repository':'winwincode','original_line':80,
'original_clause':'项目将候选、冻结提交、WorkRun/lease/fencing、角色和 evidence source 纳入交付合同',
'affected_units':['wwc-evidence-delivery','winwincode-responsibility-row-37'],
'actual_artifact_observation':'现实际输出已覆盖WorkRun/lease/fencing/记录身份/outbox/ack；冻结提交、角色和evidence source的所选合同字段/校验来源未在实际选中声明/旧有限pattern中建立。不能让DOM role或通用request记录代替。',
'needed_source_scope':{'actual_file_and_symbols':'parent saved-source query must locate the original-read Delivery/domain/session contract declarations or validators; not guessed by this artifact-only agent'},
'finite_expected_content':'只盘点原有限合同中实际冻结提交/候选/角色/evidence-source字段及相关来源或validator约束；区分WorkRun/lease/fencing，不要求外部内容真实或所有角色授权。',
'not_required':['candidate bytes or signature truth','full role authorization','all evidence sources','all publication/connector adapters','remote success'],
'formal_completion':None}]

domains=[]
for original in contract['original_main_chain_reconciliation']:
 keys,meaning=DOMAIN_CONTENT[original['id']]
 domains.append({'id':original['id'],'repository':original['repository'],'original_anchors':original['original_anchors'],
  'actual_content_readback':meaning,'actual_automatic_body_examples':[item for k in keys for item in E[k]],
  'prior_finite_model_contract_entries':original['related_entries'],
  'additional_saved_model_artifacts':(['STATE_LINEAGE_FINAL_HANDOFF.json'] if original['id']=='cpb-events-delivery' else ['WWC_PROTOCOL_EXISTING_EVIDENCE_READBACK.json','WWC_PROTOCOL_COMPUTED_SEAM_SOURCE_READBACK.json'] if original['id']=='wwc-browser-protocol' else ['documentation-source-query.json'] if original['id']=='wwc-device' else []),
  'unclosed_original_clause_ids':[g['id'] for g in gaps if original['id'] in g['affected_units']],
  'formal_completion':None,'decl_names_used_as_locators_not_purpose_proof':True})
rows=[]
for original in contract['pending_original_explanations']:
 if original['kind']!='finite_architecture_responsibility_explanation':continue
 line=original['original_anchors'][0]['source']['start_line'];keys,meaning=ROWS[(original['repository'],line)]
 rows.append({'id':original['id'],'repository':original['repository'],'original_anchors':original['original_anchors'],
  'actual_content_readback':meaning,'actual_automatic_body_examples':[item for k in keys for item in E[k]],
  'unclosed_original_clause_ids':[g['id'] for g in gaps if original['id'] in g['affected_units']],
  'formal_completion':None,'role_labels_or_example_count_do_not_establish_completion':True})
result={'kind':'original_finite_content_last_development_reconciliation','inputs':[artifact(n) for n in (
 'REPORT_COMPLETION_CONTRACT.json','RESPONSIBILITY_ACTUAL_BODY_DEVELOPMENT_INDEX.json','STATE_LINEAGE_FINAL_HANDOFF.json',
 'documentation-source-query.json','WWC_PROTOCOL_EXISTING_EVIDENCE_READBACK.json','WWC_PROTOCOL_COMPUTED_SEAM_SOURCE_READBACK.json')],
 'original_ten_domains':domains,'original_fourteen_responsibility_rows':rows,'remaining_original_finite_content':gaps,
 'meaning':'This compares original finite report content with actual saved machine prose/models. It supplies no new target-code finding, role assignment, semantic percentage or formal result. Available content must still be read from the next normal frozen reports.',
 'non_gaps_preserved':['boot no-fake is already in actual navigation port-wiring model despite no generic boot body',
  'SubmissionIntent and other unselected display statements remain in full source/model data; display truncation is not absent source',
  'unknown trait/macro/heap/runtime/credential lifetime/remote success are original boundaries, not new goals',
  'Publication/audit/export/connector areas retain original structural/interface depth; no all-adapter audit is required'],
 'formal_completion':False,'overall_original_goal_complete':False,
 'target_source_read':False,'database_read':False,'analyzer_run':False,'target_executed':False,'target_tests_run':False,'target_build_run':False}
(HERE/'REPORT_COMPLETION_LAST_DEVELOPMENT_SEMANTIC_AUDIT.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'artifact':'REPORT_COMPLETION_LAST_DEVELOPMENT_SEMANTIC_AUDIT.json','remaining_finite_clauses':[g['id'] for g in gaps],'formal_completion':False},ensure_ascii=False))
