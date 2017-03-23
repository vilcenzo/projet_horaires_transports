# -*- coding: utf-8 -*-
"""User forms."""
from flask_wtf import Form
from wtforms import PasswordField, StringField
from wtforms.validators import DataRequired, Length


class NewScreenForm(Form):
    """Register form."""

    gare_depart = StringField('Gare de Depart',
                           validators=[DataRequired(), Length(min=3, max=25)])

    gare_arrive = StringField('Gare d\'Arrive',
                              validators=[DataRequired(), Length(min=3, max=25)])

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(NewScreenForm, self).__init__(*args, **kwargs)
        self.board = None

    def validate(self):
        """Validate the form."""
        initial_validation = super(NewScreenForm, self).validate()
        if not initial_validation:
            return False
        return True
