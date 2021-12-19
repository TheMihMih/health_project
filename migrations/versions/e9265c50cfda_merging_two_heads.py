"""merging two heads

Revision ID: e9265c50cfda
Revises: f891914da13d, f565e0fb4947, 50e46e70a851, ee1a84181bb0
Create Date: 2021-11-22 12:33:32.798825

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e9265c50cfda'
down_revision = ('f891914da13d', 'f565e0fb4947', '50e46e70a851', 'ee1a84181bb0')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
