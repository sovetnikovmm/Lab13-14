from flask import Blueprint

from . import auth
from . import goods
from . import index

my_view = Blueprint('my_view', __name__)
