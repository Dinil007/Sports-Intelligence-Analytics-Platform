from sqlalchemy import text
import pandas as pd
from database.db_connection import engine


def execute_query(sql_query: str):
    """
    Execute a read-only SQL query and return a DataFrame.
    """

    # Basic safety check
    allowed = sql_query.strip().lower()

    if not (allowed.startswith("select") or allowed.startswith("with")):
        raise ValueError("Only SELECT queries are allowed.")

    return pd.read_sql(text(sql_query), engine)