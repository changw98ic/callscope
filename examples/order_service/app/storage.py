"""简单存储入口，仅供静态读取。"""

_orders: dict[str, dict[str, object]] = {}


def write_order(order_id: str, payload: dict[str, object]) -> str:
    _orders[order_id] = payload
    return order_id


def read_order(order_id: str) -> dict[str, object]:
    return _orders[order_id]
