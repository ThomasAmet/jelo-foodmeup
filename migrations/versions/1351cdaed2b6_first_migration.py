"""First migration

Revision ID: 1351cdaed2b6
Revises: 
Create Date: 2021-02-14 23:37:52.991827

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1351cdaed2b6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('recipes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('creation_date', sa.DateTime(), nullable=True),
    sa.Column('designation', sa.String(length=120), nullable=False),
    sa.Column('internal_code', sa.String(length=20), nullable=True),
    sa.Column('category', sa.String(length=120), nullable=True),
    sa.Column('commercial_name', sa.String(length=120), nullable=False),
    sa.Column('ingredients', sa.String(length=3000), nullable=True),
    sa.Column('allergens', sa.String(length=1000), nullable=True),
    sa.Column('nutrient_summary', sa.String(length=1000), nullable=True),
    sa.Column('portion_weight', sa.SmallInteger(), nullable=True),
    sa.Column('portion_cost', sa.Float(), nullable=True),
    sa.Column('expiration_days', sa.SmallInteger(), nullable=True),
    sa.Column('kcal', sa.String(length=20), nullable=True),
    sa.Column('kJ', sa.String(length=20), nullable=True),
    sa.Column('fat', sa.String(length=20), nullable=True),
    sa.Column('satur_fat', sa.String(length=20), nullable=True),
    sa.Column('carbs', sa.String(length=20), nullable=True),
    sa.Column('sugar', sa.String(length=20), nullable=True),
    sa.Column('protein', sa.String(length=20), nullable=True),
    sa.Column('salt', sa.String(length=20), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_recipes_designation'), 'recipes', ['designation'], unique=False)
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=120), nullable=True),
    sa.Column('username', sa.String(length=120), nullable=True),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_recipes_designation'), table_name='recipes')
    op.drop_table('recipes')
    # ### end Alembic commands ###