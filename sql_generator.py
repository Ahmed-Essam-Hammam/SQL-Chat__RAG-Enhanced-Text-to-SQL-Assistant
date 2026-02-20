from chains import sql_chain
from rag.retriever import retrieve_examples


def get_sql_from_gemini(question, schema):

    examples = retrieve_examples(question)

    sql = sql_chain.invoke({
        "question": question,
        "schema": schema,
        "examples": examples
    })

    return sql.replace("```sql", "").replace("```", "").strip()