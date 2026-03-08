def split_advice_sections(advice_text):
    """
    Splits AI generated financial advice into sections based on headers.
    Headers are identified as short lines ending with ':'.
    """

    sections = {}
    current_header = "Executive Summary"
    current_content = []

    if not advice_text or "API Error" in advice_text:
        return {"Error": advice_text}

    lines = advice_text.split("\n")

    for line in lines:

        stripped = line.strip()

        if not stripped:
            continue

        if stripped.endswith(":") and len(stripped) < 60:

            if current_content:
                sections[current_header] = "\n".join(current_content).strip()

            current_header = stripped[:-1]
            current_content = []

        else:
            current_content.append(line)

    if current_content:
        sections[current_header] = "\n".join(current_content).strip()

    return sections


def split_goal_sections(goal_text):
    """
    Parses goal planning output using same logic as advice parser.
    """

    return split_advice_sections(goal_text)