class User:

  def __init__(self,username,password,cart,admin):
      self.username = username
      self.password = password
      self.cart = cart
      self.admin = admin
    
  def get_username(self):
      return(self.username)

  def get_password(self):
      return(self.password)

  def get_admin(self):
      return(self.admin)

  def get_cart(self):
      return(self.cart)