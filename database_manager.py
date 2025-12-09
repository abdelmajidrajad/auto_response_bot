from database_config import get_connection
from RuleModel import Rule

import json

class DatabaseManager:
    def __init__(self):
        self.conn = get_connection()
        self.cursor = self.conn.cursor(dictionary=True)

    def add_rule(self, patterns, response, priority=5, tag=None, post_id=None, auto_reply=1, reply_once=0):
        patterns_json = json.dumps(patterns, ensure_ascii=False, indent=2) if isinstance(patterns, list) else json.dumps([patterns], ensure_ascii=False, indent=2)
        sql = """
            INSERT INTO Rule (patterns, response, priority, tag, post_id, auto_reply, reply_once)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        self.cursor.execute(sql, (patterns_json, response, priority, tag, post_id, auto_reply, reply_once))
        self.conn.commit()
        return self.cursor.lastrowid

    def addRule(self, rule: Rule):
        return self.add_rule(
            patterns=rule.patterns,
            response=rule.response,
            priority=rule.priority,
            tag=rule.tag,
            post_id=rule.post_id,
            auto_reply=rule.auto_reply,
            reply_once=rule.reply_once
        )

    def update_rule(self, rule_id, patterns=None, response=None, priority=None, tag=None, post_id=None, auto_reply=None, reply_once=None):
        updates = []
        params = []

        if patterns is not None:
            updates.append("patterns=%s")
            patterns_json = json.dumps(patterns) if isinstance(patterns, list) else json.dumps([patterns])
            params.append(patterns_json)
        if response is not None:
            updates.append("response=%s")
            params.append(response)
        if priority is not None:
            updates.append("priority=%s")
            params.append(priority)
        if tag is not None:
            updates.append("tag=%s")
            params.append(tag)
        if post_id is not None:
            updates.append("post_id=%s")
            params.append(post_id)
        if auto_reply is not None:
            updates.append("auto_reply=%s")
            params.append(auto_reply)
        if reply_once is not None:
            updates.append("reply_once=%s")
            params.append(reply_once)

        if not updates:
            return False

        sql = f"UPDATE Rule SET {', '.join(updates)} WHERE id=%s"
        params.append(rule_id)
        self.cursor.execute(sql, tuple(params))
        self.conn.commit()
        return self.cursor.rowcount
    
    def get_all_rules(self):
        sql = "SELECT * FROM Rule ORDER BY priority DESC"
        self.cursor.execute(sql)
        rules = self.cursor.fetchall()
        for rule in rules:
            if rule.get('patterns'):
                rule['patterns'] = json.loads(rule['patterns'])
        return rules

    def get_global_rules(self):
        sql = "SELECT * FROM Rule WHERE post_id IS NULL ORDER BY priority DESC"
        self.cursor.execute(sql)
        rules = self.cursor.fetchall()
        for rule in rules:
            if rule.get('patterns'):
                rule['patterns'] = json.loads(rule['patterns'])
        return rules

    def get_post_rules(self, post_id):
        sql = "SELECT * FROM Rule WHERE post_id = %s ORDER BY priority DESC"
        self.cursor.execute(sql, (post_id,))
        rules = self.cursor.fetchall()
        for rule in rules:
            if rule.get('patterns'):
                rule['patterns'] = json.loads(rule['patterns'])
        return rules

    def close(self):
        self.cursor.close()
        self.conn.close()