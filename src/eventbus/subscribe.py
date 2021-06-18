import inspect

subscribe_annotation_property = '__subscribe_annotation__'


class SubscribeAnnotation:

    def __init__(self, priority=0, sticky=False):
        self._priority = priority
        self._sticky = sticky

    @property
    def priority(self):
        return self._priority

    @property
    def sticky(self):
        return self._sticky


class Subscribe:
    """订阅装饰器，给被订阅的方法添加元信息

    订阅装饰器将会为方法添加方法元信息，用来在EventBus对类进行注册时使用。
    注意，为了降低可能产生Bug的情况，这里限制仅允许为类方法进行装饰，但并
    非不能对其他可调用类进行装饰。

    :arg priority 优先级，该方法在同一队列内处理事件的优先级
    :arg sticky 粘滞事件处理标志，在该方法被初始化时是否处理对应事件的粘滞事件
    """

    def __init__(self, priority: int = 100, sticky: bool = False):
        self.priority: int = priority
        self.sticky: bool = sticky

    def __call__(self, callable):
        """调用Subscribe装饰器对可调用对象的修改

        该方法将限制被装饰对象为类方法，由于装饰时均不以对象绑定类方法的形式进行调用，故在装饰时需要进行特殊判断。
        :param callable: 被装饰类方法
        :return:
        """
        self._check_method_valid(callable)
        setattr(callable, subscribe_annotation_property, SubscribeAnnotation(priority=self.priority, sticky=self.sticky))
        return callable

    @staticmethod
    def _check_method_valid(callable):
        # 判断方法签名是否为Class.Method(self, event: EventType)
        # 注意此处不检查classmethod/staticmethod/instancemethod,正确使用时应使用instancemethod
        qualname_splited = callable.__qualname__.split('.')
        arg_spec = inspect.getfullargspec(callable)
        if len(qualname_splited) != 2:
            raise Exception(f'当前方法{callable.__qualname__}不是类方法')
        if (len(arg_spec.args) != 2 or arg_spec.varargs is not None
                or arg_spec.varkw is not None or arg_spec.defaults is not None
                or len(arg_spec.kwonlyargs) != 0 or arg_spec.kwonlydefaults is not None
                or arg_spec.annotations.get(arg_spec.args[1]) is None):
            raise Exception(f'请检查订阅方法，当前方法{callable.__qualname__}应为Class.Method(self, event: EventType)形式')