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

