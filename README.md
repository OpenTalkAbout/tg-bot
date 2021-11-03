# tg-bot

## Start bot
### On local machine
#### Install requirements
pip3 install -r requirements.txt
#### Export tokens
export TG_BOT_TOKEN=xxxx
export OWM_TOKEN=xxxx
#### Run
python3 manage.py runserver

### On Heroku
#### Buildpacks
1. heroku/python
2. https://github.com/jonathanong/heroku-buildpack-ffmpeg-latest.git
#### Stack
heroku-20
#### Enable dyno formation
local: python3 manage.py runserver - ON