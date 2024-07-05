import sqlite3
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_name='branch_tracking.db'):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.setup_database()

    def setup_database(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS branches (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                branch_name TEXT NOT NULL,
                                repo_name TEXT NOT NULL,
                                creator TEXT NOT NULL,
                                created_at TEXT NOT NULL,
                                pr_opened_at TEXT,
                                merger TEXT,
                                merged_at TEXT,
                                reviewers TEXT,
                                details_hash TEXT,
                                UNIQUE(branch_name, repo_name)
                              )''')
        self.conn.commit()

    def fetch_unmerged_branches(self):
        self.cursor.execute('SELECT branch_name, repo_name FROM branches WHERE merged_at IS NULL')
        db_branches = self.cursor.fetchall()
        return [(row[0], row[1]) for row in db_branches]

    def fetch_branch_hash(self, branch_name, repo_name):
        self.cursor.execute('SELECT details_hash FROM branches WHERE branch_name=? AND repo_name=?', (branch_name, repo_name))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def save_branch_details(self, branch_name, repo_name, creator, created_at, pr_opened_at, merger, merged_at, reviewers, details_hash):
        self.cursor.execute('''
            INSERT INTO branches (branch_name, repo_name, creator, created_at, pr_opened_at, merger, merged_at, reviewers, details_hash)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(branch_name, repo_name) 
            DO UPDATE SET pr_opened_at=excluded.pr_opened_at, merger=excluded.merger, merged_at=excluded.merged_at, reviewers=excluded.reviewers, details_hash=excluded.details_hash
        ''', (branch_name, repo_name, creator, created_at, pr_opened_at, merger, merged_at, reviewers, details_hash))
        self.conn.commit()

    def update_branch_details(self, branch_name, repo_name, pr_opened_at, merger, merged_at, reviewers, details_hash):
        self.cursor.execute('''
            UPDATE branches
            SET pr_opened_at=?, merger=?, merged_at=?, reviewers=?, details_hash=?
            WHERE branch_name=? AND repo_name=?
        ''', (pr_opened_at, merger, merged_at, reviewers, details_hash, branch_name, repo_name))
        self.conn.commit()

    def fetch_all_branches(self):
        self.cursor.execute('SELECT * FROM branches')
        rows = self.cursor.fetchall()
        column_names = [description[0] for description in self.cursor.description]
        print(f"{' | '.join(column_names)}")
        for row in rows:
            print(f"{' | '.join(map(str, row))}")

    def close(self):
        self.conn.close()
