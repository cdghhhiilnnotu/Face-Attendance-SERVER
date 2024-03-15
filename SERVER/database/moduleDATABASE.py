import psycopg2
import json
import sys
sys.path.insert(0, '..\\')
from commons.helper import listDict

conn = psycopg2.connect(host="localhost", dbname="HAU-FACE-DATABASE", user="postgres",
                        password="1009", port=5432)
conn.set_client_encoding('UTF8')

cur = conn.cursor()

cur.execute(f"""
    SELECT MSV, TenSV, TO_CHAR(NgSinh, 'dd-mm-yyyy') AS NgSinh, LopQL, DiaChi, LinkAnh, SDT FROM SINHVIEN;
""")
sinhvien = cur.fetchall()

dictSV = listDict(sinhvien, ['MSV', 'TenSV', 'NgSinh', 'LopQL', 'DiaChi', 'LinkAnh', 'SDT'])
# print(dictSV)

cur.execute(f"""
    SELECT * FROM ADMIN;
""")
admin = cur.fetchall()

dictAdmin = listDict(admin, ['MaAD', 'TenDN', 'MatKhau'])
# print(dictAdmin)

cur.execute(f"""
    SELECT MGV, TenGV, TO_CHAR(NgSinh, 'dd-mm-yyyy') AS NgSinh, DiaChi, MatKhau, SDT FROM GIAOVIEN;
""")
giaovien = cur.fetchall()

dictGV = listDict(giaovien, ['MGV', 'TenGV', 'NgSinh', 'DiaChi', 'MatKhau', 'SDT'])
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

dictds = listDict(dsLop, ['MaDS', 'MaLop', 'MaSV', 'SoDD'])
# print(dictds)

cur.execute(f"""
    SELECT MaBC, TO_CHAR(NgayBC, 'dd-mm-yyyy HH:MM:SS') AS NgayBC, MaSV, MaLop, DiemDanh, GhiChu FROM BAOCAO;
""")
baocao = cur.fetchall()

dictBC = listDict(baocao, ['MaBC', 'NgayBC', 'MaSV', 'MaLop', 'DiemDanh', 'GhiChu'])
# print(dictBC[0])

jsonDict = {}

jsonDict['sinhvien'] = dictSV
jsonDict['giaovien'] = dictGV
jsonDict['admin'] = dictAdmin
jsonDict['lophoc'] = dictLop
jsonDict['dslop'] = dictds
jsonDict['baocao'] = dictBC

# with open("full-api.json", "w", encoding='utf-8') as outfile:
#     json.dump(jsonDict, outfile,ensure_ascii=False)

conn.commit()
cur.close()
conn.close()


