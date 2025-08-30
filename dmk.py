def apply_dmk_loss(prompt, keywords, generated_text=None):
    """
    Simulate traditional DMK loss enforcement:
    - If generated_text is provided, check if all keywords are present.
    - If not, return a flag or re-prompt.
    - If not provided, just return the prompt with keyword constraints.
    """
    if not keywords:
        return prompt if generated_text is None else (True, [])

    # If checking generated text, enforce keyword presence
    if generated_text is not None:
        missing = [kw for kw in keywords if kw.lower() not in generated_text.lower()]
        if missing:
            return False, missing  # Indicates DMK constraint not satisfied
        return True, []  # All keywords present

    # For prompting, instruct the model to include keywords
    instruction = (
        f"Write a comprehensive, well-structured long-form article (minimum {len(keywords) * 100 + 750} words) that naturally incorporates all of these important keywords: {', '.join(keywords)}. "
        f"Ensure the article is complete with a proper conclusion. Do not end abruptly or leave sentences unfinished. "
        f"The keywords should be woven seamlessly into the content, not just listed. "
        f"Context: {prompt}"
    )
    return instruction