from app import create_app
from dotenv import load_dotenv
from config import SECRET_KEY, DB_NAME, DB_USERNAME, DB_PASSWORD, DB_HOST, BOOTSTRAP_SERVE_LOCAL



load_dotenv('.env')

app = create_app()


app.config['SECRET_KEY'] = SECRET_KEY
if __name__ == '__main__':
      app.run(debug=True)
