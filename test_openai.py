import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

api_key = os.getenv('OPENAI_API_KEY')
print(f"API Key: {api_key[:8]}..." if api_key else "No API Key found.")

try:
    openai.api_key = api_key
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a test assistant."},
            {"role": "user", "content": "Say hello!"}
        ],
        max_tokens=20
    )
    print("OpenAI response:", response.choices[0].message.content)
except Exception as e:
    print("OpenAI error:", e)
