import socket
import threading

socket_client = None
receive_thread = None

def safety_exit():
  if socket_client:
    socket_client.close()
  exit()

def receive_message():
  while True:
    try:
      raw_msg = socket_client.recv(1024)
      msg = raw_msg.decode()
      if not msg == 'heart_beat':
        print(msg)
    except Exception as e:
      exit()

def menu_user_interface():
  try:
    print("############################################")
    print("1. 데이터 읽기(get)")
    print("2. 데이터 저장하기(put)")
    print("3. 종료")
    user_input = int(input())
    if user_input == 1:
      get_user_interface()
    elif user_input == 2:
      put_user_interface()
    elif user_input == 3:
      safety_exit()
    else:
      print("잘못 입력하였습니다.")
    input()
  except Exception as e:
    if e.args[0] == 10054:
      print("서버와의 연결이 끊겼습니다.")
      exit()
    print(e)

def get_user_interface():
  print("############################################")
  print("가져올 데이터의 key를 입력하세요")
  key = input()
  parsed_data = 'get<' + key + '>'
  socket_client.send(parsed_data.encode())

def put_user_interface():
  print("############################################")
  print("저장할 데이터의 key를 입력하세요")
  key = input()
  print("############################################")
  print("저장할 데이터의 값를 입력하세요")
  value = input()

  parsed_data = 'put<' + key + ',' + value + '>'
  socket_client.send(parsed_data.encode())


if __name__ == "__main__":
  print("##############소켓 클라이언트################")
  print("서버의 주소와 포트를 :로 구분하여 입력해주세요")
  # print("############################################")
  try:
    ip, port = input().split(":")
    socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_client.connect((ip, int(port)))
    receive_thread = threading.Thread(target = receive_message, args=())
    receive_thread.start()
    while True:
      menu_user_interface()
  except Exception as e:
    print("서버 접속에 실패했습니다")
    if socket_client:
      socket_client.close()
    exit()






