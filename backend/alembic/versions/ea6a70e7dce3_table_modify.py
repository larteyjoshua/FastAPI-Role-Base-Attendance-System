"""Table Modify

Revision ID: ea6a70e7dce3
Revises: 315a24936790
Create Date: 2022-10-26 00:51:54.422965

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ea6a70e7dce3'
down_revision = '315a24936790'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('attendance', sa.Column('name', sa.String(), nullable=True))
    op.drop_index('ix_attendance_userId', table_name='attendance')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('ix_attendance_userId', 'attendance', ['userId'], unique=False)
    op.drop_column('attendance', 'name')
    # ### end Alembic commands ###
