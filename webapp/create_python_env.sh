virtualenv -p /usr/bin/python3.5 proj_python_env
source proj_python_env/bin/activate
pip install -r requirements/dev.txt
pip install -r requirements/prod.txt

