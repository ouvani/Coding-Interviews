from collections import defaultdict;
def candy():
    def tree():
      return defaultdict(tree)
    database = tree()
    database["chocolate"]["snickers"] = 1.5
    database["chocolate"]["twix"] = 1.2
    database["chocolate"]["mars"] = 1.3
    database["chocolate"]["kitkat"] = 1.0
    database["gummy"]["bears"] = 0.5
    database["gummy"]["worms"] = 0.7
    database["lollipop"]["cherry"] = 0.3
    database["lollipop"]["grape"] = 0.4
    
    #print(database.items())

    prefixes = ["gu", "lo"]
    tuple_pre = tuple(prefixes) # ("gu", "lo") 

    filtered = { key: value for key, value in database.items()
                 if any(key.startswith(p) for p in prefixes) }
    #print(filtered)

    filtered = {key : value for key, value in database.items()
                if any( p in key for p in tuple_pre)}
    #print(filtered)
    

    fields = sorted(database["chocolate"].items())
    res = [f"{name}: ${price:.2f}" for name, price in fields
           if any(c in name for c in "tk")]
    print(res)
    return database

    d = {}
    d.setdefault("outer", {})["inner"] = 0

def social():
    def tree():
        return defaultdict(tree)
    users = tree()
    users ["tommy"] = {"name": "tommy", "age": 30, "location": "NYC"}
    users ["sally"] = {"name": "sally", "age": 25, "location": "LA"}
    users ["jimmy"] = {"name": "jimmy", "age": 35, "location": "Chicago"}

    for key , value in users.items():
        key[value]




def main():
    """ #basic crud
    recipes = {"pancakes": "Flour, Eggs, Milk, Sugar, Baking Powder", "omelette": "Eggs, Salt, Pepper, Cheese", "salad": "Lettuce, Tomato, Cucumber, Olive Oil, Lemon Juice", "spaghetti": "Spaghetti, Tomato Sauce, Garlic, Olive Oil, Basil"}

    recipes["cake"] = "Flour, Sugar, Eggs, Butter, Baking Powder"
    print(recipes) #set
    del recipes["omelette"] #delete
    print(recipes)
    
    k = recipes.keys()
    v = recipes.values()
    if "omelette" not in recipes:
        print("Entry was deleted") """
    
    candy()
      
if __name__ == "__main__":
    main()