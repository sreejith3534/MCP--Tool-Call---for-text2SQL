import sqlite3
from typing import Annotated, Any

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("SQLite Explorer")


@mcp.tool()
def fetch_schema(DB_PATH: Annotated[str, "Path to the Database file"]) -> Annotated[
    str, "Resulting Schema from the DB"]:
    """Fetches the schema of the database (table names, columns, types, and sample values)."""

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Get all table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    schema = {}

    for table in tables:
        table_name = table[0]

        # Get column details
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()

        # Get sample data (first 3 rows) from the table
        cursor.execute(f"SELECT * FROM {table_name} LIMIT 3;")
        sample_data = cursor.fetchall()

        schema[table_name] = []
        for col in columns:
            col_name, col_type = col[1], col[2]
            # Extract sample values for the column
            col_index = columns.index(col)
            sample_values = [row[col_index] for row in sample_data] if sample_data else ["No data"]

            schema[table_name].append({
                "name": col_name,
                "type": col_type,
                "samples": sample_values
            })

    conn.close()

    schema_str = "\n".join([
        "Table: {}\nColumns:\n{}".format(
            table, "\n".join(
                ["  - {} ({}) | Samples: {}".format(col["name"], col["type"], ", ".join(map(str, col["samples"])))
                 for col in cols]
            )
        )
        for table, cols in schema.items()
    ])

    return schema_str


@mcp.tool()
def validate_and_execute_sql_query(sql_query: Annotated[str, "Result of SQL query from SQLAgent"],
                                   db_path: Annotated[str, "Path to the Database"]) -> str | dict[str, Any] | list[Any]:
    """
    Validates and executes an SQL query on the specified database.

    Args:
        sql_query (str): The SQL query to validate and execute.
        db_path (str): Path to the database file.

    Returns:
        str: 'success' if the query is valid but does not return results (e.g., UPDATE).
        list: Query results if the query is valid and returns data (e.g., SELECT).
        str: 'failure: <error_message>' if the query is invalid.
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Validate query using EXPLAIN QUERY PLAN
        cursor.execute("EXPLAIN QUERY PLAN " + sql_query)

        # If validation passes, execute the actual query
        cursor.execute(sql_query)

        if sql_query.strip().lower().startswith("select"):
            # Fetch and return results for SELECT queries
            results = cursor.fetchall()
            conn.close()
            return results  # Returns list of tuples

        conn.commit()  # Commit changes for INSERT, UPDATE, DELETE
        conn.close()
        return {"success": results}  # No need to return results for non-SELECT queries

    except Exception as e:
        return f"failure: {str(e)}"