"""Bound hosted inference usage without storing questions or voter identity."""
import hashlib
import hmac
import secrets
import sqlite3
import threading
import time
from datetime import datetime, timezone


class Admission:
    def __init__(self, database, daily_limit=200, clock=time.monotonic):
        self.db = sqlite3.connect(database, check_same_thread=False)
        self.db.execute('CREATE TABLE IF NOT EXISTS usage (day TEXT PRIMARY KEY, questions INTEGER NOT NULL)')
        self.db.commit()
        self.daily_limit, self.clock = daily_limit, clock
        self.lock, self.salt, self.clients = threading.Lock(), secrets.token_bytes(32), {}

    def take(self, address):
        # Short-lived keyed network bucket, never persisted or returned to clients.
        key = hmac.new(self.salt, address.encode(), hashlib.sha256).digest()
        now, day = self.clock(), datetime.now(timezone.utc).date().isoformat()
        with self.lock:
            self.clients = {k: (start, count) for k, (start, count) in self.clients.items() if now - start < 300}
            start, count = self.clients.get(key, (now, 0))
            if count >= 6 or (key not in self.clients and len(self.clients) >= 4096):
                return False, 'Please wait a few minutes before asking another question.'
            current = self.db.execute('SELECT questions FROM usage WHERE day=?', (day,)).fetchone()
            if current and current[0] >= self.daily_limit:
                return False, 'The demo has reached its daily live-question limit. Reviewed sources remain available.'
            self.db.execute('INSERT INTO usage(day,questions) VALUES(?,1) ON CONFLICT(day) DO UPDATE SET questions=questions+1', (day,))
            self.db.execute('DELETE FROM usage WHERE day < ?', (day,))
            self.db.commit()
            self.clients[key] = (start, count + 1)
            return True, ''
