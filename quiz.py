import socket
from threading import Thread
import random

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

ip_address = '127.0.0.1'
port=4000

server.bind((ip_address,port))
server.listen()

list_of_clients=[]

questions=[
    "1. Which is called the first wonder of the world? \n a) The Pyramids of Egypt \n b) The Hanging Gardens of Babylon \n c) The Tomb of Mausolus \n d) The Colossus of Rhodes",
    "2. Which of the given cities is located on the bank of river Ganga? \n a)Patna \n b)Gwalior \n c)Bhopal \n d)Mathur",
    "3. The driving force of an ecosystem is \n a) Carbon Mono oxide \n b)Biogas\n c)Solar Energy \n d)Carbon dioxide",
    "4. Digestion of food in human beings begins in which part of the alimentary canal? \n a)Liver \n b)Kidney \n c)Mouth \n d)Large intestine",
    "5. The tropic of cancer does pass through which state of India? \n a) Uttar Pradesh \n b) Madhya Pradesh \n c) Bihar \n d) Andhra Pradesh"
]
answers=['a','a','c','c','b']

print("Server has started !")

def get_random_question_answer(conn):
    random_index=random.randint(0,len(questions)-1)
    random_question= questions[random_index]
    random_answer=answers[random_index]
    conn.send(random_question.encode('utf-8'))
    return random_index,random_question, random_answer

def remove_question(index):
    questions.pop(index)
    answers.pop(index)

def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)

def clientThread(conn):
    score=0
    conn.send("Welcome to this quiz game !")
    conn.send("You will receive a question. The answer to that question should be one of a,b,c,d")
    conn.send("Good luck ! \n\n".encode('utf-8'))
    index,question,answer=get_random_question_answer(conn)
    while True:
        try:
            message=conn.recv(2048).decode('utf-8')
            if message:
                if message.lower()==answer:
                    score+=1
                    conn.send(f"Your score is{score}\n\n".encode('utf-8'))
                else:
                    conn.send(f"Incorrect answer ..\n\n".encode('utf-8'))
                    remove_question(index)
                    index,question,answer=get_random_question_answer(conn)
            else:
                remove(conn)
        except:
            continue

while True:
    conn, addr = server.accept()
    list_of_clients.append(conn)
    print(addr[0]+" connected")
    new_thread = Thread(target= clientThread,args=(conn))
    new_thread.start()
