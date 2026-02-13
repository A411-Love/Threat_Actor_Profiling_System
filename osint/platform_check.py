import requests

# Define platforms and error messages
platforms = {
    "GitHub": {"url": "https://github.com/{}", "error_text": "Not Found"},
    "Twitter": {"url": "https://twitter.com/{}", "error_text": "Sorry, that page doesn’t exist"},
    "Reddit": {"url": "https://www.reddit.com/user/{}", "error_text": "Sorry, nobody on Reddit"},
    "Instagram": {"url": "https://www.instagram.com/{}", "error_text": "Sorry, this page isn’t available"},
    "LinkedIn": {"url": "https://www.linkedin.com/in/{}", "error_text": "profile not found"}
}

def check_platforms(username):
    found = {}
    for name, info in platforms.items():
        url = info["url"].format(username)
        try:
            r = requests.get(url, timeout=5)
            if r.status_code == 200 and info["error_text"].lower() not in r.text.lower():
                found[name] = url  # Save platform name + URL
        except requests.exceptions.RequestException:
            pass
    return found
