from sqlalchemy import types


class ChoiceType(types.TypeDecorator):
    """General custom type used as an enum."""

    impl = types.String

    def __init__(self, constant, **kwargs):

        constant_dict = dict((attr, getattr(constant, attr)) for attr in \
            dir(constant) if not attr.startswith('__'))

        self.choices = constant_dict
        super().__init__(**kwargs)

    def process_bind_param(self, value, dialect):
        try:
            return [v for v in self.choices.values() if v == value][0]
        except:
            return None

    def process_result_value(self, value, dialect):
        try:
            return [v for v in self.choices.values() if v == value][0]
        except:
            return None
