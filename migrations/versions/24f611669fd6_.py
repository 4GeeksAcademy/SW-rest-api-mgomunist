"""empty message

Revision ID: 24f611669fd6
Revises: a5cffa318ac2
Create Date: 2024-12-04 02:08:06.370495

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '24f611669fd6'
down_revision = 'a5cffa318ac2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('character',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('species', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('favorite',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('favorite_type', sa.String(length=50), nullable=False),
    sa.Column('item_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('password',
               existing_type=sa.VARCHAR(length=80),
               type_=sa.String(length=120),
               existing_nullable=False)
        batch_op.drop_column('is_active')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_active', sa.BOOLEAN(), nullable=False))
        batch_op.alter_column('password',
               existing_type=sa.String(length=120),
               type_=sa.VARCHAR(length=80),
               existing_nullable=False)

    op.drop_table('favorite')
    op.drop_table('character')
    # ### end Alembic commands ###
