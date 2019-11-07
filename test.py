import sys

uri = 'creds.html?ssid=circuitspecialists.com&password=c%21rcu%21t%21'
special_char_start = uri.find('%')
special_char = uri[special_char_start:special_char_start + 3]
uri = uri.replace(special_char, bytearray.fromhex(special_char.replace('%', '')).decode())
print(uri)
special_char_start = uri.find('%')


sys.exit()
while(special_char_start != ''):
    special_char = uri[special_char_start:special_char_start + 3]
    uri.replace(special_char, bytearray.fromhex(special_char.replace('%', '')).decode())
    print(uri)
    special_char_start = uri.find('%')

print(uri)