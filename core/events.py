# core/events.py

class EventBus:
    def __init__(self):
        self.listeners = {}

    def subscribe(self, event_type, fn):
        self.listeners.setdefault(event_type, []).append(fn)

    def emit(self, event_type, data):
        for fn in self.listeners.get(event_type, []):
            fn(data)