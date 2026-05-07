from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from croppilot_app.models import ChatBot

vectorizer = TfidfVectorizer(stop_words='english')
questions = []
answers = []
X = None

def load_chatbot_data():
    global questions, answers, X

    data = ChatBot.objects.all()

    questions = [q.question for q in data]
    answers = [q.answers for q in data]

    if questions:
        X = vectorizer.fit_transform(questions)

# Load once
load_chatbot_data()


def get_bot_response(user_input):
    if X is None:
        return "Chatbot not ready"

    user_vec = vectorizer.transform([user_input.lower()])
    similarity = cosine_similarity(user_vec, X)

    index = similarity.argmax()
    score = similarity[0][index]

    if score < 0.4:
        return "Sorry, I don't understand. Ask about crops, soil, or fertilizer."

    return answers[index]