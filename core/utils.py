import random
import uuid

def uid():
    return str(uuid.uuid4())[:8].upper()

def clamp(value, min_v, max_v):
    return max(min_v, min(value, max_v))