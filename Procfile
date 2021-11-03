web: gunicorn gettingstarted.wsgi --max-requests 1 --keep-alive 30 --threads=1 --workers=1 --worker-connections=1 --timeout 30 --log-file -

local: python3 manage.py runserver