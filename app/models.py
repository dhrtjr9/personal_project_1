from app import db

class User(db.Model):
    user_id = db.Column(db.String(120), primary_key=True, nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Numeric(5, 2), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    # You can add more columns such as product_id, user_id, image_url, etc.

    def __repr__(self):
        return f"<Product {self.product_name} - {self.price} - Quantity: {self.quantity}>"

# class Product(db.Model): 
#     __tablename__ = 'product'
#     product_id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
#     product_name = db.Column(db.String(100), nullable=False)
#     price = db.Column(db.Numeric(5, 2), nullable=False)
#     image_url = db.Column(db.String(255), nullable=False)
#     # user_id = db.Column(db.String(120), db.ForeignKey('users.user_id'), nullable=False)

#     Product = db.relationship('Product', back_populates="user")  # Establish the relationship between Product and User    

# class Cart(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
