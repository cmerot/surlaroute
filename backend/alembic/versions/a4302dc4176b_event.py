"""event

Revision ID: a4302dc4176b
Revises: 060f2d7bce66
Create Date: 2024-12-21 18:21:41.225496

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a4302dc4176b'
down_revision: Union[str, None] = '060f2d7bce66'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('event_event_venue_id_fkey', 'event', type_='foreignkey')
    op.drop_column('event', 'event_venue_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('event', sa.Column('event_venue_id', sa.UUID(), autoincrement=False, nullable=False))
    op.create_foreign_key('event_event_venue_id_fkey', 'event', 'org', ['event_venue_id'], ['id'])
    # ### end Alembic commands ###