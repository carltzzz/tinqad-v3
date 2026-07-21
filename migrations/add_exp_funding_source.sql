-- Migration: Add funding source column to adminteam.expenses
-- Run this script on your PostgreSQL database before deploying the code changes.

ALTER TABLE adminteam.expenses
ADD COLUMN exp_funding_source TEXT DEFAULT NULL;
