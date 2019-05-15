"""empty message

Revision ID: dad8cdacfbf5
Revises: 5b7b24dd4010
Create Date: 2019-05-15 00:53:36.027990

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dad8cdacfbf5'
down_revision = '5b7b24dd4010'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_page_view', sa.Column('user_agent', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user_page_view', 'user_agent')
    # ### end Alembic commands ###
