# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint, render_template, request, flash, redirect, url_for,jsonify
from flask_login import login_required, current_user
from horairesflaskapp.board.forms import NewBoardForm
from horairesflaskapp.board.models import Board
from horairesflaskapp.screen.models import Screen
from horairesflaskapp.utils import flash_errors


blueprint = Blueprint('board', __name__, url_prefix='/boards', static_folder='../static')


@blueprint.route('/', methods=['POST','DELETE'])
@login_required
def board():
    form = NewBoardForm(request.form)
    if request.method == 'POST':
        if form.validate():
            try:
                board = Board.create(name=form.name.data, user_id=current_user.id, chip_id=form.chip_id.data)
            except Exception as e:
                return jsonify({'status': "NOK", 'message': str(e), 'error_type': 'db_error'})

            return jsonify({'status': "OK", 'id':board.id})
        else:
            for fieldName, errorMessages in form.errors.items():
                print(fieldName)
                for err in errorMessages:
                    print(err)
            return jsonify({'status': "NOK", 'message': form.errors, 'error_type': 'form_error'})

    elif request.method == 'DELETE':

        query = Board.query.filter_by(id=request.args["board_id"], user_id=current_user.id)

        if query.count() == 0:
            message = "No record matching this board id"
            status = "NOK"
            return jsonify({'status':status,'message':message})
        elif query.count() > 1:
            message = "More than one record matching this board id"
            status = "NOK"
            return jsonify({'status': status, 'message': message})


        try:
            for s in Screen.query.filter_by(board_id=request.args["board_id"]).all():
                s.delete()
        except Exception as e:
            return jsonify({'status': "NOK", 'message': str(e)})


        try:
            query.first().delete()
        except Exception as e:
            return jsonify({'status': "NOK", 'message': str(e)})




        return jsonify({'status': "OK"})

