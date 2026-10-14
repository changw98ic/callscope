"""Local HTTP exploration API. There are deliberately no execution endpoints."""

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import sys
from typing import Any
from urllib.parse import parse_qs, unquote, urlparse

from .service import AnalysisService, ScanBusyError

MAX_BODY_BYTES = 1048576


def _assets_dir() -> Path:
    for path in (Path(__file__).resolve().parent.parent / "web", Path(sys.prefix) / "share" / "callscope" / "web"):
        if (path / "index.html").is_file():
            return path
    raise FileNotFoundError("找不到 web 资源，请从完整项目目录运行")


class CallScopeServer(ThreadingHTTPServer):
    daemon_threads = True

    def __init__(self, address: tuple[str, int], service: AnalysisService):
        self.service = service
        self.assets = _assets_dir()
        super().__init__(address, CallScopeHandler)


class CallScopeHandler(BaseHTTPRequestHandler):
    server: CallScopeServer

    def log_message(self, format: str, *args: Any) -> None:
        sys.stderr.write(f"[callscope] {self.log_date_time_string()} {format % args}\n")

    def _json(self, value: Any, status: int = 200) -> None:
        body = json.dumps(value, ensure_ascii=False, allow_nan=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(body)

    def _error(self, code: str, message: str, status: int = 400) -> None:
        self._json({"error": {"code": code, "message": message}}, status)

    def _request(self) -> tuple[str, dict[str, str]]:
        parsed = urlparse(self.path)
        return unquote(parsed.path), {key: values[-1] for key, values in parse_qs(parsed.query).items()}

    def _local_host(self) -> bool:
        host = self.headers.get("Host", "")
        try:
            parsed = urlparse("http://" + host)
            valid = parsed.hostname in {"localhost", "127.0.0.1"} and (parsed.port or 80) == self.server.server_port
        except ValueError:
            valid = False
        if not valid:
            self._error("INVALID_HOST", "本地服务仅接受 localhost/127.0.0.1 与实际监听端口", 403)
        return valid

    def do_GET(self) -> None:
        if not self._local_host():
            return
        path, query = self._request()
        service = self.server.service
        snapshot_id = query.get("snapshot_id") or None
        try:
            if path == "/api/v1/status":
                result = service.status()
            elif path == "/api/v1/report":
                result = service.project_report(snapshot_id)
            elif path == "/api/v1/versions":
                result = service.versions()
            elif path == "/api/v1/graph":
                result = service.graph(snapshot_id)
            elif path == "/api/v1/anomalies":
                result = service.findings(snapshot_id, severity=query.get("severity", ""),
                                          kind=query.get("type", ""), query=query.get("q", ""))
            elif path.startswith("/api/v1/anomalies/"):
                result = service.finding(path.removeprefix("/api/v1/anomalies/"), snapshot_id)
            elif path == "/api/v1/evidence/source":
                result = service.source(query.get("file", ""), snapshot_id, int(query.get("line", "1")))
            elif path == "/api/v1/config":
                result = service.config_info()
            elif path == "/api/v1/decisions":
                result = service.decisions(snapshot_id, query.get("finding_id"))
            elif path == "/api/v1/audit":
                result = service.store.verify_audit_chain()
            elif path in {"/", "/index.html", "/app.js", "/styles.css"}:
                self._static("index.html" if path == "/" else path[1:])
                return
            else:
                self._error("NOT_FOUND", "端点不存在", 404)
                return
            self._json(result)
        except KeyError as exc:
            self._error("NOT_FOUND", str(exc.args[0]), 404)
        except (ValueError, TypeError, OSError) as exc:
            self._error("INVALID_REQUEST", str(exc))
        except Exception as exc:
            self.log_error("Internal error: %s", exc)
            self._error("INTERNAL_ERROR", "服务错误；最后发布的快照仍保留", 500)

    def do_POST(self) -> None:
        if not self._local_host():
            return
        origin = self.headers.get("Origin")
        if origin:
            try:
                actual = urlparse(origin)
                expected = urlparse("http://" + self.headers.get("Host", ""))
                same_origin = actual.scheme == "http" and actual.hostname == expected.hostname and (actual.port or 80) == (expected.port or 80)
            except ValueError:
                same_origin = False
            if not same_origin:
                self._error("CROSS_ORIGIN_DENIED", "写入接口仅接受同源请求", 403)
                return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length < 0 or length > MAX_BODY_BYTES:
                self._error("BODY_TOO_LARGE", "请求体不能超过 1 MiB", 413)
                return
            if length and self.headers.get("Content-Type", "").split(";", 1)[0].strip() != "application/json":
                self._error("JSON_REQUIRED", "请求体必须为 application/json", 415)
                return
            data = json.loads(self.rfile.read(length).decode("utf-8")) if length else {}
            if not isinstance(data, dict):
                raise ValueError("请求体必须为 JSON 对象")
            path, _ = self._request()
            service = self.server.service
            if path == "/api/v1/scan":
                result = service.scan()
            elif path == "/api/v1/config":
                result = service.update_config(data.get("config"))
            elif path == "/api/v1/query/path":
                result = service.path(_text(data, "from"), _text(data, "to"), data.get("snapshot_id"))
            elif path == "/api/v1/graph/subgraph":
                result = service.subgraph(_text(data, "node_id"), data.get("snapshot_id"),
                                          data.get("depth", 2), data.get("direction", "both"))
            elif path == "/api/v1/diff":
                result = service.diff(_text(data, "from_snapshot"), _text(data, "to_snapshot"))
            elif path == "/api/v1/decisions":
                result = service.decide(_text(data, "snapshot_id"), _text(data, "finding_id"),
                                        _text(data, "action"), _text(data, "reason"), data.get("expires_at"))
            else:
                self._error("NOT_FOUND", "端点不存在；不提供测试、构建或执行接口", 404)
                return
            self._json(result)
        except ScanBusyError as exc:
            self._error("SCAN_BUSY", str(exc), 409)
        except KeyError as exc:
            self._error("NOT_FOUND", str(exc.args[0]), 404)
        except (ValueError, TypeError, UnicodeError, OSError) as exc:
            self._error("INVALID_REQUEST", str(exc))
        except Exception as exc:
            self.log_error("Internal error: %s", exc)
            self._error("INTERNAL_ERROR", "处理失败；查看服务日志和分析状态", 500)

    def _static(self, name: str) -> None:
        path = self.server.assets / name
        if not path.is_file():
            self._error("NOT_FOUND", "资源不存在", 404)
            return
        body = path.read_bytes()
        mime = {".html": "text/html", ".js": "text/javascript", ".css": "text/css"}[path.suffix]
        self.send_response(200)
        self.send_header("Content-Type", mime + "; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Content-Security-Policy", "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; connect-src 'self'; frame-ancestors 'none'")
        self.end_headers()
        self.wfile.write(body)


def _text(data: dict[str, Any], key: str) -> str:
    value = data.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{key} 必须为非空字符串")
    return value


def serve(service: AnalysisService, host: str = "127.0.0.1", port: int = 8787) -> None:
    if host not in {"127.0.0.1", "localhost"}:
        raise ValueError("首版是本地单用户工具；host 必须为 127.0.0.1 或 localhost")
    server = CallScopeServer((host, port), service)
    print(f"CallScope: http://127.0.0.1:{server.server_port} · 纯静态调用分析", file=sys.stderr)
    try:
        server.serve_forever(poll_interval=0.5)
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
