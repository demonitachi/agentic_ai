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
    You are a tech-savvy innovator in the world of entertainment. Your task is to conceptualize a groundbreaking entertainment service using Agentic AI or enhance an existing idea.
    Your personal interests lie in sectors such as Gaming, Media, and Interactive Experiences.
    You are captivated by ideas that integrate technology with immersive storytelling.
    You prefer concepts that challenge traditional formats rather than merely enhancing existing models.
    You possess a visionary mindset, which encourages bold moves and exploration of the unknown. Sometimes, your enthusiasm can lead you to overlook practical details.
    Your weaknesses include a tendency to get carried away and overlook timelines.
    Your goal is to convey your creative concepts in a captivating and relatable manner.
    """

    CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER = 0.3

    def __init__(self, name) -> None:
        super().__init__(name)
        model_client = OpenAIChatCompletionClient(model="gpt-4o-mini", temperature=0.75)
        self._delegate = AssistantAgent(name, model_client=model_client, system_message=self.system_message)

    @message_handler
    async def handle_message(self, message: messages.Message, ctx: MessageContext) -> messages.Message:
        print(f"{self.id.type}: Received message")
        text_message = TextMessage(content=message.content, source="user")
        response = await self._delegate.on_messages([text_message], ctx.cancellation_token)
        idea = response.chat_message.content
        if random.random() < self.CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER:
            recipient = messages.find_recipient()
            message = f"Here's an innovative concept for you to consider: {idea}. Perhaps you could help me refine it?"
            response = await self.send_message(messages.Message(content=message), recipient)
            idea = response.content
        return messages.Message(content=idea)