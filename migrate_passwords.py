"""
One-time migration script to convert all SHA-256 passwords to bcrypt.

Run this after deploying the bcrypt integration:
    python migrate_passwords.py

Requires the .env file to be configured with DB credentials and SECRET_KEY.
"""
import os
import sys
import hashlib
from dotenv import load_dotenv

load_dotenv()

sys.path.insert(0, os.path.dirname(__file__))

from app import bcrypt
from apps import dbconnect as db

# instead of storing passwords as plaintext, they are stored as hash
def migrate_passwords():
    conn = db.getdblocation()
    cursor = conn.cursor()

    cursor.execute("SELECT user_id, user_password FROM maindashboard.users")
    rows = cursor.fetchall()

    migrated = 0
    skipped = 0
    errors = 0

    for user_id, stored_hash in rows:
        if not stored_hash:
            skipped += 1
            continue

        if stored_hash.startswith('$2'):
            skipped += 1
            continue

        try:
            new_hash = bcrypt.generate_password_hash(stored_hash).decode('utf-8')
            cursor.execute(
                "UPDATE maindashboard.users SET user_password = %s WHERE user_id = %s",
                (new_hash, user_id)
            )
            conn.commit()
            migrated += 1
            print(f"  Migrated user_id={user_id}")
        except Exception as e:
            conn.rollback()
            errors += 1
            print(f"  Error migrating user_id={user_id}: {e}")

    cursor.close()
    conn.close()

    print(f"\nMigration complete: {migrated} migrated, {skipped} skipped, {errors} errors")


if __name__ == '__main__':
    print("TINQAD Password Migration: SHA-256 -> bcrypt")
    print("=" * 50)
    migrate_passwords()
