import socket
import threading

socket_client = None
receive_thread = None
command = {}

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
    for _, key in enumerate(command):
      print(command[key]['desc'])
    user_input = int(input())
    if user_input not in command:
      print("잘못 입력하였습니다.")
    command[user_input]['func']()
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
  if not key:
    print("잘못 입력하였습니다.")
    return
  parsed_data = 'get<' + key + '>'
  socket_client.send(parsed_data.encode())

def put_user_interface():
  print("############################################")
  print("저장할 데이터의 key를 입력하세요")
  key = input()
  if not key:
    print("잘못 입력하였습니다.")
    return
  print("############################################")
  print("저장할 데이터의 값를 입력하세요")
  value = input()
  if not value:
    print("잘못 입력하였습니다.")
    return

  parsed_data = 'put<' + key + ',' + value + '>'
  socket_client.send(parsed_data.encode())

def command_pattern():
  command[1] = {'desc': '1. 데이터 읽기(get)', 'func': get_user_interface}
  command[2] = {'desc': '2. 데이터 저장하기(put)', 'func': put_user_interface}
  command[3] = {'desc': '3. 종료', 'func': safety_exit}


if __name__ == "__main__":
  print("##############소켓 클라이언트################")
  print("서버의 주소와 포트를 :로 구분하여 입력해주세요")
  try:
    ip, port = input().split(":")
    socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_client.connect((ip, int(port)))
    receive_thread = threading.Thread(target = receive_message, args=())
    command_pattern()
    receive_thread.start()
    while True:
      menu_user_interface()
  except Exception as e:
    print("서버 접속에 실패했습니다")
    if socket_client:
      socket_client.close()
    exit()






