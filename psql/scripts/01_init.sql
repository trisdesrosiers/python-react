CREATE TABLE IF NOT EXISTS roles (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS registrations (
    id SERIAL PRIMARY KEY,
    unique_identifier VARCHAR(255) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    firstname VARCHAR(100),
    lastname VARCHAR(100),
    status VARCHAR(50) DEFAULT 'inactive',
    reference_id VARCHAR(255),
    signup_type VARCHAR(50) DEFAULT 'custom',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS profiles (
    id SERIAL PRIMARY KEY,
    unique_identifier VARCHAR(255) NOT NULL UNIQUE,
    role_id INTEGER REFERENCES roles(id) ON DELETE SET NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255),
    firstname VARCHAR(100),
    lastname VARCHAR(100),
    status VARCHAR(50) DEFAULT 'inactive',
    reference_id VARCHAR(255),
    signup_type VARCHAR(50) DEFAULT 'custom',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO roles (name) VALUES ('admin'), ('user') ON CONFLICT (name) DO NOTHING;

INSERT INTO profiles (unique_identifier, role_id, email, password, firstname, lastname, status, signup_type)
VALUES ('demo-user-123', 2, 'demo@example.com', 'password123', 'Demo', 'User', 'active', 'custom')
ON CONFLICT (email) DO NOTHING;

INSERT INTO registrations (unique_identifier, email, firstname, lastname, status, signup_type)
VALUES ('demo-user-123', 'demo@example.com', 'Demo', 'User', 'active', 'custom')
ON CONFLICT (email) DO NOTHING;

-- ============================================
-- REAL-TIME NOTIFICATIONS (PostgreSQL NOTIFY)
-- ============================================

-- Function to send notifications on table changes
CREATE OR REPLACE FUNCTION notify_table_change()
RETURNS TRIGGER AS $$
DECLARE
    payload JSON;
    record_data JSON;
BEGIN
    -- Build the record data based on operation type
    IF TG_OP = 'DELETE' THEN
        record_data := row_to_json(OLD);
    ELSE
        record_data := row_to_json(NEW);
    END IF;
    
    -- Build the notification payload
    payload := json_build_object(
        'table', TG_TABLE_NAME,
        'operation', TG_OP,
        'data', record_data
    );
    
    -- Send the notification
    PERFORM pg_notify('db_changes', payload::text);
    
    -- Return appropriate record
    IF TG_OP = 'DELETE' THEN
        RETURN OLD;
    ELSE
        RETURN NEW;
    END IF;
END;
$$ LANGUAGE plpgsql;

-- Create triggers for profiles table
DROP TRIGGER IF EXISTS profiles_notify_trigger ON profiles;
CREATE TRIGGER profiles_notify_trigger
    AFTER INSERT OR UPDATE OR DELETE ON profiles
    FOR EACH ROW EXECUTE FUNCTION notify_table_change();

-- Create triggers for registrations table  
DROP TRIGGER IF EXISTS registrations_notify_trigger ON registrations;
CREATE TRIGGER registrations_notify_trigger
    AFTER INSERT OR UPDATE OR DELETE ON registrations
    FOR EACH ROW EXECUTE FUNCTION notify_table_change();

-- Create triggers for roles table
DROP TRIGGER IF EXISTS roles_notify_trigger ON roles;
CREATE TRIGGER roles_notify_trigger
    AFTER INSERT OR UPDATE OR DELETE ON roles
    FOR EACH ROW EXECUTE FUNCTION notify_table_change();

