from flask import Flask, request, jsonify
from database.moduleDATABASE import jsonDict

app = Flask(__name__)

# ALL ROUTE
@app.route('/', methods=['GET'])
def get_all():
    return jsonify(jsonDict)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
