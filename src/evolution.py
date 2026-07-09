# src/evolution.py (add to existing, replace relevant parts)

def evaluate_design(design, enforce_standards=True):
    # ... original scores ...
    structural = ...  # (keep as before)
    economic = ...
    spatial = ...
    sustainability = ...

    # ---- Code Compliance Score ----
    code_penalty = 0
    for floor in design["floors"]:
        # Check room sizes
        for room in floor["rooms"]:
            min_area = MIN_ROOM_SIZES.get(room["type"], 8.0)
            w = room["polygon"][1][0] - room["polygon"][0][0]
            d = room["polygon"][3][1] - room["polygon"][0][1]
            area = w * d
            if area < min_area:
                code_penalty += (min_area - area) * 5   # penalty per sqm under
            # Egress: at least one door
            doors = [op for op in room["openings"] if op["type"] == "door"]
            if not doors:
                code_penalty += 20
            # Windows for habitable rooms
            if room["type"] not in ("corridor","bathroom","storage"):
                windows = [op for op in room["openings"] if op["type"] == "window"]
                if not windows:
                    code_penalty += 25
                else:
                    # Check daylight ratio
                    glazing_area = sum(op["width"] * 1.2 for op in windows)  # height 1.2m
                    if area > 0 and (glazing_area / area) < WINDOW_RATIO:
                        code_penalty += 15
        # Check column grid regularity (simplified)
        col_xs = [c["center"][0] for c in floor["columns"]]
        # Penalize irregular spacing
        if len(col_xs) > 2:
            diffs = np.diff(sorted(col_xs))
            if np.std(diffs) > 1.0:   # grid irregularity
                code_penalty += 10

    code_score = max(0, 100 - code_penalty)
    
    # ---- Constraint penalty for user targets ----
    target_penalty = 0
    if "target_rooms" in design and design["target_rooms"]:
        actual_rooms = sum(len(f["rooms"]) for f in design["floors"])
        target_penalty += abs(actual_rooms - design["target_rooms"]) * 10
    if "target_doors" in design and design["target_doors"]:
        actual_doors = sum(
            1 for f in design["floors"]
            for r in f["rooms"]
            for o in r["openings"] if o["type"] == "door"
        )
        target_penalty += abs(actual_doors - design["target_doors"]) * 8
    if "target_windows" in design and design["target_windows"]:
        actual_windows = sum(
            1 for f in design["floors"]
            for r in f["rooms"]
            for o in r["openings"] if o["type"] == "window"
        )
        target_penalty += abs(actual_windows - design["target_windows"]) * 5

    return {
        "Structural Score": structural,
        "Economic Score": economic,
        "Spatial Score": spatial,
        "Sustainability Score": sustainability,
        "Code Compliance Score": code_score,
        "Target Penalty": target_penalty
    }

def total_score(metrics):
    # Combine all scores; penalty reduces overall fitness
    base = sum(v for k,v in metrics.items() if k != "Target Penalty") / 5  # five agent scores
    penalty = metrics.get("Target Penalty", 0)
    return max(0, int(base - penalty * 0.2))
