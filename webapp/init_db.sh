rm -f dev.db
rm -rf migrations
export FLASK_APP=~/projet_horaires_transports/webapp/autoapp.py
export FLASK_DEBUG=1
flask db init
flask db migrate
flask db upgrade

