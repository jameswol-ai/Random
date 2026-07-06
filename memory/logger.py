from datetime import datetime

def log_event(state, msg):
    state["logs"].append({
        "time": datetime.now().isoformat(),
        "msg": msg
    })
    return state