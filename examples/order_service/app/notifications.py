"""通过模块引用形成调用环，避免在导入时读取未定义函数。"""

import app.domain as domain


def retry_notification(order_id: str, remaining: int) -> None:
    if remaining <= 0:
        return
    domain.refresh_order(order_id, remaining - 1)
