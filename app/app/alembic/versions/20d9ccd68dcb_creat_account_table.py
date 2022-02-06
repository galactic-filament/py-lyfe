"""creat account table

Revision ID: 20d9ccd68dcb
Revises:
Create Date: 2022-02-05 16:20:37.823599

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "20d9ccd68dcb"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "account",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(50), nullable=False),
        sa.Column("description", sa.Unicode(200)),
    )


def downgrade():
    op.drop_table("account")
