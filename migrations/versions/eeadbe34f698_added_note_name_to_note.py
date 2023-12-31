"""added note_name to note

Revision ID: eeadbe34f698
Revises: d3867d6802f8
Create Date: 2023-11-21 10:55:15.615672

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eeadbe34f698'
down_revision = 'd3867d6802f8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('note', schema=None) as batch_op:
        batch_op.add_column(sa.Column('note_name', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('note', schema=None) as batch_op:
        batch_op.drop_column('note_name')

    # ### end Alembic commands ###
