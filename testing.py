import requests
api_id="b2e4769a"
api_key="ebb05e24a1f6b55f2f229af673c8ed2a"
query=input("Enter a query:  ")
request = requests.get("https://api.edamam.com/api/recipes/v2?type=public&q"
                       "="+query+"&app_id="+api_id+"&app_key="+api_key)
request=request.json()
links=[]
print(type(request), type(request["hits"]))
for item in request["hits"]:
    print(item["recipe"]["url"])
print(links)

print(request)