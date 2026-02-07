"""Store SQL queries in this file."""

create_user_event_table = """CREATE TABLE IF NOT EXISTS user_event (
  id BIGSERIAL PRIMARY KEY,
  user_name TEXT NOT NULL,
  event_type TEXT NOT NULL CHECK (event_type IN ('general', 'error')),
  data JSONB NOT NULL DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
  occurred_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
"""
cursor_pagination_index = (
  "CREATE INDEX IF NOT EXISTS user_event_created_id_idx "
  "ON user_event (created_at DESC, id DESC);"
)

