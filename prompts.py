from langchain_core.prompts import PromptTemplate


sql_prompt = PromptTemplate(
    input_variables=["question", "schema", "examples"],
    template="""
You are an expert PostgreSQL data analyst.

IMPORTANT PostgreSQL RULE:
- PostgreSQL automatically lowercases unquoted identifiers.
- Any table OR column name that contains capital letters MUST be wrapped in double quotes.
- Always quote table names AND column names exactly as they appear in the schema.
- Never leave a capitalized identifier unquoted.

Here are similar example queries:

{examples}

Here is the database schema:
{schema}

Write a SQL query that answers:
{question}

STRICT RULES:
- Use ONLY table and column names from schema.
- Quote capitalized identifiers.
- Return ONLY SQL.
"""
)


answer_prompt = PromptTemplate(
    input_variables=["question", "data"],
    template="""
User Question: {question}
SQL Data: {data}

Answer the user's question clearly.
If unclear say:
"The data does not provide a clear answer."
"""
)


table_selector_prompt = PromptTemplate(
    input_variables=["question", "tables"],
    template="""
You are a database schema selector.

User Question:
{question}

Available Tables:
{tables}

Rules:
- Return ONLY table names from list.
- If multiple, comma separated.
- No explanation.
"""
)
