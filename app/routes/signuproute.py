from flask import *
from flask_wtf import *
from flask_dance.contrib.google import make_google_blueprint, google


signup_bp = Blueprint('signup', __name__)


@signup_bp.route('/')
def home():
    return render_template('signup.html')

