-- Shoe Database Schema Initialization Script
-- This script creates all necessary tables and indexes for the Shoe Database application
-- It is safe to run multiple times (uses IF NOT EXISTS)

-- Create users table for authentication
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    last_login TIMESTAMPTZ
);

-- Create shoes table for inventory management
CREATE TABLE IF NOT EXISTS shoes (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    brand TEXT NOT NULL,
    model TEXT NOT NULL,
    colorway TEXT NOT NULL,
    size DOUBLE PRECISION NOT NULL,
    price DOUBLE PRECISION NOT NULL,
    image TEXT,
    condition TEXT NOT NULL
);

-- Create index for optimizing queries on user's shoes by brand and model
CREATE INDEX IF NOT EXISTS shoes_user_brand_model_idx
ON shoes (user_id, brand, model);

-- Display success message
SELECT 'Database schema initialized successfully!' AS status;
