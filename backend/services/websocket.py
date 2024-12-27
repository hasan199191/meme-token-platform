import asyncio
import json
from datetime import datetime

class WebSocketService:
    def __init__(self):
        self.clients = set()
        self.last_prices = {}
        self.price_alerts = {}
        self.tracked_tokens = set()
        self.trend_data = {}
        
    async def register(self, websocket):
        self.clients.add(websocket)
        try:
            if self.last_prices:
                await websocket.send_json({
                    "type": "price_history",
                    "data": self.last_prices
                })
            await websocket.send_json({
                "type": "connected",
                "message": "WebSocket bağlantısı başarılı"
            })
        except Exception as e:
            print(f"Bağlantı hatası: {str(e)}")
        
    async def unregister(self, websocket):
        try:
            self.clients.remove(websocket)
            print(f"Client bağlantısı sonlandırıldı")
        except Exception as e:
            print(f"Bağlantı sonlandırma hatası: {str(e)}")
        
    async def send_price_update(self, token_id, data):
        if not self.clients:
            return
            
        message = {
            "type": "price_update",
            "data": {
                "token_id": token_id,
                **data,
                "timestamp": datetime.now().isoformat()
            }
        }
        
        await self.broadcast_message(message)
        await self.check_price_alerts(token_id, data["price"])

    async def send_market_update(self, token_id, data):
        if not self.clients:
            return
            
        message = {
            "type": "market_update",
            "data": {
                "token_id": token_id,
                "price": data["price"],
                "trend": data["trend"],
                "volume": data.get("volume", 0),
                "market_cap": data.get("market_cap", 0),
                "price_change": data.get("price_change", 0),
                "timestamp": datetime.now().isoformat()
            }
        }
        
        await self.broadcast_message(message)
        await self.check_price_alerts(token_id, data["price"])
        
    async def set_price_alert(self, token_id, price, direction="above"):
        self.price_alerts[token_id] = {
            "price": price,
            "direction": direction
        }
        
    async def check_price_alerts(self, token_id, current_price):
        if token_id in self.price_alerts:
            alert = self.price_alerts[token_id]
            triggered = (
                (alert["direction"] == "above" and current_price > alert["price"]) or
                (alert["direction"] == "below" and current_price < alert["price"])
            )
            
            if triggered:
                await self.broadcast_message({
                    "type": "price_alert",
                    "data": {
                        "token_id": token_id,
                        "price": current_price,
                        "alert_price": alert["price"],
                        "direction": alert["direction"],
                        "timestamp": datetime.now().isoformat()
                    }
                })
                del self.price_alerts[token_id]

    async def track_token(self, token_id):
        self.tracked_tokens.add(token_id)
        
    async def untrack_token(self, token_id):
        self.tracked_tokens.remove(token_id)
        
    async def get_tracked_tokens(self):
        return list(self.tracked_tokens)
        
    async def send_token_update(self, token_id, data):
        if not self.clients or token_id not in self.tracked_tokens:
            return
            
        message = {
            "type": "token_update",
            "data": {
                "token_id": token_id,
                **data,
                "timestamp": datetime.now().isoformat()
            }
        }
        
        await self.broadcast_message(message)
        
    async def broadcast_message(self, message):
        for client in self.clients.copy():
            try:
                await client.send_json(message)
            except Exception as e:
                print(f"Yayın hatası: {str(e)}")
                await self.unregister(client)

    async def broadcast(self, message_type, data):
        if not self.clients:
            return
            
        message = {
            "type": message_type,
            "data": {
                **data,
                "timestamp": datetime.now().isoformat()
            }
        }
        
        for client in self.clients.copy():
            try:
                await client.send_json(message)
            except Exception as e:
                print(f"Yayın hatası: {str(e)}")
                self.clients.remove(client)

    async def analyze_trend(self, token_id, price):
        if token_id not in self.trend_data:
            self.trend_data[token_id] = []
            
        self.trend_data[token_id].append(price)
        if len(self.trend_data[token_id]) > 10:
            self.trend_data[token_id].pop(0)
            
        if len(self.trend_data[token_id]) < 2:
            return "stable"
            
        start_price = self.trend_data[token_id][0]
        end_price = self.trend_data[token_id][-1]
        change = ((end_price - start_price) / start_price) * 100
        
        if change > 5:
            return "bullish"
        elif change < -5:
            return "bearish"
        return "stable"
        
    async def send_trend_update(self, token_id, trend):
        if not self.clients:
            return
            
        message = {
            "type": "trend_update",
            "data": {
                "token_id": token_id,
                "trend": trend,
                "timestamp": datetime.now().isoformat()
            }
        }
        
        await self.broadcast_message(message)