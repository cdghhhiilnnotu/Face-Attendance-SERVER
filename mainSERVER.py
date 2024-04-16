from flask import Flask, request, jsonify
from database.moduleDATABASE import get_json_admin, get_json_user, post_diem_danh, update_all_bao_cao
from commons.helper import api_user_loggin

app = Flask(__name__)

json_admin = get_json_admin()

# ALL ROUTE
@app.route('/', methods=['GET'])
def get_all():
    return jsonify(json_admin)

@app.route('/giaovien/logging/<username>/<password>', methods=['GET'])
def get_logging_user(username, password):
    return jsonify(api_user_loggin(username, password, json_admin['giaovien']))

@app.route('/giaovien/login_success/<username>', methods=['GET'])
def get_api_for_user(username):
    return jsonify(get_json_user(username))

@app.route('/giaovien/baocao', methods=['POST'])
def post_baocao():
    post_diem_danh(request.form['masv'],request.form['malop'],request.form['ghichu'])
    return {}, 201

@app.route('/giaovien/baocao/<malop>', methods=['GET'])
def get_all_baocao(malop):
    update_all_bao_cao(malop)
    return {}


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
