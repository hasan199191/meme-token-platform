from quart import Quart, render_template, websocket, send_from_directory
from backend.services.database import DatabaseService
from backend.services.websocket import WebSocketService
from backend.services.token_price import TokenPriceService
import asyncio

app = Quart(__name__, static_folder='static')
db_service = DatabaseService()
ws_service = WebSocketService()
price_service = TokenPriceService(ws_service)

@app.route('/')
async def index():
    try:
        islemler = await db_service.islem_listele()
        return await render_template('index.html', islemler=islemler)
    except Exception as e:
        return f"Hata: {str(e)}"

@app.websocket('/ws')
async def ws():
    try:
        await ws_service.register(websocket._get_current_object())
        while True:
            await asyncio.sleep(1)
    except Exception as e:
        print(f"WebSocket hatası: {str(e)}")
    finally:
        await ws_service.unregister(websocket._get_current_object())

@app.before_serving
async def startup():
    asyncio.create_task(price_service.start_price_feed())

@app.after_serving
async def shutdown():
    price_service.stop_price_feed()

if __name__ == '__main__':
    app.run(debug=True, port=5001)