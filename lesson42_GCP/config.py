from dataclasses import dataclass


@dataclass
class Config:
    GOOGLE_PROJECT_ID: str
    TOPIC_ID: str
    SUBSCRIPTION_ID: str
    IS_REDELIVER: bool = False
