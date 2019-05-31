"""empty message

Revision ID: 80b9c98af555
Revises: 1fc843df1198
Create Date: 2019-05-15 19:58:01.363914

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '80b9c98af555'
down_revision = '1fc843df1198'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('roles')
    op.drop_table('user_roles')
    op.add_column('user', sa.Column('role', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'role')
    op.create_table('user_roles',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('role_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], name='user_roles_role_id_fkey', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='user_roles_user_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name='user_roles_pkey'),
    sa.UniqueConstraint('user_id', name='user_roles_user_id_key')
    )
    op.create_table('roles',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='roles_pkey'),
    sa.UniqueConstraint('name', name='roles_name_key')
    )
    # ### end Alembic commands ###