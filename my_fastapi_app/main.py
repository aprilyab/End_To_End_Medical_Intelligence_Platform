from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
import crud, schemas

app = FastAPI(title="Telegram Medical Analytics API")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/api/reports/top-products", response_model=list[schemas.ProductReport])
def top_products(limit: int = 10, db: Session = Depends(get_db)):
    results = crud.get_top_products(db, limit)
    return [{"product_name": r[0], "mention_count": r[1]} for r in results]

@app.get("/api/channels/{channel_name}/activity", response_model=list[schemas.ChannelActivity])
def channel_activity(channel_name: str, db: Session = Depends(get_db)):
    results = crud.get_channel_activity(db, channel_name)
    return [{"date": r[0].strftime("%Y-%m-%d"), "message_count": r[1]} for r in results]

@app.get("/api/search/messages", response_model=list[schemas.MessageSearchResult])
def search_messages(query: str, db: Session = Depends(get_db)):
    results = crud.search_messages(db, query)
    return [
        {
            "telegram_message_id": r[0],
            "channel_name": r[1],
            "message_text": r[2],
            "posted_at": r[3].isoformat()
        } for r in results
    ]

