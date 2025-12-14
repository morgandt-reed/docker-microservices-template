-- Database initialization script
-- This runs automatically when the database container is first created

-- Create items table (if not created by SQLAlchemy)
CREATE TABLE IF NOT EXISTS items (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description VARCHAR(1000),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create index on name for faster lookups
CREATE INDEX IF NOT EXISTS idx_items_name ON items(name);

-- Create index on created_at for sorting
CREATE INDEX IF NOT EXISTS idx_items_created_at ON items(created_at DESC);

-- Insert sample data
INSERT INTO items (name, description) VALUES
    ('Sample Item 1', 'This is a demo item created during database initialization'),
    ('Sample Item 2', 'Another example item showing the microservices in action'),
    ('Docker Demo', 'Demonstrating containerized database initialization');

-- Grant permissions (redundant since user is owner, but good practice)
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO appuser;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO appuser;

-- Log completion
DO $$
BEGIN
    RAISE NOTICE 'Database initialization completed successfully';
END $$;
