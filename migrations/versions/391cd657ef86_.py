"""empty message

Revision ID: 391cd657ef86
Revises: 3704c6f27155
Create Date: 2023-07-27 17:20:56.362022

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '391cd657ef86'
down_revision = '3704c6f27155'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ['user_id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')

    # ### end Alembic commands ###
