"""empty message

Revision ID: 0ae37259d6b3
Revises: c82e8e31c0bb
Create Date: 2017-03-16 09:47:03.541861

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0ae37259d6b3'
down_revision = 'c82e8e31c0bb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('screens',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('gare_depart', sa.Integer(), nullable=False),
    sa.Column('gare_arrive', sa.Integer(), nullable=False),
    sa.Column('board_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['board_id'], ['boards.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('screens')
    # ### end Alembic commands ###
