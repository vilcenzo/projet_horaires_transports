from flask import Blueprint, render_template, request, flash, redirect, url_for,jsonify
from flask_login import login_required, current_user
from horairesflaskapp.board.forms import NewBoardForm
from horairesflaskapp.screen.models import Screen
from horairesflaskapp.utils import flash_errors
from horairesflaskapp.screen.forms import NewScreenForm


blueprint = Blueprint('screen', __name__, url_prefix='/screens', static_folder='../static')


@blueprint.route('/', methods=['POST','DELETE'])
@login_required
def screen():
    form = NewScreenForm(request.form)
    if request.method == 'POST':

        if form.validate():
            try:

                print(form.titre_affichage.data)

                screen = Screen.create(board_id=form.board_id.data, gare_depart=int(form.gare_depart.data),
                                       gare_arrive=int(form.gare_arrive.data), titre_affichage=form.titre_affichage.data,
                                       type_transport=form.type_transport.data)


            except Exception as e:
                return jsonify({'status': "NOK", 'message': str(e), 'error_type': 'db_error'})

            return jsonify({'status': "OK", 'id': screen.id})

        else:
            for fieldName, errorMessages in form.errors.items():
                print(fieldName)
                for err in errorMessages:
                    print(err)
            return jsonify({'status': "NOK", 'message': form.errors, 'error_type': 'form_error'})

    elif request.method == 'DELETE':

        query = Screen.query.filter_by(id=request.args["screen_id"])

        if query.count() == 0:
            message = "No record matching this screen id"
            status = "NOK"
            return jsonify({'status':status,'message':message, 'error_type': 'db_error'})
        elif query.count() > 1:
            message = "More than one record matching this screen id"
            status = "NOK"
            return jsonify({'status': status, 'message': message, 'error_type': 'db_error'})

        try:
            query.first().delete()
        except Exception as e:
            return jsonify({'status': "NOK", 'message': str(e), 'error_type': 'db_error'})

        return jsonify({'status': "OK"})

