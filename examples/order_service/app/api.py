"""入口与配置中的调用结构约束配套；本文件不会被分析器执行。"""

from app.domain import save_order
from app.storage import read_order


def submit_order(order_id: str, payload: dict[str, object]) -> str:
    """示例缺口：validate_order 已存在，入口没有连接到它。"""
    return save_order(order_id, payload)


def fetch_order(order_id: str) -> dict[str, object]:
    """示例缺口：绕过 get_order，直接调用了配置禁止的存储入口。"""
    return read_order(order_id)
