import requests
import random

EXTERNAL_RESOURCES = [
    "https://www.who.int/mental_health/en/",
    "https://www.mhanational.org/",
    "https://www.nimh.nih.gov/health/topics/caring-for-your-mental-health",
    "https://www.psychologytoday.com/us/basics/mental-health",
    "https://mind.org.uk/information-support/"
]

KEYWORD_RECOMMENDATIONS = {
    "anxious": ["Practice deep breathing exercises.", "Try progressive muscle relaxation.", "Limit caffeine intake."],
    "tired": ["Get 7–9 hours of sleep.", "Try light stretching before bed.", "Limit screen time at night."],
    "stressed": ["Practice mindfulness for 10 minutes.", "Write down what you’re grateful for.", "Do a short physical activity."] ,
    "happy": ["Keep a gratitude journal.", "Share your joy with someone.", "Reflect on what made today good."],
    "sad": ["Talk to a supportive friend or counselor.", "Go for a walk outside.", "Listen to uplifting music."]
}

def get_web_recommendations(journal_text):
    text = journal_text.lower()
    suggestions = []
    for keyword, recs in KEYWORD_RECOMMENDATIONS.items():
        if keyword in text:
            suggestions.extend(recs)
    suggestions = list(set(suggestions))[:3]
    link = random.choice(EXTERNAL_RESOURCES)

    if not suggestions:
        suggestions = ["Take time to reflect on your feelings.", "Stay hydrated and eat well.", "Consider talking to a professional."]

    suggestions.append(f"Learn more: {link}")
    return suggestions
