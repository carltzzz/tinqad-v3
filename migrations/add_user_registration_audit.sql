-- Migration: Add registration audit columns to maindashboard.users
-- Run this script on your PostgreSQL database before deploying the code changes.

ALTER TABLE maindashboard.users
ADD COLUMN user_registered_by INT REFERENCES maindashboard.users(user_id),
ADD COLUMN user_registered_on TIMESTAMP DEFAULT NULL;
