from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI


from langchain.chains import ConversationChain  

class txtmodel():

    def get_response(question):
        chat = ChatOpenAI()

        conversation = ConversationChain(llm=chat)  
        return conversation.run(question)
