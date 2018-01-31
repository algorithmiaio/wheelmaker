import tinys3
import sys

access_key_id = ''
secret_access_key = ''
conn = tinys3.Connection(access_key_id, secret_access_key, tls=True)

if __name__=="__main__":
    f = open(sys.argv[1], 'rb')
    conn.upload(sys.argv[1], f, sys.argv[2])
