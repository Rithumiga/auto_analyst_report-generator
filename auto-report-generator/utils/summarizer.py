import requests
from config import GROK_API_KEY, GROK_URL

def summarize_text(text, section_title="Summary"):
    prompt = f"Summarize the following text into a structured '{section_title}' section with key insights and recommendations:\n\n{text}"

    headers = {
        "Authorization": f"Bearer {GROK_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "grok-1",
        "input": prompt,
        "temperature": 0.5,
        "max_output_tokens": 800
    }

    response = requests.post(GROK_URL, headers=headers, json=payload)
    response_json = response.json()
    summary = response_json['output'][0]['content'][0]['text']
    return summary

# utils/summarizer.py

def summarize_text(text, section_title="Summary"):
    """
    Local fallback summarizer.
    Ignores Grok API and just returns a structured summary.
    """
    return local_summarize(text, section_title)

def local_summarize(text, section_title="Summary"):
    """
    Simple fallback summarizer for offline/demo use.
    """
    lines = text.split("\n")
    key_points = lines[:10]  # Take first 10 lines
    summary = f"{section_title}:\n" + "\n".join(key_points)
    return summary
