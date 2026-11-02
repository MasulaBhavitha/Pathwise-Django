IMPORTANCE_WEIGHT = {"core": 2, "recommended": 1}


def requirement_payload(requirement):
    return {
        "skill_id": requirement.skill_id,
        "skill_name": requirement.skill.name,
        "skill_slug": requirement.skill.slug,
        "category": requirement.skill.category.name,
        "required_level": requirement.required_level,
        "importance": requirement.importance,
    }


def analyze_requirements(requirements, levels_by_skill_id):
    """Score how close a student is to a career's skill bar.

    Core skills count twice as much as recommended skills. Levels above the
    requirement do not raise the score past 100.
    """
    weighted_have = 0
    weighted_need = 0
    rows = []
    gaps = []

    for requirement in requirements:
        weight = IMPORTANCE_WEIGHT.get(requirement["importance"], 1)
        current = int(levels_by_skill_id.get(requirement["skill_id"], 0) or 0)
        required = int(requirement["required_level"])
        weighted_need += required * weight
        weighted_have += min(current, required) * weight
        gap = max(0, required - current)
        row = {
            "skill_id": requirement["skill_id"],
            "skill_name": requirement["skill_name"],
            "skill_slug": requirement["skill_slug"],
            "category": requirement["category"],
            "required_level": required,
            "current_level": current,
            "importance": requirement["importance"],
            "gap": gap,
        }
        rows.append(row)
        if gap:
            gaps.append({**row, "weight": weight})

    score = round(100 * weighted_have / weighted_need) if weighted_need else 0
    gaps.sort(key=lambda item: (-(item["gap"] * item["weight"]), item["skill_name"]))
    return score, rows, gaps
