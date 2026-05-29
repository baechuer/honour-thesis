ALTER TABLE subscriptions ADD COLUMN status TEXT NOT NULL DEFAULT 'active';
UPDATE subscriptions SET status = 'active' WHERE status IS NULL;
