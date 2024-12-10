from .card import initialize_card_route
from .user import initialize_user_route
from .accessLog import initialize_access_log_route

def initilize_routes(app):
    initialize_user_route(app)
    initialize_card_route(app)
    initialize_access_log_route(app)