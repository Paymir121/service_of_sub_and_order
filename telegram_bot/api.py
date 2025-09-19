import asyncio
import logging

from fastapi import FastAPI, Response

from db import Connection
from models import get_automapped

app = FastAPI()
conn = Connection()
automapped = get_automapped()

@app.get("/check/")
async def check_app():
    logging.info(f"API.1: check")
    return Response("Hell world")

@app.get("/get_order/{order_id}/")
async def get_order(order_id: int = None):
    logging.info(f"API.2: get order_id={order_id}")
    from bot import notify_new_order
    delivered: bool = await notify_new_order(order_id=order_id)
    if delivered:
        logging.info(f"API.2.1: Отправили в ТГ get order_id={order_id}")
    else:
        logging.warning(f"API.2.3: Не Отправили в ТГ get order_id={order_id}")

async def run_bot():
    try:
        from bot import bot_main
        await bot_main()
    except asyncio.CancelledError:
        logging.info("API.3: Bot stopped gracefully")
    except Exception as e:
        logging.error(f"API.4: Bot error: {e}")

if __name__ == "__main__":
    logging.info("API.5: Application start")
    import uvicorn

    async def main():
        config = uvicorn.Config(
            app,
            host="0.0.0.0",
            port=8080,
            log_level="info"
        )
        server = uvicorn.Server(config)
        await asyncio.gather(
            server.serve(),
            run_bot()
        )


    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("API.6: Application stopped by user")
