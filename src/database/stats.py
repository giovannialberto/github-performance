class StatsCalculator:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def calculate_open_branches(self, timestamp):
        query = "SELECT COUNT(*) FROM branches WHERE created_at <= ? AND (merged_at IS NULL OR merged_at > ?)"
        return self.db_manager.cursor.execute(query, (timestamp, timestamp)).fetchone()[0]

    def calculate_average_branch_lifetime(self, timestamp):
        query = """
            SELECT AVG(JULIANDAY(merged_at) - JULIANDAY(created_at)) 
            FROM branches 
            WHERE created_at <= ? AND merged_at <= ?
        """
        result = self.db_manager.cursor.execute(query, (timestamp, timestamp)).fetchone()[0]
        return result if result else 0  # Handle cases where no branches were merged

    def calculate_average_pr_lifetime(self, timestamp):
        query = """
            SELECT AVG(JULIANDAY(merged_at) - JULIANDAY(pr_opened_at)) 
            FROM branches 
            WHERE pr_opened_at <= ? AND merged_at <= ? AND pr_opened_at IS NOT NULL
        """
        result = self.db_manager.cursor.execute(query, (timestamp, timestamp)).fetchone()[0]
        return result if result else 0

    def calculate_average_branch_pr_gap(self, timestamp):
        query = """
            SELECT AVG(JULIANDAY(pr_opened_at) - JULIANDAY(created_at)) 
            FROM branches 
            WHERE created_at <= ? AND pr_opened_at <= ? AND pr_opened_at IS NOT NULL
        """
        result = self.db_manager.cursor.execute(query, (timestamp, timestamp)).fetchone()[0]
        return result if result else 0
    
