
from requests import request
import urllib
import json
import hashlib
import hmac
import base64
import time
from datetime import datetime, timedelta

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

def get_res_file_name():
    return "ByM_update_response_{}.txt".format(datetime.now().strftime("%Y%m%d_%H%M%S"))

def get_prams_status(AWSAccessKeyId, Secre_Key, MWSAuthToken, SellerId, FeedSubmissionId, MarketplaceIdList):
    r_fname = "MWS_responce_{}.xlsx".format(iso8601timestamp())
    Secre_Key = Secre_Key #"a5Y0LP0n94U3JUeg1AWUmz45qEhbn2x09f/2ilHi"
    HTTPVerb = "POST"
    Protoc = "https://"
    MWSEndpoints = {"DE":"mws-eu.amazonservices.com","GB":"mws-eu.amazonservices.com",
                    "FR":"mws-eu.amazonservices.com", "IT":"mws-eu.amazonservices.com",
                    "ES":"mws-eu.amazonservices.com", "NL": "mws-eu.amazonservices.com"
                    }

    MWSHost = MWSEndpoints["DE"].lower()
    HTTPRequestURI = "/Feeds/2009-01-01"
    url = Protoc + MWSHost + HTTPRequestURI

    params = {}
    params["AWSAccessKeyId"] = AWSAccessKeyId
    params["MWSAuthToken"] = MWSAuthToken
    params["SellerId"] = SellerId
    params["SignatureMethod"] = "HmacSHA256"
    params["SignatureVersion"] = "2"
    params["Timestamp"] = iso8601timestamp()        #   Create and Add ISO-8601 Timestamp to <params>
    params["Version"] = "2009-01-01"
    params["Action"] = "GetFeedSubmissionResult"
    params["FeedSubmissionId"] = FeedSubmissionId
    params["MarketplaceIdList.Id.1"] = MarketplaceIdList
    params["PurgeAndReplace"] = "false"

    CanonicKV = canonic_query_str(params)
    StrToSign = "{}\n{}\n{}\n{}".format(HTTPVerb,MWSHost, HTTPRequestURI, CanonicKV)
    params["Signature"] = get_SHA256(StrToSign, Secre_Key)  #   Create Signature (Base64-Hmac-SHA256) of StrToSign

    #   Create HTTP Header
    headers = {}
    headers["User-Agent"] = "SareKaya/amws.app.adebayoea0.1 (Language=Python/3.8; Platform=Windows/10/pro)"
    headers["Content-Type"] = "application/x-www-form-urlencoded"
    headers["Host"] = MWSHost

    #   Query request
    print("sending request...\n\n")

    r = request(HTTPVerb, url, params = params, headers = headers)
    print(r.status_code)
    print(type(r.status_code))
    print(r.headers)
    print(type(r.headers))
    print("\n" + r.text + "\n" )

    res_file_name = get_res_file_name()
    with open(res_file_name, 'wb') as f:
        for chunk in r.iter_content(chunk_size=256):
            f.write(chunk)

    return f
