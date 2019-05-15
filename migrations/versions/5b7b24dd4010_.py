"""empty message

Revision ID: 5b7b24dd4010
Revises: c3a77393e2f8
Create Date: 2019-05-14 23:56:44.805867

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5b7b24dd4010'
down_revision = 'c3a77393e2f8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('projectdetails_project_id_fkey', 'projectdetails', type_='foreignkey')
    op.create_foreign_key(None, 'projectdetails', 'projectheader', ['project_id'], ['id'])
    op.drop_constraint('user_username_key', 'user', type_='unique')
    op.drop_column('user', 'username')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('username', sa.VARCHAR(length=20), autoincrement=False, nullable=False))
    op.create_unique_constraint('user_username_key', 'user', ['username'])
    op.drop_constraint(None, 'projectdetails', type_='foreignkey')
    op.create_foreign_key('projectdetails_project_id_fkey', 'projectdetails', 'projectdetails', ['project_id'], ['id'])
    # ### end Alembic commands ###
