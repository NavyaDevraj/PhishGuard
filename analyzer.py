
import ipaddress
from urllib.parse import urlparse


def analyze_url(url):

    url = url.strip()

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    risk_score = 0
    indicators = []

    # 1. Check URL length
    if len(url) > 75:
        indicators.append("Unusually long URL")
        risk_score += 1

    # 2. Check HTTP connection
    if url.startswith("http://"):
        indicators.append("Insecure HTTP connection")
        risk_score += 2

    # 3. Check IP address
    hostname = urlparse(url).hostname

    try:
        ipaddress.ip_address(hostname)
        indicators.append("IP address used instead of domain")
        risk_score += 3

    except ValueError:
        pass

    # 4. Check @ symbol
    if "@" in url:
        indicators.append("@ symbol detected in URL")
        risk_score += 3

    # 5. Check suspicious keywords
    suspicious_keywords = [
        "login", "verify", "banking",
        "password", "account", "secure"
    ]

    found_keywords = []

    for word in suspicious_keywords:
        if word in url.lower():
            found_keywords.append(word)

    if found_keywords:
        indicators.append(
            "Suspicious keywords: " + ", ".join(found_keywords)
        )
        risk_score += 1

    # 6. Calculate risk level
    if risk_score <= 1:
        risk_level = "LOW"
    elif risk_score <= 4:
        risk_level = "MEDIUM"
    else:
        risk_level = "HIGH"

    return {
        "url": url,
        "score": risk_score,
        "risk": risk_level,
        "indicators": indicators
    }
