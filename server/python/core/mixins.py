from sitename.decorators import login_required_node


class LoginRequiredRelayMixin:
    @classmethod
    @login_required_node
    def get_node(cls, id, context, info):
        try:
            return cls._meta.model.objects.get(id=id)
        except cls._meta.model.DoesNotExist:
            return None
