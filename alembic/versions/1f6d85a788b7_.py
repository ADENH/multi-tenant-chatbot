"""empty message

Revision ID: 1f6d85a788b7
Revises: 
Create Date: 2025-02-23 05:13:34.681229

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1f6d85a788b7'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('role', sa.String(), nullable=True))
    op.alter_column('users', 'tenant_id',
               existing_type=sa.INTEGER(),
               type_=sa.INTEGER(),
               existing_nullable=True)
    op.drop_constraint('users_username_key', 'users', type_='unique')
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.drop_constraint('users_tenant_id_fkey', 'users', type_='foreignkey')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key('users_tenant_id_fkey', 'users', 'tenants', ['tenant_id'], ['id'])
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.create_unique_constraint('users_username_key', 'users', ['username'])
    op.alter_column('users', 'tenant_id',
               existing_type=sa.String(),
               type_=sa.INTEGER(),
               existing_nullable=True)
    op.drop_column('users', 'role')
    # ### end Alembic commands ###
