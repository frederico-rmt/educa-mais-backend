"""create user table

Revision ID: eb5436342da5
Revises:
Create Date: 2025-07-12 18:17:55.756736

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import text

# revision identifiers, used by Alembic.
revision = "eb5436342da5"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()

    # Cria schema educa_mais se não existir
    conn.execute(text("CREATE SCHEMA IF NOT EXISTS educa_mais"))


def downgrade():
    conn = op.get_bind()

    # Remove schema (cuidado: CASCADE remove tabelas dentro)
    conn.execute(text("DROP SCHEMA IF EXISTS educa_mais CASCADE"))