"""
Example call to the API
"""
import http.client
import json
#
# conn = http.client.HTTPSConnection("api.aigcbest.top")
# payload = json.dumps({
#    "model": "moonshot-v1-128k",
#    "messages": [
#       {
#          "role": "user",
#          "content": "Hello!"
#       }
#    ]
# })
# headers = {
#    'Accept': 'application/json',
#    'Authorization': 'Bearer <API-key>',
#    'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
#    'Content-Type': 'application/json'
# }
# conn.request("POST", "/v1/chat/completions", payload, headers)
# res = conn.getresponse()
# data = res.read()
# print(data.decode("utf-8"))
# print("-" * 25)
# data_dict = json.loads(data)
# print(data_dict)
# print("-" * 25)
# print(data_dict.get('choices')[0].get('message').get('content'))
# print(data_dict.get('usage'))


"""
Check available models
"""
import http.client

conn = http.client.HTTPSConnection("api.aigcbest.top")
payload = ''
headers = {
   'Authorization': 'Bearer <API-key>',
   'User-Agent': 'Apifox/1.0.0 (https://apifox.com)'
}
conn.request("GET", "/v1/models", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))