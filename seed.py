from app import app
from models import db, User

db.drop_all()
db.create_all()

u1 = User(
    username="cupcake",
    password="12345", # unhashed
    email="cupcake@cupcakes.com",
    first_name="I Love",
    last_name="Cupcakes",
    is_admin=False
)

u2 = User(
    username="taco",
    password="12345", # unhashed
    email="taco@tacos.com",
    first_name="I Love",
    last_name="Tacos",
    is_admin=False
)

db.session.add_all([u1, u2])
db.session.commit()
