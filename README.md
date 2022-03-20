## Installation

Install weather-app project in your local machine

```bash
git clone https://github.com/imchandr/Weather.git
```
```bash
cd Weather

```

now install required packages and dependencies for project.
i have used pipenv in this project and if you have installed pipenv run

```bash
pipenv install
```
if you are using pip use
```bash
pip install -r requirments.txt
```
now activate your virtual inviroment with command(for pipenv)

```bash
pipenv shell
```

- now run makemigrations and migrate commands to create db
```bash
python manage.py makemigrations
```
```bash
python manage.py migrate
```
- to run the backend development server type and following the commands from root directory
```bash
python manage.py runserver
```

- to run the front-end development server type and following the commands from within frontend directory
```bash
npx start
```


## Instructions and usage
### weather app has three section
   ### 1. backend and api's
   #### http://127.0.0.1:8000/api/ on local https://opnweather-api.herokuapp.com/api/ deployed on heroku
   gives you list of available city to choose in dropdown menu
   can perform get, post, put, delete on this api end-pont
  ```bash
  GET http://127.0.0.1:8000/api/
  ```
  ```bash
  POST http://127.0.0.1:8000/api/
  body
  {

  "name": "London",
  "lat": "dumy-data",
  "long": "dumy-data"
  }
  ```
  ```bash
  PUT http://127.0.0.1:8000/api/<id>
  body
  {

  "name": "NewYork",

  }
  ```
  ```bash
  DELETE http://127.0.0.1:8000/api/<id>

  ```
  #### http://127.0.0.1:8000/weather/<city_name api link> on local https://opnweather-api.herokuapp.com/weather/ on heroku and follow the api button to display specific data for that city
  gives you filtered weather data-points from openweather-api for given city
      
  ### 2. django template front-end
  front-end build with django-template and django backend
  ```bash
  python manage.py runserver  and goto
  http://127.0.0.1:8000/ for react front-end
  http://127.0.0.1:8000/weather for django-template frontend