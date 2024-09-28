from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain_openai import ChatOpenAI
from sqlalchemy import create_engine
from langchain_community.vectorstores import FAISS
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_openai import OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv
import pandas as pd
import streamlit as st
import os
from langchain_core.prompts import (
    ChatPromptTemplate,
    FewShotPromptTemplate,
    MessagesPlaceholder,
    PromptTemplate,
    SystemMessagePromptTemplate,
)

#set environment variable
load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv("OpenAI")

#load csv file
def date_format(x):
    return pd.to_datetime(x, format='%B %Y').to_period('M')
df = pd.read_csv("Google_Data.csv")
#change the data type
#df['Month of LOG_DATE'] = df['Month of LOG_DATE'].apply(date_format)
for column in df.columns:
    try:
        df[column] = pd.to_numeric(df[column].str.replace(',', ''))
    except (AttributeError, ValueError):
        pass
#print(df.dtypes)
#print(df.columns.tolist())
#print(df.head())

#change csv file into SQL file
engine = create_engine("sqlite:///Google_Data.db")
df.to_sql("Google_Data", engine, index=False, if_exists='replace')

googleDb = SQLDatabase(engine=engine)
#print(googleDb.dialect)
#print(googleDb.get_usable_table_names())

#googleDb.run("SELECT * FROM Google WHERE `Month of LOG_DATE` = 'December 2021';")

#create SQL agent
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
#agent_executor = create_sql_agent(llm, db = googleDb, agent_type="openai-tools", verbose=True)

#agent_executor.invoke({"input": "In Google, What is the average clicks"})

examples = [
    {
        "input": "List all advertisement infromation.",
        "query": "SELECT * FROM Google_Data;"},
    {
        "input": "What month corresponds to the maximum conversion value.",
        "query": "SELECT `Month of LOG_DATE` FROM Google_Data WHERE CONVERSION_VALUE_USD_COUNT = (SELECT MAX(CONVERSION_VALUE_USD_COUNT) FROM Google_Data);",
    },
    {
        "input": "List all network type during December 2021.",
        "query": "SELECT DISTINCT NETWORK FROM Google_Data WHERE `Month of LOG_DATE` = 'December 2021';",
    },
    {
        "input": "How many advertisements during April 2023",
        "query": "SELECT COUNT(*) FROM Google_Data WHERE `Month of LOG_DATE` = 'April 2023';",
    },
    {
        "input": "List all conversion times of the image advertisement",
        "query": "SELECT CONVERSIONS FROM Google_Data WHERE AD_TYPE = 'IMAGE_AD';",
    },
    {
        "input": "What is the minimum conversion value in the youtube?",
        "query": "SELECT MIN(CONVERSION_VALUE_USD_COUNT) FROM Google_Data WHERE NETWORK = 'YOUTUBE';",
    },
    {
        "input": "List all advertisement of of the shopping channel in the mixed network ",
        "query": "SELECT * FROM Google_Data WHERE ADVERTISING_CHANNEL_TYPE = 'SHOPPING' AND NETWORK = 'MIXED';",
    },
    {
        "input": "List all impressions of responsive advertisement.",
        "query": "SELECT IMPRESSIONS FROM Google_Data WHERE AD_TYPE = 'RESPONSIVE_SEARCH_AD';",
    },
    {
        "input": "which advertisement is the most cost-effective?",
        "query": "SELECT `Month of LOG_DATE`, NETWORK, AD_TYPE, (CONVERSION_VALUE_USD_COUNT/SPEND_USD) AS ConversionPerCost FROM Google_Data WHERE CONVERSION_VALUE_USD_COUNT > 0 AND SPEND_USD > 0 AND (CONVERSION_VALUE_USD_COUNT/SPEND_USD) > 0 ORDER BY ConversionPerCost DESC LIMIT 1;",
    },
    {
        "input": "Which advertisement has the highest spend?",
        "query": "SELECT * FROM Google_Data ORDER BY SPEND_USD DESC LIMIT 1;",
    },
    {
        "input": "How many advertisement are there",
        "query": "SELECT COUNT(*) FROM Google_Data",
    },
    {
        "input": "What is the average conversion times",
        "query": "SELECT AVG(CONVERSIONS) FROM Google_Data;",
    },
    {
        "input": "which advertisement is most cost efficient during 2023?",
        "query": "SELECT `Month of LOG_DATE`, NETWORK, AD_TYPE, (CONVERSION_VALUE_USD_COUNT/SPEND_USD) AS ConversionPerCost FROM Google_Data WHERE SUBSTR(`Month of LOG_DATE`, -4) = '2023' AND CONVERSION_VALUE_USD_COUNT > 0 AND SPEND_USD > 0 AND (CONVERSION_VALUE_USD_COUNT/SPEND_USD) > 0 ORDER BY ConversionPerCost DESC LIMIT 1;",
    },
    {
        "input": "which advertisement has highest spending during 2023?",
        "query": "SELECT * FROM Google_Data WHERE SUBSTR(`Month of LOG_DATE`, -4) = '2023' ORDER BY SPEND_USD DESC LIMIT 1;",
    },
    {
        "input": "List all advertisement during 2023.",
        "query": "SELECT * FROM Google_Data WHERE SUBSTR(`Month of LOG_DATE`, -4) = '2023';",
    },
    {
        "input": "which advertisement is the least cost efficient in 2022? Assume both spend and conversion greater than 0.",
        "query": "SELECT `Month of LOG_DATE`, NETWORK, AD_TYPE, (CONVERSION_VALUE_USD_COUNT/SPEND_USD) AS ConversionPerCost FROM Google_Data WHERE SUBSTR(`Month of LOG_DATE`, -4) = '2022' AND CONVERSION_VALUE_USD_COUNT > 0 AND SPEND_USD > 0 AND (CONVERSION_VALUE_USD_COUNT/SPEND_USD) > 0 ORDER BY ConversionPerCost ASC LIMIT 1;"
    },
    {
        "input": "what is the maximum spending?",
        "query": "SELECT MAX(SPEND_USD) FROM Google_Data;"
    },
    {
        "input": "what is the minimum clicks which clicks greater than 0?",
        "query": "SELECT MIN(CLICKS) FROM Google_Data WHERE CLICKS > 0;"
    }
]

example_selector = SemanticSimilarityExampleSelector.from_examples(
    examples,
    OpenAIEmbeddings(),
    FAISS,
    k=5,
    input_keys=["input"],
)

system_prefix = """You are an agent designed to interact with a SQL database.
Given an input question, create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer.
Unless the user specifies a specific number of examples they wish to obtain, always limit your query to at most {top_k} results.
You can order the results by a relevant column to return the most interesting examples in the database.
Never query for all the columns from a specific table, only ask for the relevant columns given the question.
You have access to tools for interacting with the database.
Only use the given tools. Only use the information returned by the tools to construct your final answer.
You MUST double check your query before executing it. If you get an error while executing a query, rewrite the query and try again.

DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database.

If the question does not seem related to the database, just return "I don't know" as the answer.

Here are some examples of user inputs and their corresponding SQL queries:"""

few_shot_prompt = FewShotPromptTemplate(
    example_selector=example_selector,
    example_prompt=PromptTemplate.from_template(
        "User input: {input}\nSQL query: {query}"
    ),
    input_variables=["input", "dialect", "top_k"],
    prefix=system_prefix,
    suffix="",
)

full_prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate(prompt=few_shot_prompt),
        ("human", "{input}"),
        MessagesPlaceholder("agent_scratchpad"),
    ]
)

prompt_val = full_prompt.invoke(
    {
        "input": "How many advertisement are there?",
        "top_k": 5,
        "dialect": "SQLite",
        "agent_scratchpad": [],
    }
)
#print(prompt_val.to_string())

memory = ConversationBufferMemory(memory_key="agent_scratchpad")
chatAgent = create_sql_agent(
    llm=llm,
    db=googleDb,
    prompt=full_prompt,
    memory=memory,
    verbose=True,
    agent_type="openai-tools",
)

#chatAgent.invoke({"input": "How many rows are there?"})

#chatAgent.invoke({"input": "List the advertisment type of top 3 conversation value"})

#set streamlit
st.set_page_config(page_title="Google Database")
st.title("Talk to your database")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Try to chat with your database!"):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = chatAgent.invoke({"input": prompt})
    with st.chat_message("assistant"):
        st.markdown(response["output"])
    st.session_state.messages.append({"role": "assistant", "content": response["output"]})