import re


def split_into_sections(text):
    """
    Split a document into logical sections based on
    numbered headings.
    """

    text = text.replace("\r\n", "\n")

    matches = list(
        re.finditer(
            r"(?m)^\s*(\d+\.\s+[^\n]+)",
            text
        )
    )

    if not matches:
        return [text.strip()]

    sections = []

    # Introductory content before section 1
    if matches[0].start() > 0:
        intro = text[:matches[0].start()].strip()

        if intro:
            sections.append(intro)

    # Numbered sections
    for i, match in enumerate(matches):

        start = match.start()

        if i + 1 < len(matches):
            end = matches[i + 1].start()
        else:
            end = len(text)

        section = text[start:end].strip()

        if section:
            sections.append(section)

    return sections


def chunk_text(text):
    """
    Return logical document sections as chunks.
    """

    return split_into_sections(text)