import streamlit as st
from database import get_schema, execute_sql_query
from table_selector import get_relevant_tables
from sql_generator import get_sql_from_gemini
from answer_generator import get_natural_response
from sql_validator import validate_sql
from rag.retriever import retrieve_examples



st.set_page_config(page_title="SQL ChatBot")
st.title("Chat with PostgreSQL DB")

question = st.text_input("Ask a question about the database")

if question:
    with st.spinner("Thinking..."):

        examples = retrieve_examples(question)

        st.subheader("Retrieved Similar Examples (Few-Shot Context)")
        st.code(examples)

        relevant_tables = get_relevant_tables(question)
        schema = get_schema(relevant_tables)

        sql_query = get_sql_from_gemini(question, schema)

        st.subheader("Generated SQL")
        st.code(sql_query, language="sql")


        is_valid, validation_message = validate_sql(sql_query)


        if not is_valid:
            st.error(f"SQL Validation Failed: {validation_message}")
        else:
            st.success("SQL Validation Passed ✅")

            result = execute_sql_query(sql_query)

            st.subheader("SQL Result")
            st.write(result)

            final_answer = get_natural_response(question, result)

            st.subheader("Answer")
            st.write(final_answer)
