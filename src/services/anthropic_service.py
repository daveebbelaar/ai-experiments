import anthropic
import os
import json
from dotenv import load_dotenv


class AnthropicService:
    def __init__(self):
        load_dotenv()
        self.llm = anthropic.Anthropic(
            api_key=os.getenv("ANTHROPIC_API_KEY"),
        )

    def generate_reponse(self, prompt: str):

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

        message = self.llm.messages.create(
            # model="claude-3-opus-20240229",  # Most powerful model
            model="claude-3-sonnet-20240229",  # Most balanced model
            max_tokens=1000,
            temperature=0.0,
            system=SYSTEM_PROMPT,
            messages=[
                {"role": "user", "content": prompt},
                {
                    "role": "assistant",
                    "content": "{",
                },  # Prefill Claude's response to force JSON output
            ],
        )

        # Attempt to correctly escape and format the JSON string
        try:
            # Create a valid JSON string with the escaped content
            json_string = "{" + message.content[0].text
            result = json.loads(json_string)
            return result
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
            return None


anthropic_service = AnthropicService()


result = anthropic_service.generate_reponse(
    prompt="Write a linkedin post about the often overlooked importance data plays in AI strategy."
)

print(result["content"])
