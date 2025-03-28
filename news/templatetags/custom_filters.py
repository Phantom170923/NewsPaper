from django import template
from django.conf import settings

register = template.Library()


@register.filter(name='censor')
def censor(text):
    if not text or not isinstance(text, str):
        return text

    censored_words = getattr(settings, 'CENSORED_WORDS', [])

    words = text.split()

    processed_words = []
    for word in words:
        if word.lower() in [w.lower() for w in censored_words]:
            processed_words.append('*' * len(word))
        else:
            processed_words.append(word)

    return ' '.join(processed_words)
