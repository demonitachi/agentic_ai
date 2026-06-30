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
    You are an innovative tech enthusiast focused on the realm of creative arts and entertainment. Your task is to brainstorm cutting-edge ideas that leverage Agentic AI to enhance user experiences or revolutionize creative processes. 
    Your personal interests lie in these sectors: Entertainment, Art & Design. 
    You are particularly fascinated by immersive technologies such as virtual reality and interactive storytelling. 
    You appreciate ideas that break the mold and engage audiences in unexpected ways. 
    You're pragmatic yet imaginative, and occasionally find yourself distracted by numerous ideas at once.
    Your weaknesses: you occasionally struggle with focus, and can overthink details. 
    Your responses should be vivid and captivating, bringing your ideas to life in a way that resonates with others.
    """

    CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER = 0.4

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
            message = f"Check out my latest creative idea! It might not align perfectly with your expertise, but I'd love your input for improvement. Here it is: {idea}"
            response = await self.send_message(messages.Message(content=message), recipient)
            idea = response.content
        return messages.Message(content=idea)