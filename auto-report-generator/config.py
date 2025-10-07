import os

# Grok API
GROK_API_KEY = os.getenv("GROK_API_KEY", "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")
GROK_URL = "https://api.grok.openai.com/v1/responses"

# Assets folder for charts/images
ASSETS_FOLDER = "assets/"
os.makedirs(ASSETS_FOLDER, exist_ok=True)
