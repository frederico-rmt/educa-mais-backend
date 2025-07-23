"""create question table

Revision ID: 91bbd274ea68
Revises: eb5436342da6
Create Date: 2025-07-22 22:27:27.185763

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '91bbd274ea68'
down_revision: Union[str, Sequence[str], None] = 'eb5436342da6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
  op.create_table('discursive_questions',
    sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
    sa.Column('uuid', sa.String, nullable=False),
    sa.Column('id_author', sa.String, sa.ForeignKey('educa_mais.users.uuid'), nullable=False),
    sa.Column('title', sa.String, nullable=False),
    sa.Column('prompt', sa.String, nullable=False),
    sa.Column('expected_answer', sa.String, nullable=False),
    sa.Column('criteria', sa.String, nullable=False),
    sa.Column('tags', sa.ARRAY(sa.String), nullable=False),
    sa.Column('topic', sa.String, nullable=False),
    sa.Column('difficulty', sa.String, nullable=False),
    sa.Column('grade_level', sa.String, nullable=False),
    sa.Column('created_at', sa.String, nullable=False),
    schema='educa_mais'
  )

def downgrade() -> None:
  op.drop_table('discursive_questions', schema='educa_mais')
