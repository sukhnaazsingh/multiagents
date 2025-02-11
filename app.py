from dotenv import load_dotenv
from flask import Flask

from endpoints.customer_care.routes import customer_care_bp
from endpoints.event_agent.routes import event_bp
from endpoints.mock.routes import mock_bp
from endpoints.route_agent.routes import route_bp
from endpoints.trends_agent.routes import trends_bp
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)

CORS(app, supports_credentials=True, origins=["http://localhost:3000"])

app.register_blueprint(customer_care_bp, url_prefix="/customer-care")
app.register_blueprint(event_bp, url_prefix="/event")
app.register_blueprint(route_bp, url_prefix="/route")
app.register_blueprint(trends_bp, url_prefix="/trends")
app.register_blueprint(mock_bp, url_prefix="/mock")

if __name__ == "__main__":
    app.run(debug=True)
