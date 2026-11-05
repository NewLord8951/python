import asyncio
import os
import time

async def download(name, seconds):
    print(f"Начало {name}")
    await asyncio.sleep(3)
    print(f"Конец {name}")


    
async def main():
    await asyncio.gather(
        download("file1", 1),
        download("file2", 1),
        download("file3", 1)
    )
    file_size1 = os.path.getsize(filename="file1")
    file_size2 = os.path.getsize(filename="file2")
    file_size3 = os.path.getsize(filename="file3")
    print(f"Размеры: [{file_size1}, {file_size2}, {file_size3}]")
    suma = file_size1 + file_size2 + file_size3
    print(f"Сумма: {suma}")

start = time.perf_counter()
asyncio.run(main())
print(f"Время: {start}")
