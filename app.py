from flask import Flask
from routes.routes import predict_route, ticket_route

app = Flask(__name__)

# Register routes
app.register_blueprint(predict_route)
app.register_blueprint(ticket_route)

if __name__ == '__main__':
    # Run the Flask app on port 5000
    app.run(host='0.0.0.0', port=5000)
