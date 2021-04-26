#!flask/bin/python
import json
from flask import Flask, Response ,request
from helloworld.flaskrun import flaskrun
import requests
from flask import Flask, Response, request
from flask_cors import CORS
import boto3
import datetime
from datetime import datetime

application = Flask(__name__)
CORS(application, resources={r"/*": {"origins": "*"}})
@application.route('/', methods=['GET'])
def get():
    return Response(json.dumps({'Output': 'Hello World'}), mimetype='application/json', status=200)
@application.route('/', methods=['POST'])
def post():
    return Response(json.dumps({'Output': 'Hello World'}), mimetype='application/json', status=200)
@application.route('/calc/bit', methods=['GET'])
def post_currency_bit():
    return Response(json.dumps(get_bitcoin_index()), mimetype='application/json', status=200)
def get_bitcoin_index():
    url = 'https://api.coindesk.com/v1/bpi/currentprice.json'
    response = requests.get(url).json()['bpi']['USD']['rate']
    return response
# return generic data
@application.route('/get_generic', methods=['GET'])
def get_generic_data():
    return Response(json.dumps(generic_data), mimetype='application/json', status=200)
# mock data
currency_rate = {
    'usd' : 3.3,
    'pound' : 4.5,
    'euro' : 4.8
}
#generic data
generic_data = [
    {
    "id":1,
    "title": "wtf",
    "body": "good will"
    },
    {
    "id":2,
    "title": "wtf2",
    "body": "good will2"
    }
   ]
   
# get example for multiplication
# test get  
# curl -i http://"localhost:8000/v1/multiply?first_num=12.1&second_num=12"
@application.route('/v1/multiply', methods=['GET', 'POST'])
def get_mult_res():
    first_num = request.args.get('first_num')
    second_num = request.args.get('second_num')
    res = float(first_num) * float(second_num) 
    return Response(json.dumps({'multiplication result': res}), mimetype='application/json', status=200)
    
# get example for multiplication
# test get  
# curl -i http://"localhost:8000/v1/calcbit?first_num=5"
@application.route('/v1/calcbit', methods=['GET', 'POST'])
def get_mult_calc():
    first_num = request.args.get('first_num')
    second_num = get_bitcoin_index().replace(",", "")
    res = round(float(first_num) * float(second_num)) 
    return Response(json.dumps({'Bit Cost result': res}), mimetype='application/json', status=200)
    
@application.route('/get_forms', methods=['GET'])
def get_frm():
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('forms')
    # replace table scan
    resp = table.scan()
    print(str(resp))
    return Response(json.dumps(str(resp['Items'])), mimetype='application/json', status=200)
    
# curl -i -X POST -d'{"form_title":"form title1", "form_body":"where is it?","form_type":"finance"}' -H "Content-Type: application/json" http://localhost:8000/set_form/frm4
# curl -i -X POST -d'{"form_title":"form title1", "form_body":"where is it?","form_type":"finance"}' -H "Content-Type: application/json" http://ec2-34-207-127-59.compute-1.amazonaws.com/set_form/frm5
@application.route('/set_form/<frm_id>', methods=['POST'])
def set_doc(frm_id):
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('forms')
    # get post data  
    data = request.data
    # convert the json to dictionary
    data_dict = json.loads(data)
    # retreive the parameters
    form_body = data_dict.get('form_body','default')
    form_title = data_dict.get('form_title','defualt')
    form_type = data_dict.get('form_type','defualt')
    item={
    'form_id': frm_id,
    'form_body': form_body,
    'form_title': form_title,
    'form_type':form_type
     }
     
    table.put_item(Item=item)
    return Response(json.dumps(item), mimetype='application/json', status=200)
# curl -i http://"localhost:8000/del_form?formId=fx01&formType=finance"
@application.route('/del_form', methods=['GET'])
def del_item():
    formId = request.args.get('formId')
    formType = request.args.get('formType')
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('forms')
    table.delete_item(
    Key={
        'form_id': formId,
        'form_type': formType
    }
    )
    # replace table scan
    resp = table.scan()
    print(str(resp))
    return Response(json.dumps(str(resp['Items'])), mimetype='application/json', status=200)
    
# curl -i http://"localhost:8000/get_form?formId=fx01&formType=finance"
@application.route('/get_form', methods=['GET'])
def get_item():
    formId = request.args.get('formId')
    formType = request.args.get('formType')
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('forms')
    resp = table.get_item(
    Key={
        'form_id': formId,
        'form_type': formType
    }
    )
    # replace table scan
    
    print(str(resp))
    return Response(json.dumps(str(resp['Item'])), mimetype='application/json', status=200) 
    
@application.route('/upload_file', methods=['GET'])
def upload_file():
    time = str(datetime.now())
    file_name = 'myUpload' + time
    bucket = 'my-upload-bucket-nivbn'
    client = boto3.client('s3')
    return client.put_object(Body='', Bucket=bucket, Key=file_name)
    
    
if __name__ == '__main__':
    flaskrun(application)