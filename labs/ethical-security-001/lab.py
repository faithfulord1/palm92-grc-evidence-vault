"""Palm92 SQL injection lab. Synthetic, in-memory, offline educational target.
Run: python lab.py > evidence.json
This is not a reproduction of PHP vulnerabilities or a production login system.
"""
import sqlite3
import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone


def database():
    db = sqlite3.connect(':memory:')
    db.execute('CREATE TABLE records (owner TEXT, note TEXT)')
    db.executemany('INSERT INTO records VALUES (?, ?)', [
        ('alice', 'Fictional Alice record'), ('bob', 'Fictional Bob record'),
        ("O'Neil", 'Fictional apostrophe record')])
    return db


def vulnerable_lookup(db, owner):
    # Deliberately unsafe teaching example. Never use in an application.
    return db.execute("SELECT note FROM records WHERE owner = '" + owner + "'").fetchall()


def fixed_lookup(db, owner):
    return db.execute('SELECT note FROM records WHERE owner = ?', (owner,)).fetchall()


def run():
    db = database()
    checks = []
    def check(name, condition):
        checks.append({'test': name, 'passed': bool(condition)})
        if not condition:
            raise AssertionError(name)
    check('baseline only returns Alice record', vulnerable_lookup(db, 'alice') == [('Fictional Alice record',)])
    payload = "alice' OR '1'='1"
    before = vulnerable_lookup(db, payload)
    after = fixed_lookup(db, payload)
    check('unsafe query exposes all three synthetic records', len(before) == 3)
    check('fixed query rejects injection as unmatched literal', after == [])
    check('fixed query preserves valid lookup', fixed_lookup(db, 'alice') == [('Fictional Alice record',)])
    check('fixed query supports legitimate apostrophe', fixed_lookup(db, "O'Neil") == [('Fictional apostrophe record',)])
    check('unknown owner returns no data', fixed_lookup(db, 'unknown') == [])
    check('empty owner returns no data', fixed_lookup(db, '') == [])
    db.close()
    return {
        'case': 'PALM92-LAB-001', 'executed_at_utc': datetime.now(timezone.utc).isoformat(),
        'scope': 'Original offline Python/SQLite teaching target; synthetic records only; no network listeners or requests',
        'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'finding': 'CWE-89: string-concatenated SQL permits synthetic cross-record disclosure',
        'remediation': 'Bind the owner value using a parameterized query',
        'before_records_returned': len(before), 'after_records_returned': len(after),
        'checks': checks, 'passed': len(checks),
        'limitations': 'Not a PHP CVE reproduction, penetration test of Palm92 services, or production security certification. Owner authorization must be enforced separately in real systems.'
    }

if __name__ == '__main__':
    print(json.dumps(run(), indent=2))
