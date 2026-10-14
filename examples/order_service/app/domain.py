"""领域函数；这里只演示调用关系，不向分析器声明业务正确性。"""

from app.notifications import retry_notification
from app.storage import read_order, write_order


def validate_order(payload: dict[str, object]) -> bool:
    """存在实现不意味着调用链已经接入，也不证明其业务逻辑正确。"""
    return "items" in payload


def save_order(order_id: str, payload: dict[str, object]) -> str:
    return write_order(order_id, payload)


def get_order(order_id: str) -> dict[str, object]:
    return read_order(order_id)


def refresh_order(order_id: str, remaining: int) -> None:
    """与 retry_notification 组成调用环；含计数条件，环本身不是不终止证据。"""
    if remaining <= 0:
        return
    retry_notification(order_id, remaining - 1)
