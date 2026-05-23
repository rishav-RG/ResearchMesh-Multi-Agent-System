from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import web_search , scrape_url
from dotenv import load_dotenv

load_dotenv()

# create llm model
llm = ChatOpenAI(model = "gpt-4.1-mini",temperature=0)

# web search agent
def build_search_agent():
    return create_agent(
        model = llm,
        tools = [web_search]
    )

# scrape reader agent
def build_reader_agent():
    return create_agent(
        model = llm,
        tools = [scrape_url]
    )

