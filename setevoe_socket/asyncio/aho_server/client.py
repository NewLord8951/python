import asyncio
 
async def main():
    reader, writer = await asyncio.open_connection("127.0.0.1", 7000)
    while True:
        text = input("Сообщение (exit - выход): ")
        writer.write((text + "\n").encode("utf-8"))
        await writer.drain()
        if text == "exit":
            break
        data = await reader.readline()
        print("Ответ:", data.decode("utf-8").strip())
    writer.close()
    await writer.wait_closed()
 
asyncio.run(main())