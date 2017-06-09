# PyForum

A simple Forum written in Python using the micro framework Flask. https://grinch.su/pyforum

Linux:

```
export APP_SETTINGS='config.DevelopmentConfig'
export APP_MAIL_USERNAME=''
export APP_MAIL_PASSWORD=''
```
Windows

```
set APP_SETTINGS=config.DevelopmentConfig
```

```
pip install -r req*/base or prod
python manage.py create_db
python manage.py create_admin
python manage.py run
```