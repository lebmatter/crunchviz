Copy Crunchbase 'base_data' folder to 'static/base_data' folder.

run:
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver