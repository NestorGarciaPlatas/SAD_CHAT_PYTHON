import socket, _thread, sys
HOST = "127.0.0.1"
PORT = 22222
RECV_BUFFER = 4096
nickused = True

mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Use TCP and ipV4
mysocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
mysocket.bind((HOST, PORT)) # Link a host and port
mysocket.listen() # Enable the socket to listen to new conections

socket_dict = dict() # [Socket; User] -> (Key; Value)
user_dict = dict() # [User; Socket] -> (Key; Value)

def broadcast(message, connect, nick):
    for client in socket_dict:
        # Send to all the chat members execept the sender
        if client != connect:
            try:
                client.send(message)
            except:
                client.close()
                # Link broken: remove the client
                del socket_dict[connect]
                del user_dict[nick]

def private_chat(message, connect, dest, usr):
        try:
            dest.send(message)
        except:
            dest.close()
            # Link broken: remove the client
            del socket_dict[connect]
            del user_dict[usr]

def thread_client(connect, addr):

    while True:
        try:
            message = connect.recv(RECV_BUFFER)
            nick = socket_dict[connect].replace("\n", "")
            # Processing the message sent by the client, it can be a normal message, a private chat or the exit word
            if message.decode() == "exit\n":
                exit_message = "Thank you for using the chat-room. Untill next time!\n"
                connect.send(exit_message.encode())
                print("\033[1m\033[3m" + nick + "\033[0m" + " logged out.\n" + "There are " + str(len(socket_dict)-1) + " users in chat.")
                broadcast(("\033[1m\033[3m" + nick + "\033[0m" + " logged out. " + "There are " + str(len(socket_dict)-1) + " users in chat.\n").encode(), connect, nick)
                del user_dict[nick.replace("\n", "")]
                del socket_dict[connect]
                break
            elif message.decode()[0] == "&":
                frase=message.decode()
                pre=frase.find("&")
                post=frase.rfind("&")
                if pre == post:
                    # Wrong syntax
                    nickname_message = "\033[1m\033[3m" + "$" + nick + "$ " + "\033[0m"
                    message_to_send = nickname_message.encode() + message
                    print(nickname_message + message.decode(), end='', flush = True)
                    broadcast(message_to_send, connect, nick)
                else:
                    dest= message.decode()[pre+1:post]
                    message_to_send=("\033[1m\033[3m\033[1;34m" + "$" + dest + "$ " + "\033[0m" + message.decode()[post+1:]).encode()
                    try:
                        private_chat(message_to_send,connect,user_dict[dest],dest)
                    except:
                        connect.send("Non-existing user.\n".encode())
            else:
                nickname_message = "\033[1m\033[3m" + "$" + nick + "$ " + "\033[0m"
                message_to_send = nickname_message.encode() + message
                print(nickname_message + message.decode(), end='', flush = True)
                broadcast(message_to_send, connect, nick)

        except:
            connect.send("Error processing the message\n".encode())
            continue

while True:

    connect, addr = mysocket.accept()
    connect.send("Welcome to the chat-room. Introduce your nickname: ".encode())
    try:
        mynickname = connect.recv(RECV_BUFFER).decode()
        # Recieve and check if the name is already in use, if so, request another one
        while nickused:
            if mynickname in socket_dict.values():
                connect.send("The nickname introduced already exists, try another one: ".encode())
                mynickname = connect.recv(RECV_BUFFER).decode()
            else:
                welcome_message = "\nWelcome to the chat-room! " + "\033[1m\033[3m" + mynickname.replace("\n", "") + "\033[0m" + "! You have entered correctly.\nType 'exit' to log out.\nType '$emoji$' to see the EmojiMenu.\nType '&user&' to send a private message to user.\n\n"
                connect.send(welcome_message.encode())
                nickused = False
                socket_dict[connect] = mynickname
                user_dict[mynickname.replace("\n", "")] = connect
    except:
        connect.send("Error processing the message\n".encode())

    # Valid username start thread
    nickused = True
    print("\033[1m\033[3m" + mynickname.replace("\n", "") + "\033[0m" + " just connectected.\n" + "There are " + str(len(socket_dict)) + " users in chat.")
    broadcast(("\033[1m\033[3m" + mynickname.replace("\n", "") + "\033[0m" + " just connectected. " + "There are " + str(len(socket_dict)) + " users in chat.\n").encode(), connect, mynickname.replace("\n", ""))
    _thread.start_new_thread(thread_client, (connect, addr))
