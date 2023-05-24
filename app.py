"""Flask app for Cupcakes"""
from flask import Flask, request, redirect, render_template, flash, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Cupcake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///cupcakes"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'ohsosecret'


toolbar = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route("/")
def root():
    """Render homepage."""
    return render_template("index.html")


# GET REQUEST
@app.route('/api/cupcakes')
def list_cupcakes():
    """get JSON with all cupcakes"""
    # Cupcake.query.all()
    cupcakes = [cupcake.to_dict() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=cupcakes)


@app.route('/api/cupcakes/<int:id>')
def get_cupcake(id):
    """Returns JSON for one cupcake in particular"""
    cupcake = Cupcake.query.get_or_404(id)
    return jsonify(cupcake=cupcake.to_dict())

# POST REQUEST


@app.route('/api/cupcakes', methods=["POST"])
def create_cupcake():
    """create a new cupcake and return JSON of new cupcake"""

    data = request.json
    # create new cupcake with required model data
    new_cupcake = Cupcake(
        flavor=data["flavor"],
        image=data["image"] or None,
        rating=data["rating"],
        size=data["size"])
    
    # add new one to the database
    db.session.add(new_cupcake)
    db.session.commit()
    # show new cupcake JSON after post and show 201 created status
    response_json = jsonify(cupcake=new_cupcake.to_dict())
    return (response_json, 201)

# UPDATE REQUEST


@app.route('/api/cupcakes/<int:id>', methods=["PATCH"])
def update_cupcake(id):
    """update specific cupcake and respond with JSON of updated cupcake"""

    data = request.json

    cupcake = Cupcake.query.get_or_404(id)

    cupcake.flavor = data['flavor']
    cupcake.rating = data['rating']
    cupcake.size = data['size']
    cupcake.image = data['image']

    db.session.add(cupcake)
    db.session.commit()

    return jsonify(cupcake=cupcake.to_dict())

# DELETE REQUEST


@app.route('/api/cupcakes/<int:id>', methods=["DELETE"])
def delete_cupcake(id):
    """Deletes a particular cupcake"""
    cupcake = Cupcake.query.get_or_404(id)
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(message="deleted")
