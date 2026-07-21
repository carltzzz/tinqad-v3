-- Migration: Add receipt link column to adminteam.expenses
-- Run this script on your PostgreSQL database before deploying the code changes.

ALTER TABLE adminteam.expenses
ADD COLUMN exp_receipt_link TEXT DEFAULT NULL;
