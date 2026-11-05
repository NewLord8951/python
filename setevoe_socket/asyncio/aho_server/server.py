import asyncio
from datetime import datetime

async def handle_client(reader, writer):
    count = 0
    timee = datetime.now().strftime("%H:%M:%S")
    addr = writer.get_extra_info("peername")
    print("Подключился клиент:", addr)
    while True:
        data = await reader.readline()
        if not data:
            break
        text = data.decode("utf-8").strip()
        if text == "exit":
            break
        elif text == "count":
            answer = f"Вы отправили сообщений: {count}\n"
            writer.write(answer.encode("utf-8"))
        elif text == "time":
            answer = f"Время: {timee}\n"
            writer.write(answer.encode("utf-8"))
        else:
            answer = f"Эхо: {text}\n"
            writer.write(answer.encode("utf-8"))
        count += 1
        await writer.drain()
    writer.close()
    await writer.wait_closed()
    print("Клиент отключился:", addr)
 
async def main():
    server = await asyncio.start_server(
        handle_client, "127.0.0.1", 7000)
    print("Сервер запущен...")
    async with server:
        await server.serve_forever()
 
asyncio.run(main())