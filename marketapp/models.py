from datetime import datetime
from flask_sqlalchemy import SQLAlchemy


db=SQLAlchemy()


class Admin(db.Model):
    admin_id=db.Column(db.Integer, autoincrement=True,primary_key=True)
    admin_username=db.Column(db.String(20),nullable=True)
    admin_pwd=db.Column(db.String(200),nullable=True)

class Category(db.Model):
    cat_id=db.Column(db.Integer, autoincrement=True,primary_key=True)
    cat_name=db.Column(db.String(20),nullable=False)
    #set relationship
    productdeets = db.relationship("Product", back_populates="catdeets")

class Product(db.Model):
    product_id = db.Column(db.Integer, autoincrement=True,primary_key=True)
    product_userid = db.Column(db.Integer, db.ForeignKey('user.user_id'),nullable=False)  
    product_category = db.Column(db.Integer, db.ForeignKey('category.cat_id'),nullable=False)  
    product_name = db.Column(db.Text(),nullable=False)
    product_slug = db.Column(db.String(100), unique=True)
    product_price = db.Column(db.Text())
    product_image = db.Column(db.String(100))
    product_desc = db.Column(db.Text())
    
    
    #set relationships
    catdeets = db.relationship("Category", back_populates="productdeets")
    productreviews = db.relationship("Reviews", back_populates="theproduct",cascade="all, delete-orphan")
    
class Reviews(db.Model):
    rev_id = db.Column(db.Integer, autoincrement=True,primary_key=True)
    rev_user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'),nullable=False) 
    rev_productid = db.Column(db.Integer, db.ForeignKey('product.product_id'),nullable=False) 
    rev_text = db.Column(db.String(255),nullable=False)
    rev_title = db.Column(db.String(255),nullable=False)
    rev_date= db.Column(db.DateTime(), default=datetime.utcnow)
  
#   set relationship
    review_by = db.relationship('User',back_populates='user_reviews')
    theproduct = db.relationship("Product", back_populates="productreviews")
  

class User(db.Model):  
    user_id = db.Column(db.Integer, autoincrement=True,primary_key=True)
    user_fullname = db.Column(db.String(100),nullable=False)
    user_email = db.Column(db.String(120)) 
    user_pwd=db.Column(db.String(120),nullable=True)
    user_pix=db.Column(db.String(120),nullable=True) 
    user_datereg=db.Column(db.DateTime(), default=datetime.utcnow)#default 


    
    #set relationship    
    user_reviews=db.relationship("Reviews",back_populates='review_by')    

class Payment(db.Model):
    payment_id = db.Column(db.Integer, autoincrement=True,primary_key=True)
    payment_user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'),nullable=False) 
    payment_order_id= db.Column(db.Integer, db.ForeignKey('order.order_id'),nullable=False)
    payment_amt = db.Column(db.Float,nullable=False)
    payment_date=db.Column(db.DateTime(), default=datetime.utcnow)
  
  
  # set relationship
    payment_by= db.relationship("User",backref="userpayment")
    order_by= db.relationship("Order",backref="userorder")


class Order(db.Model):
    order_id = db.Column(db.Integer, autoincrement=True,primary_key=True)
    order_user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'),nullable=False)
    order_product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'),nullable=False)
    order_state_id = db.Column(db.Integer, db.ForeignKey('state.state_id'),nullable=False)
    order_lga_id = db.Column(db.Integer, db.ForeignKey('lga.lga_id'),nullable=False)
    order_email = db.Column(db.String(120))
    order_refno = db.Column(db.String(120))
    order_delivery_address = db.Column(db.String(120),nullable=False)
    order_product_qty = db.Column(db.Integer,nullable=False)
    order_unitprice = db.Column(db.Float,nullable=False)
    order_amt = db.Column(db.Float,nullable=False)
    order_date=db.Column(db.DateTime(), default=datetime.utcnow)
    order_status = db.Column(db.String(120))


#set relationship
    user_order= db.relationship("User",backref="myorders")
    product_by=db.relationship("Product",backref="myproduct")
    order_state=db.relationship("State",backref="mystate")
    order_lga=db.relationship("Lga",backref="mylga")


class State(db.Model):  
    state_id = db.Column(db.Integer, autoincrement=True,primary_key=True)
    state_name = db.Column(db.String(100),nullable=False)

# set relationship
   



class Lga(db.Model):  
    lga_id = db.Column(db.Integer, autoincrement=True,primary_key=True)
    lga_state_id = db.Column(db.Integer, db.ForeignKey('state.state_id'),nullable=False) 
    lga_name = db.Column(db.String(100),nullable=False)

# set relationship
    user_state= db.relationship("State",backref="lga_ofuser")
   
    



    
     


  
    

