import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'exam_portal.settings')
django.setup()

from exams.models import Question
from django.contrib.auth.models import User

# Get the admin user
admin_user = User.objects.filter(username='admin').first()

# Paste your 150 questions here in this exact format
questions_data = [
    # French
    ("French", "Comment tu t'appelles ?", "Je m'appelle Paul.", "J'ai dix ans.", "Ça va bien.", "J'habite à Lagos.", "A"),
    ("French", "Quel âge as-tu ?", "J'ai dix ans.", "Je m'appelle Paul.", "Ça va bien.", "Je suis Nigérian.", "A"),
    ("French", "Comment ça va ?", "Ça va bien.", "Je m'appelle Paul.", "J'ai dix ans.", "J'habite à Lagos.", "A"),
    # ... Add the rest of your 50 French questions here ...

    # English
    ("English", "What is your name?", "My name is John.", "I am ten years old.", "I am fine.", "I live in Lagos.", "A"),
    ("English", "How old are you?", "I am ten years old.", "My name is John.", "I am fine.", "I live in Lagos.", "A"),
    # ... Add the rest of your 50 English questions here ...

    # Yoruba
    ("Yoruba", "Kí ni orúkọ rẹ?", "Orúkọ mi ni Adé.", "Orúkọ mi ni Bọ́lá.", "Orúkọ mi ni Ṣadé.", "Orúkọ mi ni Túndé.", "A"),
    # ... Add the rest of your 50 Yoruba questions here ...
]

def seed():
    print("Seeding questions...")
    count = 0
    for lang, text, opt_a, opt_b, opt_c, opt_d, correct in questions_data:
        # Avoid duplicates if the build runs multiple times
        if not Question.objects.filter(text=text).exists():
            Question.objects.create(
                language=lang,
                text=text,
                option_a=opt_a,
                option_b=opt_b,
                option_c=opt_c,
                option_d=opt_d,
                correct_answer=correct,
                created_by=admin_user
            )
            count += 1
    print(f"Successfully added {count} questions!")

if __name__ == '__main__':
    seed()