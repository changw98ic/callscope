"""Display actual saved record/guard operations; no analysis or target I/O."""
import hashlib
import html
import json
from pathlib import Path

OUT=Path(__file__).resolve().parent
source=OUT/'winwincode-delivery-evidence-contract-report.json'
report=json.loads(source.read_text())
explanation=report['architecture']['responsibility_explanations']
base='/architecture/responsibility_explanations'
selected={(s['file'],s['symbol']) for chain in report['functional_chains'] for s in chain['source_scope']['selected_definitions']}

def cell(value,limit=500):
 text='unknown' if value is None else str(value)
 text=text.replace('\n',' ').replace('|','&#124;').replace('`','&#96;')
 return html.escape(text[:limit],quote=False)+(' [展示截断；完整值见引用]' if len(text)>limit else '')

lines=['# 交付 Evidence：实际字段与条件盘点','',
 '本视图只复制正常报告保存的生产源码操作，`presentation_only=true`；没有增加判定。完整报告：`'+source.name+'`。',
 '正常源码延续、调用成功、字段运行值、角色权限和 Runtime 真实性互相独立；此盘点不证明后四项。',
 '完整操作、source hash、源码位置与 evidence 引用均保留在每个 JSON pointer。','']
counts={'record_construction':0,'record_fields':0,'guard_rejection':0}
for index,operation in enumerate(explanation['operations']):
 owner=operation['actual_owner'];key=(owner['file'],owner['symbol'])
 if key not in selected or operation['operation_kind'] not in counts:continue
 operands=operation.get('operands',{});kind=operation['operation_kind'];counts[kind]+=1
 pointer=base+'/operations/'+str(index)
 location=(operation.get('source_locations') or [owner['location']])[0]
 lines+=['## '+cell(owner['symbol'])+' · '+cell(operands.get('record_type_source') if kind=='record_construction' else '源退出条件'),'',
  '来源：`'+cell(location['file'])+':'+str(location['line'])+'`；`'+pointer+'`。','']
 if kind=='record_construction':
  lines+=['| 实际字段 | 捕获初始化来源 |','|---|---|']
  for field in operands.get('record_fields',[]):
   counts['record_fields']+=1;lines.append('| '+cell(field.get('name'))+' | '+cell(field.get('source_text'))+' |')
  lines+=['','保存边界：`closed_captured_shape='+str(operands.get('closed_captured_shape','unknown')).lower()+'`，`runtime_field_presence_or_value_proven=false`。','']
 else:
  lines+=['- 条件：`'+cell(operands.get('condition_source'))+'`。',
    '- 退出形式：`'+cell(operands.get('exit_kind'))+'`；`'+cell(operands.get('exit_source'))+'`。',
    '- 保存边界：`guard_truth_or_rejection_observed='+str(operands.get('guard_truth_or_rejection_observed','unknown')).lower()+'`；`return_is_error_or_business_rejection_proven='+str(operands.get('return_is_error_or_business_rejection_proven','unknown')).lower()+'`。','']
text='\n'.join(lines)+'\n';target=OUT/'winwincode-delivery-evidence-contract-inventory.md'
with target.open('x',encoding='utf-8') as stream:stream.write(text)
metadata={'kind':'saved_record_and_guard_presentation','presentation_only':True,'input_report':source.name,'input_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'input_snapshot_id':report['snapshot']['id'],'selection':'actual selected declaration record_construction and guard_rejection operations','copied_counts':counts,'new_assessment_computed':False,'runtime_authenticity_or_role_authority_inferred':False,'output':target.name,'output_sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'line_count':len(text.splitlines()),'display_source_char_limit':500,'full_operations_preserved_in_input':True,'target_executed':False}
with (OUT/'DELIVERY_EVIDENCE_INVENTORY_INPUTS.json').open('x',encoding='utf-8') as stream:json.dump(metadata,stream,ensure_ascii=False,indent=2);stream.write('\n')
print(json.dumps(metadata,ensure_ascii=False),flush=True)
