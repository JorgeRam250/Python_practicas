"""${message}"""

revision = ${repr(revision)}
down_revision = ${repr(down_revision)}
branch_labels = ${repr(branch_labels)}
depends_on = ${repr(depends_on)}

from alembic import op
import sqlalchemy as sa


def upgrade() -> None:
    ${upgrades if upgrades else "op.execute('SELECT 1')"}


def downgrade() -> None:
    ${downgrades if downgrades else "op.execute('SELECT 1')"}
