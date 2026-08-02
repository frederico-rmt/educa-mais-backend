"""create user table

Revision ID: eb5436342da6
Revises: eb5436342da5
Create Date: 2025-07-12 18:17:55.756736

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'eb5436342da6'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
  op.create_table('users',
    sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
    sa.Column('uuid', sa.String, nullable=False, unique=True),
    sa.Column('name', sa.String, nullable=False),
    sa.Column('email', sa.String, unique=True, nullable=False),
    sa.Column('password', sa.String, nullable=False),
    sa.Column('role', sa.String, nullable=False),
    schema='educa_mais'
  )

  op.execute("""
    INSERT INTO educa_mais.users (uuid, name, email, password, role)
    VALUES (
      'b372c8fc-67fd-4565-aed2-2a159d2fd80d',
      'teacher1',
      'teacher1@example.com',
      '$2b$12$XX0ZmgezHunoyvzUWm/0c.vuyfhFO.f4oRBvPoTiCIWZ//OwDub46',
      'teacher'
    );
  """)

  op.execute("""
    INSERT INTO educa_mais.users (uuid, name, email, password, role)
    VALUES (
      'ea8996d0-7968-4126-8a24-7970e2142b82',
      'student1',
      'student1@example.com',
      '$2b$12$XX0ZmgezHunoyvzUWm/0c.vuyfhFO.f4oRBvPoTiCIWZ//OwDub46',
      'student'
    );
  """)

def downgrade() -> None:
  op.drop_table('users', schema='educa_mais')
