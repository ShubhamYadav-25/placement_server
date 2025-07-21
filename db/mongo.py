from pymongo import MongoClient
from pymongo.server_api import ServerApi
import gridfs

uri = "mongodb+srv://shub252005:SIGQb4hSIf4h17eg@cluster0.f0wnde2.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))

db = client['placement_info']
users_collection = db['users']
user_resumes = db['user_resumes']
fs = gridfs.GridFS(db)
