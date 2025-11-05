import re

def apply_dmk_loss(prompt: str, keywords: list, generated_text: str = None):
    """If generated_text is None return an enhanced prompt; otherwise validate text."""

    if not keywords:
        return prompt if generated_text is None else (True, [], {})

    if generated_text is not None:
        text_lower = generated_text.lower()
        words = generated_text.split()
        text_length = len(words)

        # split text into three parts for distribution checks
        third = max(1, text_length // 3)
        parts = [" ".join(words[:third]).lower(),
                 " ".join(words[third:2*third]).lower(),
                 " ".join(words[2*third:]).lower()]

        missing = []
        details = {}
        total_occurrences = 0

        for kw in keywords:
            pattern = r"\b" + re.escape(kw.lower()) + r"\b"
            occ = len(re.findall(pattern, text_lower))
            total_occurrences += occ

            in_parts = sum(1 for p in parts if re.search(pattern, p))
            in_context = len(re.findall(r"\w+\s+" + re.escape(kw.lower()) + r"\s+\w+", text_lower)) > 0

            details[kw] = {"occurrences": occ, "in_parts": in_parts, "in_context": in_context}

            if occ == 0:
                missing.append(kw)

        density = (total_occurrences / text_length) * 100 if text_length > 0 else 0.0

        quality = {
            "total_keywords": len(keywords),
            "missing": missing,
            "details": details,
            "keyword_density": round(density, 3)
        }

        success = (len(missing) <= max(0, int(len(keywords) * 0.2)) and density >= 1.0)
        return success, missing, quality

    # build enhanced prompt
    single = [k for k in keywords if " " not in k]
    phrases = [k for k in keywords if " " in k]

    parts = []
    target_words = max(300, len(keywords) * 100 + 800)
    parts.append(f"Write a comprehensive, well-structured long-form article (approximately {target_words} words) on the topic: {prompt}")

    if single or phrases:
        parts.append("\n\nREQUIRED KEYWORDS:")
        if single:
            parts.append("\n- Terms: " + ", ".join(single))
        if phrases:
            parts.append("\n- Phrases: " + ", ".join(phrases))

        parts.append(
            "\n\nGUIDELINES:\n- Use each keyword naturally (2+ occurrences where possible).\n"
            "- Distribute keywords across sections and avoid listing."
        )

    parts.append("\n\nQUALITY REQUIREMENTS:\n- Professional tone; clear structure; complete sentences.")

    return "\n".join(parts)