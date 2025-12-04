-- ============================================
-- REAL-TIME NOTIFICATIONS (PostgreSQL NOTIFY)
-- Run this script to add triggers to existing database
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

-- Verify triggers were created
SELECT 
    trigger_name, 
    event_object_table, 
    action_timing, 
    event_manipulation
FROM information_schema.triggers 
WHERE trigger_name LIKE '%_notify_trigger';

