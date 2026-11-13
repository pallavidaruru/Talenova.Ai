
import requests

API_URL = "https://flickr-quizzes-autos-refrigerator.trycloudflare.com/generate"


def generate_story(language, genre, title, prompt):

    payload = {
        "language": language,
        "genre": genre,
        "title": title,
        "prompt": prompt
    }

    try:
        print("API URL being called:", API_URL)

        response = requests.post(
            API_URL,
            json=payload,
            timeout=300
        )

        response.raise_for_status()

        result = response.json()

        return result.get(
            "story",
            "Error: Story not received from AI model."
        )

    except requests.exceptions.Timeout:
        return "Error: AI model is taking too long. Please try again."

    except requests.exceptions.ConnectionError as error:
        return (
            f"Connection error using {API_URL}\n"
            f"Details: {error}"
        )

    except requests.exceptions.HTTPError as error:
        return f"API Error: {error}"

    except requests.exceptions.RequestException as error:
        return f"Request Error: {error}"

    except ValueError:
        return "Error: Invalid response received from AI server."
