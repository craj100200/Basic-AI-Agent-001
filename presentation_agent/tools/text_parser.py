def parse_slides(file_path):
    slides = []

    with open(file_path, "r") as f:
        lines = [line.strip() for line in f.readlines()]

    i = 0
    while i < len(lines):
        if lines[i] == "[SLIDE_START]":
            i += 1

            # Read title
            if lines[i] != "[TITLE_START]":
                raise ValueError("Expected [TITLE_START]")
            i += 1

            title_lines = []
            while lines[i] != "[TITLE_END]":
                title_lines.append(lines[i])
                i += 1

            title = " ".join(title_lines)
            i += 1  # skip TITLE_END

            bullets = []
            while lines[i] != "[SLIDE_END]":
                if lines[i]:
                    bullets.append(lines[i])
                i += 1

            slides.append({
                "title": title,
                "bullets": bullets
            })

        i += 1

    return slides
