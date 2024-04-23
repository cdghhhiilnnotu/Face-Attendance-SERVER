import psycopg2
import json
import sys
sys.path.insert(0, '..\\')
from commons.helper import *

def get_connection():
    conn = psycopg2.connect(host="localhost", dbname="HAU-FACE-DB", user="postgres",
                        password="1009", port=5432)
    conn.set_client_encoding('UTF8')
    return conn

def get_json_admin_A():
    conn = get_connection()
    # cur = conn.cursor()
    return api_for_admin_A(conn) 

def get_json_admin():
    conn = get_connection()
    # cur = conn.cursor()
    return api_for_admin(conn)

def get_json_user(username):
    conn = get_connection()
    # cur = conn.cursor()
    return api_for_user_by(conn, username)

def post_diem_danh(masv, malop, ghichu):
    conn = get_connection()
    post_bao_cao(conn, masv, malop, ghichu)
    update_dd_student(conn, masv, malop)

def update_all_bao_cao(malop):
    conn = get_connection()
    update_report_student(conn, malop)

def execute_SQL(sql_query):
    conn = get_connection() 
    cur = conn.cursor()
    cur.execute(sql_query)
    conn.commit()
    cur.close()
    conn.close()

# with open("full-api.json", "w", encoding='utf-8') as outfile:
#     json.dump(jsonDict, outfile,ensure_ascii=False)

# conn.commit()
# cur.close()
# conn.close()


