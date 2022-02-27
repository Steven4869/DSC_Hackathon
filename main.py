from flask import Flask, render_template, request, redirect
import requests
import configparser
import pymysql
pymysql.install_as_MySQLdb()
from flask_mysqldb import MySQL
import yaml

app = Flask(__name__)

db = yaml.full_load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
mysql = MySQL(app)

@app.route("/")
def home():
    return render_template('index.html')
@app.route("/services")
def services():
    return render_template('services.html')
@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/weather")
def weather():
    return render_template('weather.html')
@app.route("/results", methods=['POST'])
def results():
    zip_code=request.form['ZipCode']
    country_code=request.form['CountryCode']
    if(zip_code.isnumeric() and country_code.isalpha()):
        data = get_weather(zip_code, country_code, get_api())
        seconds = data["dt"]
        place = data["name"]
        temp = "{0:.2f}".format(data["main"]["temp"])
        weather = data["weather"][0]["description"]
        rain = data["rain"]
        humidity = data["humidity"]
        speed = data["speed"]

        return render_template('results.html', place=place, temp=temp, weather=weather, rain=rain, humidity=humidity,speed=speed)
    else:
        return "Error"


def get_api():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['openweathermap']['api']
def get_weather(zip_code,country_code, api_key):
    #.format allows us to take the variable that we are passing in functions to take in string
    api_url="http://api.openweathermap.org/data/2.5/weather?zip={},{}&units=metric&cnt=7&appid={}".format(zip_code,country_code,api_key)
    r = requests.get(api_url)
    return r.json()
@app.route("/register", methods=['GET', 'POST'])
def register():
    return render_template('register.html')

@app.route("/login_validation")
def login_validation():
    return "Login Successfully"
if(__name__== '__main__'):
    app.run(debug=True)