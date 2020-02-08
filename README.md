# Coingate Sandbox Payment App
**How to install:** 
1. Clone current repository **git clone https://github.com/glitzybunny/django-stat-app.git**
2. **pip install -r requirements.txt**
3. Create the MYSQL DB conf file( take a look to the instance of DB conf file below). 
4. Specify an absolute path to your DB conf file into <span style="color:lightgreen">DATABASE_CONF_PATH</span> variable in settings.py
5. Migrate. **python manage.py migrate** 
6. Run Django built in webserver. **python manage.py runserver**
7. It works now! Check it out on **localhost:8000**


**E.g. of DB conf file and an absolute path to the conf file:** 
<span style="color:lightgreen">
DATABASE_CONF_PATH = '/run/media/root/drive/dev/stat_app/stat_app/stat_app/my.cnf'
</span>

**Instance of the DB conf file('my.cnf' in my case). Set your DB params**
```
[client]
database = YOUR_DB_NAME
host = YOUR_HOST_NAME_OR_LOCALHOST
user = YOUR_USERNAME(MYSQL USERNAME)
password = YOUR_PASSWORD(MYSQL PASSWORD
default-character-set = utf8
```
* Created two serializers for fixtures (custom fixtures -> Django fixtures)
* Created CORS tester. Check out *cors-tester.html* to find out how to work with that.  
 



Implementasion is not throught Coingate Callbacks(it would be the best decision to track Order status)because they do work in localhost. Check out the link below.  
https://developer.coingate.com/docs/payment-callback#private-nework--localhost