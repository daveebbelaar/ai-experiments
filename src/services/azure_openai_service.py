import os
from openai import AzureOpenAI
from dotenv import load_dotenv
from openai._types import NotGiven
import json

NOT_GIVEN = NotGiven()


class AzureOpenAIService:
    def __init__(self):
        load_dotenv()
        self.azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        self.api_key = os.getenv("AZURE_OPENAI_KEY")
        self.api_version = "2023-12-01-preview"
        self.deployment_name = "gpt-4-turbo"
        self.message_history = []

    @property
    def client(self):
        if not hasattr(self, "_client"):
            self._client = AzureOpenAI(
                azure_endpoint=self.azure_endpoint,
                api_key=self.api_key,
                api_version=self.api_version,
            )
        return self._client

    def chat_completion_one_shot(
        self,
        messages: list,
        max_tokens: int | NotGiven = NOT_GIVEN,
        temperature: int | NotGiven = NOT_GIVEN,
        response_format: dict | NotGiven = NOT_GIVEN,
    ):
        # Is stateless and doesn't store the message history
        response = self.client.chat.completions.create(
            model=self.deployment_name,  # deployment name used in Azure
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
            response_format=response_format,
        )
        return response.choices[0].message.content

    def generate_response(self, prompt: str):

        SYSTEM_PROMPT = (
            "You are a marketing expert, specialized in writing LinkedIn posts to build a personal brand on the platform."
            "Always start with a strong hook on the first line and limit posts to 800 characters or less."
            "Use emoijs where appropriate, but never more than 3 in one post"
            "The user will provide the topics and extra details to include in the post."
            "Output in JSON format, with the following keys: content, keywords, title"
            "content: the full linkedin post, with the content properly escaped and formatted with every paragraph separated by a newline character."
            "keywords: list of relevant keywords for the post,"
            "title: a title for the post for internal reference in CMS"
        )

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ]

        try:
            response = self.chat_completion_one_shot(
                messages=messages,
                response_format={"type": "json_object"},
                temperature=0,
            )
            response_json = json.loads(response)
            return response_json
        except json.JSONDecodeError:
            print("Could not parse headers due to invalid JSON")
            return None


azure_openai_service = AzureOpenAIService()

result = azure_openai_service.generate_response(
    prompt="Write a linkedin post about the often overlooked importance data plays in AI strategy."
)

print(result["content"])
