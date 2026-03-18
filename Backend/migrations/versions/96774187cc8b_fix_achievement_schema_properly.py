"""fix_achievement_schema_properly

Revision ID: 96774187cc8b
Revises: b527abdc640c
Create Date: 2025-06-24 22:32:45.672519

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '96774187cc8b'
down_revision = 'b527abdc640c'
branch_labels = None
depends_on = None


def upgrade():
    # Drop foreign key constraint first
    with op.batch_alter_table('user_achievements', schema=None) as batch_op:
        batch_op.drop_constraint('user_achievements_ibfk_3', type_='foreignkey')
    
    # Change achievements.id to VARCHAR(64)
    with op.batch_alter_table('achievements', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=mysql.INTEGER(display_width=11),
               type_=sa.String(length=64),
               existing_nullable=False,
               autoincrement=False)
    
    # Change user_achievements.achievement_id to VARCHAR(64)
    with op.batch_alter_table('user_achievements', schema=None) as batch_op:
        batch_op.alter_column('achievement_id',
               existing_type=mysql.INTEGER(display_width=11),
               type_=sa.String(length=64),
               existing_nullable=False)
    
    # Re-add foreign key constraint
    with op.batch_alter_table('user_achievements', schema=None) as batch_op:
        batch_op.create_foreign_key('user_achievements_ibfk_3', 'achievements', ['achievement_id'], ['id'])


def downgrade():
    # Drop foreign key constraint
    with op.batch_alter_table('user_achievements', schema=None) as batch_op:
        batch_op.drop_constraint('user_achievements_ibfk_3', type_='foreignkey')
    
    # Change user_achievements.achievement_id back to INTEGER
    with op.batch_alter_table('user_achievements', schema=None) as batch_op:
        batch_op.alter_column('achievement_id',
               existing_type=sa.String(length=64),
               type_=mysql.INTEGER(display_width=11),
               existing_nullable=False)
    
    # Change achievements.id back to INTEGER
    with op.batch_alter_table('achievements', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.String(length=64),
               type_=mysql.INTEGER(display_width=11),
               existing_nullable=False,
               autoincrement=True)
    
    # Re-add foreign key constraint
    with op.batch_alter_table('user_achievements', schema=None) as batch_op:
        batch_op.create_foreign_key('user_achievements_ibfk_3', 'achievements', ['achievement_id'], ['id'])
