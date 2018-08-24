class MetaFlyweight(type):
    def __init__(cls, name, bases, dct):
        super().__init__(name, bases, dct)
        cls._instances = dict()
        cls.__new__ = MetaFlyweight._get_instance

    def _get_instance(cls, *args, **kwargs):
        return cls._instances.setdefault(
            (args, tuple(kwargs.items())), object.__new__(cls))
