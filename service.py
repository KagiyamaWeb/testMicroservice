import requests
import xmltodict
import json
import urllib
import datetime

from flask import Flask

app = Flask(__name__)
cur_url = 'https://www.cbr.ru/scripts/XML_valFull.asp'
course_url = 'http://www.cbr.ru/scripts/XML_daily.asp'

@app.route("/api/currency", methods=['GET'])
def get_currency():
    r = requests.get(cur_url)
    currency = json.loads(json.dumps(xmltodict.parse(r.content)))
    cur_list = []
    for item in currency['Valuta']['Item']:
        cur_list.append((item["ISO_Char_Code"], item["EngName"]))
    return json.dumps(cur_list, indent = 3)

@app.route("/api/course/<currency>/<first_date>/<second_date>", methods=['GET'])
def get_difference(currency, first_date, second_date):
    datetime_obj = datetime.datetime.strptime(first_date, "%Y-%d-%m")
    params = {'date_req' : datetime_obj.strftime("%d/%m/%Y")}
    r = requests.get(course_url, params = params)
    fst_values = json.loads(json.dumps(xmltodict.parse(r.content)))
    for cur in fst_values["ValCurs"]["Valute"]:
        if cur['CharCode'] == currency:
            fst_value = round(float(cur['Value'].replace(',','.')), 2)
 
    datetime_obj = datetime.datetime.strptime(second_date, "%Y-%d-%m") 
    params = {'date_req' : datetime_obj.strftime("%d/%m/%Y")}
    r = requests.get(course_url, params = params)
    snd_values = json.loads(json.dumps(xmltodict.parse(r.content)))
    for cur in snd_values["ValCurs"]["Valute"]:
        if cur['CharCode'] == currency:
            snd_value = round(float(cur['Value'].replace(',','.')), 2) 

    difference = round((snd_value - fst_value), 2)
    return json.dumps((fst_value, snd_value, difference), indent = 3)


    
        
        
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=80, debug = True)