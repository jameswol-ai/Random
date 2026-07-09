import hashlib, json, uuid
from pathlib import Path
from datetime import datetime

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
USER_FILE = DATA_DIR / "random_users.json"
XP_PER_LEVEL = 100

def hash_password(password: str) -> str:
    return hashlib.sha256((password + "random_salt_42").encode()).hexdigest()

def load_users() -> list:
    if USER_FILE.exists():
        try:
            with open(USER_FILE) as f:
                return json.load(f)
        except:
            return []
    return []

def save_users(users: list):
    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=2)

def get_user(username: str) -> dict | None:
    for u in load_users():
        if u["username"] == username:
            return u
    return None

def create_user(username: str, password: str, role: str = "user") -> dict:
    users = load_users()
    if get_user(username):
        raise ValueError("Username already exists.")
    user = {
        "username": username,
        "password_hash": hash_password(password),
        "role": role,
        "level": 1,
        "xp": 0,
        "badges": [],
        "created": datetime.now().isoformat()
    }
    users.append(user)
    save_users(users)
    return user

def authenticate(username: str, password: str) -> dict | None:
    user = get_user(username)
    if user and user["password_hash"] == hash_password(password):
        return user
    return None

def update_user_data(username: str, updates: dict):
    users = load_users()
    for u in users:
        if u["username"] == username:
            u.update(updates)
            break
    save_users(users)

def xp_for_level(level: int) -> int:
    return level * XP_PER_LEVEL

def add_xp(username: str, amount: int) -> bool:
    user = get_user(username)
    if not user:
        return False
    old_level = user["level"]
    user["xp"] += amount
    while user["xp"] >= xp_for_level(user["level"]):
        user["xp"] -= xp_for_level(user["level"])
        user["level"] += 1
        badge = f"level_{user['level']}"
        if user["level"] % 5 == 0 and badge not in user["badges"]:
            user["badges"].append(badge)
    update_user_data(username, {"level": user["level"], "xp": user["xp"], "badges": user["badges"]})
    return user["level"] > old_level
