"""empty message

Revision ID: e7902d3da1d4
Revises: 55f6e2570a1d
Create Date: 2022-03-02 16:42:32.391149

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e7902d3da1d4'
down_revision = '55f6e2570a1d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('profile', schema=None) as batch_op:
        batch_op.add_column(sa.Column('last_login', sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('profile', schema=None) as batch_op:
        batch_op.drop_column('last_login')

    # ### end Alembic commands ###
