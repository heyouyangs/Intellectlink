from flask import *
from flask_wtf import *


signup_bp = Blueprint('signup', __name__)


@signup_bp.route('/')
def home():
    return render_template('signup.html')