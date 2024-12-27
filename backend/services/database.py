import sqlite3
from datetime import datetime

class DatabaseService:
    def __init__(self):
        self.db_path = "algorand_meme.db"
        self.init_db()

    def init_db(self):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS price_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    token_id INTEGER NOT NULL,
                    price REAL NOT NULL,
                    timestamp TEXT NOT NULL,
                    trend TEXT NOT NULL
                )""")
                
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    token_id INTEGER NOT NULL,
                    sender TEXT NOT NULL,
                    receiver TEXT NOT NULL,
                    amount REAL NOT NULL,
                    timestamp TEXT NOT NULL
                )""")
                conn.commit()
        except Exception as e:
            print(f"Veritabanı başlatma hatası: {str(e)}")

    async def get_price_history(self, token_id, limit=100):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT price, timestamp, trend 
                    FROM price_history 
                    WHERE token_id = ? 
                    ORDER BY timestamp DESC 
                    LIMIT ?
                """, (token_id, limit))
                return cursor.fetchall()
        except Exception as e:
            print(f"Fiyat geçmişi alma hatası: {str(e)}")
            return []

    async def save_price(self, token_id, price, trend):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO price_history (token_id, price, timestamp, trend) VALUES (?, ?, ?, ?)",
                    (token_id, price, datetime.now().isoformat(), trend)
                )
                conn.commit()
                return True
        except Exception as e:
            print(f"Fiyat kaydetme hatası: {str(e)}")
            return False

    async def get_market_summary(self, token_id):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT 
                        MAX(price) as high_24h,
                        MIN(price) as low_24h,
                        AVG(price) as avg_24h,
                        COUNT(*) as total_updates
                    FROM price_history 
                    WHERE token_id = ? 
                    AND timestamp >= datetime('now', '-24 hours')
                """, (token_id,))
                result = cursor.fetchone()
                if result:
                    return {
                        "high_24h": result[0],
                        "low_24h": result[1],
                        "avg_24h": result[2],
                        "update_count": result[3]
                    }
                return None
        except Exception as e:
            print(f"Piyasa özeti alma hatası: {str(e)}")
            return None

    async def save_transaction(self, token_id, sender, receiver, amount):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO transactions (token_id, sender, receiver, amount, timestamp) VALUES (?, ?, ?, ?, ?)",
                    (token_id, sender, receiver, amount, datetime.now().isoformat())
                )
                conn.commit()
                return True
        except Exception as e:
            print(f"İşlem kaydetme hatası: {str(e)}")
            return False

    async def get_transaction_history(self, token_id, limit=100):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT sender, receiver, amount, timestamp
                    FROM transactions
                    WHERE token_id = ?
                    ORDER BY timestamp DESC
                    LIMIT ?
                """, (token_id, limit))
                return cursor.fetchall()
        except Exception as e:
            print(f"İşlem geçmişi alma hatası: {str(e)}")
            return []

    async def get_holder_stats(self, token_id):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT 
                        COUNT(DISTINCT sender) + COUNT(DISTINCT receiver) as total_holders,
                        SUM(amount) as total_volume,
                        COUNT(*) as total_transactions
                    FROM transactions
                    WHERE token_id = ?
                    AND timestamp >= datetime('now', '-24 hours')
                """, (token_id,))
                result = cursor.fetchone()
                if result:
                    return {
                        "holder_count": result[0],
                        "volume_24h": result[1],
                        "tx_count_24h": result[2]
                    }
                return None
        except Exception as e:
            print(f"Holder istatistikleri alma hatası: {str(e)}")
            return None

    async def islem_listele(self):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT DISTINCT token_id
                    FROM transactions
                """)
                token_ids = cursor.fetchall()
                
                islemler = []
                for (token_id,) in token_ids:
                    # Token bilgilerini al
                    cursor.execute("""
                        SELECT 
                            COUNT(DISTINCT sender) + COUNT(DISTINCT receiver) as holder_count,
                            SUM(amount) as total_volume,
                            MIN(timestamp) as creation_time
                        FROM transactions 
                        WHERE token_id = ?
                    """, (token_id,))
                    stats = cursor.fetchone()
                    
                    # Cüzdan listesini al
                    cursor.execute("""
                        SELECT DISTINCT sender as address, 
                               SUM(CASE WHEN sender = ? THEN -amount ELSE amount END) as balance
                        FROM transactions 
                        WHERE token_id = ?
                        GROUP BY sender
                        HAVING balance > 0
                        ORDER BY balance DESC
                        LIMIT 5
                    """, (token_id, token_id))
                    wallets = cursor.fetchall()
                    
                    islemler.append({
                        "token_id": token_id,
                        "token_adi": f"Token #{token_id}",
                        "toplam_arz": stats[1] or 0,
                        "dolasim_arzi": stats[1] or 0,
                        "islem_zamani": stats[2],
                        "cuzdan_listesi": [
                            {"address": addr, "balance": bal}
                            for addr, bal in wallets
                        ]
                    })
                
                return islemler
                
        except Exception as e:
            print(f"İşlem listesi alma hatası: {str(e)}")
            return []