"""Models for Cupcake app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFAULT_IMG_URL = "https://tinyurl.com/demo-cupcake"

def connect_db(app):
    db.app = app
    db.init_app(app)

    app.app_context().push()

class Cupcake(db.Model):
    """Cupcake Model"""

    __tablename__ = "cupcakes"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    flavor = db.Column(db.Text, nullable=False)
    size = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    image = db.Column(db.Text, nullable=False, default=DEFAULT_IMG_URL)

    def to_dict(self):
        """Returns a dict representation of todo which we can turn into JSON"""
        return {
            'id': self.id,
            'flavor': self.flavor,
            'size': self.size,
            'rating': self.rating,
            'image': self.image
        }

# # update method to make PATCH route cleaner
#     def update(self, data):
#         self.flavor = data.get('flavor', self.flavor)
#         self.image = data.get('image', self.image)
#         self.rating = data.get('rating', self.rating)
#         self.size = data.get('size', self.size)

    def __repr__(self):
        return f"<Id={self.id} Flavor={self.flavor} size={self.size} rating={self.rating} >"