from flask import Blueprint

main = Blueprint('main', __name__ )

from . import wm1core, wm1base, proxy, info