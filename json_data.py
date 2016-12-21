import json;

file = open("data.json","r");
k = file.read();
js = json.loads(k)
print js["queue"]
print js["domain"]