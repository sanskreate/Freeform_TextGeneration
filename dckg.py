import re
from collections import Counter

def generate_keywords(prompt, domain, top_n=10):
    """
    Lightweight keyword extraction using word frequency and stopwords.
    """
    stopwords = set([
        "the", "is", "in", "and", "to", "of", "a", "for", "on", "with", "as", "by", "an", "be", "are", "at", "from", "that", "this", "it", "or", "was", "but", "not", "can", "has", "have", "will", "which", "their", "more", "than", "about", "into", "also", "such", "other", "use", "used", "using", "these", "may", "been", "were", "should", "could", "would", "our", "your", "his", "her", "its", "they", "them", "he", "she", "we", "you", "i"
    ])
    words = re.findall(r'\w+', prompt.lower())
    keywords = [w for w in words if w not in stopwords and len(w) > 3]
    freq = Counter(keywords)
    return [w for w, _ in freq.most_common(top_n)]