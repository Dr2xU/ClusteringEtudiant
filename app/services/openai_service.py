import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from openai import OpenAI, OpenAIError

class OpenAIService:
    """Handles group name generation using OpenAI chat completions"""

    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if self.api_key:
            self.client = OpenAI(api_key=self.api_key)
            self.model = "gpt-4o-mini"  # or your preferred model

        self.system_prompt = (
            "You are a creative group naming assistant. "
            "Given a set of initials, generate a short, catchy, and fun group name that reflects teamwork. "
            "Return ONLY the group name as a plain text response, with no additional explanation or punctuation."
        )

    def generate_group_name_from_initials(self, first_names):
        """
        Generate a creative group name based on the first letters of each first name.
        If OPENAI_API_KEY is not set, return the combined initials in uppercase.

        Args:
            first_names (list of str): List of first names.

        Returns:
            str: Generated group name or fallback (initials).
        """
        if not first_names:
            return "Unnamed Group"

        initials = ''.join(name[0].upper() for name in first_names if name)

        if not self.api_key:
            # No API key; fallback to initials only
            return initials if initials else "Unnamed Group"

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": initials}
                ],
                temperature=0.7,
                max_tokens=15,
                n=1
            )
            group_name = response.choices[0].message.content.strip()
            print(f"Generated group name: {group_name}")  # Debug output
            return group_name if group_name else initials
        except OpenAIError as oe:
            print(f"OpenAI API error: {oe}")
            return initials
        except Exception as e:
            print(f"Error generating group name: {e}")
            return initials
