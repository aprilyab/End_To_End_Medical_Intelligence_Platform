from sqlalchemy.orm import Session
from sqlalchemy import text

def get_top_products(db: Session, limit: int = 10):
    query = text("""
    SELECT message_text, COUNT(*) as mention_count
    FROM raw.fct_messages
    GROUP BY message_text
    ORDER BY mention_count DESC
    LIMIT 5;
""")

    return db.execute(query, {"limit": limit}).fetchall()

def get_channel_activity(db: Session, channel_name: str):
    query = text("""
        SELECT date::date AS date, COUNT(*) AS message_count
        FROM raw.fct_messages
        WHERE channel_name = :channel_name
        GROUP BY date::date
        ORDER BY date
    """)
    return db.execute(query, {"channel_name": channel_name}).fetchall()

def search_messages(db: Session, query_text: str):
    query = text("""
        SELECT telegram_message_id, channel_name, message_text, date
        FROM raw.fct_messages
        WHERE message_text ILIKE :query_text
        ORDER BY date DESC
        LIMIT 50
    """)
    return db.execute(query, {"query_text": f"%{query_text}%"}).fetchall()
if __name__ == "__main__":
    from database import SessionLocal
    db = SessionLocal()

    # Test: top 5 most detected products
    results = get_top_products(db, 5)
    for r in results:
        print(r)

    db.close()
