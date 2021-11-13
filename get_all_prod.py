from webapp import create_app
from webapp.food.parsers import parser


app = create_app()
with app.app_context():
    parser.page_changer()
