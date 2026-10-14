"""Build a report-scope completion contract, never target judgments.

Reads only unchanged original reports and iteration11 scope/catalog/alignment.
No target source, databases, detector, compiler, tests or synthetic fixtures.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
EXISTING_CONTRACT=HERE/'REPORT_COMPLETION_CONTRACT.json'
if EXISTING_CONTRACT.exists():
    prior=json.loads(EXISTING_CONTRACT.read_text())
    if prior.get('scope2_finite_content_preflight') or prior.get('completion_assessment',{}).get('actual_new_publication_inputs'):
        raise SystemExit('Refusing to overwrite actual content/formal readback with an initial pending contract.')
PREVIOUS = ROOT / 'reports/astra-iteration11'
CATALOG_PATH = PREVIOUS / 'REPORT_ALIGNMENT_CATALOG.json'
ALIGNMENT_PATH = PREVIOUS / 'REPORT_ALIGNMENT_RESULTS.json'
SCOPE_PATH = PREVIOUS / 'REPORT_SCOPE_GAPS.md'
OLD = 'old_formal_finite_relation_supported'
PENDING = 'new_implementation_pending'

def sha(data): return hashlib.sha256(data).hexdigest()
def artifact(path):
    raw=path.read_bytes()
    return {'file':str(path.relative_to(ROOT)), 'sha256':sha(raw), 'bytes':len(raw)}

catalog=json.loads(CATALOG_PATH.read_text())
alignment=json.loads(ALIGNMENT_PATH.read_text())
reports={r['repository']:r for r in catalog['original_reports']}
actual_bytes={repo:(ROOT/r['file']).read_bytes() for repo,r in reports.items()}
for repo,r in reports.items():
    if sha(actual_bytes[repo]) != r['source_hash']: raise ValueError('Original report changed: '+repo)


def anchor(repo,line):
    candidates=[s for s in reports[repo]['statements'] if s['source']['start_line'] <= line <= s['source']['end_line']]
    if len(candidates)!=1: raise ValueError(f'Expected exact original statement at {repo}:{line}')
    s=candidates[0]; span=s['source']
    if sha(actual_bytes[repo][span['start_byte']:span['end_byte']])!=span['span_hash']:
        raise ValueError('Original span identity mismatch')
    return {'catalog_statement_id':s['id'], 'source':span, 'original_statement':s['actual_statement'],
        'origin':'unchanged_original_report_scope_not_new_target_evidence'}


def compact_ref(ref):
    return {k:v for k,v in ref.items() if k in {'artifact','artifact_sha256','json_pointer','target_value_sha256',
        'origin','canonical_hash_encoding','finding_id','evidence_id'}}

refs={}
for repo in alignment['original_reports']:
    for section in repo['sections']:
        for ref in section['automatic_evidence_refs']:
            rid=ref.get('snapshot_identity',{}).get('rule_id')
            if rid:
                k=(repo['repository'],rid)
                item=compact_ref(ref)
                if item not in refs.setdefault(k,[]): refs[k].append(item)

GOALS=[
 ('codepatchbay','CPB-01','cpb-astra-pipeline-retry-integrated',[50,88,90], '提交参数、metadata/消息与实际预算消费者分开；独立phase/infra预算不是提交选项已消费的反证'),
 ('codepatchbay','CPB-02','cpb-complete-terminal-classification',[96,98], '状态生产/投影、terminal分类、recover guard和底层封口反证；terminal与recoverable分开'),
 ('codepatchbay','CPB-03','cpb-astra-active-key-complete',[102,104,106], '源检查/保护区/写入生成条件交错，并保留顺序复用、pending和description反证'),
 ('winwincode','WWC-01','wwc-navigation-complete-judgment',[94,96,98], '可见导航缺delivery经实际端口/闭包到提交前拒绝；有效URL/fake/Chat反证保留'),
 ('winwincode','WWC-02','wwc-report-device-spec-command-flow',[58,104,106,108], 'UI字段、实际协议、Device条件非空guard及local/Chat分支；optional不是分支免除'),
]
# Each item names an existing saved relation, not a new expected target result.
CHAINS={
 'codepatchbay':[
 ('cpb-captured-record-resource-writers',[34,35,36,37,38,39,40],'所选写者/同token消费者与拒绝来源；职责解释仍另列待完成'),
 ('cpb-event-index-projection',[78],'event serializer→append、projection→index writer与重建/doctor来源；独立提交边界'),
 ('cpb-report-access-audit-response',[64,113],'Hub access audit失败到响应字段/发送实参，与job尾部audit对象分开'),
 ('cpb-report-agent-execution-policy',[68],'allowlist、注入pool、readonly/失败分类、环境与sandbox分支'),
 ('cpb-report-completion-gate-conditions',[74],'checklist、mutating条件、verdict门与readonly/docs/parent豁免'),
 ('cpb-report-conditional-delivery-result',[80,82],'autoFinalize、持久结果/读回、attempt/finalizer/journal与queue projection；发布条件单列'),
 ('cpb-report-engine-stage-chain',[60,62],'注入ctx与创建/准备/规划/冻结/DAG正常顺序、前置提前返回'),
 ('cpb-report-job-audit-best-effort',[64,113],'正常/panic相同收尾目标及caught失败；不与access审计混合'),
 ('cpb-report-readiness-abrupt-guard',[48],'readiness结果、失败提前返回与之后enqueue正常到达条件'),
 ('cpb-report-trusted-probe-command-source',[70],'HEAD policy、predicate lookup、结构化execFile与shell=false来源'),
 ('cpb-report-unsupported-probe-evidence',[72],'未支持方法的失败record与marker；不是静默放行或验证齐备'),
 ('cpb-trusted-command-lineage',[70],'stdout/JSON/policy parser到lookup/command实参的中间来源'),
 ('cpb-unsupported-record-retention',[72],'true marker、指定skip、返回集合/ledger/artifact content来源与覆盖边界'),
 ],
 'winwincode':[
 ('wwc-browser-continuation-lifecycle',[48],'generation/context/abort/closed、suspension与局部写回条件'),
 ('wwc-captured-record-resource-writers',[34,35,36,37,38,39,40],'捕获writer/interface/consumer来源；有限职责解释仍另列待完成'),
 ('wwc-report-adapter-durable-exact-turn',[74],'submission intent→persist→exact reconcile，prompt/digest条件'),
 ('wwc-report-chat-delivery-workrun-requests',[56],'Chat的Delivery/spec/WorkItem/WorkRun请求及guard/结果绑定'),
 ('wwc-report-chat-retained-request-identities',[42,56],'当前尝试保留请求、delivery投影与不同request身份'),
 ('wwc-report-device-provider-deployment',[86],'Server unsupported与独立Device/worker provider安装来源分开'),
 ('wwc-report-kernel-create-session-interface',[76],'Kernel create_session单独接口及线程创建来源'),
 ('wwc-report-kernel-reconcile-exact-interface',[76],'Kernel exact reconcile单独接口与指定turn history来源'),
 ('wwc-report-kernel-submit-turn-interface',[76],'Kernel submit_turn输入和session thread start/steer来源'),
 ('wwc-report-outbox-ack-correlation-fields',[80],'所选Family/tuple/codec、SQL列参数和ack删除来源'),
 ('wwc-report-production-adapter-embedded-kernel',[72],'adapter私有目录/helper/store/outbox/bridge与Kernel构造来源'),
 ('wwc-report-submission-intent-kernel-order',[74],'同一提交的intent/persist/reconcile正常顺序；与重叠规则不重复计覆盖'),
 ('wwc-report-worker-adapter-record-identities',[42,66,68,74],'dispatch/job/lease/workspace/profile/thread/session/turn投影和消费者'),
 ('wwc-report-worker-bootstrap-entries',[64],'remote/managed两个入口与共同run_worker的来源'),
 ('wwc-report-worker-production-construction',[64,68],'真实生产构造及generic port候选；不全局绑定唯一实现'),
 ('wwc-report-worker-typed-dispatch',[66],'typed message/replay/dispatch/checkout/ensure-thread及拒绝来源'),
 ('wwc-report-workrun-finite-selection',[60],'effective state/依赖量词/活动排除/selected ID recheck有限表'),
 ('wwc-report-workrun-state-guards',[60],'start_next/start_item验证与选择guard来源；不穷举aggregate'),
 ]}

old_entries=[]
for repo,gid,rid,lines,content in GOALS:
    saved_state=alignment['saved_result_inventory'][repo]['goal_statuses_copied_from_saved_results'][gid]
    old_entries.append({'id':gid,'repository':repo,'kind':'registered_condition_judgment','status':OLD,
        'original_anchors':[anchor(repo,l) for l in lines], 'finite_content_to_preserve':content,
        'prior_formal':{'series':'v13','saved_state':saved_state,'refs':refs[(repo,rid)]},
        'automatic_output_selector':{'collection':'judgments','key':'goal_id','equals':gid},
        'required_output_fields':['assessment','derived_judgment','conditions','refutations','necessary_gaps','obligations','finding_id','evidence_id'],
        'new_formal_readback':None})
for repo,items in CHAINS.items():
    for rid,lines,content in items:
        state=alignment['saved_result_inventory'][repo]['chain_states_copied_from_saved_results'][rid]
        old_entries.append({'id':rid,'repository':repo,'kind':'finite_source_relation','status':OLD,
            'original_anchors':[anchor(repo,l) for l in lines], 'finite_content_to_preserve':content,
            'prior_formal':{'series':'v13','saved_state':state,'refs':refs[(repo,rid)]},
            'automatic_output_selector':{'collection':'functional_chains','key':'rule_id','equals':rid},
            'required_output_fields':['assessment','pattern','source_facts','source_scope','analysis_gaps','trusted_models','policy_declarations','finding_id','evidence_id'],
            'completion_scope':'the saved finite source relation only; original clauses require reconciliation below',
            'new_formal_readback':None})

ROW_SUPPORT={
 'codepatchbay':{
 34:['CPB-01','CPB-03','cpb-report-readiness-abrupt-guard'],
 35:['CPB-01','CPB-03','cpb-report-conditional-delivery-result'],
 36:['CPB-01','cpb-report-conditional-delivery-result'],
 37:['CPB-01','cpb-report-engine-stage-chain','cpb-report-completion-gate-conditions'],
 38:['cpb-trusted-command-lineage','cpb-unsupported-record-retention','cpb-report-completion-gate-conditions'],
 39:['CPB-02','cpb-event-index-projection','cpb-report-agent-execution-policy','cpb-report-conditional-delivery-result'],
 40:['cpb-captured-record-resource-writers'],
 },
 'winwincode':{
 34:['WWC-01','WWC-02','wwc-browser-continuation-lifecycle','wwc-report-chat-retained-request-identities'],
 35:['WWC-02','wwc-report-chat-retained-request-identities','wwc-report-outbox-ack-correlation-fields'],
 36:['WWC-02','wwc-report-device-provider-deployment'],
 37:['WWC-02','wwc-report-workrun-finite-selection','wwc-captured-record-resource-writers'],
 38:['wwc-report-worker-typed-dispatch','wwc-report-worker-adapter-record-identities','wwc-report-worker-production-construction'],
 39:['wwc-report-production-adapter-embedded-kernel','wwc-report-adapter-durable-exact-turn','wwc-report-kernel-create-session-interface','wwc-report-kernel-submit-turn-interface','wwc-report-kernel-reconcile-exact-interface'],
 40:['wwc-report-device-provider-deployment'],
 }}
pending=[]
for repo in ('codepatchbay','winwincode'):
    for line in range(34,41):
        original=anchor(repo,line)
        pending.append({'id':f'{repo}-responsibility-row-{line}','repository':repo,
            'kind':'finite_architecture_responsibility_explanation','status':PENDING,'original_anchors':[original],
            'prior_related_entries':ROW_SUPPORT[repo][line],
            'existing_capture_is_not_yet_this_explanation':True,
            'automatic_output_contract':{
                'integrated_container':'/architecture/responsibility_explanations',
                'container_confirmed_from_current_core_schema':True,'exact_pointer_after_publication':None,
                'semantic_selector':{'original_report':original['source']['file'],'original_start_line':line},
                'required_fields':['operations','declaration_explanations','source_location_index','evidence_reference_index','explicit_source_transfers','normal_source_orders','authenticated_interface_reuse','communication_boundaries','computed_source_contract_seams','analysis_gaps','assessment'],
                'required_declaration_fields':['actual_owner','summary','summary_statement_ids','statements','all_operation_refs'],
                'required_statement_fields':['text','operation_kind','operation_id','operation_pointer','source_evidence_refs_pointer','source_locations','guards','source_order','limitations'],
                'pooled_reference_condition':'Thin source locations/evidence refs must resolve through this responsibility object indexes to actual captured hashes/spans and evidence contexts. A selected prior finding is not proof of a new operation.',
                'computed_seam_condition':'Dynamic import/process/receiver/channel/state-lineage explanation pointers must resolve to the actual saved finite source analysis, preserving its alternatives, conditions and unknown effects.',
                'navigation_labels_are_not_evidence':True,
                'field_names_may_follow_actual_implementation':True},
            'finite_completion_condition':'由实际保存操作/接口/组合/协议来源解释原表这一行的有限分工和关键边界；每一正向解释可下钻，未覆盖子域明确保留。仅目录名、函数名、原表文本或writer计数不满足。',
            'not_required':['unique canonical owner theorem','all writers','all authorization','all heap/resource equality','runtime effects'],
            'new_formal_readback':None})
pending.append({'id':'wwc-device-documentation-deployment-comparison','repository':'winwincode',
    'kind':'finite_documentation_code_comparison','status':PENDING,'original_anchors':[anchor('winwincode',40),anchor('winwincode',86),anchor('winwincode',88)],
    'prior_related_entries':['wwc-report-device-provider-deployment','wwc-document-device-provider-deployment-scope'],
    'automatic_output_contract':{'integrated_container':'/documentation_comparisons',
        'container_confirmed_by_root_integration':True,'exact_pointer_after_publication':None,
        'required_content_fields':['document_claims','documentation_comparisons','relation_witnesses','source_relation_fact_ids','comparison','conditions','bounds','necessary_gaps'],
        'required_finite_aspects':['documented_control_plane_scope_and_device_source_route','credential_material_reference_and_lifetime','worker_stream_protocol_and_local_consumer'],
        'required_document_content':['literal sentence','heading/block context','explicit scope/quantifier','source hash and byte span'],
        'required_deployment_content':['actual selected source facts','branch/callback conditions','selected provider candidate scope'],
        'comparison_cannot_infer_global_exclusivity_from_control_plane_internal_scope':True,
        'credential_lifetime_or_protocol_bypass_proof_not_required':True,
        'field_names_may_follow_actual_implementation':True},
    'finite_completion_condition':'自动定位原文所指长期Credential/Provider归属的具体文档表述，与实际Server/Worker/Device生产来源做局部对照；按实际来源给出适用部署及说明差异或未知，不从人工报告复制比较结果。',
    'not_required':['all architecture documentation consistency','all credential paths','secret audit','global unique Kernel/provider theorem'],
    'new_formal_readback':None})

# Source-domain reconciliation prevents "31 green items" hiding an original
# finite clause.  It is neither paragraph scoring nor fresh target review.
GROUPS=[
 ('cpb-command-queue','codepatchbay',[46,48,50,54,56],['CPB-01','CPB-03','cpb-report-readiness-abrupt-guard'],
  ['动态命令候选与executorRoot覆盖条件','实际队列/assignment/attempt/inbox/worker/bridge接缝','readiness提前返回和参数接受/实际消费分开']),
 ('cpb-engine-audit','codepatchbay',[60,62,64],['CPB-01','cpb-report-engine-stage-chain','cpb-report-job-audit-best-effort','cpb-report-access-audit-response'],
  ['broker/local服务组合与可注入ctx边界','创建/准备/规划/冻结/DAG和早退','正常/panic job audit与access audit主体分开']),
 ('cpb-probe-gates','codepatchbay',[68,70,72,74],['cpb-report-agent-execution-policy','cpb-report-trusted-probe-command-source','cpb-trusted-command-lineage','cpb-report-unsupported-probe-evidence','cpb-unsupported-record-retention','cpb-report-completion-gate-conditions'],
  ['allowlist/pool/readonly/environment/sandbox分支','可信命令字段来源，expectedEvidence不作命令而可参与独立保护路径','static scope计量只支持声明范围变更；未支持方法失败record及hardGate反证','checklist优先、mutating和各豁免条件']),
 ('cpb-events-delivery','codepatchbay',[78,80,82],['CPB-02','cpb-event-index-projection','cpb-report-conditional-delivery-result','cpb-review-fixed-state-lineage','cpb-finalizer-conditional-publication'],
  ['终态封口与event/index不同提交边界、重建/doctor','FIXED→job_superseded→新lineage task的真实生产来源','GitHub发布与本地dry-run的具体配置/授权条件','completed/assignment/finalizer/reconciler/远端成功概念分离']),
 ('wwc-browser-protocol','winwincode',[48,50,52],['WWC-01','WWC-02','wwc-browser-continuation-lifecycle'],
  ['生产boot无fake seed、实际scope/port来源','generation/abort旧结果边界','typed协议/字段身份而非跨语言假CALLS','原bytes/hash/派生解析映射与未知保留']),
 ('wwc-chat-workrun','winwincode',[42,56,58,60],['WWC-02','wwc-report-chat-delivery-workrun-requests','wwc-report-chat-retained-request-identities','wwc-report-workrun-finite-selection'],
  ['Chat独立创建与请求重用反证','create/update authority的scope/repository/Device baseline/verification条件','runnable/依赖/活动排除/selected ID recheck','身份不能折叠为一个session_id']),
 ('wwc-worker','winwincode',[64,66,68],['wwc-report-worker-bootstrap-entries','wwc-report-worker-production-construction','wwc-report-worker-typed-dispatch','wwc-report-worker-adapter-record-identities'],
  ['两入口共同worker来源及短期凭据/执行事实边界','typed replay/dispatch/checkout/profile/容量/adapter来源','generic候选与唯一运行实现分开，故障收尾不全称']),
 ('wwc-kernel','winwincode',[72,74,76],['wwc-report-production-adapter-embedded-kernel','wwc-report-adapter-durable-exact-turn','wwc-report-submission-intent-kernel-order','wwc-report-kernel-create-session-interface','wwc-report-kernel-submit-turn-interface','wwc-report-kernel-reconcile-exact-interface'],
  ['实际嵌入式Kernel构造、helper/store/outbox来源','intent→persist→exact reconcile正常顺序','create/submit/exact reconcile三个接口分离，不要求崩溃演练']),
 ('wwc-evidence-delivery','winwincode',[80,82],['wwc-report-workrun-finite-selection','wwc-report-worker-adapter-record-identities','wwc-report-outbox-ack-correlation-fields'],
  ['候选/冻结提交/WorkRun/lease/fencing/角色/evidence source所选身份来源','durable outbox/ack有限来源','外部日志/bytes/签名/provider真实性与未审adapter排除']),
 ('wwc-device','winwincode',[86,88],['wwc-report-device-provider-deployment','wwc-document-device-provider-deployment-scope','wwc-device-documentation-deployment-comparison'],
  ['unsupported不能抹去设备侧provider来源','文档绝对口径与local/Device部署差异','provider位置与Kernel唯一性是不同命题']),
]
reconciliation=[]
for gid,repo,lines,entries,clauses in GROUPS:
    reconciliation.append({'id':gid,'repository':repo,'original_anchors':[anchor(repo,l) for l in lines],
        'related_entries':entries,'original_finite_clauses_to_find_in_actual_output':clauses,
        'mapping_is_not_semantic_completion':True,'actual_v14_clause_readback':None,
        'required_action':'正式新report中逐项定位实际来源和机器生成解释；若某原子句没有来源，显式列未完成，不因已有rule支持而关闭。'})

excluded=[]
for repo,lines in [('codepatchbay',[18,20,22,24,26,110,111,112,113,114]),('winwincode',[18,20,22,24,26,82,114,115,116,117,118,119])]:
    excluded.append({'repository':repo,'original_anchors':[anchor(repo,l) for l in lines],
        'meaning':'保持原阅读深度/未审范围和不成立推断；只要求准确报告范围，不新增全领域审计或运行证明。'})

contract={
 'schema':'callscope.original-finite-report-completion-contract.v1','target_publication':'v14',
 'purpose':'Complete the original already-read finite code-level report propositions with actual automatic evidence and explanations; release creation alone does not end the task.',
 'origin':'session-authorized implementation scope mapped from unchanged original reports; not target evidence or detector policy',
 'inputs':[artifact(CATALOG_PATH),artifact(ALIGNMENT_PATH),artifact(SCOPE_PATH),*[artifact(ROOT/r['file']) for r in reports.values()]],
 'allowed_current_statuses':{OLD:'Actual v13 saved finite relationship status copied from prior alignment; not a whole-paragraph semantic score.',PENDING:'New automatic explanation/comparison or actual new-publication readback still absent.'},
 'prior_formal_snapshot_identities':{r['repository']:r['automatic_snapshot_identity'] for r in alignment['original_reports']},
 'prior_five_judgments_and_source_relations':old_entries,
 'pending_original_explanations':pending,
 'original_main_chain_reconciliation':reconciliation,
 'report_level_required_outputs':[
  {'fields':['coverage','project_declarations','diagnostics'],'requirement':'原选择/解析/排除/声明身份与阅读深度分开；manifest/docs意图不是经代码证明的功能。','original_anchors':[anchor('codepatchbay',17),anchor('codepatchbay',28),anchor('winwincode',17),anchor('winwincode',28)]},
  {'fields':['judgments','functional_chains','architecture','report_scope'],'requirement':'保存成立条件、实际反证、未解析接缝与原未审，不把unknown当目标缺功能；不把source-only上升为运行成功。','original_anchors':[anchor('codepatchbay',11),anchor('winwincode',11)]},
  {'fields':['source_relation_index','overlapping_source_selections'],'requirement':'presentation/navigation不新增评级；重叠来源不增加语义覆盖；原Finding/Evidence/完整pattern可下钻。','origin':'existing report representation boundary, not extra target functionality'},
 ],
 'original_excluded_and_negative_inference_boundaries':excluded,
 'completion_conditions':[
  {'id':'identity','required':'两个正式新report与保存finding/evidence绑定真实snapshot/source/policy/tool身份，原报告hash/span不变；不能拿development当正式。'},
  {'id':'frozen-observation-integrity','required':'原26观察按既有冻结协议逐项保留身份、确定调用位置/路径与指定未知原因，不改evidence_only语义迁就新结果；实际比较和发布身份可核对，26不是全文分母。'},
  {'id':'preserve-original-findings','required':'五原判断的当前自动结果、必要关系、条件与反证都有实际保存依据；不以包装状态或旧指针代替新readback。'},
  {'id':'preserve-finite-relations','required':'31原有限关系按rule_id逐项找到当前实际pattern/facts/scope/gaps；原有限关系的源码证据保持，不以条目数量或更名代替。'},
  {'id':'explain-original-tables','required':'原两张职责表的各行均有机器生成的有限职责/接口/边界解释与真实来源；不要求全owner/全授权/全资源证明。'},
  {'id':'compare-device-documentation','required':'文档具体原文与代码实际部署来源做有限机器对照；由实际新结果得出比较，不复制原人工结论。'},
  {'id':'no-original-clause-left-behind','required':'十个主链domain的原有限子句逐项有实际输出/证据；特别CPB:80 FIXED→superseded→lineage及GitHub/dry-run不能被31项状态遮蔽。'},
  {'id':'preserve-scope','required':'原未审/结构盘点和运行未验证保持排除；目录/来源存在不等于全行为审计。'},
  {'id':'actual-generated-artifacts','required':'最终JSON/Markdown来自系统保存结果，索引指针和解释refs可核对；completion回填只读取实际新结果，不写手工目标判断。'},
 ],
 'insufficient_stop_reasons':['a new version or release/report file exists','five judgments or 31 source-chain rows are green without original-content reconciliation','130 paragraph/table catalog entries merely have links','more facts, modules, rows, nodes or resolved calls','handwritten architecture prose without actual derived evidence','unmodeled cases relabeled as environmental assumptions','all unknowns removed or stronger unreviewed guarantees demanded'],
 'not_required_to_finish':['target execution/tests/builds/sandbox','whole-program correctness or every source line','all ownership/authorization/protocol/security paths','all dynamic dispatch, trait, heap or concurrent interleavings','remote effects or provider/ack/candidate bytes authenticity','new Astra approval/re-review','literal paragraph-by-paragraph reproduction or functional coverage percentage'],
 'pending_followup_source_checks':[
  {'original_anchor':anchor('codepatchbay',80),'kind':'original_finite_clause_without_established_producer_ref','status':PENDING,
   'note':'Responsibilities owner reports no selected review-dispatch producer in v13 source scopes; requires actual automatic production-branch source before explaining FIXED→superseded→lineage. This is a scope-tracking gap, not a fresh target defect judgment.'},
  {'original_anchor':anchor('codepatchbay',80),'kind':'original_configuration_boundary_needs_actual_refs','status':PENDING,
   'note':'GitHub versus local dry-run requires actual saved configuration/guard/branch references; existing delivery source coverage alone does not manufacture them.'},
 ],
 'implementation_schema_observations':{'architecture_module':artifact(ROOT/'callscope/architecture_responsibilities.py'),
  'architecture_container':'/architecture/responsibility_explanations',
  'architecture_actual_content_fields':['operations','declaration_explanations','explicit_source_transfers','normal_source_orders','assessment'],
  'architecture_navigation_is_not_proof':True,
  'documentation_module':artifact(ROOT/'callscope/documentation_relations.py'),
  'documentation_container':'/documentation_comparisons','schema_observation_does_not_complete_target_propositions':True},
 'completion_assessment':{'status':PENDING,'complete':False,'actual_new_publication_inputs':[],
  'reason':'v14 formal output has not been read; no new completion or semantic-equivalence result has been computed.'},
 'paragraph_scoring_performed':False,'functional_coverage_percentage_computed':False,
 'target_source_read':False,'database_read':False,'analyzer_run':False,'target_executed':False,
 'target_tests_run':False,'target_build_run':False,'manual_new_target_judgments_generated':False,
}
(HERE/'REPORT_COMPLETION_CONTRACT.json').write_text(json.dumps(contract,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'old_judgments':len(GOALS),'old_source_relations':sum(map(len,CHAINS.values())),
 'original_responsibility_rows':14,'documentation_comparison_pending':True,
 'new_publication_readback_performed':False,'completion':contract['completion_assessment']},ensure_ascii=False))
