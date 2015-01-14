"""
http://127.0.0.1:5000/

Unique Identifier 7b42a0eefcbe4c83bc8add350124257f

secret 665e05a7e5a14300888b25829bf8a112
"""
import requests
from flask import Flask, request
app = Flask(__name__)

class OauthData:
    unique_identifier = "7b42a0eefcbe4c83bc8add350124257f"
    secret_key = "665e05a7e5a14300888b25829bf8a112"
    IndexPage = "http://localhost:5000"
    Callback = "http://localhost:5000/callback"
    Attendance = "http://localhost:5000/get_attendance"
    scope = "read%20write"
    access_token = ""
    

def get_aut_request():
    return "https://oauth.yandex.ru/authorize?response_type=code" \
            "&client_id={0}".format(OauthData.unique_identifier)

@app.route("/")
def index():
    url = '<a href={0}>Авторизация</a><br>' \
          '<a href={1}>Посещаемость</a><br>'.format(get_aut_request(), OauthData.Attendance)
    return url

@app.route("/callback")
def callback():
    if not OauthData.access_token:
        error = request.args.get('error')
        if error:
            return "Error: " + error
        code = request.args.get('code')
        print("Code value: ", code)
        OauthData.access_token = get_token(code)
        return '<a>Авторизация выполнена</a> <br>' \
               '<a href={0}>Назад</a>'.format(OauthData.IndexPage)
    return '<a>Вы уже авторизованы</a> <br>' \
           '<a href={0}>Назад</a>'.format(OauthData.IndexPage)

@app.route("/get_attendance")
def get_attendance():
    headers = {"Authorization" : "Bearer " + OauthData.access_token}
    print("access_token=",OauthData.access_token)
    response_json = requests.get("http://api-metrika.yandex.ru/stat/traffic/summary.json?id=22267882&pretty=1&date1=20140901&date2=20141231&token=" + OauthData.access_token,  headers=headers).json()
    print ("JSON answer from API =", response_json)
    if "error" in response_json:
        return ("Error: " + response_json["error"] + 
                "<br>Ошибка: " + response_json["error_description"]) + '<br>' \
           '<a href={0}>Назад</a>'.format(OauthData.IndexPage)
    return ("Информация о странице:<br><br>Количество отказов: " + str(response_json["max"]["denial"]) +
            "<br>Количество посещений:" + str(response_json["max"]["visits"]) +
            "<br>Количество просмотров:" + str(response_json["max"]["page_views"])) + \
            "<br>Глубина просмотра:" + str(response_json["max"]["depth"]) +\
            '<br>' \
            '<a href={0}>Назад</a>'.format(OauthData.IndexPage)





def get_token(code):
    post_data = {"grant_type" : "authorization_code",
                 "code": code,
                 "client_id": OauthData.unique_identifier,
                 "client_secret": OauthData.secret_key}
    response = requests.post("https://oauth.yandex.ru/token", data=post_data)
    print("status", response.status_code)
    token_json = response.json()
    print ("Token JSON = ",token_json)
    token = token_json["access_token"] if "access_token" in token_json.keys() else ""
    print ("token =", token)
    return token

    
if __name__ == "__main__":
    app.run(debug=True)