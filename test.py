import json

import requests

token = "0F8ofm1AYuuCiIU9uimnq4fnqsm7905zacLkeEmC2rDLgAYVYwsIE9fgAUPNaagQ"

# it = json.dumps(
#     {
#         "token": token,
#         "data": [
#             {
#                 "product_id": 1,
#                 "name": "23",
#                 "image": "2e",
#                 "price": 1243
#             }
#         ]
#     }
# )
# print(it)
#
# response = requests.post(
#     "http://127.0.0.1:814/products/add",
#     data=it
# )
#
# print(response.text)

# response = requests.post("http://127.0.0.1:8000/register", data = json.dumps({
#     "token": token,
#     "username": "sad21eaf",
#     "user_id": 1234
# }))

# response = requests.post("http://127.0.0.1:814/products/delete", data=json.dumps({"token": token, "product_id": 1}))

response = requests.get("http://192.168.52.80/products/all")

print(response.text)
