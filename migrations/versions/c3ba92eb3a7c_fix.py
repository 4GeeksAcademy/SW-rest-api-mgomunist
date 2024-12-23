"""Fix

Revision ID: c3ba92eb3a7c
Revises: 24f611669fd6
Create Date: 2024-12-04 02:50:19.814385

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c3ba92eb3a7c'
down_revision = '24f611669fd6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('favorite', schema=None) as batch_op:
        batch_op.add_column(sa.Column('planet_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('people_id', sa.Integer(), nullable=True))
        # Nombres de las claves foráneas
        batch_op.create_foreign_key('fk_planet_id', 'planet', ['planet_id'], ['id'])
        batch_op.create_foreign_key('fk_people_id', 'people', ['people_id'], ['id'])
        batch_op.drop_column('item_id')
        batch_op.drop_column('favorite_type')

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_active', sa.Boolean(), nullable=False))
        batch_op.alter_column('password',
               existing_type=sa.VARCHAR(length=120),
               type_=sa.String(length=80),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('password',
               existing_type=sa.String(length=80),
               type_=sa.VARCHAR(length=120),
               existing_nullable=False)
        batch_op.drop_column('is_active')

    with op.batch_alter_table('favorite', schema=None) as batch_op:
        batch_op.add_column(sa.Column('favorite_type', sa.VARCHAR(length=50), nullable=False))
        batch_op.add_column(sa.Column('item_id', sa.INTEGER(), nullable=False))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('people_id')
        batch_op.drop_column('planet_id')

    # ### end Alembic commands ###
