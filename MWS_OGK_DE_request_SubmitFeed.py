from requests import request
import xml.etree.ElementTree as ET
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
    db = open(fn,"r")
    return db.readlines()

def get_flat_file_name():
    return "OGK_update_requestbody{}.txt".format(datetime.now().strftime("%Y%m%d_%H%M%S%f"))

def get_res_file_name():
    return "OGK_update_response_{}.txt".format(datetime.now().strftime("%Y%m%d_%H%M%S"))

def create_upload_file(dbf_name,f_row):
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
            wfile = open(flat_file_name,"w")
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
Secre_Key = "the secret key goes here" #***5     seller account secret key here. type str()
HTTPVerb = "POST"
Protoc = "https://"
MWSEndpoints = {"DE":"mws-eu.amazonservices.com","GB":"mws-eu.amazonservices.com",
                "FR":"mws-eu.amazonservices.com", "IT":"mws-eu.amazonservices.com",
                "ES":"mws-eu.amazonservices.com", "NL": "mws-eu.amazonservices.com"
                }

MWSHost = MWSEndpoints["DE"].lower()
HTTPRequestURI = "/Feeds/2009-01-01"
url = Protoc + MWSHost + HTTPRequestURI

#def get_params()
for f_fname in flat_file_names:
    params = {}
    params["AWSAccessKeyId"] = "enter access key here" #***6     Access key here. type str()
    params["MWSAuthToken"] = "enter auth token value here" #***7     Authentication token here. type str()
    params["SellerId"] = "enter seller id here" #***8    enter seller id here. type str()
    params["SignatureMethod"] = "HmacSHA256"
    params["SignatureVersion"] = "2"
    params["Timestamp"] = iso8601timestamp()        #   Create and Add ISO-8601 Timestamp to <params>
    params["Version"] = "2009-01-01"
    params["Action"] = "SubmitFeed"
    params["FeedType"] = "_POST_FLAT_FILE_LISTINGS_DATA_"
    params["MarketplaceIdList.Id.1"] = "A1PA6795UKMFR9"
    params["PurgeAndReplace"] = "false"
    params["ContentMD5Value"] = flat_file_names[f_fname]    #   Create Base64 MD5-hash of FeedContent
#    print(params["ContentMD5Value"] +"\n")

    CanonicKV = canonic_query_str(params)
    StrToSign = "{}\n{}\n{}\n{}".format(HTTPVerb,MWSHost, HTTPRequestURI, CanonicKV)
#    print(StrToSign + "\n")
    params["Signature"] = get_SHA256(StrToSign, Secre_Key)  #   Create Signature (Base64-Hmac-SHA256) of StrToSign
    #print(params["Signature"])

#   Create HTTP Header
    headers = {}
    headers["User-Agent"] = "Online-GalleryKing/amws.app.adebayoea0.1 (Language=Python/3.8; Platform=Windows/10/pro)"
    headers["Content-Type"] = "application/x-www-form-urlencoded"
    headers["Host"] = MWSHost
    headers["ContentMD5Value"] = params["ContentMD5Value"]

#   Query request
    print("sending request...\n\n")

    r = request(HTTPVerb, url, params = params, data = readfile(f_fname), headers = headers)
    print(r.status_code)
    print(type(r.status_code))
    print(r.headers)
    print(type(r.headers))
    print("\n" + r.text + "\n" )
    r_content = r.content
    #print(r_content.decode("utf-8"))

    res_file_name = get_res_file_name()
    with open(res_file_name, 'wb') as f:
        for chunk in r.iter_content(chunk_size=256):
            f.write(chunk)
    
    res_file_tree = ET.parse(res_file_name)
    res_file_root = res_file_tree.getroot()

    
    FeedSubmissionId = res_file_root[0][0][0].text #**** Submission Id <------Emmanuel this is new field
    FeedProcessingStatus = res_file_root[0][0][3].text.strip("_") #**** Processing Status  <------Emmanuel this is new field

    wait_time = 20 #***9    interface for time before next upload. type int()
    dt = datetime.now() + timedelta(minutes = wait_time)
    #wait_time_count = 0
    while datetime.now() < dt:
        print("\nHochladen erfolgreich!")
        time.sleep(310)
        wait_time = wait_time - 5
        print("\n\n...The next upload will start in {} minutes.".format(wait_time))
        print("\ngoin to sleep...", datetime.now().strftime("%Y-%m-%dT%H:%M:%S"))
    print("#\n#\n#\nThe next upload is now being sent...")
print("All data have been processed!")
