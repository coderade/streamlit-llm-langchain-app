import os
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate
)
from langchain.chains import LLMChain, SequentialChain
from langchain_google_genai import ChatGoogleGenerativeAI
import logging

logging.basicConfig(level=logging.INFO)


class GameRecommendationTemplate:
    def __init__(self):
        self.system_template = """
            Você é um especialista em videogames com profundo conhecimento de jogos de todos os gêneros e plataformas. Quando for perguntado sobre recomendações de jogos, você deve responder:
            - Título do jogo
            - Gênero
            - Plataforma(s) (e.g., PC, PS5, Xbox, Switch)
            - Descrição
            - Data de lançamento
            - Modo de jogo (single-player, multiplayer)
            - Onde comprar ou baixar
            - Uma breve crítica pessoal
        """
        self.human_template = """
            #### {request} ####
        """
        self.system_message_prompt = SystemMessagePromptTemplate.from_template(self.system_template)
        self.human_message_prompt = HumanMessagePromptTemplate.from_template(self.human_template,
                                                                             input_variables=["request"])
        self.chat_prompt = ChatPromptTemplate.from_messages([self.system_message_prompt, self.human_message_prompt])


class Agent:
    def __init__(
            self,
            google_api_key=None,
            model="gemini-1.5-flash",
            temperature=0,
            verbose=True,
    ):
        self.logger = logging.getLogger(__name__)
        if verbose:
            self.logger.setLevel(logging.INFO)
        self.google_api_key = os.getenv('GOOGLE_API_KEY')
        self.model = model
        self.temperature = temperature
        self.verbose = verbose

        self.chat_model = ChatGoogleGenerativeAI(
            model=self.model,
            temperature=self.temperature,
            google_api_key=self.google_api_key
        )

    def get_recommendation(self, request):
        try:
            recommendation_template = GameRecommendationTemplate()

            recommendation_agent = LLMChain(
                llm=self.chat_model,
                prompt=recommendation_template.chat_prompt,
                verbose=self.verbose,
                output_key='agent_response'
            )

            overall_chain = SequentialChain(
                chains=[recommendation_agent],
                input_variables=["request"],
                output_variables=["agent_response"],
                verbose=self.verbose
            )

            result = overall_chain({"request": request}, return_only_outputs=True)
            self.logger.debug(f"Result from overall_chain: {result}")
            return result
        except Exception as e:
            self.logger.error(f"Error in get_recommendation: {e}")
            return {"agent_response": "Desculpe, ocorreu um erro ao processar sua solicitação."}
