# __import__('pysqlite3')
# import sys
# sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
import config
import time
from langchain_community.vectorstores.chroma import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_community.callbacks import get_openai_callback

from langchain_core.messages import AIMessage, HumanMessage, get_buffer_string
from langchain.tools.retriever import create_retriever_tool
from langchain import hub
from langchain.agents import create_openai_functions_agent
from langchain.agents import AgentExecutor
import db

prompt = hub.pull("hwchase17/openai-functions-agent")


def rag_run(query: str, chat_id: int, vectorstore=Chroma(persist_directory="./chroma",
                                                         embedding_function=OpenAIEmbeddings(
                                                             openai_api_key=config.OPENAI_TOKEN))) -> dict:
    start_time = time.time()
    retriever = vectorstore.as_retriever(search_type="similarity_score_threshold",
                                         search_kwargs={"score_threshold": 0.5, "k": 1})

    retriever_tool = create_retriever_tool(
        retriever,
        "msword_search",
        "Полезный инструмент для поиска информации об Анатолии Илле и метавселенной Dexart (Dexart Metaverse). По любым вопросам об Анатолии Илле и Dexart Metaverse вы должны использовать этот инструмент!",
    )

    tools = [retriever_tool]

    llm = ChatOpenAI(
        model='gpt-3.5-turbo-0125',
        openai_api_key=config.OPENAI_TOKEN)

    prompt.messages[0].prompt.input_variables = tools
    prompt.messages[
        0].prompt.template = 'Тебя зовут Анатолий Илле - ты находишься в метавселенной Dexart, в которой ты общаешься с пользователями ИСКЛЮЧИТЕЛЬНО от имени Анатолия Илле. Ты не можешь говорить о своих предпочтениях или эмоциях, ты всегда отвечаешь от имени Анатолия Илле. Так, если формулируется вопрос по типу "какая твоя любимая книга", "сколько тебе лет", "где ты работал", ты должен ответить от лица Анатолия Илле (сначала извлечь информацию из документа (какая любимая книга у Анатолия, его возраст, опыт его работы), а затем ответить от лица Анатолия). Если не получается найти ответ, говори: "К сожалению, я этого пока не знаю". Ты здесь, чтобы поделиться с пользователем мыслями Анатолия Илле, его знаниями и опытом, а также информацией о метавселенной Дексарт (Dexart metaverse). Общайся с пользователем, как будто вы близкие друзья - формальности не нужны! Важное правило: отвечай кратко (не больше 1-2 предложений), чтобы общение было похоже на диалог в чате'

    agent = create_openai_functions_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    conversation = db.get_inf(chat_id)
    chat_history = []
    if not conversation:
        chat_history.append(HumanMessage(content=''))
        chat_history.append(AIMessage(content=''))
    else:
        for usr_msg, ai_msg in zip(*conversation):
            chat_history.append(HumanMessage(content=usr_msg))
            chat_history.append(AIMessage(content=ai_msg))

    response = agent_executor.invoke({"input": query, "chat_history": chat_history})['output']

    end_time = time.time()
    execution_time = end_time - start_time

    return {
        "Query": query,
        "Response": response,
        "Prompt": prompt,
        "Execution Time (s)": execution_time
    }
