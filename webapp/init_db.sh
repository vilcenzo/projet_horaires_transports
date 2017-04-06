rm -f dev.db
rm -rf migrations
flask db init
flask db migrate
flask db upgrade
flask fill_stations_transilien

