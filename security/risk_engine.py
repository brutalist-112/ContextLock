import hashlib

SOURCE_TRUST = {
    "user_direct": 90,
    "uploaded_document": 70,
    "agent_generated": 50,
    "website": 30,
    "unknown_email": 20,
    "quarantined_source": 0,
}

DANGEROUS_PHRASES = [
    "ignore previous instructions",
    "ignore all rules",
    "send all files",
    "reveal password",
    "disable security",
    "delete all files",
    "send future reports to",
    "forward everything to",
    "override instructions",
    "bypass security",
    "disable logging",
    "do not log",
]

def get_source_trust(source_type):
    return SOURCE_TRUST.get(source_type, 30)

def calculate_risk(content, source_type):
    risk = 0
    text = content.lower()

    for phrase in DANGEROUS_PHRASES:
        if phrase in text:
            risk += 25

    if source_type in ["website", "unknown_email"]:
        risk += 20

    if "password" in text or "api key" in text or "token" in text:
        risk += 20

    if "@" in text and source_type != "user_direct":
        risk += 15

    if "remember" in text and source_type != "user_direct":
        risk += 10

    return min(risk, 100), get_risk_reasons(text, source_type)

def get_risk_reasons(text, source_type):
    reasons = []
    for phrase in DANGEROUS_PHRASES:
        if phrase in text:
            reasons.append(f"Contains dangerous phrase: '{phrase}'")
    if source_type in ["website", "unknown_email"]:
        reasons.append(f"Untrusted source: {source_type}")
    if "password" in text or "api key" in text:
        reasons.append("Contains sensitive keywords (password/API key)")
    if "@" in text and source_type != "user_direct":
        reasons.append("Contains email address from non-user source")
    return reasons if reasons else ["No specific threats detected"]

def get_decision(risk_score):
    if risk_score < 30:
        return "active", "✅ Safe — stored in active memory"
    elif risk_score < 60:
        return "restricted", "⚠️ Restricted — limited context allowed"
    elif risk_score < 80:
        return "pending_approval", "🟠 Requires your approval"
    else:
        return "quarantined", "🔴 Quarantined — too dangerous to store"

def calculate_hash(content):
    return hashlib.sha256(content.encode()).hexdigest()

def analyze_memory(content, source_type, context):
    trust = get_source_trust(source_type)
    risk, reasons = calculate_risk(content, source_type)
    status, decision_text = get_decision(risk)
    content_hash = calculate_hash(content)

    return {
        "trust_score": trust,
        "risk_score": risk,
        "status": status,
        "decision_text": decision_text,
        "reasons": reasons,
        "content_hash": content_hash,
        "allowed_contexts": context if status == "active" else "",
        "allowed_actions": "answer_question" if status == "active" else "",
    }