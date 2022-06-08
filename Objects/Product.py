class Product:

  def __init__(self,product_name,price,quantity,size_lst):
    self.product_name = product_name
    self.price = price
    self.quantity = quantity
    self.size_lst = size_lst

  def __str__(self):
    return {"product_name":self.product_name,"price":self.price,"quantity":self.quantity,"size":self.size_lst}