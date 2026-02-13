import requests
from bs4 import BeautifulSoup

platforms = {
    "GitHub": {"url": "https://github.com/{}", "error_text": "Not Found"},
    "Twitter": {"url": "https://twitter.com/{}", "error_text": "Sorry, that page doesn’t exist"},
    "Reddit": {"url": "https://www.reddit.com/user/{}", "error_text": "Sorry, nobody on Reddit"},
    "Instagram": {"url": "https://www.instagram.com/{}", "error_text": "Sorry, this page isn’t available"},
    "LinkedIn": {"url": "https://www.linkedin.com/in/{}", "error_text": "profile not found"},
    "Facebook": {"url": "https://www.facebook.com/{}", "error_text": "content not available"},
    "TikTok": {"url": "https://www.tiktok.com/@{}", "error_text": "Page not found"},
    "Pinterest": {"url": "https://www.pinterest.com/{}", "error_text": "Page Not Found"},
    "Medium": {"url": "https://medium.com/@{}", "error_text": "Page not found"},
    "YouTube": {"url": "https://www.youtube.com/{}", "error_text": "Page not found"},
    "StackOverflow": {"url": "https://stackoverflow.com/users/{}", "error_text": "Page not found"},
    "SoundCloud": {"url": "https://soundcloud.com/{}", "error_text": "Page not found"},
}

def get_github_repos(username):
    try:
        url = f"https://github.com/{username}"
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, "html.parser")
            repo_tag = soup.find("span", {"class": "Counter"})
            if repo_tag:
                return int(repo_tag.text.strip())
    except:
        pass
    return 0

def check_platforms(username):
    found = {}
    github_repos = 0

    for name, info in platforms.items():
        url = info["url"].format(username)
        try:
            r = requests.get(url, timeout=5)
            if r.status_code == 200 and info["error_text"].lower() not in r.text.lower():
                found[name] = url
                if name == "GitHub":
                    github_repos = get_github_repos(username)
        except:
            pass

    return found, github_repos
