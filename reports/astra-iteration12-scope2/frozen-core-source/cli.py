"""CLI for static analysis. Findings never act as an automatic merge gate."""

import argparse
from dataclasses import asdict
import json
import os
from pathlib import Path
import sqlite3
import sys
import tempfile

from . import __version__
from .graph import diff_snapshots, find_path
from .service import AnalysisService
from .store import Store


def _dump(value, output: str | None = None) -> None:
    if output:
        path = Path(output)
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary = None
        try:
            with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent,
                                             prefix="." + path.name + ".", delete=False) as stream:
                temporary = Path(stream.name)
                json.dump(value, stream, ensure_ascii=False, indent=2, allow_nan=False)
                stream.write("\n")
            os.replace(temporary, path)
            temporary = None
        finally:
            if temporary is not None:
                temporary.unlink(missing_ok=True)
    else:
        json.dump(value, sys.stdout, ensure_ascii=False, indent=2, allow_nan=False)
        sys.stdout.write("\n")


def _snapshot(store: Store, snapshot_id: str | None):
    value = store.get_snapshot(snapshot_id) if snapshot_id else store.latest()
    if value is None:
        raise ValueError("没有可用快照，请先 scan 或指定已存在的 --snapshot")
    return value


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="callscope", description="纯静态源码结构与合同分析；不运行目标代码、测试或构建")
    parser.add_argument("--version", action="version", version=__version__)
    commands = parser.add_subparsers(dest="command", required=True)
    storage = argparse.ArgumentParser(add_help=False)
    storage.add_argument("--db", default=".callscope/callscope.sqlite3", help="快照数据库（默认当前目录下 .callscope/）")
    project = argparse.ArgumentParser(add_help=False, parents=[storage])
    project.add_argument("root", help="只读分析的项目目录")
    project.add_argument("--config", help="静态约束 JSON；默认 ROOT/.callscope.json")
    project.add_argument("--engine", choices=["auto", "full", "cocoindex"], default="auto",
                         help="auto 使用可用的 CocoIndex 工具依赖；full 禁用前端缓存，检测始终全量")

    scan = commands.add_parser("scan", parents=[project], help="静态构图、全量检测并原子发布快照")
    scan.add_argument("--json", action="store_true", help="输出机器可读快照及发现")
    scan.add_argument("--output", help="把完整 JSON 报告写入指定文件")
    serve = commands.add_parser("serve", parents=[project], help="启动本地探索界面")
    serve.add_argument("--host", choices=["127.0.0.1", "localhost"], default="127.0.0.1")
    serve.add_argument("--port", type=int, default=8787)
    serve.add_argument("--watch", action="store_true", help="后台周期读取源码，变化产生新快照")
    serve.add_argument("--interval", type=float, default=2.0)
    commands.add_parser("mcp", parents=[project], help="以 stdio JSON-RPC 提供静态分析 MCP 工具")

    path = commands.add_parser("path", parents=[storage], help="查询一条已解析的最短静态调用路径")
    path.add_argument("source", metavar="FROM")
    path.add_argument("target", metavar="TO")
    path.add_argument("--snapshot")
    diff = commands.add_parser("diff", parents=[storage], help="比较两个不可变快照")
    diff.add_argument("old", metavar="OLD")
    diff.add_argument("new", metavar="NEW")
    versions = commands.add_parser("versions", parents=[storage], help="列出已发布快照")
    versions.add_argument("--project-id")
    anomalies = commands.add_parser("anomalies", parents=[storage], help="读取静态发现，不执行项目")
    anomalies.add_argument("--snapshot")
    anomalies.add_argument("--severity", choices=["high", "medium", "low", "info"])
    anomalies.add_argument("--type")
    anomalies.add_argument("--json", action="store_true")
    report = commands.add_parser("report", parents=[storage], help="从保存源码和分析证据生成项目报告，不执行目标")
    report.add_argument("--snapshot")
    report.add_argument("--format", choices=["json","markdown"], default="markdown")
    report.add_argument("--output")
    baseline = commands.add_parser("baseline", parents=[storage], help="对照冻结源码观察，列出已重现关系与能力缺口")
    baseline.add_argument("baseline_file", help="Astra 或人工审查形成的数据基准 JSON")
    baseline.add_argument("--snapshot", help="当前快照；默认最新发布快照")
    baseline.add_argument("--repo-id", help="基准中的仓库 ID；省略时按快照项目根匹配")
    baseline.add_argument("--compare-snapshot", help="同项目旧快照，用同一冻结基准比较能力变化")
    baseline.add_argument("--compare-db", help="旧快照所在数据库；省略时使用 --db，不改写旧快照")
    baseline.add_argument("--output", help="将对照 JSON 原子写入指定文件")
    decide = commands.add_parser("decide", parents=[storage], help="追加人工处置，不改写检测事实")
    decide.add_argument("finding_id", metavar="FINDING_ID")
    decide.add_argument("--snapshot", required=True)
    decide.add_argument("--action", required=True, choices=["accept_risk", "false_positive", "fix_planned"])
    decide.add_argument("--reason", required=True)
    decide.add_argument("--expires-at")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    service = None
    store = None
    try:
        if args.command in {"scan", "serve", "mcp"}:
            service = AnalysisService(args.root, args.db, args.config, engine=args.engine)
            if args.command == "scan":
                summary = service.scan()
                snapshot = service.snapshot(summary["snapshot_id"])
                findings = service.findings(snapshot.id)["items"]
                if args.json or args.output:
                    _dump({"snapshot": asdict(snapshot), "findings": findings, "publication": summary}, args.output)
                else:
                    print(f"快照 {snapshot.id} · {snapshot.project_name} · {snapshot.status}")
                    print(f"{len(snapshot.files)} 文件 / {len(snapshot.nodes)} 节点 / {len(snapshot.edges)} 调用 / {len(findings)} 发现")
                    for item in findings:
                        print(f"[{item['severity']}/{item['status']}] {item['title']}  ({item['id']})")
                    print("结果来自纯静态源码与声明模型；未执行目标代码、测试或构建。")
            elif args.command == "serve":
                if not 1 <= args.port <= 65535:
                    raise ValueError("port 必须为 1 到 65535")
                try:
                    service.scan()
                except Exception as exc:
                    print(f"初始分析失败（界面仍可查看状态与修改配置）: {exc}", file=sys.stderr)
                if args.watch:
                    service.start_watch(args.interval)
                from .server import serve
                serve(service, args.host, args.port)
            else:
                from .mcp import run_stdio
                run_stdio(service)
        else:
            store = Store(args.db)
            if args.command == "path":
                snapshot = _snapshot(store, args.snapshot)
                _dump(find_path(snapshot, args.source, args.target))
            elif args.command == "diff":
                old, new = _snapshot(store, args.old), _snapshot(store, args.new)
                _dump(diff_snapshots(old, new, store.get_findings(old.id), store.get_findings(new.id)))
            elif args.command == "versions":
                _dump({"items": store.list_snapshots(args.project_id)})
            elif args.command == "report":
                from .project_report import build_project_report,render_markdown
                snapshot = _snapshot(store,args.snapshot)
                report = build_project_report(snapshot,store.get_findings(snapshot.id))
                if args.format=="json":
                    _dump(report,args.output)
                else:
                    rendered = render_markdown(report)
                    if args.output:
                        path=Path(args.output)
                        path.parent.mkdir(parents=True,exist_ok=True)
                        path.write_text(rendered,encoding="utf-8")
                    else:
                        sys.stdout.write(rendered)
            elif args.command == "anomalies":
                snapshot = _snapshot(store, args.snapshot)
                findings = [asdict(f) for f in store.get_findings(snapshot.id)
                            if (not args.severity or f.severity == args.severity) and (not args.type or f.type == args.type)]
                if args.json:
                    _dump({"snapshot_id": snapshot.id, "items": findings})
                else:
                    print(f"快照 {snapshot.id} · {len(findings)} 条静态发现")
                    for item in findings:
                        print(f"[{item['severity']}/{item['status']}] {item['title']} ({item['id']})")
            elif args.command == "baseline":
                from .baseline import evaluate_baseline, load_baseline
                baseline = load_baseline(args.baseline_file)
                snapshot = _snapshot(store, args.snapshot)
                current = evaluate_baseline(snapshot, baseline, args.repo_id)
                result = {"current": current}
                if args.compare_snapshot or args.compare_db:
                    previous_store = Store(args.compare_db) if args.compare_db else store
                    try:
                        previous_snapshot = _snapshot(previous_store, args.compare_snapshot)
                    finally:
                        if previous_store is not store:
                            previous_store.close()
                    if previous_snapshot.project_id != snapshot.project_id:
                        raise ValueError("基准能力对比必须使用同一项目的两个快照")
                    previous = evaluate_baseline(previous_snapshot, baseline, args.repo_id)
                    before = {item["id"]: item for item in previous["observations"]}
                    changes = [{"id": item["id"], "before": before[item["id"]]["status"],
                                "after": item["status"],
                                "before_expectation_satisfied": before[item["id"]].get("expectation_satisfied"),
                                "after_expectation_satisfied": item.get("expectation_satisfied")}
                               for item in current["observations"]
                               if item["status"] != before[item["id"]]["status"] or
                               item.get("expectation_satisfied") != before[item["id"]].get("expectation_satisfied")]
                    result.update(previous=previous, changes=changes,
                                  interpretation="仅比较冻结源码观察的静态重现能力，不表示项目功能通过率。")
                _dump(result, args.output)
            elif args.command == "decide":
                _dump({"decision": store.record_decision(args.snapshot, args.finding_id, args.action,
                                                         args.reason, expires_at=args.expires_at)})
        # Structural findings intentionally do not set a failing process status.
        return 0
    except (ValueError, KeyError, OSError, RuntimeError, sqlite3.Error) as exc:
        print(f"callscope: {exc}", file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        return 130
    finally:
        if service:
            service.close()
        if store:
            store.close()

