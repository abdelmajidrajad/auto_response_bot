from dataclasses import dataclass, asdict
from typing import List, Optional
import json


@dataclass
class Rule:
    patterns: List[str]
    response: str
    priority: int = 5
    tag: Optional[str] = None
    post_id: Optional[int] = None
    auto_reply: int = 1
    reply_once: int = 0
    id: Optional[int] = None
    created_at: Optional[str] = None

    def to_dict(self) -> dict:
        data = asdict(self)
        return {k: v for k, v in data.items() if v is not None}

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)

    @classmethod
    def from_dict(cls, data: dict) -> 'Rule':
        return cls(
            patterns=data.get('patterns', []),
            response=data.get('response', ''),
            priority=data.get('priority', 5),
            tag=data.get('tag'),
            post_id=data.get('post_id'),
            auto_reply=data.get('auto_reply', 1),
            reply_once=data.get('reply_once', 0),
            id=data.get('id'),
            created_at=data.get('created_at')
        )

    @classmethod
    def from_json(cls, json_str: str) -> 'Rule':
        data = json.loads(json_str)
        return cls.from_dict(data)