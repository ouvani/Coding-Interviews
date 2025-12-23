
class InMemoryDBLevel3:
  def __init__(self):
    self.store: dict[str, dict[str, Any]] = {}

  def set_at_with_ttl(self, key:str, field:str, value: str, start:int, ttl:int) ->None:
    if key not in self.store:
      self.store[key]= {"field": field, "val": value,"start":start, "ttl":ttl}
    self.store[key] = {"val": value,"start":start, "ttl":ttl}
  def get_at(self, key:str, field:str, timestamp:int) -> str |None:
    self.clean_up(key, field, timestamp)
    if not self.store[key]:
      return f"{key}, {field}, {self.store[key].values()}" 
    
  def clean_up(self, key:str, field:str, timestamp:int) -> None:
    if timestamp >= self.store[key]["start"] + self.store[key]["ttl"]:
      del self.store[key]
  def delete_at(self, key:str, field:str, timestamp:int):
    self.clean_up(key, field, timestamp)
    if not self.store[key]:
      del self.store[key]


def main():
  db = InMemoryDBLevel3()
  db.set_at_with_ttl("user1", "session", "abc", start=100, ttl=10)
 
  print(db.get_at("user1", "session", timestamp=105))
  # print(db.get_at("user1", "session", timestamp=111))

if __name__ =="__main__":
  main()