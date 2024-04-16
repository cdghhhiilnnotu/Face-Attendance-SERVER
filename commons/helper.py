import json
from datetime import datetime

def tuple2dict(tpl, nameCol):
    newDict = {}
    for i in range(len(tpl)):
        newDict[nameCol[i]] = tpl[i]
    return newDict

def listDict(lst, nameCol):
    allUser = []
    for x in lst:
        allUser.append(tuple2dict(x, nameCol))
    return allUser

def api_user_loggin(username, password,user_api):
    for x in user_api:
        if x['MaGV'] == username:
            if x['MatKhau'] == password:
                return x
    return {}

def api_for_admin(conn):
    cur = conn.cursor()
    cur.execute(f"""
        SELECT MaSV, TenSV, TO_CHAR(NgSinh, 'dd-mm-yyyy') AS NgSinh, LopQL, DiaChi, LinkAnh, SDT FROM SINHVIEN;
    """)
    sinhvien = cur.fetchall()

    dictSV = listDict(sinhvien, ['MaSV', 'TenSV', 'NgSinh', 'LopQL', 'DiaChi', 'LinkAnh', 'SDT'])
    # print(dictSV)

    cur.execute(f"""
        SELECT MaGV, TenGV, TO_CHAR(NgSinh, 'dd-mm-yyyy') AS NgSinh, DiaChi, MatKhau, SDT FROM GIAOVIEN;
    """)
    giaovien = cur.fetchall()

    dictGV = listDict(giaovien, ['MaGV', 'TenGV', 'NgSinh', 'DiaChi', 'MatKhau', 'SDT'])
    # print(dictGV)

    cur.execute(f"""
        SELECT * FROM LOPHOC;
    """)
    lophoc = cur.fetchall()

    dictLop = listDict(lophoc, ['MaLop', 'TenMon', 'MaGV', 'LichHoc', 'PhongHoc', 'SoluongSV', 'SoNgay'])
    # print(dictLop)

    cur.execute(f"""
        SELECT * FROM DSLOP;
    """)
    dsLop = cur.fetchall()

    dictDS = listDict(dsLop, ['MaDS', 'MaLop', 'MaSV', 'SoDD'])
    # print(dictDS)

    cur.execute(f"""
        SELECT MaBC, TO_CHAR(NgayBC, 'dd-mm-yyyy HH:MM:SS') AS NgayBC, MaSV, MaLop, DiemDanh, GhiChu FROM BAOCAO;
    """)
    baocao = cur.fetchall()

    dictBC = listDict(baocao, ['MaBC', 'NgayBC', 'MaSV', 'MaLop', 'DiemDanh', 'GhiChu'])

    conn.commit()
    cur.close()
    conn.close()

    json_admin = {}

    json_admin['sinhvien'] = dictSV
    json_admin['giaovien'] = dictGV
    # json_admin['admin'] = dictAdmin
    json_admin['lophoc'] = dictLop
    json_admin['dslop'] = dictDS
    json_admin['baocao'] = dictBC

    return json_admin

def api_for_user_by(conn, magv):

    cur = conn.cursor()
    cur.execute(f"""
        SELECT MaSV, TenSV, TO_CHAR(NgSinh, 'dd-mm-yyyy') AS NgSinh, LopQL, DiaChi, LinkAnh, SDT FROM SINHVIEN
        WHERE MaSV IN (SELECT MaSV FROM DSLOP WHERE MALOP IN (SELECT MALOP FROM LOPHOC WHERE MaGV = '{magv}'));
    """)
    sinhvien = cur.fetchall()

    dictSV = listDict(sinhvien, ['MaSV', 'TenSV', 'NgSinh', 'LopQL', 'DiaChi', 'LinkAnh', 'SDT'])


    cur.execute(f"""
        SELECT MaGV, TenGV, TO_CHAR(NgSinh, 'dd-mm-yyyy') AS NgSinh, DiaChi, MatKhau, SDT FROM GIAOVIEN WHERE MaGV = '{magv}'
    """)
    giaovien = cur.fetchall()

    dictGV = listDict(giaovien, ['MaGV', 'TenGV', 'NgSinh', 'DiaChi', 'MatKhau', 'SDT'])

    cur.execute(f"""
        SELECT * FROM LOPHOC WHERE MAGV = '{magv}';
    """)
    lophoc = cur.fetchall()

    dictLop = listDict(lophoc, ['MaLop', 'TenMon', 'MaGV', 'LichHoc', 'PhongHoc', 'SoluongSV', 'SoNgay'])

    cur.execute(f"""
        SELECT * FROM DSLOP WHERE MALOP IN (SELECT MALOP FROM DSLOP WHERE MALOP IN (SELECT MALOP FROM LOPHOC WHERE MAGV = '{magv}'));
    """)
    dsLop = cur.fetchall()

    dictDS = listDict(dsLop, ['MaDS', 'MaLop', 'MaSV', 'SoDD'])

    cur.execute(f"""
        SELECT MaBC, TO_CHAR(NgayBC, 'dd-mm-yyyy HH:MM:SS') AS NgayBC, MaSV, MaLop, DiemDanh, GhiChu FROM BAOCAO
        WHERE MALOP IN (SELECT MALOP FROM DSLOP WHERE MALOP IN (SELECT MALOP FROM LOPHOC WHERE MAGV = '{magv}'));
    """)
    baocao = cur.fetchall()

    dictBC = listDict(baocao, ['MaBC', 'NgayBC', 'MaSV', 'MaLop', 'DiemDanh', 'GhiChu'])

    cur.execute(f"""
        SELECT SV.MaSV, SV.TenSV, SV.LopQL, DS.MaLop, DS.SoDD FROM SINHVIEN SV INNER JOIN DSLop DS
        ON SV.MaSV = DS.MaSV
        WHERE DS.MaLop IN (SELECT MALOP FROM DSLOP WHERE MALOP IN (SELECT MALOP FROM LOPHOC WHERE MAGV = '{magv}'))
    """)
    baocao_all = cur.fetchall()

    dictBC_all = listDict(baocao_all, ['MaSV', 'TenSV', 'LopQL', 'MaLop', 'DiemDanh'])
    

    conn.commit()
    cur.close()
    conn.close()


    json_user = {}
    json_user['sinhvien'] = dictSV
    json_user['giaovien'] = dictGV
    json_user['lophoc'] = dictLop
    json_user['dslop'] = dictDS
    json_user['baocao'] = dictBC
    json_user['baocao_all'] = dictBC_all
    return json_user

def api_for_admin_A(conn):
    cur = conn.cursor()
    cur.execute(f"""
        SELECT * FROM ADMIN;
    """)
    admin = cur.fetchall()

    dictAdmin = listDict(admin, ['MaAD', 'TenDN', 'MatKhau'])
    # print(dictAdmin)

    cur.execute(f"""
        SELECT MaSV, TenSV, TO_CHAR(NgSinh, 'dd-mm-yyyy') AS NgSinh, LopQL, DiaChi, LinkAnh, SDT FROM SINHVIEN;
    """)
    sinhvien = cur.fetchall()

    dictSV = listDict(sinhvien, ['MaSV', 'TenSV', 'NgSinh', 'LopQL', 'DiaChi', 'LinkAnh', 'SDT'])
    # print(dictSV)

    cur.execute(f"""
        SELECT MaGV, TenGV, TO_CHAR(NgSinh, 'dd-mm-yyyy') AS NgSinh, DiaChi, MatKhau, SDT FROM GIAOVIEN;
    """)
    giaovien = cur.fetchall()

    dictGV = listDict(giaovien, ['MaGV', 'TenGV', 'NgSinh', 'DiaChi', 'MatKhau', 'SDT'])
    # print(dictGV)

    cur.execute(f"""
        SELECT * FROM LOPHOC;
    """)
    lophoc = cur.fetchall()

    dictLop = listDict(lophoc, ['MaLop', 'TenMon', 'MaGV', 'LichHoc', 'PhongHoc', 'SoluongSV', 'SoNgay'])
    # print(dictLop)

    cur.execute(f"""
        SELECT * FROM DSLOP;
    """)
    dsLop = cur.fetchall()

    dictDS = listDict(dsLop, ['MaDS', 'MaLop', 'MaSV', 'SoDD'])
    # print(dictDS)

    cur.execute(f"""
        SELECT MaBC, TO_CHAR(NgayBC, 'dd-mm-yyyy HH:MM:SS') AS NgayBC, MaSV, MaLop, DiemDanh, GhiChu FROM BAOCAO;
    """)
    baocao = cur.fetchall()

    conn.commit()
    cur.close()
    conn.close()

    dictBC = listDict(baocao, ['MaBC', 'NgayBC', 'MaSV', 'MaLop', 'DiemDanh', 'GhiChu'])

    json_admin_A = {}

    json_admin_A['sinhvien'] = dictSV
    json_admin_A['giaovien'] = dictGV
    json_admin_A['admin'] = dictAdmin
    json_admin_A['lophoc'] = dictLop
    json_admin_A['dslop'] = dictDS
    json_admin_A['baocao'] = dictBC

    return json_admin_A

def update_dd_student(conn, msv, malop):
    cur = conn.cursor()
    cur.execute(f"""
        UPDATE DSLop SET SoDD = (
            SELECT count(*) FROM BAOCAO 
            WHERE MaSV = '{msv}' AND MaLop = '{malop}' AND DIEMDANH = '1' 
        )
        WHERE MaSV = '{msv}' AND MaLop = '{malop}'
    """)
    conn.commit()
    cur.close()
    conn.close()

def id_bao_cao_generated(conn):
    cur = conn.cursor()
    cur.execute(f"""
        SELECT MaBC FROM BAOCAO;
    """)
    list_MaBC = list(cur.fetchall())
    list_numMaBC = [x[0].split("BC")[-1] for x in list_MaBC]
    num_generate = -1
    for i, maBC in enumerate(list_numMaBC):
        if not int(maBC.split("BC")[-1]) == i + 1:
            num_generate = i + 1
            break
    if num_generate == -1:
        num_generate = len(list_numMaBC) + 1
    return "BC{:08d}".format(num_generate)

def time_bao_cao_generated():
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")

def post_bao_cao(conn, masv, malop, ghichu):
    cur = conn.cursor()
    cur.execute(f"""
        INSERT INTO BAOCAO (MaBC, NgayBC, MaSV, MaLop, DiemDanh, GhiChu)
        VALUES 
        ('{id_bao_cao_generated(conn)}', '{time_bao_cao_generated()}', '{masv}', '{malop}', 1, '{ghichu}');
    """)

def update_report_student(conn, malop):
    cur = conn.cursor()
    cur.execute(f"""
        UPDATE DSLOP
        SET SoDD = (
        SELECT COUNT(*)
        FROM BAOCAO
        WHERE MASV = DSLOP.MASV
            AND MALOP = '{malop}'
            AND DIEMDANH = '1'
        )
        WHERE DSLOP.MALOP = '{malop}';
    """)
    conn.commit()
    cur.close()
    conn.close()
