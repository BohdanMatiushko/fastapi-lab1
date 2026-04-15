"""add password_hash to users

Revision ID: a1b2c3d4e5f6
Revises: 433f0a2bae05
Create Date: 2026-04-15 21:36:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = 'a1b2c3d4e5f6'
down_revision = '433f0a2bae05'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('users', sa.Column('password_hash', sa.String(length=255), nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'password_hash')
