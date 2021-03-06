"""empty message

Revision ID: 4a3af16ce5e
Revises: 20d455cecce
Create Date: 2015-07-02 16:15:22.289441

"""

# revision identifiers, used by Alembic.
revision = '4a3af16ce5e'
down_revision = '20d455cecce'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('results', sa.Column('file_to_convert', sa.String(), nullable=True))
    op.add_column('results', sa.Column('output1', sa.String(), nullable=True))
    op.add_column('results', sa.Column('output2', sa.String(), nullable=True))
    op.drop_column('results', 'result_no_stop_words')
    op.drop_column('results', 'url')
    op.drop_column('results', 'result_all')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('results', sa.Column('result_all', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('results', sa.Column('url', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('results', sa.Column('result_no_stop_words', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('results', 'output2')
    op.drop_column('results', 'output1')
    op.drop_column('results', 'file_to_convert')
    ### end Alembic commands ###
