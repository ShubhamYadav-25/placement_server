from flask import Flask, render_template
from flask_cors import CORS
from routes.auth_routes import auth_routes
from routes.resume_routes import resume_routes
from db.mongo import users_collection
# Flask server.py or app.py

app = Flask(__name__)
CORS(app)

# Register routes
app.register_blueprint(auth_routes)
app.register_blueprint(resume_routes)

@app.route('/')
def show_users():
    users = list(users_collection.find({}, {"_id": 0}))
    return render_template('users.html', users=users)

if __name__ == '__main__':
    app.run(debug=True)
