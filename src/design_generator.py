# src/design_generator.py
import uuid, random, math, numpy as np
from .knowledge_base import get_domain

# ── ARCHITECTURAL STANDARDS ──
MIN_ROOM_SIZES = {
    "living": 16.0, "kitchen": 8.0, "dining": 10.0,
    "bedroom": 10.0, "bathroom": 4.0, "study": 8.0,
    "office": 10.0, "meeting": 12.0, "reception": 8.0,
    "hall": 6.0, "corridor": 1.5 * 1.2,  # minimum width 1.2 m
    "storage": 4.0
}

DOOR_WIDTHS = {
    "main": 0.9,    # entrance / living / office
    "interior": 0.8,
    "bathroom": 0.75
}

WINDOW_RATIO = 0.15  # 15% of floor area for glazing

STRUCTURAL_GRID = 4.0   # metres; columns at intersections

ROOM_TYPES = {
    "Residential": ["living","kitchen","dining","bedroom","bathroom","corridor","study"],
    "Commercial": ["office","meeting","reception","kitchen","bathroom","corridor"],
    "Industrial": ["hall","storage","bathroom","office"]
}

def create_floor_layout(level, building_type, total_area, modules,
                        floor_area_m2, num_rooms, num_doors, num_windows,
                        enforce_standards=True):
    """
    Generate a single floor plan with architectural standards.
    Returns a floor dict or None if impossible.
    """
    if floor_area_m2 is None:
        floor_area_m2 = total_area / (modules * 0.5 + 1)

    # ---- Determine floor dimensions ----
    side = int(math.sqrt(floor_area_m2)) + 1
    width = max(6, min(side, 20))
    depth = max(6, min(side, 20))
    # Snap width/depth to structural grid multiples
    if enforce_standards:
        width = max(STRUCTURAL_GRID, round(width / STRUCTURAL_GRID) * STRUCTURAL_GRID)
        depth = max(STRUCTURAL_GRID, round(depth / STRUCTURAL_GRID) * STRUCTURAL_GRID)

    # ---- Room types and sizes ----
    domain = get_domain(building_type)
    available_types = ROOM_TYPES.get(domain, ROOM_TYPES["Commercial"])
    if num_rooms is None:
        num_rooms = 4  # safe default

    # Choose room types intelligently: include essential ones
    room_types = _assign_room_types(domain, num_rooms, building_type)

    # Calculate minimum total width required
    min_width_needed = 0.0
    for rt in room_types:
        min_area = MIN_ROOM_SIZES.get(rt, 8.0)
        if rt == "corridor":
            min_width = 1.5  # corridor width
        else:
            min_width = max(2.0, math.sqrt(min_area))   # square root approximation
        min_width_needed += min_width

    # If total required width exceeds floor width, we need to adjust:
    # scale down rooms proportionally (still respect minimums as much as possible)
    available_width = width - 0.2 * len(room_types)  # account for wall thickness
    if available_width <= 0:
        return None

    room_widths = []
    remaining_width = available_width
    for rt in room_types:
        min_w = MIN_ROOM_SIZES.get(rt, 8.0) / depth if rt != "corridor" else 1.5
        room_widths.append(min_w)
        remaining_width -= min_w
    # Distribute extra width equally
    if remaining_width > 0:
        extra = remaining_width / len(room_widths)
        for i in range(len(room_widths)):
            room_widths[i] += extra

    # Build rooms
    rooms = []
    cum_x = 0.0
    for i, rt in enumerate(room_types):
        w = room_widths[i]
        # Ensure at least a tiny space
        if w < 1.5:
            w = 1.5
        # Clip to remaining floor width
        if cum_x + w > width:
            w = width - cum_x
        if w < 1.5:
            break   # not enough space

        poly = [(cum_x, 0), (cum_x + w, 0), (cum_x + w, depth), (cum_x, depth)]
        rooms.append({"name": f"{rt.capitalize()} {i+1}", "type": rt, "polygon": poly, "openings": []})
        cum_x += w

    # ---- Place doors ----
    if num_doors is None:
        num_doors = len(rooms) + 1
    _place_doors(rooms, num_doors, enforce_standards)

    # ---- Place windows ----
    if num_windows is None:
        num_windows = len(rooms)  # at least one per habitable room
    _place_windows(rooms, num_windows, depth, enforce_standards)

    # ---- Structural elements ----
    walls = _create_walls(width, depth)
    interior_walls = []
    cur_x = 0
    for room in rooms:
        if cur_x > 0:
            interior_walls.append({"start": (cur_x, 0), "end": (cur_x, depth), "thickness": 0.2})
        cur_x += room_widths[rooms.index(room)] if rooms.index(room) < len(room_widths) else 2.0
    walls.extend(interior_walls)

    columns = _place_columns(width, depth, enforce_standards)
    beams = _place_beams(width, depth)

    return {
        "level": level,
        "height": 3.0,
        "rooms": rooms,
        "walls": walls,
        "columns": columns,
        "beams": beams,
        "slab": {"thickness": 0.2}
    }

def _assign_room_types(domain, count, building_type):
    """Return a list of room types respecting essential spaces."""
    if domain == "Residential":
        essential = ["living", "kitchen", "bathroom"]
        if "Villa" in building_type:
            essential.append("dining")
        if count < len(essential):
            # force essentials
            types = essential[:count]
        else:
            types = essential + random.choices(["bedroom","study","corridor","bathroom"], k=count-len(essential))
    elif domain == "Commercial":
        essential = ["office", "bathroom", "corridor"]
        if "Hotel" in building_type:
            essential = ["reception","bathroom","corridor","bedroom"]  # hotel rooms
        types = essential + random.choices(["meeting","kitchen","office"], k=max(0, count-len(essential)))
    else:  # Industrial
        essential = ["hall", "bathroom", "storage"]
        types = essential + random.choices(["office","hall"], k=max(0, count-len(essential)))
    # Trim to exact count
    return types[:count]

def _place_doors(rooms, total_doors, enforce_standards):
    """Assign doors to rooms guaranteeing at least one per room and egress."""
    # Every room must have at least one door
    for room in rooms:
        door_width = DOOR_WIDTHS["main"] if room["type"] in ["living","office","meeting","reception"] else DOOR_WIDTHS["interior"]
        if room["type"] == "bathroom":
            door_width = DOOR_WIDTHS["bathroom"]
        # Place door on the wall facing the corridor (y=0) or opposite
        wall_y = 0 if rooms.index(room) % 2 == 0 else room["polygon"][3][1]  # alternate sides
        door_x = room["polygon"][0][0] + (room["polygon"][1][0] - room["polygon"][0][0]) / 2 - door_width/2
        room["openings"].append({
            "type": "door",
            "start": (door_x, wall_y),
            "end": (door_x, wall_y + (0.9 if wall_y == 0 else -0.9)),
            "width": door_width
        })
    # Additional doors randomly (if total_doors > room count)
    extra = total_doors - len(rooms)
    if extra > 0:
        for _ in range(extra):
            room = random.choice(rooms)
            # second door on another wall (e.g., depth side)
            wall_y = room["polygon"][3][1]  # opposite side
            door_x = room["polygon"][0][0] + random.uniform(0.5, room["polygon"][1][0] - room["polygon"][0][0] - 0.5)
            room["openings"].append({
                "type": "door",
                "start": (door_x, wall_y),
                "end": (door_x, wall_y - 0.9),
                "width": DOOR_WIDTHS["interior"]
            })

def _place_windows(rooms, total_windows, depth, enforce_standards):
    """Place windows on external walls (y=depth) for habitable rooms."""
    # Only habitable rooms get windows (exclude corridors)
    habitable = [r for r in rooms if r["type"] not in ("corridor", "bathroom", "storage")]
    if not habitable:
        return
    # Distribute windows equally among habitable rooms, at least one each if possible
    base = total_windows // len(habitable)
    remainder = total_windows % len(habitable)
    assigned = 0
    for i, room in enumerate(habitable):
        nw = base + (1 if i < remainder else 0)
        if nw == 0:
            continue
        # Window size based on room width and daylight ratio
        room_width = room["polygon"][1][0] - room["polygon"][0][0]
        if enforce_standards:
            room_area = room_width * depth
            glazing_area = room_area * WINDOW_RATIO
            # Assume window height 1.2 m, so width = glazing_area / 1.2
            win_width = glazing_area / 1.2
            win_width = min(win_width, room_width * 0.8)  # no wider than 80% of room width
        else:
            win_width = room_width * 0.6
        win_width = max(0.6, win_width)
        # Place window centered on external wall
        x0 = room["polygon"][0][0] + (room_width - win_width) / 2
        for _ in range(nw):
            room["openings"].append({
                "type": "window",
                "start": (x0, depth),
                "end": (x0 + win_width, depth),
                "width": win_width
            })
            assigned += 1
    # If we still have windows left, put extras on larger rooms
    remaining = total_windows - assigned
    while remaining > 0 and habitable:
        room = random.choice(habitable)
        room_width = room["polygon"][1][0] - room["polygon"][0][0]
        win_width = min(1.2, room_width * 0.4)
        x0 = room["polygon"][0][0] + random.uniform(0, room_width - win_width)
        room["openings"].append({
            "type": "window",
            "start": (x0, depth),
            "end": (x0 + win_width, depth),
            "width": win_width
        })
        remaining -= 1

def _create_walls(width, depth):
    return [
        {"start": (0,0), "end": (width,0), "thickness": 0.3},
        {"start": (width,0), "end": (width,depth), "thickness": 0.3},
        {"start": (width,depth), "end": (0,depth), "thickness": 0.3},
        {"start": (0,depth), "end": (0,0), "thickness": 0.3}
    ]

def _place_columns(width, depth, enforce):
    cols = []
    # Corner columns
    cols.append({"center":(0,0),"size":0.3,"shape":"square"})
    cols.append({"center":(width,0),"size":0.3,"shape":"square"})
    cols.append({"center":(0,depth),"size":0.3,"shape":"square"})
    cols.append({"center":(width,depth),"size":0.3,"shape":"square"})
    # Grid columns
    if enforce:
        for x in np.arange(STRUCTURAL_GRID, width, STRUCTURAL_GRID):
            for y in np.arange(STRUCTURAL_GRID, depth, STRUCTURAL_GRID):
                if x < width - 0.5 and y < depth - 0.5:
                    cols.append({"center":(x, y),"size":0.25,"shape":"circle"})
    else:
        # few intermediate columns
        for x in np.linspace(width*0.3, width*0.7, max(2, int(width/5))):
            cols.append({"center":(x, depth/2),"size":0.25,"shape":"circle"})
    return cols

def _place_beams(width, depth):
    return [
        {"start":(0, 0.2), "end":(width, 0.2), "width":0.2},
        {"start":(0, depth-0.2), "end":(width, depth-0.2), "width":0.2},
        ]
