"""add user table

Revision ID: a8137680306f
Revises: 4f61ca24f012
Create Date: 2022-10-28 23:59:10.602516

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a8137680306f'
down_revision = '4f61ca24f012'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
        sa.Column('id',sa.Integer(),nullable=False),
        sa.Column('email',sa.String(),nullable=False),
        sa.Column('password',sa.String(),nullable=False),
        sa.Column('created_at',sa.TIMESTAMP(timezone=True),
        server_default=sa.text('now()'), nullable=False ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
        
        )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
