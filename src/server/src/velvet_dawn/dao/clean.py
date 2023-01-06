import velvet_dawn
from velvet_dawn.dao import app,db

# When called directly, drops all tables from the DB specified in velvet_dawn.dao
if __name__ == "__main__":
    with app.app_context():
        db.init_app(app)
        db.drop_all()
        print("Game state cleaned")