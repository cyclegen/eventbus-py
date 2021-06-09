# eventbus-py
EventBus的Python实现

## Example

- 调用规范 
  由于设计时考虑到可能会存在多个实例的情况，故使用ContextVar来包装EventBus实例方便使用者调用。
  ```python
  from eventbus import bus, Subscribe
  class Example:
    pass
  class A:
    def __init__(self):
      bus.get().register(a)
  
    @Subscribe(priority=100, sticky=True)
    def on_example(self, event: Example):
        bus.get().cancel_delivery(event)
        bus.get().unregister(a)
    
  a = A()
  bus.get().post(a)
  ```
