from flask import Blueprint

hooks_bp = Blueprint('hooks', __name__, url_prefix='/api/hooks')

from . import routes  # importa le rotte dopo aver creato il blueprint
