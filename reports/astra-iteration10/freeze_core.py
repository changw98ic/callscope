"""Record the implementation before normal static publications.

Source syntax and content identities are checked. No target code or tests run.
"""
import ast
import hashlib
import json
from pathlib import Path
from callscope import __version__
from callscope.analysis_inputs import tool_identity
from callscope.models import ANALYZER_VERSION,DETECTOR_VERSION,SCHEMA_VERSION
from publication_identity import check_contracts,digest_file,write_json


def main():
    directory=Path(__file__).resolve().parent
    check_contracts(directory)
    expected=("0.12.0","static-multilang-12","call-rules-11-whole-judgments","2")
    if (__version__,ANALYZER_VERSION,DETECTOR_VERSION,SCHEMA_VERSION)!=expected:
        raise RuntimeError("v12 implementation versions have not been set")
    package=directory.parents[1]/"callscope"
    paths=sorted(package.rglob("*.py"))
    hashes={}
    archive=directory/"frozen-core-source"
    for path in paths:
        raw=path.read_bytes()
        ast.parse(raw.decode("utf-8"),filename=str(path))
        relative=path.relative_to(package)
        hashes[relative.as_posix()]=hashlib.sha256(raw).hexdigest()
        destination=archive/relative
        destination.parent.mkdir(parents=True,exist_ok=True)
        destination.write_bytes(raw)
    archive.mkdir(parents=True,exist_ok=True)
    (archive/"pyproject.delivery.toml").write_bytes((package.parent/"pyproject.toml").read_bytes())
    freeze={"package_version":__version__,"publication_series":"v12",
        "analyzer_version":ANALYZER_VERSION,"detector_version":DETECTOR_VERSION,"schema_version":SCHEMA_VERSION,
        "tool_identity":tool_identity(),"package_source_sha256":hashes,
        "module_sha256":{name[:-3]:value for name,value in hashes.items() if "/" not in name},
        "benchmark_reports":{f"astra-baseline/{name}":digest_file(directory.parent/"astra-baseline"/name)
            for name in ("CODEPATCHBAY_ANALYSIS.md","WINWINCODE_ANALYSIS.md")},
        "policy_files":{f"{repository}-policy.json":digest_file(directory/f"{repository}-policy.json")
            for repository in ("codepatchbay","winwincode")},
        "freeze_basis":"Completed source-derived analyzers and normal saved-source observations; original reports remain the benchmark. No recurring Astra approval gate.",
        "target_executed":False,"target_tests_run":False,"target_build_run":False,"tool_test_suite_run":False}
    write_json(directory/"CORE_FREEZE.json",freeze)
    print(json.dumps({"version":__version__,"tool_identity":freeze["tool_identity"],"python_source_files":len(paths)}))


if __name__=="__main__":
    main()
