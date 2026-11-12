import requests

API_URL = "https://versions-clinton-girlfriend-boys.trycloudflare.com/generate"

def generate_story(language, genre, title, prompt):

    payload = {
        "language": language,
        "genre": genre,
        "title": title,
        "prompt": prompt
    }

    try:
        response = requests.post(
            API_URL,
            json=payload,
            timeout=300
        )

        response.raise_for_status()

        result = response.json()
        return result["story"]

    except requests.exceptions.RequestException as error:
        return f"Connection error: {error}"