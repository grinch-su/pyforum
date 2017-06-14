# PyForum

A simple Forum written in Python using the micro framework Flask. https://grinch.su/pyforum

Linux:

```
export APP_SETTINGS='config.DevelopmentConfig'
export APP_MAIL_USERNAME='example@domain.com'
export APP_MAIL_PASSWORD='qwerty1'
```
Windows

```
set APP_SETTINGS=config.DevelopmentConfig
set APP_MAIL_USERNAME=example@domain.com
set APP_MAIL_PASSWORD=qwerty1
```

```
pip install -r requirements/developer or producrion
python manage.py create_db
python manage.py create_admin
python manage.py run
```
