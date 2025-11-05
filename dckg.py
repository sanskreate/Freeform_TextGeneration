import re
from collections import Counter
import math

def generate_keywords(prompt: str, domain: str = None, top_n: int = 10):
    """Generate top keywords and phrases from a prompt.

    This implementation is intentionally lightweight and domain-agnostic. It
    returns a mix of single-word and two-word phrases ordered by a simple
    frequency-and-heuristic scoring function.
    """

    if not prompt:
        return []

    # Basic stopword set (kept small for performance)
    stopwords = {
        "the", "is", "in", "and", "to", "of", "a", "for", "on",
        "with", "as", "by", "an", "be", "are", "at", "from", "that",
        "this", "it", "or", "was", "but", "not", "can", "has", "have",
        "will", "which", "their", "more", "than", "about", "into",
        "also", "such", "other", "use", "used", "using", "these", "may",
        "been", "were", "should", "could", "would", "our", "your"
    }

    # Tokenize (lowercase) and extract words
    words = re.findall(r"\b[a-z0-9]+\b", prompt.lower())

    # Filter single words
    filtered_words = [w for w in words if w not in stopwords and len(w) > 3]

    # Bigrams from adjacent filtered words
    bigrams = []
    for i in range(len(filtered_words) - 1):
        bigrams.append(f"{filtered_words[i]} {filtered_words[i+1]}")

    word_freq = Counter(filtered_words)
    bigram_freq = Counter(bigrams)

    scored = {}
    total = sum(word_freq.values()) or 1

    # score single words
    for w, f in word_freq.items():
        tf = f / total
        length_boost = 1 + max(0, (len(w) - 4)) * 0.06
        scored[w] = tf * length_boost * (1 + (f - 1) * 0.15)

    # score bigrams with a phrase bonus
    for b, f in bigram_freq.items():
        tf = (f / total) * 1.8
        scored[b] = tf * 1.2

    # Return top_n by score
    results = [k for k, _ in sorted(scored.items(), key=lambda x: x[1], reverse=True)]
    return results[:top_n]