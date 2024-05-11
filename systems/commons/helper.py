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

def api_admin_loggin(username, password,user_api):
    for x in user_api:
        if x['MaAD'] == username:
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

    cur.execute(f"""
        SELECT MaAD, TenDN, MatKhau FROM ADMIN;
    """)
    admin = cur.fetchall()

    dictAdmin = listDict(admin, ['MaAD', 'TenDN', 'MatKhau'])

    conn.commit()
    cur.close()
    conn.close()

    json_admin = {}

    json_admin['sinhvien'] = dictSV
    json_admin['giaovien'] = dictGV
    json_admin['admin'] = dictAdmin
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

    cur.execute(f"""
        SELECT SV.MaSV, SV.TenSV, SV.LopQL, DS.MaLop, TO_CHAR(DS.NgayBC, 'dd-mm-yyyy HH:MM:SS') AS NgayBC, DS.GhiChu FROM SINHVIEN SV INNER JOIN BAOCAO DS
        ON SV.MaSV = DS.MaSV
        WHERE DS.MaLop IN 
        (SELECT MALOP FROM DSLOP WHERE MALOP IN 
        (SELECT MALOP FROM LOPHOC WHERE MAGV = '{magv}'))
    """)
    baocao_detail = cur.fetchall()

    dictBC_detail = listDict(baocao_detail, ['MaSV', 'TenSV', 'LopQL', 'MaLop', 'DiemDanh', 'GhiChu'])

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
    json_user['baocao_detail'] = dictBC_detail
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
        SELECT MaBC FROM BAOCAO ORDER BY MaBC;
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

def id_admin_generated(conn):
    cur = conn.cursor()
    cur.execute(f"""
        SELECT MaAD FROM ADMIN ORDER BY MaAD;
    """)
    list_MaAD = list(cur.fetchall())
    list_numMaAD = [x[0].split("AD")[-1] for x in list_MaAD]
    num_generate = -1
    for i, maAD in enumerate(list_numMaAD):
        if not int(maAD.split("AD")[-1]) == i + 1:
            num_generate = i + 1
            break
    if num_generate == -1:
        num_generate = len(list_numMaAD) + 1
    return "AD{:08d}".format(num_generate)

def time_bao_cao_generated():
    now = datetime.now()
    print(now)
    print(now.strftime("%Y-%m-%d %H:%M:%S"))
    return now.strftime("%Y-%m-%d %H:%M:%S")

def id_danh_sach_generated(conn):
    cur = conn.cursor()
    cur.execute(f"""
        SELECT MaDS FROM DSLOP ORDER BY MaDS;
    """)
    list_MaDS = list(cur.fetchall())
    list_numMaDS = [x[0].split("DS")[-1] for x in list_MaDS]
    num_generate = -1
    for i, MaDS in enumerate(list_numMaDS):
        if not int(MaDS.split("DS")[-1]) == i + 1:
            num_generate = i + 1
            break
    if num_generate == -1:
        num_generate = len(list_numMaDS) + 1
    return "DS{:08d}".format(num_generate)

def id_giang_vien_generated(conn):
    cur = conn.cursor()
    cur.execute(f"""
        SELECT MaGV FROM GIAOVIEN ORDER BY MaGV;
    """)
    list_MaGV = list(cur.fetchall())
    list_numMaGV = [x[0].split("GV")[-1] for x in list_MaGV]
    num_generate = -1
    for i, maGV in enumerate(list_numMaGV):
        if not int(maGV.split("GV")[-1]) == i + 1:
            num_generate = i + 1
            break
    if num_generate == -1:
        num_generate = len(list_numMaGV) + 1
    return "GV{:08d}".format(num_generate)

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
