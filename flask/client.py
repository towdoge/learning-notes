import requests
import socket
import json
# res = socket.gethostbyname(socket.gethostname())
# print(res)
res = '10.7.71.113'

# send request post to res
# user_info = {"logId": "111"}
# user_info = json.dumps(user_info)
# print(user_info)
# r = requests.post("http://{}:7399/post/post/copyFile".format(res), data=user_info)
# get return info from server.py
# print(r.text)


r = requests.post("http://{}:7399/post/run".format(res), data='10086')
print(r.text)
