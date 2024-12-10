from .card import initialize_card_route
from .user import initialize_user_route

def initilize_routes(app):
    initialize_user_route(app)
    initialize_card_route(app)