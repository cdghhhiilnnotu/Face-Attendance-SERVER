import psycopg2
import json
import sys
sys.path.insert(0, '..\\')
from commons.helper import listDict, api_for_admin, api_for_user_by, api_for_admin_A

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


# with open("full-api.json", "w", encoding='utf-8') as outfile:
#     json.dump(jsonDict, outfile,ensure_ascii=False)

# conn.commit()
# cur.close()
# conn.close()


