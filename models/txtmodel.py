from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI


from langchain.chains import ConversationChain  

class txtmodel():

    def get_response(question):
        chat = ChatOpenAI()
        conversation = ConversationChain(llm=chat)

        # Si l'étudiant a cliqué sur "Tuteur Virtuel"
        if question.lower() == "virtual_tutor":
            return "Vous avez choisi le Tuteur Virtuel. Comment puis-je vous aider davantage ?"

        # Si l'étudiant a cliqué sur "Tuteur Réel"
        elif question.lower() == "real_tutor":
            return "Vous avez choisi le Tuteur Réel. Un tuteur réel sera disponible pour vous aider."

        # Sinon, traiter la question normalement
        return conversation.run(question)
