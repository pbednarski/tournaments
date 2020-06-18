class User:
  def __init__(self, name, email, dateofbirth, password, access, _id=None):
    self.Id = _id
    self.Name = name
    self.Email = email
    self.DateOfBirth = dateofbirth
    self.Password = password
    self.Access = access
