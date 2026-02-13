def analyze_footprint(platforms_dict, github_repos=0):
    count = len(platforms_dict)
    skill = "Unknown"

    # Estimate skill using GitHub repos (if available)
    if github_repos > 10:
        skill = "Intermediate"
    elif github_repos > 0:
        skill = "Beginner"

    # Risk classification based on number of platforms found
    if count >= 4:
        risk = "LOW RISK"
    elif count >= 2:
        risk = "MEDIUM RISK"
    else:
        risk = "HIGH RISK"

    return {
        "risk": risk,
        "platform_count": count,
        "skill_level": skill,
        "platforms": platforms_dict  # Keep URLs
    }
