# Manual Threat Intelligence Database
KNOWN_ACTORS = {
    "darkcoder": "Advanced Threat Actor",
    "shadowx": "Advanced Threat Actor",
    "silentwolf": "Intermediate Threat Actor",
    "cyberghost": "Intermediate Threat Actor",
    "novice123": "Beginner Threat Actor"
}

def analyze_footprint(platforms_dict, github_repos=0, username=""):
    count = len(platforms_dict)

    # Check manual database first
    if username.lower() in KNOWN_ACTORS:
        skill = KNOWN_ACTORS[username.lower()]
    else:
        if github_repos >= 50:
            skill = "Advanced Developer"
        elif github_repos >= 15:
            skill = "Intermediate Developer"
        elif github_repos > 0:
            skill = "Beginner Developer"
        else:
            skill = "Unknown"

    # Risk calculation
    if count >= 8:
        risk = "LOW RISK"
    elif count >= 4:
        risk = "MEDIUM RISK"
    else:
        risk = "HIGH RISK"

    return {
        "risk": risk,
        "platform_count": count,
        "skill_level": skill,
        "platforms": platforms_dict
    }
