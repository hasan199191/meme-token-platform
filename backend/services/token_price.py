import asyncio
import random
from datetime import datetime

class TokenPriceService:
    def __init__(self, websocket_service):
        self.ws_service = websocket_service
        self.running = False
        self.price_history = {}
        self.base_price = 0.5
        self.volatility = 0.1

    async def start_price_feed(self):
        self.running = True
        try:
            while self.running:
                price = await self.calculate_token_price()
                trend = await self.get_price_trend()
                stats = await self.get_market_stats()
                
                await self.ws_service.send_price_update(
                    token_id=1015673913,
                    data={
                        "price": price,
                        "trend": trend,
                        "stats": stats
                    }
                )
                print(f"Fiyat güncellendi: {price}, Trend: {trend}")
                await asyncio.sleep(5)
        except Exception as e:
            print(f"Fiyat akışı hatası: {str(e)}")

    def stop_price_feed(self):
        self.running = False

    async def calculate_token_price(self):
        try:
            current_time = datetime.now().timestamp()
            price_change = random.uniform(-self.volatility, self.volatility)
            new_price = max(0.001, self.base_price * (1 + price_change))
            
            self.price_history[current_time] = new_price
            self.base_price = new_price
            
            cutoff_time = current_time - (24 * 3600)
            self.price_history = {k: v for k, v in self.price_history.items() if k > cutoff_time}
            
            return new_price
        except Exception as e:
            print(f"Fiyat hesaplama hatası: {str(e)}")
            return self.base_price

    async def get_market_stats(self):
        try:
            if not self.price_history:
                return None

            current_time = datetime.now().timestamp()
            cutoff_time = current_time - (24 * 3600)
            daily_prices = [v for k, v in self.price_history.items() if k > cutoff_time]

            if not daily_prices:
                return None

            return {
                "current_price": self.base_price,
                "high_24h": max(daily_prices),
                "low_24h": min(daily_prices),
                "price_change_24h": ((self.base_price - daily_prices[0]) / daily_prices[0]) * 100 if daily_prices else 0,
                "volume_24h": sum(daily_prices) * random.uniform(1000, 10000),
                "market_cap": self.base_price * 21000000
            }
        except Exception as e:
            print(f"Market istatistikleri hesaplanamadı: {str(e)}")
            return None

    async def get_price_trend(self):
        try:
            prices = list(self.price_history.values())
            if len(prices) < 2:
                return "stable"
            
            trend = (prices[-1] - prices[0]) / prices[0]
            if trend > 0.05:
                return "bullish"
            elif trend < -0.05:
                return "bearish"
            return "stable"
        except Exception as e:
            print(f"Trend hesaplama hatası: {str(e)}")
            return "stable"