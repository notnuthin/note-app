"""update note model

Revision ID: 1d8cc01346ef
Revises: eeadbe34f698
Create Date: 2023-11-22 23:48:49.581564

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1d8cc01346ef'
down_revision = 'eeadbe34f698'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('note', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', sa.String(), nullable=True))
        batch_op.drop_column('note_name')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('note', schema=None) as batch_op:
        batch_op.add_column(sa.Column('note_name', sa.VARCHAR(), nullable=True))
        batch_op.drop_column('name')

    # ### end Alembic commands ###