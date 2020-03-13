from dateutil import parser
from graphql_relay.node.node import from_global_id

from .utils import is_date


class UpdateAttributesMixin:
    def update(self, exclude=(), **args):
        for field_name in args:
            if field_name not in exclude:
                if is_date(args[field_name]):
                    try:
                        setattr(self, field_name,
                                parser.parse(args[field_name]))
                    except AttributeError:
                        pass
                else:
                    try:
                        # assume the field is complex data type and
                        # try to get it's id attribute

                        if type(args[field_name]) is not bool:
                            field = None

                            if args[field_name]:
                                field = from_global_id(args[field_name].id)[1]
                                setattr(self, "{}_id".format(
                                    field_name), field)
                            else:
                                setattr(self, field_name, field)

                        else:
                            raise AttributeError
                    except AttributeError:
                        try:
                            # assume the field is global relay id and
                            # try convert it to Django model id
                            field = from_global_id(args[field_name])[1]
                            setattr(self, field_name, field)
                        except Exception:
                            try:
                                setattr(self, field_name, args[field_name])
                            except AttributeError:
                                pass
                    except Exception:
                        # if it is still complex data type but it's id
                        # attribute is not a relay global id
                        field = None

                        if args[field_name]:
                            field = args[field_name].id

                        setattr(self, "{}_id".format(
                            field_name), field)

        self.save()
