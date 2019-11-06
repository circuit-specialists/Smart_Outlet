import json

f = open('client_response.txt','r', encoding='utf-16')
temp = f.read()
f.close()
temp = temp.replace('\r', '').replace('\n\n\n\n', '').replace('\n\n', '\", ').replace(': ', '\": \"').replace('\n', '\"')
temp = temp[temp.find("Host") - 1: -3]
dict = "{" + temp + "}"
dict = json.loads(dict)
print(dict["Referer"])