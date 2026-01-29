from flask_pymongo import PyMongo

# Setup MongoDB here
# mongo = PyMongo(uri="mongodb://localhost:27017/database")
mongo = PyMongo()


def init_extensions(app):
    mongo.init_app(app)
    
    # Test connection
    try:
        # Ping MongoDB to verify connection
        mongo.db.command('ping')
        print("Successfully connected to MongoDB")
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")
