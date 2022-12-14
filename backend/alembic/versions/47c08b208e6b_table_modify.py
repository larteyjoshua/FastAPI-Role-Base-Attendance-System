"""Table Modify

Revision ID: 47c08b208e6b
Revises: f406f9e2b11b
Create Date: 2022-10-26 01:16:20.362714

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '47c08b208e6b'
down_revision = 'f406f9e2b11b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('attendance', 'userId',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('attendance', 'userId',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###
