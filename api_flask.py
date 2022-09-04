from flask import Flask,render_template
from flask_restful import Resource, Api, reqparse
import ast
app = Flask(__name__)
api = Api(app)


class photo(Resource):
    def post(self):
        with open(r"ewe.txt", encoding='UTF8') as f:
            contents = f.read()
        return {'data': contents}, 200  # return data and 200 OK code
    pass
api.add_resource(photo, '/photo')



class test(Resource):
    def get(self):
        with open(r"ewe.txt", encoding='UTF8') as f:
            contents = f.read()
        return {'data': contents}, 200  # return data and 200 OK code
    pass
api.add_resource(test, '/test')



@app.route('/')
def home():
   return render_template('upload.html')
   
if __name__ == '__main__':
   app.run(host='localhost', port=8080)  # run our Flask app