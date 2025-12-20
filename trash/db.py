class InMemoryDBLevel1:
    def __init__(self):
        self.store:  dict[str, dict[str,str]] = {}
    def set(self, key:str, field:str, value:str) -> None:
        if key not in self.store:
            self.store[key] = {}
        self.store[key][field]= value
    def get(self, key:str, field:str) -> str|None:
            return self.store.get(key, {}).get(field)
    def delete(self, key:str, field:str) -> bool:
        if key in self.store and field in self.store[key]:
            del self.store[key][field] #delete sub tree
            if not self.store[key]: #delete empty field with useless key
                del self.store[key]
            return True
        return False
    def scan(self, key:str) -> list[str]:
        if key not in self.store:
            return []
        sorted_items = sorted(self.store[key].items())
        results = [f"{key}({value})" for key , value in sorted_items]
        return results
    def scan_by_prefix(self, key:str, prefix:str) -> list[str]:
        if key not in self.store:
            return []
        
        sorted_items = sorted(self.store[key].items()) 
        
        filtered =[
            (field, value) for field, value in sorted_items
            if field.startswith(prefix)
        ]
        
        return [f"{key}({value})" for key, value in filtered]
    

def main():
    db = InMemoryDBLevel1()
    db.set("user1", "name", "Alice")
    print(db.get("user1", "name"))          # → Alice
    print(db.delete("user1", "name"))       # → True
    print(db.get("user1", "name"))          # → None

    db = InMemoryDBLevel1()
    db.set("user1", "age", "30")
    db.set("user1", "email", "alice@example.com")
    db.set("user1", "name", "Alice")

    print(db.scan("user1"))
    # → ['age(30)', 'email(alice@example.com)', 'name(Alice)']

    print(db.scan_by_prefix("user1", "e"))
    # → ['email(alice@example.com)']

if __name__ == "__main__":
    main()