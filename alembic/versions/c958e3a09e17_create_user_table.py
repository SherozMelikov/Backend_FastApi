"""create user table

Revision ID: c958e3a09e17
Revises: 5aac097414e0
Create Date: 2026-05-06 19:37:20.032102

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c958e3a09e17'
down_revision: Union[str, Sequence[str], None] = '5aac097414e0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
