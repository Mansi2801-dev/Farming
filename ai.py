import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# 🔑 Use your Groq API key
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

# 🔹 Language mapping
LANGUAGE_MAP = {
    "hi": "Hindi",
    "en": "English",
    "mr": "Marathi",
    "pa": "Punjabi",
    "kn": "Kannada",
    "ta": "Tamil",
    "te": "Telugu"
}


def get_ai_response(query, context, language="en"):
    try:
        lang_name = LANGUAGE_MAP.get(language, "the same language as the query")

        # Extract context safely
        crop = context.get("crop", "unknown")
        current_price = context.get("current_price", "not available")
        last_week_price = context.get("last_week_price", "not available")
        weather = context.get("weather", "not available")

        # 🔥 Strong Prompt
        prompt = f"""
You are an expert agricultural advisor helping Indian farmers.

Farmer Query:
"{query}"

Context:
- Crop: {crop}
- Current Price: {current_price}
- Last Week Price: {last_week_price}
- Weather: {weather}

Instructions:
1. Respond in {lang_name}
2. Give a clear decision (Sell now / Wait / Recommended crop)
3. Give a short, simple reason
4. Keep it easy for farmers to understand
5. Avoid technical terms

Format strictly:

Decision:
<your answer>

Reason:
<your explanation>
"""

        # 🔹 Groq API call
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a helpful agricultural expert."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"""
Decision:
Error

Reason:
Something went wrong. Please try again.
Details: {str(e)}
"""


# 🔹 Test it directly
if __name__ == "__main__":
    query = "Should I sell wheat now?"

    context = {
        "crop": "Wheat",
        "current_price": 2100,
        "last_week_price": 1900,
        "weather": "Clear"
    }

    language = "en"

    print(get_ai_response(query, context, language))