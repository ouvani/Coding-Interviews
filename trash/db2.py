from typing import Any, Dict
import copy

class InMemoryDB3:
  def __init__(self):
    self.db: dict[str, dict[str, Any]] = {}
    self.snapshots: dict[int, dict[str, dict[str, Any]]] = {}

  def set(self, key:str, value: str, meta: Any) -> None:
    self.db.setdefault(key, {})[value] = meta

  def get(self, key:str, value:str) -> Any | None:
    if key in self.db and value in self.db[key]:
      return self.db[key][value]
    return None
  
  def delete(self, key:str, value:str) -> bool:
    if key in self.db and value in self.db[key]:
      del self.db[key][value] 

      if not self.db[key]:
        del self.db[key]
      return True
    return False

  def scan(self, key: str) -> list[str]:
    if key not in self.db:
      return []

    sort = sorted(self.db[key].items())
    return [f"{k} ({v})" for k, v in sort]
  
  def scan_by_prefix(self, key:str, pre:str):
    if key not in self.db:
      return []

    sort = sorted(self.db[key].items())
    result = [f"{field} ({meta})" for field, meta in sort 
        if field.startswith(pre) 
      ]
    return result
  
#PART 3

  def set_at(self, key:str, field:str, val:Any, start:int, ttl:int ) -> None:
    self.db.setdefault(key, {})[field] = {"val": val, "start": start, "ttl": ttl}
  

  def is_expired(self, meta:dict[str, Any], timestamp:int) -> bool:
    if timestamp >= meta["start"] + meta["ttl"]:
      return True
    return False

  def clean(self, key:str, timestamp:int):
    if key not in self.db:
      return 
    
    to_delete =[
      field for field, meta in self.db[key].items()
      if self.is_expired(meta, timestamp)
    ]

    for entry in to_delete:
      del self.db[key][entry]
    if not self.db[key]: # drop-level empty key
      del self.db[key]

  def get_at(self, key:str, field:str, timestamp:int) -> Any | None:
    self.clean(key, timestamp)

    result = self.get(key, field)

    if not result:
      return None
    return result["val"]
  
  def delete_at(self, key:str, field:str, timestamp:int) -> bool:
    self.clean(key, timestamp)
    return self.delete(key, field)
    

  def backup(self, t_backup:int) -> None:
    self.snapshots[t_backup] = copy.deepcopy(self.db)
  
  def restore(self, t_backup:int, t_now:int) -> None:
    if t_backup not in self.snapshots:
      return
    
    for key, field in list(self.db.items()):
      for field, meta in list(field.items()):
        elasped = t_backup - meta["start"]
        remaining = max(meta["ttl"] - elasped, 0)

        meta["start"] = t_now
        meta["ttl"] = remaining

        if remaining <= 0:
          del self.db[key][field]

      if not self.db[key]:
          del self.db[key]

    
    
      



    
def main():
  db = InMemoryDB3()
  """
  db.set("user1", "name", "Alice")
  print(db.get("user1", "name"))          # → Alice
  print(db.delete("user1", "name"))       # → True
  print(db.get("user1", "name"))          # → None

  db = InMemoryDB3()
  db.set("user1", "age", "30")
  db.set("user1", "email", "alice@example.com")
  db.set("user1", "name", "Alice")
  db.set("user1", "eggs", "bacon")

  print(db.scan("user1"))
  # → ['age(30)', 'email(alice@example.com)', 'name(Alice)']

  print(db.scan_by_prefix("user1", "e"))
  # → ['email(alice@example.com)']

  db.set_at("sess", "token", "abc123", 100, 10)

  print(db.get_at("sess", "token", timestamp=105))   # -> abc123
  print(db.get_at("sess", "token", timestamp=111))   # -> None (expired)
  print(db.delete_at("sess", "token", timestamp=112))  # -> False 
  
  """

  # Populate a few entries with TTL
  db.set_at("u1", "sess", "xyz", start=10, ttl=100)   # expires at 110
  db.set_at("u1", "temp", "tmp", start=20, ttl=30)   # expires at 50

  # Take a snapshot at time 40
  db.backup(40)

  # Fast‑forward time, change the DB, then restore to the snapshot
  db.set_at("u1", "new", "value", start=45, ttl=20)
  print(db.get_at("u1", "new", timestamp=46))   # -> value

  # Restore to snapshot taken at 40, pretending "now" is 200
  db.restore(t_backup=40, t_now=200)

  # After restore:
  print(db.get_at("u1", "sess", timestamp=210))   # still alive (remaining 90)
  print(db.get_at("u1", "temp", timestamp=210))   # None (already expired at restore)
  print(db.get_at("u1", "new", timestamp=210))    # None (field didn't exist in snapshot)



  print()

if __name__ == "__main__":
  main()