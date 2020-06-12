class User:
  def __init__(self, name, password, access, id = None):
    self.Id = id
    self.Name = name
    self.Password = password
    self.Access = access
