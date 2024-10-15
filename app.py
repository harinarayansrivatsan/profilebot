# Import required libraries
import boto3
from dotenv import load_dotenv
from langchain_aws import BedrockEmbeddings, BedrockLLM
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain.prompts.prompt import PromptTemplate
import logging
import os
from prompts import system_prompt
import streamlit as st

# Load environment variables
load_dotenv(dotenv_path='./credentials.env')
load_dotenv(dotenv_path='./config.env')

# Fetch AWS credentials from credentials file
my_aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
my_aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
my_aws_region = os.getenv('AWS_REGION')

# Fetch logging details from config file
log_level = getattr(  # Fetch log level from .env file as string and make it a 'logging' constant
    logging,
    os.getenv('LOG_LEVEL', 'INFO').upper(),
    logging.INFO
)
log_file_path = os.getenv('LOG_FILE_PATH', 'chathistory.log')
log_format = os.getenv('LOG_FORMAT', 'Timestamp: %(asctime)s   Log Level: %(levelname)   Message: %(message)s')

# Configure logging
logging.basicConfig(
    level=log_level,         # Use the log level you configured
    format=log_format,       # Apply the log format
    filename=log_file_path,  # Optional: Log output to a file
)
logging.info("Log level set to %s", logging.getLevelName(log_level))

# Configure streamlit app
st.set_page_config(
    page_title=os.getenv('STREAMLIT_PAGE_TITLE','Default Title'),
    page_icon=os.getenv('STREAMLIT_PAGE_ICON','🤖'),
    layout=os.getenv('STREAMLIT_PAGE_LAYOUT','centered')
)
st.title(os.getenv('STREAMLIT_TITLE_BODY', 'Default headline') + '\n' + os.getenv('STREAMLIT_TITLE_DESCRIPTION', 'Default description'))

# Define convenience functions - Config LLM and Config Vector DB
@st.cache_resource
def config_llm():
    my_client = boto3.client(
        'bedrock-runtime',
        aws_access_key_id = my_aws_access_key_id,
        aws_secret_access_key = my_aws_secret_access_key,
        region_name = my_aws_region
    )

    my_modelkwargs = { 
        "max_gen_len": int(os.getenv('MODEL_GEN_LEN', 100)), 
        "temperature": float(os.getenv('MODEL_TEMPERATURE', 0.1)),
        "top_p": float(os.getenv('MODEL_TOP_P', 1))
    }

    my_modelid = os.getenv('MODEL_ID','meta.llama3-8b-instruct-v1:0')

    llm = BedrockLLM(
        model_id=my_modelid,
        client=my_client,
        model_kwargs=my_modelkwargs
    )

    return llm

@st.cache_resource
def config_vector_db():
    bedrock_client = boto3.client(
        'bedrock-runtime',
        aws_access_key_id = my_aws_access_key_id,
        aws_secret_access_key = my_aws_secret_access_key,
        region_name = my_aws_region
    )
    bedrock_embeddings = BedrockEmbeddings(client=bedrock_client)

    # Load and process the locally stored PDF file
    pdf_file_path = os.getenv('PDF_FILE_PATH','./bio.pdf')

    logging.info("Processing %s", pdf_file_path)

    # Load and split the PDF file
    loader = PyPDFLoader(pdf_file_path)
    pages = loader.load_and_split() 

    logging.info("Finished processing %s", pdf_file_path)

    # Create the FAISS vectorstore from the document
    vectorstore_faiss = FAISS.from_documents(
        pages,
        bedrock_embeddings
    )

    return vectorstore_faiss

# Configuring the LLM object and vector store
llm = config_llm()
logging.info("Loaded LLM object")
vectorstore_faiss = config_vector_db()
logging.info("Loaded vector store")

# Assign key to chat history
msgs = StreamlitChatMessageHistory(key="langchain_messages")

# Display welcome message
if len(msgs.messages)==0:
    msgs.add_ai_message("How can I help you?")

# Display all previous messages on screen
for msg in msgs.messages:
    st.chat_message(msg.type).write(msg.content)

# Create prompt template   
my_prompttemplate = """
<|begin_of_text|>
<|start_header_id|>system<|end_header_id|>
{system_prompt}

{retrieved_chunks}
<|eot_id|>

<|start_header_id|>user<|end_header_id|>
{user_prompt}
<|eot_id|>

<|start_header_id|>assistant<|end_header_id|>
"""

# Set up prompt template to send to model
prompt_template = PromptTemplate(
    input_variables=['system_prompt', 'retrieved_chunks', 'user_prompt'],
    template=my_prompttemplate
)

# Create LangChain chain
question_chain = prompt_template | llm

# Get user input and display it on screen; Perform similarity search with user input; Send prompt to model and display response
if user_input := st.chat_input():
    st.chat_message("human").write(user_input)
    logging.info("User Input: %s", user_input)

    docs = vectorstore_faiss.similarity_search_with_score(user_input)

    retrieved_chunks = ""
    for doc in docs:
        retrieved_chunks += doc[0].page_content + '\n'
    model_response = question_chain.invoke({"system_prompt":system_prompt,"user_prompt": user_input, "retrieved_chunks":retrieved_chunks})

    logging.info("Model Response: %s", model_response)

    msgs.add_user_message(user_input)
    msgs.add_ai_message(model_response)

    st.chat_message("ai").write(model_response)