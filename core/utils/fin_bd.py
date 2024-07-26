import asyncpg


class FinBD:

    def __init__(self, user_id):
        """Connect to the database."""
        self.conn = psycopg2.connect(
            database="fin_bd",
            user="postgres",
            password="1234567890",
            host="localhost",
            port="5432"
        )
        self.cur = self.conn.cursor()

    def user_exists(self, user_id):
        """Check if the user in the database."""
        self.cur.execute("SELECT 'id' FROM 'users' WHERE user_id = %s", (user_id,))
        return bool(self.cur.fetchone())

    def get_user_id(self, user_id):
        """Get the user id from the database."""
        self.cur.execute("SELECT 'id' FROM 'users' WHERE user_id = %s", (user_id,))
        return self.cur.fetchone()[0]

    def add_user(self, user_id):
        """Add the user to the database."""
        self.cur.execute("INSERT INTO 'users' (user_id) VALUES (%s)", (user_id,))
        self.conn.commit()

    def add_record(self, user_id, amount, description):
        """Add the record to the database."""
        self.cur.execute("INSERT INTO 'financial_records' (user_id, amount, description) VALUES (%s, %s, %s)", (user_id, amount, description))
        self.conn.commit()

    def get_records(self, user_id):
        """Get the records of the user from the database."""
        self.cur.execute("SELECT * FROM 'financial_records' WHERE user_id = %s", (user_id,))
        return self.cur.fetchall()

    def __del__(self):
        self.cur.close()
        self.conn.close()