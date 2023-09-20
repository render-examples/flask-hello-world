import requests
from bs4 import BeautifulSoup
import langchain
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.llms import OpenAI
from langchain import PromptTemplate

from models import scrapPdf as sp
from models import scrapUrl as su

from flask import Flask, request
from flask import jsonify

class Llm:
    def callLlm(user_question, url):

        if url.endswith(".pdf"):
            scrap = sp.ScrapPdf.load_pdf_content(url)
            print("URL "+scrap)
        else:
            scrap = su.ScrapUrl.scrapUrl(url)
            print("URL "+scrap)

        # scapping text from PDF
        # scrapP = sp.load_pdf_content("C:/Users/JerryHeritiana(RAPP)/OneDrive - OneWorkplace/Documents/IAGORA/FUNCHATGPTSerge.pdf")
        # scrapP = sp.load_pdf_content("https://www.furet.com/media/pdf/feuilletage/9/7/8/2/8/0/4/1/9782804171018.pdf")
        # scrapU = su.scrapUrl("https://en.wikipedia.org/wiki/GPT-4")

        text = scrap.replace('\n', '')

        # Open a new file called 'output.txt' in write mode and store the file object in a variable
        with open('output.txt', 'w', encoding='utf-8') as file:
            # Write the string to the file
            file.write(text)

        # load the document
        with open('./output.txt', encoding='utf-8') as f:
            text = f.read()

        # define the text splitter
        text_splitter = RecursiveCharacterTextSplitter(    
            chunk_size = 500,
            chunk_overlap  = 100,
            length_function = len,
        )

        texts = text_splitter.create_documents([text])

        # define the embeddings model
        embeddings = OpenAIEmbeddings()

        # use the text chunks and the embeddings model to fill our vector store
        db = Chroma.from_documents(texts, embeddings)

        # user_question = "C'est quoi chatGPT"

        # use our vector store to find similar text chunks
        results = db.similarity_search(
            query = user_question,
            n_results=5
        )

        # define the prompt template
        template = """
        Tu es un chat bot qui aime aider les gens ! Compte tenu des sections contextuelles suivantes, répondez à la
        question en utilisant uniquement le contexte donné. Si tu n'es pas sûr et que la réponse n'est pas
        explicitement écrite dans la documentation, dites "Désolé, je ne sais pas comment vous aider."

        Context sections:
        {context}

        Question:
        {users_question}

        Answer:
        """

        prompt = PromptTemplate(template=template, input_variables=["context", "users_question"])

        # fill the prompt template
        prompt_text = prompt.format(context = results, users_question = user_question)
        # print(prompt_text)

        # define the LLM you want to use
        llm = OpenAI(temperature=1)

        # ask the defined LLM
        result = llm(prompt_text)
        print(result.encode("utf-8"))
        return result.encode("utf-8")