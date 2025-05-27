CREATE TABLE IF NOT EXISTS tickets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    phone TEXT NOT NULL,
    priority INTEGER NOT NULL,
    attachments TEXT,
    status TEXT NOT NULL DEFAULT 'new',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_user ON tickets (user_id);
CREATE INDEX IF NOT EXISTS idx_status ON tickets (status);
CREATE INDEX IF NOT EXISTS idx_priority ON tickets (priority);