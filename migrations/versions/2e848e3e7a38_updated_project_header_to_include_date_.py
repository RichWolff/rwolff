"""Updated Project header to include date created and date modified

Revision ID: 2e848e3e7a38
Revises: fc854b03adbb
Create Date: 2019-05-17 15:43:10.596455

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2e848e3e7a38'
down_revision = 'fc854b03adbb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('projectdetails', sa.Column('displayOrder', sa.Integer(), nullable=False))
    op.add_column('projectheader', sa.Column('date_created', sa.DateTime(), nullable=False))
    op.add_column('projectheader', sa.Column('date_last_update', sa.DateTime(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('projectheader', 'date_last_update')
    op.drop_column('projectheader', 'date_created')
    op.drop_column('projectdetails', 'displayOrder')
    # ### end Alembic commands ###
