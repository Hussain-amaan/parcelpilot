import re


def clean_text(text):
    """
    Clean layout-preserved PDF text while keeping
    meaningful paragraphs, sections, and bullet points.
    """

    # Normalize line endings
    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    # Normalize bullet characters
    text = text.replace("●", "-")

    # Remove excessive spaces at the beginning/end of lines
    lines = []

    for line in text.split("\n"):
        line = line.strip()

        if line:
            # Collapse repeated spaces
            line = re.sub(r"[ \t]+", " ", line)
            lines.append(line)
        else:
            # Preserve a blank line as a paragraph separator
            if lines and lines[-1] != "":
                lines.append("")

    # Remove excessive blank lines
    cleaned = "\n".join(lines)

    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)

    return cleaned.strip()