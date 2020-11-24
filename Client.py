import socket, select, sys, _thread

RECV_BUFFER = 4096

HOST = "127.0.0.1"#str(sys.argv[1])
PORT = 22222#int(sys.argv[2])
exit = False
inside = False

my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    my_socket.connect((HOST, PORT)) # WE CONNECT TO THE CORRESPONDING ADDRESS AND PORT
except:
    print("\033[1;31m" + "Unable to connect to the server" + "\033[0;m")
    sys.exit()

def emoji():
    print("\033[F\033[K" , end = '', flush = True)
    trace = True
    while True:
            if trace == True:
                print("Bienvenido al menu de emojis selecione el deseado "+"1 \U0001F600"+" 2 \U0001F970"+" 3 \U0001F496"+" 4 \U0001F40D"+" 5 \U0001F595"+" 6 \U0001F922"+" 7 \U0001F927"+" 8 \U0001F9A0"+" 9 \U0001F451"+" 10 \U0001F4AF"+" 11 \U0001F468\U0000200D\U0001F4BB")

            numero = int(input())
            print("\033[F\033[K" , end = '', flush = True)

            if numero == 1 :
                return"\U0001F600"
            elif numero ==2 :
                return "\U0001F970"
            elif numero ==3 :
                return "\U0001F496"
            elif numero ==4 :
                return "\U0001F40D"
            elif numero ==5 :
                return "\U0001F595"
            elif numero ==6 :
                return "\U0001F922"
            elif numero ==7 :
                return "\U0001F927"
            elif numero ==8 :
                return "\U0001F9A0"
            elif numero ==9 :
                return "\U0001F451"
            elif numero ==10 :
                return "\U0001F4AF"
            elif numero ==11 :
                return "\U0001F468\U0000200D\U0001F4BB"
            else:
                print("\033[F\033[K" , end = '', flush = True)
                print("Fuera de rango "+"1 \U0001F600"+" 2 \U0001F970"+" 3 \U0001F496"+" 4 \U0001F40D"+" 5 \U0001F595"+" 6 \U0001F922"+" 7 \U0001F927"+" 8 \U0001F9A0"+" 9 \U0001F451"+" 10 \U0001F4AF"+" 11 \U0001F468\U0000200D\U0001F4BB")
                trace = False




while not exit:
    socket_list = [sys.stdin, my_socket]

    #IT RETURNS 3 LIST, BUT WE ARE GOING TO USE readable_sockets. SOCKETS THAT WE CONNECT (INPUT) CLIENT AND THEY ARE READY TO BE READ

    readable_sockets, writable_sockets, exceptional_sockets = select.select(socket_list, [], [])

    for s in readable_sockets:
        if s == my_socket: # IT MEANS USER IS SENDING A MESSAGE
            my_data = s.recv(RECV_BUFFER)
            print(my_data.decode(), end = '', flush = True) #flush = True to flush the buffer output
            if my_data.decode() == "Thank you for using the chat-room. Untill next time!\n":
                exit = True
                break
            elif "Welcome to the chat-room. Introduce your nickname: " in my_data.decode():
                inside = True

        else: # IT MEANS THE USER IS WRITTING THE MESSAGE THAT IS GOING TO SEND
            if not inside:
                my_line = sys.stdin.readline() #THIS IS FOR READING THE LINE
                my_socket.send(my_line.encode())#THIS IS FOR SENDING THE LINE
            else:
                my_line = sys.stdin.readline()
                if my_line == "$emoji$\n":#FOR THE EMOJIMENU
                    throw=(emoji()+"\n")
                    my_socket.send(throw.encode())
                    print("\033[F\033[K\033[1;32m\033[1m\033[3m" + "$MyClient$ " + "\033[0m" + throw, end = '', flush = True)
                elif my_line[0] == "&": #FOR STYLISH PORPOSES FOR CLIENT TO USE THE PRIVATE CHAT
                    pre=my_line.find("&")
                    post=my_line.rfind("&")
                    if pre == post:
                        my_socket.send(my_line.encode())
                    else:
                        my_socket.send(my_line.encode())
                        dest= my_line[pre+1:post]
                        print("\033[F\033[K\033[1;32m\033[1m\033[3m$MyClient$ \033[0mto \033[1m\033[3m\033[1;34m$" + dest + "$\033[0m" + my_line[post+1:], end = '', flush = True)

                else:
                    my_socket.send(my_line.encode())
                    if my_line == "exit\n" :
                        print("\033[F\033[K")

                    else:
                        print("\033[F\033[K\033[1;32m\033[1m\033[3m" + "$MyClient$ " + "\033[0m" + my_line, end = '', flush = True) # WE ERASE THE LINE THAT WE CREATED AND WE PRINTED WITH $MyClient

my_socket.close()
