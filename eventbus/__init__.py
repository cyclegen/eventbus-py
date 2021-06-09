from .subscribe import Subscribe
from contextvars import ContextVar
from .eventbus import EventBus
bus: ContextVar[EventBus] = ContextVar('bus', default=EventBus())
