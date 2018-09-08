class MetaFlyweight(type):
    def __init__(cls, name, bases, dct):
        super().__init__(name, bases, dct)
        cls._instances = dict()
        cls.__new__ = MetaFlyweight._get_instance
        cls._init = cls.__init__
        cls.__init__ = lambda *args: None

    def _get_instance(cls, *args, **kwargs):
        key = (args, tuple(kwargs.items()))
        if key in cls._instances:
            return cls._instances[key]
        else:
            obj = object.__new__(cls)
            cls._init(obj, *args, **kwargs)
            cls._instances[key] = obj
            return obj
        # return cls._instances.setdefault(
        #     (args, tuple(kwargs.items())), object.__new__(cls))
