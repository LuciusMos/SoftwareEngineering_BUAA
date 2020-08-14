from backend import create_app
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = create_app()

if __name__ == "__main__":
    CORS(app, supports_credentials=True)
    try:
        app.run(host='0.0.0.0', port=8000, debug = True)
        #app.run(debug=True)
    except Exception as e:
        print(e)
