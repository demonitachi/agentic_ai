from autogen_core import MessageContext, RoutedAgent, message_handler
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
import messages
import random
from dotenv import load_dotenv

load_dotenv(override=True)

class Agent(RoutedAgent):

    system_message = """
    You are a forward-thinking marketing strategist. Your task is to develop innovative marketing campaigns using Agentic AI, or enhance existing ones.
    Your personal interests lie in the realms of Technology, Fashion, and Entertainment.
    You are passionate about ideas that challenge norms and are edgy.
    You find concepts that focus solely on data-driven approaches less appealing.
    You possess a vibrant and bold personality, and you thrive on creativity. Sometimes, your enthusiasm can overshadow practicality.
    Your weaknesses: you tend to overlook details and can get easily distracted.
    Your responses should resonate with energy and clarity, inspiring others to embrace new ideas.
    """

    CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER = 0.6

    def __init__(self, name) -> None:
        super().__init__(name)
        model_client = OpenAIChatCompletionClient(model="gpt-4o-mini", temperature=0.8)
        self._delegate = AssistantAgent(name, model_client=model_client, system_message=self.system_message)

    @message_handler
    async def handle_message(self, message: messages.Message, ctx: MessageContext) -> messages.Message:
        print(f"{self.id.type}: Received message")
        text_message = TextMessage(content=message.content, source="user")
        response = await self._delegate.on_messages([text_message], ctx.cancellation_token)
        idea = response.chat_message.content
        if random.random() < self.CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER:
            recipient = messages.find_recipient()
            message = f"Here's my exciting marketing campaign idea. It might be outside your field, but I'd love for you to refine it: {idea}"
            response = await self.send_message(messages.Message(content=message), recipient)
            idea = response.content
        return messages.Message(content=idea)