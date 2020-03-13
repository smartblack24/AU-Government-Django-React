from functools import wraps


def login_required(method):
    @wraps(method)
    def _impl(self, *method_args, **method_kwargs):
        info = method_args[-1]

        if info.context:
            if info.context.user.is_authenticated:
                return method(self, *method_args, **method_kwargs)
            else:
                return method_args[0].context.error

        return method(self, *method_args, **method_kwargs)

    return _impl


def login_required_node(method):
    @wraps(method)
    def _impl(cls, *args, **method_kwargs):
        info = args[0]
        id = args[1]
        if info.context.user.is_authenticated:
            return method(cls, id=id, context=info.context, info=info, **method_kwargs)
        else:
            raise info.context.error

    return _impl


def login_required_relay(method):
    @wraps(method)
    def _impl(cls, *args, **method_kwargs):
        info = args[-1]
        if info.context.user.is_authenticated:
            return method(cls, context=info.context, *args, **method_kwargs)
        else:
            raise info.context.error

    return _impl
