"""Create user_event table

Revision ID: 0001_create_user_event_table
Revises:
Create Date: 2026-02-06 17:00
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0001_create_user_event_table'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create the `user_event` table and the descending index used for cursor pagination."""
    op.create_table(
        'user_event',
        sa.Column('id', sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column('user_name', sa.Text(), nullable=False),
        sa.Column('event_type', sa.Text(), nullable=False),
        sa.Column('data', postgresql.JSONB(), nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')),
        sa.Column('occurred_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')),
        sa.CheckConstraint("event_type IN ('general','error')", name='user_event_event_type_check'),
    )

    # Create the index with DESC ordering as in your plain SQL. Alembic's op.create_index
    # does not expose column ordering, so use raw SQL which is Postgres-specific.
    op.execute(
        """
        CREATE INDEX IF NOT EXISTS user_event_occurred_id_idx
        ON user_event (occurred_at DESC, id DESC);
        """
    )


def downgrade() -> None:
    """Drop the index and the `user_event` table."""
    op.execute("DROP INDEX IF EXISTS user_event_occurred_id_idx;")
    op.drop_table('user_event')
