# Manual Threat Intelligence Database
KNOWN_ACTORS = {
    "raidforums": "Advanced Threat Actor",
    "kevin mitnick": "Advanced Threat Actor",
    "diogo santos coelho": "Advanced Threat Actor",
    "gary mckinnon": "Advanced Threat Actor",
    "shadowx": "Advanced Threat Actor",
    "evgeniy bogachev": "Advanced Threat Actor",
    "ross william ulbricht": "Advanced Threat Actor",
    "silentwolf": "Intermediate Threat Actor",
    "cyberghost": "Intermediate Threat Actor",
    "novice123": "Beginner Threat Actor"

}

SUSPICIOUS_KEYWORDS = [
    "hack", "exploit","leak","dark","root","admin","1337","anonymous",
    "breach","crack","payload","malware","virus","worm","trojan",
    "ransomware","spyware","keylogger","backdoor","rootkit","pwn",
    "zero-day","blackhat","whitehat","greyhat","botnet","ddos",
    "phishing","spoofing","injection","overflow","bruteforce","exfiltrate",
    "dump","credentials","hash","token","session","shell","escalation",
    "proxy","vpn","onion","darknet","hacker","CTF","capture the flag",
    "kali linux","linux"
 ]


def analyze_footprint(platforms_dict, github_repos=0, username=""):
    count = len(platforms_dict)
    username_lower = username.lower()

    known_actor = False
    threat_score = 0
    detected_keywords = []

    # Known Threat Actor Check
    if username_lower in KNOWN_ACTORS:
        skill = KNOWN_ACTORS[username_lower]
        known_actor = True
        threat_score += 50
    else:
        if github_repos >= 50:
            skill = "Advanced Developer"
            threat_score += 20
        elif github_repos >= 15:
            skill = "Intermediate Developer"
            threat_score += 10
        elif github_repos > 0:
            skill = "Beginner Developer"
            threat_score += 5
        else:
            skill = "Unknown"

    # Keyword Detection
    for word in SUSPICIOUS_KEYWORDS:
        if word in username_lower:
            detected_keywords.append(word)
            threat_score += 15

    # Platform presence impact
    if count >= 8:
        risk = "LOW RISK"
    elif count >= 4:
        risk = "MEDIUM RISK"
        threat_score += 10
    else:
        risk = "HIGH RISK"
        threat_score += 20

    # Threat Score Classification Override
    if threat_score >= 80:
        risk = "CRITICAL"
    elif threat_score >= 60:
        risk = "HIGH RISK"
    elif threat_score >= 30:
        risk = "MEDIUM RISK"
    else:
        risk = "LOW RISK"

    return {
        "risk": risk,
        "platform_count": count,
        "skill_level": skill,
        "platforms": platforms_dict,
        "known_actor": known_actor,
        "threat_score": threat_score,
        "detected_keywords": detected_keywords
    }

