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
                           validators=[DataRequired(message="Le nom de la carte est obligatoire"), Length(min=3, max=25, message="Le nom de carte doit contenir entre 3 et 25 caractères")],widget=AngularJSTextInput())
    chip_id = StringField('Numero Série Carte',
                       validators=[DataRequired(message="Le numéro de série de la carte est obligatoire"), Length(min=3, max=25, message="Le numéro de série de la carte doit contenir entre 3 et 25 caractères")], widget=AngularJSTextInput())

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(NewBoardForm, self).__init__(*args, **kwargs)
        self.board = None

    def validate(self):
        """Validate the form."""
        initial_validation = super(NewBoardForm, self).validate()
        if not initial_validation:
            return False
        board = Board.query.filter_by(chip_id=self.chip_id.data).first()
        if board:
            self.chip_id.errors.append('Numéro de série deja utilise')
            return False
        return True
