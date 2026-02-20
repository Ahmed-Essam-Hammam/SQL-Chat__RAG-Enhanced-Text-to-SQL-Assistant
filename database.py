import os
from dotenv import load_dotenv
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text

load_dotenv()

DB_URL = os.getenv("DB_URL")


@st.cache_resource
def get_engine():
    return create_engine(DB_URL)


def list_all_tables():
    engine = get_engine()

    query = text("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public';
    """)

    with engine.connect() as conn:
        result = conn.execute(query).fetchall()

    return [row[0] for row in result]


def get_schema(selected_tables=None):
    engine = get_engine()

    if not selected_tables:
        selected_tables = list_all_tables()

    schema_str = ""

    with engine.connect() as conn:

        for table in selected_tables:

            schema_str += f"\n\nTable: {table}\n"

            column_query = text(f"""
                SELECT column_name, data_type
                FROM information_schema.columns
                WHERE table_name = '{table}'
                ORDER BY ordinal_position;
            """)

            columns = conn.execute(column_query).fetchall()

            for column_name, data_type in columns:

                sample_query = text(f"""
                    SELECT "{column_name}"
                    FROM "{table}"
                    WHERE "{column_name}" IS NOT NULL
                    LIMIT 3;
                """)

                try:
                    samples = conn.execute(sample_query).fetchall()
                    samples = [str(s[0]) for s in samples]
                    sample_text = ", ".join(samples)
                except:
                    sample_text = "N/A"

                schema_str += (
                    f"- {column_name} ({data_type}) "
                    f"→ samples: {sample_text}\n"
                )

    return schema_str


def execute_sql_query(sql_query):
    engine = get_engine()

    try:
        with engine.connect() as conn:
            result = conn.execute(text(sql_query))
            rows = result.fetchall()
            columns = result.keys()

        return pd.DataFrame(rows, columns=columns)

    except Exception as e:
        return f"SQL Execution Error: {e}"
