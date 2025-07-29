"""create discursive answers table

Revision ID: 33e14fab2335
Revises: 91bbd274ea68
Create Date: 2025-07-23 21:28:08.072354

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '33e14fab2335'
down_revision: Union[str, Sequence[str], None] = '91bbd274ea68'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
  op.create_table('discursive_answers',
    sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
    sa.Column('uuid', sa.String, nullable=False),
    sa.Column('id_question', sa.String, sa.ForeignKey('educa_mais.discursive_questions.uuid'), nullable=False),
    sa.Column('id_student', sa.String, sa.ForeignKey('educa_mais.users.uuid'), nullable=False),
    sa.Column('answer', sa.String, nullable=False),
    sa.Column('grade', sa.Integer, nullable=False),
    sa.Column('feedback', sa.String, nullable=False),
    sa.Column('created_at', sa.Integer, nullable=False),
    sa.Column('corrected_at', sa.Integer, nullable=False),
    schema='educa_mais'
  )

def downgrade() -> None:
  op.drop_table('discursive_answers', schema='educa_mais')