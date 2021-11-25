import requests
import json
import base64
import hmac
import hashlib
import datetime, time

production = False
base_url = "https://api.gemini.com" if production else "https://api.sandbox.gemini.com"
endpoint = "/v1/order/new"
url = base_url + endpoint

gemini_api_key = "insert production key" if production else "account-NKVDNTSKjgpRLhX8w5fk"
gemini_api_secret = ("insert production secret" if production else "daz6CVKPVidwfpawpaxL7rC7mFn").encode()
def trans(ticket):
    t = datetime.datetime.now()
    payload_nonce =  str(int(time.mktime(t.timetuple())*1000))
    payload = {
    "request": "/v1/order/new",
        "nonce": payload_nonce,
        "symbol": ticket.symbol,
        "amount": ticket.amount,
        "price": ticket.price,
        "side": ticket.side,
        "type": "exchange limit",
        "options": ["fill-or-kill"] 
    }

    encoded_payload = json.dumps(payload).encode()
    b64 = base64.b64encode(encoded_payload)
    signature = hmac.new(gemini_api_secret, b64, hashlib.sha384).hexdigest()

    request_headers = { 'Content-Type': "text/plain",
                        'Content-Length': "0",
                        'X-GEMINI-APIKEY': gemini_api_key,
                        'X-GEMINI-PAYLOAD': b64,
                        'X-GEMINI-SIGNATURE': signature,
                        'Cache-Control': "no-cache" }

    response = requests.post(url,
                            data=None,
                            headers=request_headers)
    new_order = response.json()
    print(new_order)