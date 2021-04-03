from requests import request
import urllib
import json
import hashlib
import hmac
import base64
import time
from datetime import datetime, timedelta

def readfile(feed_doc):
    """Calculate "message digest" of a file. This function takes in filepath as string"""
    with open(feed_doc, "rb") as doc:
        doc_content = doc.read()
        return doc_content

def get_md5(file_path):
    """Calculate "message digest" of a file. This function takes in string"""
    content = readfile(file_path)
    hasher = hashlib.md5()
    hasher.update(content)
    return  base64.b64encode(hasher.digest()).decode("utf-8")

def get_SHA256(str_val, sec_key):
    """ Calculate Hmac SHA256 "message digest" of a string with secret key.
    This function takes in Two parameters of type string value"""
    str_val = bytes(str_val, 'utf-8')
    sec_key = bytes(sec_key, 'utf-8')
    signature = base64.b64encode(hmac.new(sec_key, msg = str_val, digestmod = hashlib.sha256).digest())
    return signature.decode("utf-8")

def canonic_query_str(dict):
    """returns canonical string"""
    LstKV = []
    for key in sorted(dict):
        LstKV.append((key,dict[key]))
    params = urllib.parse.urlencode(LstKV, quote_via=urllib.parse.quote)
    return params

def iso8601timestamp():
    current_time = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")
    timestamp = current_time[:-4] + "Z"
    return timestamp

def readlinefile(fn):
    db = open(fn,"r", encoding='utf-8', errors='ignore')
    return db.readlines()

def get_flat_file_name():
    return "OGK_update_requestbody{}.txt".format(datetime.now().strftime("%Y%m%d_%H%M%S%f"))

def get_res_file_name():
    return "OGK_update_response_{}.txt".format(datetime.now().strftime("%Y%m%d_%H%M%S"))

def create_upload_file(dbf_name, f_row):
    chunk_size = 500 #***1     enter amount of product items. type int()
    chunk_start_position = 3 #***2     enter row num of the first item. type int()
    chunk_end_position = chunk_start_position + chunk_size
    db_file = readlinefile(dbf_name)
    print(len(db_file)-chunk_start_position)
    file_writen_count = 0
    flat_file_names = {}
    while chunk_size > 0:
        if chunk_end_position < len(db_file):
            flat_file_name = get_flat_file_name()
            print(flat_file_name)
            wfile = open(flat_file_name,"w", encoding='utf-8', errors='ignore')
            for line in db_file[:3]:
                wfile.write(line)
            if file_writen_count < 1:
                for line in db_file[chunk_start_position : chunk_end_position]:
                    wfile.write(line)
                wfile.close()
                print("a")
                print(chunk_end_position - f_row)
                file_writen_count = file_writen_count + 1
                chunk_start_position = chunk_start_position + chunk_size
                chunk_end_position = chunk_end_position + chunk_size
                time.sleep(4)
                flat_file_names[flat_file_name] = get_md5(flat_file_name)
                print(flat_file_names[flat_file_name])
                time.sleep(1)
            else:
                for line in db_file[chunk_start_position : chunk_end_position]:
                    wfile.write(line)
                wfile.close()
                print("b")
                print(chunk_end_position - f_row)
                file_writen_count = file_writen_count + 1
                chunk_start_position = chunk_start_position + chunk_size
                chunk_end_position = chunk_end_position + chunk_size
                time.sleep(4)
                flat_file_names[flat_file_name] = get_md5(flat_file_name)
                print(flat_file_names[flat_file_name])
                time.sleep(1)
        else:
            flat_file_name = get_flat_file_name()
            print(flat_file_name)
            wfile = open(flat_file_name,"w")
            for line in db_file[:3]:
                wfile.write(line)
            for line in db_file[chunk_start_position : ]:
                wfile.write(line)
            wfile.close()
            print("c")
            print(len(db_file)-f_row)
            flat_file_names[flat_file_name] = get_md5(flat_file_name)
            print(flat_file_names[flat_file_name])
            chunk_size = 0
        #print(flat_file_names)
    return flat_file_names

field_row = 3 #***3     enter number of field rows. type int()
fname = "filename.txt" #***4     enter filename for upload. type str()


flat_file_names = create_upload_file(fname,field_row)
r_fname = "MWS_responce_{}.xlsx".format(iso8601timestamp())

# flat_file_names = create_upload_file(fname, field_row, chunk_size, chunk_start_postion,)