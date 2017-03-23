# -*- coding: utf-8 -*-
"""User forms."""
from wtforms.widgets import TextInput
from flask_wtf import Form
from wtforms import PasswordField, StringField
from wtforms.validators import DataRequired, Length

from .models import Board


class AngularJSTextInput(TextInput):
    def __call__(self, field, **kwargs):
        for key in list(kwargs):
            if key.startswith('ng_'):
                kwargs['ng-' + key[3:]] = kwargs.pop(key)
        return super(AngularJSTextInput, self).__call__(field, **kwargs)


class NewBoardForm(Form):
    """Register form."""

    name = StringField('Nom Carte',
                           validators=[DataRequired(), Length(min=3, max=25)],widget=AngularJSTextInput())

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(NewBoardForm, self).__init__(*args, **kwargs)
        self.board = None

    def validate(self):
        """Validate the form."""
        initial_validation = super(NewBoardForm, self).validate()
        if not initial_validation:
            return False
        #board = Board.query.filter_by(name=self.name.data).first()
        #if board:
        #    self.name.errors.append('Nom de carte deja utilise')
        #    return False
        return True
