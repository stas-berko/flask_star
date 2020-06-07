"""Add SubPlanVersioning model

Revision ID: 66f4b1d3eea9
Revises: 49952fde9c90
Create Date: 2020-06-07 16:29:48.403095

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '66f4b1d3eea9'
down_revision = '49952fde9c90'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('billing_cycles', schema=None) as batch_op:
        batch_op.alter_column('end_date',
               existing_type=sa.TIMESTAMP(),
               type_=sa.TIMESTAMP(timezone=True),
               existing_nullable=True)
        batch_op.alter_column('start_date',
               existing_type=sa.TIMESTAMP(),
               type_=sa.TIMESTAMP(timezone=True),
               existing_nullable=True)

    with op.batch_alter_table('data_usages', schema=None) as batch_op:
        batch_op.alter_column('from_date',
               existing_type=sa.TIMESTAMP(),
               type_=sa.TIMESTAMP(timezone=True),
               existing_nullable=True)
        batch_op.alter_column('to_date',
               existing_type=sa.TIMESTAMP(),
               type_=sa.TIMESTAMP(timezone=True),
               existing_nullable=True)

    with op.batch_alter_table('subscriptions', schema=None) as batch_op:
        batch_op.alter_column('activation_date',
               existing_type=sa.TIMESTAMP(),
               type_=sa.TIMESTAMP(timezone=True),
               existing_nullable=True)
        batch_op.alter_column('expiry_date',
               existing_type=sa.TIMESTAMP(),
               type_=sa.TIMESTAMP(timezone=True),
               existing_nullable=True)

    with op.batch_alter_table('subscriptions_plan_version', schema=None) as batch_op:
        batch_op.add_column(sa.Column('creation_date', sa.TIMESTAMP(timezone=True), nullable=False))
        batch_op.alter_column('activation_date',
               existing_type=sa.TIMESTAMP(),
               type_=sa.TIMESTAMP(timezone=True),
               existing_nullable=False)
        batch_op.alter_column('end_date',
               existing_type=sa.TIMESTAMP(),
               type_=sa.TIMESTAMP(timezone=True),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('subscriptions_plan_version', schema=None) as batch_op:
        batch_op.alter_column('end_date',
               existing_type=sa.TIMESTAMP(timezone=True),
               type_=sa.TIMESTAMP(),
               existing_nullable=False)
        batch_op.alter_column('activation_date',
               existing_type=sa.TIMESTAMP(timezone=True),
               type_=sa.TIMESTAMP(),
               existing_nullable=False)
        batch_op.drop_column('creation_date')

    with op.batch_alter_table('subscriptions', schema=None) as batch_op:
        batch_op.alter_column('expiry_date',
               existing_type=sa.TIMESTAMP(timezone=True),
               type_=sa.TIMESTAMP(),
               existing_nullable=True)
        batch_op.alter_column('activation_date',
               existing_type=sa.TIMESTAMP(timezone=True),
               type_=sa.TIMESTAMP(),
               existing_nullable=True)

    with op.batch_alter_table('data_usages', schema=None) as batch_op:
        batch_op.alter_column('to_date',
               existing_type=sa.TIMESTAMP(timezone=True),
               type_=sa.TIMESTAMP(),
               existing_nullable=True)
        batch_op.alter_column('from_date',
               existing_type=sa.TIMESTAMP(timezone=True),
               type_=sa.TIMESTAMP(),
               existing_nullable=True)

    with op.batch_alter_table('billing_cycles', schema=None) as batch_op:
        batch_op.alter_column('start_date',
               existing_type=sa.TIMESTAMP(timezone=True),
               type_=sa.TIMESTAMP(),
               existing_nullable=True)
        batch_op.alter_column('end_date',
               existing_type=sa.TIMESTAMP(timezone=True),
               type_=sa.TIMESTAMP(),
               existing_nullable=True)

    # ### end Alembic commands ###
