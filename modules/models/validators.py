from wtforms import ValidationError


class Unique:
    def __init__(self, model_class, message):
        self.model_class = model_class
        self.message = message

    def __call__(self, form, field):

        check = self.model_class.query.filter(self.model_class.email == field.data).first()
        if 'id' in form:
            model_id = form.id.data
        else:
            model_id = None
        if check and (model_id is None or model_id != check.id):
            raise ValidationError(self.message)


class GreaterThan:
    def __init__(self, field_name, message):
        self.field_name = field_name
        self.message = message

    def __call__(self, form, field):

        if field.data < form[self.field_name].data:
            raise ValidationError(self.message)
