# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from horairesflaskapp.board.forms import NewBoardForm
from horairesflaskapp.screen.forms import NewScreenForm
from horairesflaskapp.board.models import Board
from horairesflaskapp.screen.models import Screen



blueprint = Blueprint('user', __name__, url_prefix='/users', static_folder='../static')


@blueprint.route('/', methods=['GET'])
@login_required
def members():
    """List members."""

    form_board = NewBoardForm()
    form_screen = NewScreenForm()
    boards = Board.query.filter_by(user_id=current_user.id).all()
    screens = []
    for b in boards:
        screens.append(Screen.query.filter_by(board_id=b.id).all())
    return render_template('users/members.html', form_board=form_board, boards=boards, form_screen=form_screen, screens=screens)
