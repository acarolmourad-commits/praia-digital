"""Pure validation: no network, filesystem writes, git or credentials."""

def normalize_slide(slide, context="slide"):
    if not isinstance(slide, (list, tuple)) or len(slide) not in (3, 4):
        raise ValueError(f"{context}: expected 3 or 4 text fields")
    if any(not isinstance(field, str) or not field.strip() for field in slide):
        raise ValueError(f"{context}: fields must be non-empty strings")
    return slide[0], slide[1], "\n".join(slide[2:])


def validate_queue(queue):
    if not isinstance(queue, list) or not queue:
        raise ValueError("queue must be a non-empty list")
    normalized = []
    seen = set()
    for index, topic in enumerate(queue):
        if not isinstance(topic, dict):
            raise ValueError(f"topic {index}: expected an object")
        for key in ("id", "badge", "title", "caption"):
            if not isinstance(topic.get(key), str) or not topic[key].strip():
                raise ValueError(f"topic {index}: missing or invalid {key}")
        if topic["id"] in seen:
            raise ValueError(f"duplicate topic id: {topic['id']}")
        seen.add(topic["id"])
        slides = topic.get("slides")
        if not isinstance(slides, list) or not 1 <= len(slides) <= 8:
            raise ValueError(f"topic {index}: expected 1 to 8 slides (plus cover and CTA)")
        item = dict(topic)
        item["slides"] = [normalize_slide(slide, f"topic {index}, slide {i}")
                          for i, slide in enumerate(slides)]
        normalized.append(item)
    return normalized
