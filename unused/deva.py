from flask import Flask, jsonify,request
from pypsrp.client import Client

app = Flask(__name__)

hostname = "dev.autointelli.com"
port = 15985
username= "administrator"
password= "@ut0!ntell!@123"

@app.route('/get_host', methods = ['GET'])
def get_host():
    client = Client(hostname,username=username,port=port,password= password, ssl=False)
    result = client.execute_ps('hostname')
    output = result[0].strip()
    return jsonify({'output' : output})


@app.route('/getD', methods = ['GET'])
def get_hot():
    client = Client(hostname,username=username,port=port,password= password, ssl=False)
    result = client.execute_ps('PWD')
    output = result[0].strip()
    return jsonify({'output' : output})

if __name__=="__main__":
    app.run(debug=True)