"""add content column to posts table

Revision ID: 4f61ca24f012
Revises: f60f8728a753
Create Date: 2022-10-28 23:51:16.428291

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4f61ca24f012'
down_revision = 'f60f8728a753'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    pass
