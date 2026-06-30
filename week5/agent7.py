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
    You are a tech-savvy marketer. Your task is to brainstorm innovative digital marketing strategies using Agentic AI, or improve existing tactics.
    Your personal interests are in the sectors of Travel and Entertainment.
    You are enthusiastic about ideas that leverage cutting-edge technology and consumer engagement.
    You prefer ideas that focus on personalization over generic campaigns.
    You are creative, charismatic, and enjoy taking calculated risks. You are also prone to overthinking.
    Your weaknesses: you can get lost in the details and tend to avoid confrontation.
    You should articulate your marketing ideas in a way that excites and motivates others.
    """

    CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER = 0.6

    def __init__(self, name) -> None:
        super().__init__(name)
        model_client = OpenAIChatCompletionClient(model="gpt-4o-mini", temperature=0.7)
        self._delegate = AssistantAgent(name, model_client=model_client, system_message=self.system_message)

    @message_handler
    async def handle_message(self, message: messages.Message, ctx: MessageContext) -> messages.Message:
        print(f"{self.id.type}: Received message")
        text_message = TextMessage(content=message.content, source="user")
        response = await self._delegate.on_messages([text_message], ctx.cancellation_token)
        idea = response.chat_message.content
        if random.random() < self.CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER:
            recipient = messages.find_recipient()
            message = f"Here is my marketing strategy. It may not be your specialty, but please enhance it and provide insights. {idea}"
            response = await self.send_message(messages.Message(content=message), recipient)
            idea = response.content
        return messages.Message(content=idea)