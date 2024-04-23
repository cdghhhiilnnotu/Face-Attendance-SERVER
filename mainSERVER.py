from flask import Flask, request, jsonify
from database.moduleDATABASE import *
from commons.helper import *

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
def post_report():
    post_diem_danh(request.form['masv'],request.form['malop'],request.form['ghichu'])
    return {}, 201

@app.route('/giaovien/baocao/<malop>', methods=['GET'])
def get_all_baocao(malop):
    update_all_bao_cao(malop)
    return {}

# DELETE
@app.route('/admin/<admin_id>', methods=['DELETE'])
def delete_admin(admin_id):
    execute_SQL(f"""DELETE FROM admin WHERE MaAD = '{admin_id}'""")
    global json_admin
    json_admin = get_json_admin()
    return {}

@app.route('/giaovien/<giaovien_id>', methods=['DELETE'])
def delete_giaovien(giaovien_id):
    execute_SQL(f"""DELETE FROM giaovien WHERE MaGV = '{giaovien_id}'""")
    global json_admin
    json_admin = get_json_admin()
    return {}

@app.route('/sinhvien/<sinhvien_id>', methods=['DELETE'])
def delete_sinhvien(sinhvien_id):
    execute_SQL(f"""DELETE FROM sinhvien WHERE MaSV = '{sinhvien_id}'""")
    global json_admin
    json_admin = get_json_admin()
    return {}

@app.route('/lophoc/<lophoc_id>', methods=['DELETE'])
def delete_lophoc(lophoc_id):
    execute_SQL(f"""DELETE FROM lophoc WHERE MaLop = '{lophoc_id}'""")
    global json_admin
    json_admin = get_json_admin()
    return {}

@app.route('/baocao/<baocao_id>', methods=['DELETE'])
def delete_baocao(baocao_id):
    execute_SQL(f"""DELETE FROM baocao WHERE MaBC = '{baocao_id}'""")
    global json_admin
    json_admin = get_json_admin()
    return {}

@app.route('/dslop/<dslop_id>', methods=['DELETE'])
def delete_dslop(dslop_id):
    execute_SQL(f"""DELETE FROM dslop WHERE MaDS = '{dslop_id}'""")
    global json_admin
    json_admin = get_json_admin()
    return {}

# ADMIN - POST, PUT 
@app.route('/admin/post', methods=['POST'])
def post_admin():
    execute_SQL(f"""INSERT INTO ADMIN
                    VALUES
                    ('{id_admin_generated(get_connection())}', '{request.form["TenDN"]}', '{request.form["MatKhau"]}');""")
    global json_admin
    json_admin = get_json_admin()
    return {}, 201

@app.route('/admin/put', methods=['PUT'])
def put_admin():
    execute_SQL(f"""UPDATE ADMIN SET
                    TenDN = '{request.form["TenDN"]}', MatKhau = '{request.form["MatKhau"]}' WHERE MaAD = '{request.form["MaAD"]}';""")
    global json_admin
    json_admin = get_json_admin()
    return {}, 201


# GIAOVIEN - POST, PUT 
@app.route('/teacher/post', methods=['POST'])
def post_teacher():
    execute_SQL(f"""INSERT INTO GIAOVIEN (MaGV, TenGV, NgSinh, DiaChi, MatKhau, SDT)
                    VALUES
                    ('{request.form["MaGV"]}', 
                    '{request.form["TenGV"]}',
                    '{request.form["NgSinh"]}',
                    '{request.form["DiaChi"]}',
                    '{request.form["MatKhau"]}',
                    '{request.form["SDT"]}');""")
    global json_admin
    json_admin = get_json_admin()
    return {}

@app.route('/teacher/put', methods=['PUT'])
def put_teacher():
    execute_SQL(f"""UPDATE GIAOVIEN SET
                    NgSinh = '{request.form["NgSinh"]}' ,
                    DiaChi = '{request.form["DiaChi"]}' ,
                    MatKhau = '{request.form["MatKhau"]}', 
                    TenGV = '{request.form["TenGV"]}' ,
                    SDT = '{request.form["SDT"]}' 
                    WHERE MaGV = '{request.form["MaGV"]}';""")
    global json_admin
    json_admin = get_json_admin()
    return {}

# SINHVIEN - POST, PUT 
@app.route('/student/post', methods=['POST'])
def post_student():
    execute_SQL(f"""INSERT INTO SINHVIEN (MaSV, TenSV, NgSinh, LopQL, DiaChi, LinkAnh, SDT)
                    VALUES
                    ('{request.form["MaSV"]}', 
                    '{request.form["TenSV"]}',
                    '{request.form["NgSinh"]}',
                    '{request.form["LopQL"]}',
                    '{request.form["DiaChi"]}',
                    '{request.form["LinkAnh"]}',
                    '{request.form["SDT"]}');""")
    global json_admin
    json_admin = get_json_admin()
    return {}

@app.route('/student/put', methods=['PUT'])
def put_student():
    execute_SQL(f"""UPDATE SINHVIEN SET
                    NgSinh = '{request.form["NgSinh"]}' ,
                    DiaChi = '{request.form["DiaChi"]}' ,
                    LopQL = '{request.form["LopQL"]}', 
                    TenSV = '{request.form["TenSV"]}' ,
                    LinkAnh = '{request.form["LinkAnh"]}' ,
                    SDT = '{request.form["SDT"]}' 
                    WHERE MaSV = '{request.form["MaSV"]}';""")
    global json_admin
    json_admin = get_json_admin()
    return {}


# LOPHOC - POST, PUT 
@app.route('/lophoc/post', methods=['POST'])
def post_lophoc():
    execute_SQL(f"""INSERT INTO LOPHOC (MaLop, TenMon, MaGV, LichHoc, PhongHoc, SoluongSV, SoNgay)
                    VALUES
                    ('{request.form["MaLop"]}', 
                    '{request.form["TenMon"]}',
                    '{request.form["MaGV"]}',
                    '{request.form["LichHoc"]}',
                    '{request.form["PhongHoc"]}',
                    '{request.form["SoluongSV"]}',
                    '{request.form["SoNgay"]}');""")
    global json_admin
    json_admin = get_json_admin()
    return {}

@app.route('/lophoc/put', methods=['PUT'])
def put_lophoc():
    execute_SQL(f"""UPDATE LOPHOC SET
                    SoNgay = '{request.form["SoNgay"]}' ,
                    TenMon = '{request.form["TenMon"]}' ,
                    MaGV = '{request.form["MaGV"]}', 
                    LichHoc = '{request.form["LichHoc"]}' ,
                    PhongHoc = '{request.form["PhongHoc"]}' ,
                    SoluongSV = '{request.form["SoluongSV"]}' 
                    WHERE MaLop = '{request.form["MaLop"]}';""")
    global json_admin
    json_admin = get_json_admin()
    return {}


# BAOCAO - POST, PUT 
@app.route('/baocao/post', methods=['POST'])
def post_baocao():
    execute_SQL(f"""INSERT INTO BAOCAO (MaBC, NgayBC, MaSV, MaLop, DiemDanh, GhiChu)
                    VALUES
                    ('{request.form["MaBC"]}', 
                    '{request.form["NgayBC"]}',
                    '{request.form["MaSV"]}',
                    '{request.form["MaLop"]}',
                    '{request.form["DiemDanh"]}',
                    '{request.form["GhiChu"]}');""")
    global json_admin
    json_admin = get_json_admin()
    return {}

@app.route('/baocao/put', methods=['PUT'])
def put_baocao():
    execute_SQL(f"""UPDATE BAOCAO SET
                    NgayBC = '{request.form["NgayBC"]}' ,
                    MaSV = '{request.form["MaSV"]}' ,
                    MaLop = '{request.form["MaLop"]}', 
                    DiemDanh = '{request.form["DiemDanh"]}' ,
                    GhiChu = '{request.form["GhiChu"]}' 
                    WHERE MaBC = '{request.form["MaBC"]}';""")
    global json_admin
    json_admin = get_json_admin()
    return {}

# DSLOP - POST, PUT 
@app.route('/dslop/post', methods=['POST'])
def post_dslop():
    execute_SQL(f"""INSERT INTO dslop (MaDS, MaLop, MaSV, SoDD)
                    VALUES
                    ('{request.form["MaDS"]}', 
                    '{request.form["MaLop"]}',
                    '{request.form["MaSV"]}',
                    '{request.form["SoDD"]}');""")
    global json_admin
    json_admin = get_json_admin()
    return {}

@app.route('/dslop/put', methods=['PUT'])
def put_dslop():
    execute_SQL(f"""UPDATE dslop SET
                    MaLop = '{request.form["MaLop"]}' ,
                    MaSV = '{request.form["MaSV"]}' ,
                    SoDD = '{request.form["SoDD"]}'
                    WHERE MaDS = '{request.form["MaDS"]}';""")
    global json_admin
    json_admin = get_json_admin()
    return {}


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
