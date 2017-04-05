# -*- coding: utf-8 -*-
"""User forms."""
from flask_wtf import Form
from wtforms import PasswordField, StringField, SelectField, ValidationError
from wtforms.validators import DataRequired, Length
from wtforms.widgets import TextInput

from horairesflaskapp.stations_transilien.models import StationTransilien

class AngularJSTextInput(TextInput):
    def __call__(self, field, **kwargs):
        for key in list(kwargs):
            if key.startswith('ng_'):
                kwargs['ng-' + key[3:]] = kwargs.pop(key)
        return super(AngularJSTextInput, self).__call__(field, **kwargs)


def stations_transilien():
    return StationTransilien.query


class NewScreenForm(Form):
    """Register form."""

    titre_affichage = StringField('Titre Affichage',
                                  validators=[DataRequired(message="Titre affichage doit être renseigné"),
                                              Length(min=1, max=18, message="Titre affichage doit contenir entre 1 et 18 lettres")],
                                  widget=AngularJSTextInput(), render_kw={'maxlength': 18})

    gare_depart = SelectField('Gare de Depart', choices=[('', u'Gare de départ')])
    gare_arrive = SelectField('Gare d\'Arrive', choices=[('', u'Gare d\'arrivée')])

    type_transport = SelectField('Type de Transport', choices=[('', 'Type de ligne'), ('SNCF', 'SNCF'), ('RATP', 'RATP')])

    board_id = StringField('board id')

    @staticmethod
    def validate_type_transport(form, field):
        if field.data == '':
            raise ValidationError('Veuillez selectionner un mode de transport')

    @staticmethod
    def validate_gare_depart(form, field):
        if field.data == '':
            raise ValidationError('Veuillez selectionner une gare de depart')

    @staticmethod
    def validate_gare_arrive(form, field):
        if field.data == '':
            raise ValidationError('Veuillez selectionner une gare d\'arrivée')


    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(NewScreenForm, self).__init__(*args, **kwargs)
        self.gare_depart.choices.extend([(str(s.uic), s.name) for s in StationTransilien.query.order_by(StationTransilien.name).all()])
        self.gare_arrive.choices.extend([(str(s.uic), s.name) for s in StationTransilien.query.order_by(StationTransilien.name).all()])

        self.board = None

    def validate(self):
        """Validate the form."""
        initial_validation = super(NewScreenForm, self).validate()
        if not initial_validation:
            return False
        return True
