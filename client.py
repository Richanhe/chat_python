import socket
import threading
import tkinter as tk
from tkinter import Button, scrolledtext
from tkinter import messagebox

HOST = '192.168.5.101'
PORT = 1234

DARK_GREY = '#121212'
MEDIUM_GREY = '#1F1B24'
OCEAN_BLUE = '#464EB8'
WHITE = "white"
FONT = ("Helvetica", 17)
BUTTON_FONT = ("Helvetica", 15)
SMALL_FONT = ("Helvetica", 13)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def add_message(message):
    message_box.config(state=tk.NORMAL)
    message_box.insert(tk.END, message + '\n')
    message_box.config(state=tk.DISABLED)


def connect():
    try:
        client.connect((HOST, PORT))
        add_message("[SERVER]: Conectado com sucesso")
    except:
        messagebox.showerror("Erro", "Erro ao se conectar")

    username = username_textbox.get()
    if username != '':
        client.sendall(username.encode())
    else:
        messagebox.showerror("User inválido", "User não pode estar vazio")

    threading.Thread(target=listen_for_msg_from_server, args=(client,)).start()

    username_textbox.config(state=tk.DISABLED)
    username_button.config(state=tk.DISABLED)


def send_message():
    message = message_textbox.get().strip()  #strip p/ remover espaços extras
    if message:
        try:
            client.sendall(message.encode())
            if message == '/quit':
                client.close()  
                root.destroy()  
            else:
                message_textbox.delete(0, tk.END)  #limpa a caixa de entrada
        except Exception as e:
            messagebox.showerror("Erro", "Não foi possível enviar a mensagem.")
            print(f"Erro ao enviar mensagem: {e}")
    else:
        messagebox.showerror("Mensagem vazia", "Mensagem não pode estar vazia")

root = tk.Tk()
root.geometry("600x600")
root.title("CHAT")
root.resizable(False, False)

root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=4)
root.grid_rowconfigure(2, weight=1)

top_frame = tk.Frame(root, width=600, height=100, bg=DARK_GREY)
top_frame.grid(row=0, column=0, sticky=tk.NSEW)

middle_frame = tk.Frame(root, width=600, height=400, bg=MEDIUM_GREY)
middle_frame.grid(row=1, column=0, sticky=tk.NSEW)

bottom_frame = tk.Frame(root, width=600, height=100, bg=DARK_GREY)
bottom_frame.grid(row=2, column=0, sticky=tk.NSEW)

username_label = tk.Label(top_frame, text="Username:", font=FONT, bg=DARK_GREY, fg=WHITE)
username_label.pack(side=tk.LEFT, padx=10)

username_textbox = tk.Entry(top_frame, font=FONT, bg=MEDIUM_GREY, fg=WHITE, width=23)
username_textbox.pack(side=tk.LEFT)

username_button = tk.Button(top_frame, text="Entrar", font=FONT, bg=OCEAN_BLUE, fg=WHITE, command=connect)
username_button.pack(side=tk.LEFT, padx=8)

message_textbox = tk.Entry(bottom_frame, font=FONT, bg=MEDIUM_GREY, fg=WHITE, width=38)
message_textbox.pack(side=tk.LEFT, padx=10)

message_button = tk.Button(bottom_frame, text="Enviar", font=BUTTON_FONT, bg=OCEAN_BLUE, fg=WHITE, command=send_message)
message_button.pack(side=tk.LEFT, padx=10)

message_box = scrolledtext.ScrolledText(middle_frame, font=SMALL_FONT, bg=MEDIUM_GREY, fg=WHITE, width=67, height=26.5)
message_box.config(state=tk.DISABLED)
message_box.pack(side=tk.TOP)


def listen_for_msg_from_server(client):
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message:
                add_message(message)
            else:
                messagebox.showerror("ERRO", "Mensagem recebida está vazia")
        except:
            break


def main():
    root.mainloop()


if _name_ == '_main_':
    main()
