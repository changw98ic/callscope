"""Static syntax/identity/link review of the delivered tool and saved artifacts.

This performs no tests, import of target code, build, or browser verification.
"""
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tomllib
from urllib.parse import unquote
from callscope.analysis_inputs import tool_identity


def main():
    directory=Path(__file__).resolve().parent
    root=directory.parents[1]
    package=root/'callscope'
    identity=tool_identity()
    python_files=sorted(package.rglob('*.py'))
    for file in python_files:
        ast.parse(file.read_text(), filename=str(file))
    js=subprocess.run(['node','--check',str(root/'web/app.js')],
                      check=True,capture_output=True,text=True)
    init=ast.parse((package/'__init__.py').read_text())
    package_version=next(ast.literal_eval(node.value) for node in init.body
                         if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='__version__' for t in node.targets))
    project=tomllib.loads((root/'pyproject.toml').read_text())
    summaries=[json.loads((directory/f'{name}-summary.json').read_text())
               for name in ('codepatchbay','winwincode')]
    scan_ids=[item['stats']['component_versions']['tool']['source_hash'] for item in summaries]
    documents=sorted((root/'docs').glob('*.md'))+[root/'README.md']+sorted(directory.glob('*.md'))
    missing=[]
    count=0
    for document in documents:
        text=document.read_text()
        for target in re.findall(r'\[[^\]]+\]\(([^\)]+)\)',text):
            target=target.strip().strip('<>')
            if not target or target.startswith(('https://','http://','mailto:','app://','#','skill://')):
                continue
            target=unquote(target.split('#',1)[0])
            target=re.sub(r':\d+$','',target)
            path=Path(target) if target.startswith('/') else document.parent/target
            count+=1
            if not path.exists():
                missing.append({'document':str(document.relative_to(root)),'target':target})
    baseline=directory.parent/'astra-baseline/capability-baseline.json'
    states=[]
    for name in ('codepatchbay','winwincode'):
        repo=root.parent/name
        base=['git','-c','core.fsmonitor=false','-c','core.hooksPath=/dev/null','-C',str(repo)]
        status=subprocess.run(base+['status','--porcelain'],check=True,capture_output=True,text=True)
        commit=subprocess.run(base+['rev-parse','HEAD'],check=True,capture_output=True,text=True)
        states.append({'repository':name,'commit':commit.stdout.strip(),
                       'porcelain':status.stdout,'clean':not status.stdout,
                       'operation':'read-only git status/rev-parse with hooks and fsmonitor disabled'})
    (directory/'target-state-observations.json').write_text(json.dumps(states,ensure_ascii=False,indent=2)+'\n')
    artifact={
        'verification_mode':'normal static scans and saved queries, independent source/artifact review, syntax/link checks; no test suite',
        'package_version':package_version,'pyproject_version':project['project']['version'],
        'tool_identity':identity,'formal_scan_tool_identities_match':all(value==identity['source_hash'] for value in scan_ids),
        'frozen_baseline_sha256':hashlib.sha256(baseline.read_bytes()).hexdigest(),
        'tool_python_source_syntax_review_files':len(python_files),
        'javascript_source_syntax_check':'node --check web/app.js',
        'markdown_documents_checked':len(documents),'local_links_checked':count,'missing_local_links':missing,
        'target_state_artifact':'target-state-observations.json','saved_query_artifact':'saved-query-observations.json',
        'target_executed':False,'target_tests_run':False,'target_build_run':False,
        'tool_test_suite_run':False,'browser_verification_run':False,'package_installation_verification_run':False}
    (directory/'verification-summary.json').write_text(json.dumps(artifact,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(artifact,ensure_ascii=False))


if __name__=='__main__':
    main()
