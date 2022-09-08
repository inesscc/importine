from flask import Flask
from flask import  request
import pandas as pd
from flask import jsonify
import os
from flask_swagger_ui import get_swaggerui_blueprint


app = Flask(__name__)

### swagger specific ###
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Seans-Python-Flask-REST-Boilerplate"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
### end swagger specific ###



@app.route('/')
def home():
    return jsonify({ "mensaje": "Bienvenido a la API de INE"}) 


@app.route('/data', methods = ['GET'])
def download_data():
     name = request.args.get('dataset')
     year = request.args.get('year')
        
     file = "data/{encuesta}/{encuesta}_{year}.feather".format(encuesta = name, year = year) #/home/klaus/ine/importine/
     data = pd.read_feather(file)
     data2 = data.iloc[0:300, 0:10 ]
     json_data = jsonify({"data": data2.to_dict()})
     return json_data
 
 
@app.route('/datasets', methods = ['GET'])
def get_dataset_list():
    files_dic = {name:os.listdir("data/" + name)  for name in os.listdir("data/")}
    files_dic2 = {k: [v.replace(".feather", "") for v in l if v.find("feather") != -1 ]  for k, l in files_dic.items()}
    json_data = jsonify({ "datasets": files_dic2})
    return json_data

@app.route("/colnames", methods = ["GET"])
def get_columns():
    name = request.args.get('dataset')
    year = request.args.get('year')
   
    file = "data/{encuesta}/{encuesta}_{year}.feather".format(encuesta = name, year = year) #/home/klaus/ine/importine/
    data = pd.read_feather(file)
    cols = list(data .columns)
    json_data = jsonify({"data": cols})
    return json_data


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)


