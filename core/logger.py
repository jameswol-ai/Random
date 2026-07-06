from datetime import datetime

def log_event(mem, msg, save_fn):
    mem["logs"].append({
        "time": datetime.now().isoformat(),
        "msg": msg
    })
    save_fn(mem)