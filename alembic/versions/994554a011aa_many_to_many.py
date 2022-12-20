"""Many to many?

Revision ID: 994554a011aa
Revises: 8ddf4a89c174
Create Date: 2022-12-20 08:37:52.867128

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '994554a011aa'
down_revision = '8ddf4a89c174'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('catcustomer_table',
    sa.Column('cat_id', sa.Integer(), nullable=False),
    sa.Column('customer_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['cat_id'], ['cat.id'], ),
    sa.ForeignKeyConstraint(['customer_id'], ['customer.id'], ),
    sa.PrimaryKeyConstraint('cat_id', 'customer_id')
    )
    op.add_column('cat', sa.Column('customer_id', sa.Integer(), nullable=True))
    op.drop_constraint('cat_owner_id_fkey', 'cat', type_='foreignkey')
    op.create_foreign_key(None, 'cat', 'customer', ['customer_id'], ['id'])
    op.drop_column('cat', 'owner_id')
    op.add_column('customer', sa.Column('name', sa.String(length=256), nullable=False))
    op.add_column('customer', sa.Column('age', sa.Integer(), nullable=True))
    op.add_column('customer', sa.Column('password', sa.String(length=64), nullable=True))
    op.drop_index('ix_customer_email', table_name='customer')
    op.drop_index('ix_customer_phone', table_name='customer')
    op.drop_column('customer', 'is_donator')
    op.drop_column('customer', 'first_name')
    op.drop_column('customer', 'phone')
    op.drop_column('customer', 'second_name')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('customer', sa.Column('second_name', sa.VARCHAR(length=256), autoincrement=False, nullable=True))
    op.add_column('customer', sa.Column('phone', sa.VARCHAR(length=32), autoincrement=False, nullable=True))
    op.add_column('customer', sa.Column('first_name', sa.VARCHAR(length=256), autoincrement=False, nullable=True))
    op.add_column('customer', sa.Column('is_donator', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.create_index('ix_customer_phone', 'customer', ['phone'], unique=False)
    op.create_index('ix_customer_email', 'customer', ['email'], unique=False)
    op.drop_column('customer', 'password')
    op.drop_column('customer', 'age')
    op.drop_column('customer', 'name')
    op.add_column('cat', sa.Column('owner_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'cat', type_='foreignkey')
    op.create_foreign_key('cat_owner_id_fkey', 'cat', 'customer', ['owner_id'], ['id'])
    op.drop_column('cat', 'customer_id')
    op.drop_table('catcustomer_table')
    # ### end Alembic commands ###
