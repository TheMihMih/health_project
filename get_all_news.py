from webapp import create_app
from webapp.news.parser.utils import get_snippets

app = create_app()
with app.app_context():
    get_snippets()