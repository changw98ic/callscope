"""动态回调示例：参数的具体调用目标不从源码猜测。"""

from typing import Callable


def dispatch_hook(callback: Callable[[str], None], order_id: str) -> None:
    callback(order_id)
