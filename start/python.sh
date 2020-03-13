
export $(../../.env)

if [[ $SITE_URL == "http://128.199.74.157:8000" ]]
then
  python manage.py migrate &&
  python manage.py runserver $HOST:$WEB_PORT --settings=sitename.settings.stage
else
  python manage.py migrate &&
  python manage.py runserver $HOST:$WEB_PORT
fi
