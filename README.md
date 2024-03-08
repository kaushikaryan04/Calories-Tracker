## Calories Tracker app
First make a virtual env  
```
virtualenv env
```
Activate this env 
```
source env/bin/activate
```
Download required packages 
```
pip install -r requirements.txt
```
Now migrate  
```
python manage.py makemigrations
python manage.py migrate
```
Run server
```
python manage.py runserver
```
## Testing api endpoints 
Register user 
url -> http://localhost:8000/api/register  
example parameters  
```
{
    "username":"kaushikfrompostman2",
    "password":"1234",
    "height":190,
    "weight":50,
    "age":25,
    "gender":"male",
    "activity":"light"
}
```

Login to aquire token 
url -> http://localhost:8000/api/token/
```
{
    "username":"kaushikfrompostman2",
    "password":"1234",
}
```
Note that the output token given by this request should be attached to every request header bellow  
Track Calories  
url -> http://localhost:8000/api/dailytrack  
```
{
    "calories":"2000"
    "date":"2024-03-04"
}
```
Get Record in json form  
url -> http://localhost:8000/api/getrecord  
Download record in pdf form 
url -> http://localhost:8000/api/generatereport  
Download record in csv form 
url -> http://localhost:8000/api/generatecsv  
