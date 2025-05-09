"""v0.2.3.1 fix

Revision ID: 4da3184bf8fb
Revises: c8fde8696467
Create Date: 2025-02-25 20:41:04.821439

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '4da3184bf8fb'
down_revision: Union[str, None] = 'c8fde8696467'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('chat', sa.Column('last_message_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'chat', 'message', ['last_message_id'], ['id'])
    op.drop_column('chat', 'last_message_date')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('chat', sa.Column('last_message_date', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'chat', type_='foreignkey')
    op.drop_column('chat', 'last_message_id')
    # ### end Alembic commands ###
