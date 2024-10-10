# ProfileBot - Your Personal Digital Assistant

ProfileBot is a Retrieval-Augmented Generation (RAG) based chatbot that helps recruiters interact with a candidate's profile (generally a bio or resume) in a question-and-answer format.
This application allows users to upload their own PDF document and leverage the power of Large Language Models (LLMs) to create a personalized digital assistant that can answer queries about the candidate.

## Features
- **Document-based Q&A**: Ask questions about your own document (e.g., resume, bio, or profile).
- **LLM-powered responses**: ProfileBot uses advanced language models from AWS Bedrock to generate intelligent and personalized responses.
- **Streamlit UI**: A user-friendly interface to interact with the bot in a conversational manner.
- **Customizable settings**: Modify configurations for the model, PDF file, and logging through environment variables.

## Prerequisites
Before setting up the application, ensure you have the following installed:
- Python 3.8 or above
- An AWS account with credentials for accessing AWS Bedrock services
- Pip for package management

## Getting Started

### 1. Clone the repository
Clone this repository to your local machine using:
```bash
git clone https://github.com/harinarayansrivatsan/profilebot.git
```

### 2. Install dependencies
Navigate to the project directory and install the required Python packages using `pip`:
```bash
cd profilebot
pip install -r requirements.txt
```

### 3. Add your own document
Replace the default `bio.pdf` file with your own PDF document. Ensure the file is named `bio.pdf` and located in the project directory.

### 4. Configure environment variables
Create `.env` files to store your AWS credentials and custom configurations. You can use the provided sample files for reference:

(Remove 'sample_' from the filenames before using)

- **`credentials.env`**: Store your AWS access key and secret key.

    ```bash
    AWS_ACCESS_KEY_ID=your-aws-access-key
    AWS_SECRET_ACCESS_KEY=your-aws-secret-key
    AWS_REGION=your-aws-bedrock-region
    ```

- **`config.env`**: Modify this file for customizable settings such as log configurations, model parameters, and PDF file path.

    ```bash
    LOG_FILE_PATH=your-log-file-path.log
    LOG_LEVEL=INFO
    LOG_FORMAT='Timestamp: %(asctime)s Log Level: %(levelname)s Message: %(message)s'

    CANDIDATE_FIRST_NAME=your-first-name
    CANDIDATE_MIDDLE_NAME=your-middle-name
    CANDIDATE_LAST_NAME=your-last-name

    STREAMLIT_PAGE_TITLE='your-page-title'
    STREAMLIT_PAGE_ICON=📝
    STREAMLIT_PAGE_LAYOUT='your-page-layout'
    STREAMLIT_TITLE_BODY='your-title-body'
    STREAMLIT_TITLE_DESCRIPTION='your-title-description'

    MODEL_ID='your-llm-model-id'
    MODEL_MAX_TOKENS_TO_SAMPLE=your-max-tokens-to-sample
    MODEL_TEMPERATURE=your-temperature
    MODEL_TOP_P=your-top-p

    PDF_FILE_PATH=your-pdf-file-path
    ```

### 5. Run the application
To launch the application, run the following command:
```bash
streamlit run app.py
```
Open your browser and go to the displayed URL (e.g., `http://X.X.X.X:8501`) to start interacting with your personal digital assistant.

### 6. Use the chatbot
Once the application is running, you can ask questions related to the contents of your uploaded PDF document. The chatbot will use the document as a source to provide accurate and relevant answers.

## Customization

### Change Document
You can replace the default `bio.pdf` file with any PDF document you want the assistant to answer questions about. Just ensure that the file path in the `config.env` is updated accordingly:

```bash
PDF_FILE_PATH=your-file.pdf
```

### Model Configuration
You can also customize the behavior of the language model by adjusting parameters in the `config.env` file, such as `MODEL_MAX_TOKENS_TO_SAMPLE`, `MODEL_TEMPERATURE`, and `MODEL_TOP_P`.

## Logging
The application logs important events such as user queries and model responses. You can find the logs in the file specified in the `LOG_FILE_PATH` (default is `chathistory.log`). You can also configure the log level and format through the `config.env`.

## System Prompts
ProfileBot uses a system prompt defined in `prompts.py`. This prompt governs the behavior and tone of the bot when interacting with users. You can customize the system prompt in the `prompts.py` file, specifically the `system_prompt` and `special_instructions` variables, to fit your specific requirements.

## Deploying on AWS EC2 with ALB
For users wanting to deploy this application on AWS, a `sample_streamlit.service` file is included. This allows you to set up ProfileBot as a service on an EC2 instance. Additionally, it can be configured to work with an Application Load Balancer (ALB) for enhanced availability and scalability.

## Future Improvements
- **Fetch documents from AWS S3**: Integrate support to fetch documents directly from an S3 bucket. This can help users store and retrieve documents more securely without needing to upload files manually.
- **Deployment on EC2 with ALB and custom domain**: Provide streamlined instructions for deploying ProfileBot on an EC2 instance with an Application Load Balancer and integrating a custom domain name using AWS Route 53.
- **UI Enhancement**: Improve the user interface by transitioning from Streamlit to a more modern framework like React or Vue.js for a better user experience and responsiveness.
