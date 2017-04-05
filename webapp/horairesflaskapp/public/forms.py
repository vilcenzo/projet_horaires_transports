# -*- coding: utf-8 -*-
"""Public forms."""
from flask_wtf import Form
from wtforms import PasswordField, StringField
from wtforms.validators import DataRequired

from horairesflaskapp.user.models import User


class LoginForm(Form):
    """Login form."""

    username = StringField('Nom d\'utilisateur', validators=[DataRequired()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(LoginForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        """Validate the form."""
        initial_validation = super(LoginForm, self).validate()
        if not initial_validation:
            return False

        self.user = User.query.filter_by(username=self.username.data).first()
        if not self.user:
            self.username.errors.append('Utilisateur inconnu')
            return False

        if not self.user.check_password(self.password.data):
            self.password.errors.append('Mot de passe invalide')
            return False

        if not self.user.active:
            self.username.errors.append('Utilisateur non activé')
            return False
        return True
