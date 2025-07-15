from pydantic import BaseModel
from typing import List

class ProductReport(BaseModel):
    product_name: str
    mention_count: int

class ChannelActivity(BaseModel):
    date: str
    message_count: int

class MessageSearchResult(BaseModel):
    telegram_message_id: int
    channel_name: str
    message_text: str
    posted_at: str
