import socket

ip, port = "127.0.0.1", "8395"
socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_client.connect((ip, int(port)))

while True:
  print("과부화(get)시킬 횟수를 입력하세요")
  cnt = int(input())
  print("key를 입력하세요")
  key = input()
  for i in range(cnt):
    parsed_data = 'get<' + key + '>'
    encoded_data = parsed_data.encode()
    socket_client.sendall(encoded_data)
