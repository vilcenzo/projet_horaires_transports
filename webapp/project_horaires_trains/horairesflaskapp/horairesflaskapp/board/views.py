# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint, render_template, request, flash, redirect, url_for,jsonify
from flask_login import login_required, current_user
from horairesflaskapp.board.forms import NewBoardForm
from horairesflaskapp.board.models import Board
from horairesflaskapp.utils import flash_errors


blueprint = Blueprint('board', __name__, url_prefix='/boards', static_folder='../static')


@blueprint.route('/', methods=['POST','DELETE'])
@login_required
def board():
    if request.method == 'POST':
        try:
            Board.create(name=request.json["name"], user_id=current_user.id)
        except Exception as e:
            return jsonify({'status': "NOK", 'message': str(e)})

        return jsonify({'status': "OK"})

    elif request.method == 'DELETE':

        query = Board.query.filter_by(name=request.args["name"], user_id=current_user.id)

        if query.count() == 0:
            message = "No record matching this board name"
            status = "NOK"
            return jsonify({'status':status,'message':message})
        elif query.count() > 1:
            message = "More than one record matching this board name"
            status = "NOK"
            return jsonify({'status': status, 'message': message})

        Board.query.filter_by(name=request.args["name"], user_id=current_user.id).first().delete()
        return jsonify({'status': "OK"})

