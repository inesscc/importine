
from fastapi import FastAPI
import os
import re

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World   aaaa asdfsdfsdf"}



# Obtener listado de datasets con su respectivo identificador
@app.get("/datasets") 
async def get_dataset_list():     
     files_dic = {name:os.listdir("data/" + name)  for name in os.listdir("data/")}
     files_dic2 = {k: [v.replace(".feather", "") for v in l if v.find("feather") != -1 ]  for k, l in files_dic.items()}
     files_dic2 = {k: [re.sub(".*_", "", v) for v in l ]  for k, l in files_dic2.items()}
     files_dic2  = {k:sorted(v) for k,v in files_dic2 .items()}
     return files_dic2


@app.get('/datasets/{dataset}')
def get_specific_dataset_list(dataset):
     path = "data/{dataset}/".format(dataset = dataset)
     files_dic = {dataset:os.listdir(path)}
     files_dic2 = {k: [v.replace(".feather", "") for v in l if v.find("feather") != -1  ]  for k, l in files_dic.items()}
     files_dic2 = {k: [re.sub(".*_", "", v) for v in l ]  for k, l in files_dic2.items()}
     files_dic2  = {k:sorted(v) for k,v in files_dic2 .items()}     
     return files_dic2


# =============================================================================
# from flask import Flask
# from flask import  request
# import pandas as pd
# from flask import jsonify, redirect, flash, url_for, render_template, abort
# import os
# from flask_swagger_ui import get_swaggerui_blueprint
# import re
# from werkzeug.utils import secure_filename
# 
# 
# 
# app = Flask(__name__)
# 
# #app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
# app.config['UPLOAD_EXTENSIONS'] = ['.csv', '.feather']
# app.config['UPLOAD_PATH'] = 'data_test'
# UPLOAD_PATHS = ["ene_test", "esi_test", "epf_personas", "epf_gastos", "enusc"]
# 
# ### swagger specific ###
# SWAGGER_URL = '/swagger'
# API_URL = '/static/swagger.json'
# SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
#     SWAGGER_URL,
#     API_URL,
#     config={
#         'app_name': "Seans-Python-Flask-REST-Boilerplate"
#     }
# )
# app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
# ### end swagger specific ###
# 
# 
# def validate_path(user_path):
#     if user_path in UPLOAD_PATHS:
#         return True
#     else:
#         return False
# 
# def build_full_path(user_path, filename):
#     return "data/" + user_path + "/" + filename
#     
# 
# @app.route('/upload')
# def index():
#     return render_template('index.html')
# 
# @app.route('/upload', methods=['GET', 'POST'])
# def upload_file():
#     if request.method == 'POST':
#         
#         # Validar la constraseña 
#         password = request.form.get("clave")
#         processed_text = password.upper()
#         if processed_text != "HOLA":
#             return "contraseña incorrecta", 400
# 
#         # Validar la ruta 
#         path = request.form.get("folder")
#         if validate_path(path) == False:
#             return "la ruta es incorrecta", 400
#            
#         # Subir archivo
#         uploaded_file = request.files['file']
#         filename = secure_filename(uploaded_file.filename)
#         full_path = build_full_path(path, filename)
# 
#         if filename != '':
#             file_ext = os.path.splitext(filename)[1]
#             if file_ext not in app.config['UPLOAD_EXTENSIONS']:
#                 #abort(400)
#                 return "formato no aceptado", 400
#             uploaded_file.save(full_path)
#         return redirect(url_for('index'))
#     return render_template('index.html')
# 
# 
# 
# 
# @app.route('/')
# def home():
#     return jsonify({ "mensaje": "Bienvenido a la API de INE"}) 
# 
# # Obtener datos con método difícil
# @app.route('/data', methods = ['GET'])
# def download_data():
#      name = request.args.get('dataset')
#      year = request.args.get('year')    
#      file = "data/{encuesta}/{encuesta}_{year}.feather".format(encuesta = name, year = year) #/home/klaus/ine/importine/
#      data = pd.read_feather(file)
#      data2 = data.iloc[0:300, 0:10 ]
#      json_data = jsonify({"data": data2.to_dict()})
#      return json_data
#  
# # Obtener datos con la url fácil
# @app.route('/data/<string:dataset>/<string:version>', methods = ['GET'])
# def download_data2(dataset, version):
#         
#      file = "data/{dataset}/{dataset}_{year}.feather".format(dataset = dataset, year = version) #/home/klaus/ine/importine/
#      data = pd.read_feather(file)
#      data2 = data.iloc[0:300 ]
#      data2.fillna("", inplace=True)
#      json_data = jsonify({"data": data2.to_dict()})
#      return json_data
# 
# # Obtener listado de datasets con su respectivo identificador
# @app.route('/datasets', methods = ['GET'])
# def get_dataset_list():
#     
#     files_dic = {name:os.listdir("data/" + name)  for name in os.listdir("data/")}
#     files_dic2 = {k: [v.replace(".feather", "") for v in l if v.find("feather") != -1 ]  for k, l in files_dic.items()}
#     files_dic2 = {k: [re.sub(".*_", "", v) for v in l ]  for k, l in files_dic2.items()}
#     files_dic2  = {k:sorted(v) for k,v in files_dic2 .items()}
#     json_data = jsonify({ "datasets": files_dic2}) 
#     return json_data
# 
# # Obtener listado de datasets para una encuesta en específico
# @app.route('/datasets/<string:dataset>', methods = ['GET'])
# def get_specific_dataset_list(dataset):
#     path = "data/{dataset}/".format(dataset = dataset)
#     files_dic = {dataset:os.listdir(path)}
#     files_dic2 = {k: [v.replace(".feather", "") for v in l if v.find("feather") != -1  ]  for k, l in files_dic.items()}
#     files_dic2 = {k: [re.sub(".*_", "", v) for v in l ]  for k, l in files_dic2.items()}
#     files_dic2  = {k:sorted(v) for k,v in files_dic2 .items()}
#     
#     json_data = jsonify({ "datasets": files_dic2})
#     return json_data
# 
# # Comprobar que el archivo tenga la extensión permitida
# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
# 
# 
# 
# # Obtener columnas de un dataset
# @app.route('/colnames/<string:dataset>/<string:version>', methods = ['GET'])
# def get_columns(dataset, version):
#     file = "data/{dataset}/{dataset}_{year}.feather".format(dataset = dataset, year = version) #/home/klaus/ine/importine/
#     data = pd.read_feather(file)
#     cols = list(data .columns)
#     json_data = jsonify({"data": cols})
#     return json_data
# 
# 
# if __name__ == '__main__':
#     app.run(host="0.0.0.0", port=8000)
# =============================================================================


