import requests

api_id = "b2e4769a"
api_key = "ebb05e24a1f6b55f2f229af673c8ed2a"

mealdict = {"B": "Breakfast", "L": "Lunch", "D": "Dinner", "S": "Snack"}
dishdict = {"M": "Main%20course", "P": "Desserts", "D": "Drinks"}
query = input("Enter some ingredients you want your recipe to have:  ")
meal = input("Pick a meal type; Breakfast (B), Lunch (L), Dinner (D), Snack ("
             "S):  ")
meal = mealdict[meal[0].upper()]
dish = input("Pick a dish type; Main course (M), Pudding (P), Drink (D):   ")
dish = dishdict[dish[0].upper()]
request = requests.get("https://api.edamam.com/api/recipes/v2?type=public&q"
                       "=" + query + "&app_id=" + api_id + "&app_key=" + api_key
                       + "&dishType="+dish+"&mealType="+meal)

request = request.json()
links = []
for item in request["hits"]:
    print(item["recipe"]["url"])
print(links)

print(request)
