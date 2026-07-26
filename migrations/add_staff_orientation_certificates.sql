-- Migration: Create adminteam.staff_orientation_certificates table
-- Run this script on your PostgreSQL database before deploying the code changes.
-- This adds a child table for dynamic orientation/training certificate entries.
-- Old flat columns on staff_profiles (ob_w_admin_date, etc.) are kept for backward compatibility.

CREATE TABLE IF NOT EXISTS adminteam.staff_orientation_certificates (
    certificate_id SERIAL PRIMARY KEY,
    staff_profile_id INTEGER NOT NULL REFERENCES adminteam.staff_profiles(staff_profile_id) ON DELETE CASCADE,
    training_name TEXT NOT NULL,
    date_of_training DATE,
    certificate_link TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_staff_orientation_certificates_profile
    ON adminteam.staff_orientation_certificates(staff_profile_id);
