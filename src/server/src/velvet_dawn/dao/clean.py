import velvet_dawn
from velvet_dawn.dao import app, db

# When called directly, drops all tables from the DB specified in velvet_dawn.dao
if __name__ == "__main__":
    with app.app_context():
        # TODO Delete delete new data store
        velvet_dawn.dao.instance.clear()
        db.init_app(app)
        db.drop_all()
        print("Game state cleaned")
