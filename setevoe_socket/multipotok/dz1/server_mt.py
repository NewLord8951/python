import socket
import threading

i = 0
lock = threading.Lock()


def handle_client(conn, addr):
  global i
  print(f'Подключился клиент: {addr}')
  try:
    while True:
      data = conn.recv(1024)
      if not data:
        break
      response = data.decode('utf-8').upper().encode('utf-8')
      conn.sendall(response)
  except Exception as e:
    print(f'Ошибка с клиентом {addr}: {e}')
  finally:
    conn.close()
    with lock:
      i -= 1
      print(f'Клиент отключился: {addr}. Активных клиентов: {i}')


def start_server():
  global i
  server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  server.bind(('127.0.0.1', 5000))
  server.listen()
  print('Сервер запущен...')

  try:
    while True:
      conn, addr = server.accept()
      with lock:
        i += 1
        print(f'Вот такая хуйня собачка: {i}')

      t = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
      t.start()
  except KeyboardInterrupt:
    print('\nСервер остановлен.')
  finally:
    server.close()


if __name__ == '__main__':
  start_server()
