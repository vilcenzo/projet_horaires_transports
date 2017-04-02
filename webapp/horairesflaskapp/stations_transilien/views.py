from horairesflaskapp.stations_transilien.models import StationTransilien


from flask import Blueprint, request,jsonify
from flask_login import login_required


blueprint = Blueprint('station_transilien', __name__, url_prefix='/stations_transilien', static_folder='../static')


@blueprint.route('/', methods=['GET'])
@login_required
def stations_transilien():
    print(request.args)
    uic = request.args['uic']

    station = StationTransilien.query.filter_by(uic=uic).first()

    return jsonify(**dict(name=station.name, uic=uic))

