"""Small stdio MCP server exposing only static exploration capabilities."""

from dataclasses import asdict
import json
import math
import sys
from typing import Any

from . import __version__
from .service import AnalysisService


def _schema(properties: dict[str, Any], required: list[str] | None = None) -> dict[str, Any]:
    return {"type": "object", "properties": properties, "required": required or [], "additionalProperties": False}


TEXT = {"type": "string"}
TOOLS = [
    {"name": "scan_project", "description": "只读源码进行静态扫描，发布不可变调用图；不运行代码、测试或构建。", "inputSchema": _schema({})},
    {"name": "query_graph", "description": "读取固定快照调用图，或查询节点周边；深度限制只用于展示。", "inputSchema": _schema({"snapshot_id": TEXT, "node_id": TEXT, "depth": {"type": "integer", "minimum": 0, "maximum": 8}, "direction": {"type": "string", "enum": ["both", "in", "out"]}})},
    {"name": "get_anomalies", "description": "读取静态约束违反、结构发现与不确定项；不宣称功能正确。", "inputSchema": _schema({"snapshot_id": TEXT, "severity": TEXT, "type": TEXT, "q": TEXT})},
    {"name": "get_project_report", "description": "从保存的图和分析证据生成项目报告，区分完整判断、局部证据、结构与未审范围。", "inputSchema": _schema({"snapshot_id": TEXT})},
    {"name": "get_evidence", "description": "读取发现的静态证据或快照内源码；不能读取任意当前文件。", "inputSchema": _schema({"snapshot_id": TEXT, "finding_id": TEXT, "file": TEXT, "line": {"type": "integer"}})},
    {"name": "find_call_path", "description": "查询一条最短已解析调用路径，区分 found/not_found/unknown。", "inputSchema": _schema({"snapshot_id": TEXT, "from": TEXT, "to": TEXT}, ["from", "to"])},
    {"name": "list_versions", "description": "列出当前项目不可变静态分析快照。", "inputSchema": _schema({})},
    {"name": "compare_snapshots", "description": "比较调用结构及发现变化，同时标记分析配置和检测器可比性。", "inputSchema": _schema({"from_snapshot": TEXT, "to_snapshot": TEXT}, ["from_snapshot", "to_snapshot"])},
]


def _required(args: dict[str, Any], name: str) -> str:
    value = args.get(name)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} 必须为非空字符串")
    return value


def _call(service: AnalysisService, name: str, args: dict[str, Any]) -> Any:
    tool = next((item for item in TOOLS if item["name"] == name), None)
    if tool is None:
        raise ValueError(f"未知工具: {name}")
    schema = tool["inputSchema"]
    if set(args) - set(schema["properties"]):
        raise ValueError("参数包含未声明字段")
    for required in schema["required"]:
        _required(args, required)
    for key, value in args.items():
        prop = schema["properties"][key]
        if prop["type"] == "string" and not isinstance(value, str):
            raise ValueError(f"{key} 必须为字符串")
        if prop["type"] == "integer" and (isinstance(value, bool) or not isinstance(value, int)):
            raise ValueError(f"{key} 必须为整数")
        if "enum" in prop and value not in prop["enum"]:
            raise ValueError(f"{key} 值不受支持")
    sid = args.get("snapshot_id")
    if name == "scan_project":
        return service.scan()
    if name == "query_graph":
        if args.get("node_id"):
            return service.subgraph(args["node_id"], sid, args.get("depth", 2), args.get("direction", "both"))
        return service.graph(sid)
    if name == "get_anomalies":
        return service.findings(sid, severity=args.get("severity", ""), kind=args.get("type", ""), query=args.get("q", ""))
    if name == "get_project_report":
        return service.project_report(sid)
    if name == "get_evidence":
        if args.get("finding_id"):
            return service.finding(args["finding_id"], sid)
        return service.source(_required(args, "file"), sid, args.get("line", 1))
    if name == "find_call_path":
        return service.path(args["from"], args["to"], sid)
    if name == "list_versions":
        return service.versions()
    return service.diff(args["from_snapshot"], args["to_snapshot"])


def _reply(request_id: Any, *, result: Any = None, error: dict[str, Any] | None = None) -> None:
    response: dict[str, Any] = {"jsonrpc": "2.0", "id": request_id}
    response["error" if error is not None else "result"] = error if error is not None else result
    sys.stdout.write(json.dumps(response, ensure_ascii=False, separators=(",", ":"), allow_nan=False) + "\n")
    sys.stdout.flush()


def run_stdio(service: AnalysisService) -> None:
    # Newline-delimited JSON-RPC; stdout contains protocol messages only.
    while True:
        line = sys.stdin.buffer.readline(1048577)
        if not line:
            break
        if len(line) > 1048576:
            if not line.endswith(b"\n"):
                while True:
                    remainder = sys.stdin.buffer.readline(1048577)
                    if not remainder or remainder.endswith(b"\n"):
                        break
            _reply(None, error={"code": -32700, "message": "消息超过 1 MiB"})
            continue
        try:
            request = json.loads(line)
        except (ValueError, UnicodeError):
            _reply(None, error={"code": -32700, "message": "无效 JSON-RPC 消息"})
            continue
        if not isinstance(request, dict) or request.get("jsonrpc") != "2.0" or not isinstance(request.get("method"), str):
            _reply(None, error={"code": -32600, "message": "必须为具有 method 的 JSON-RPC 2.0 对象"})
            continue
        if "id" in request:
            ident = request["id"]
            valid_id = ident is None or isinstance(ident, str) or type(ident) is int or (type(ident) is float and math.isfinite(ident))
            if not valid_id:
                _reply(None, error={"code": -32600, "message": "id 必须为字符串、有限数值或 null"})
                continue
        if "id" not in request:
            continue
        request_id = request["id"]
        method = request.get("method")
        params = request.get("params", {})
        if not isinstance(params, dict):
            _reply(request_id, error={"code": -32602, "message": "params 必须为对象"})
            continue
        if method == "initialize":
            supported = {"2024-11-05", "2025-03-26", "2025-06-18"}
            requested = params.get("protocolVersion")
            if not isinstance(requested, str):
                _reply(request_id, error={"code": -32602, "message": "protocolVersion 必须为字符串"})
                continue
            protocol = requested if requested in supported else "2025-06-18"
            _reply(request_id, result={"protocolVersion": protocol, "capabilities": {"tools": {"listChanged": False}},
                                       "serverInfo": {"name": "callscope", "version": __version__},
                                       "instructions": "仅静态调用分析；scan_project 后查询固定快照。无执行、测试或修复工具。"})
        elif method == "ping":
            _reply(request_id, result={})
        elif method == "tools/list":
            _reply(request_id, result={"tools": TOOLS})
        elif method == "tools/call":
            try:
                arguments = params.get("arguments", {})
                if not isinstance(arguments, dict):
                    raise ValueError("arguments 必须为对象")
                value = _call(service, _required(params, "name"), arguments)
                _reply(request_id, result={"content": [{"type": "text", "text": json.dumps(value, ensure_ascii=False, allow_nan=False)}], "isError": False})
            except Exception as exc:
                _reply(request_id, result={"content": [{"type": "text", "text": str(exc)}], "isError": True})
        else:
            _reply(request_id, error={"code": -32601, "message": f"不支持的方法: {method}"})
