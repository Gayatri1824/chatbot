import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox

HOST = '127.0.0.1'
PORT = 1234

DARK_GREY = '#121212'
MEDIUM_GREY = '#1F1B24'
OCEAN_BLUE = '#464EB8'
WHITE = "white"
FONT = ("Helvetica", 14)   # reduced so it fits nicely
BUTTON_FONT = ("Helvetica", 12)
SMALL_FONT = ("Helvetica", 11)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def add_message(message):
    message_box.config(state=tk.NORMAL)
    message_box.insert(tk.END, message + '\n')
    message_box.config(state=tk.DISABLED)

def connect():
    try:
        client.connect((HOST, PORT))
        add_message("[SERVER] Successfully connected to the server")
    except:
        messagebox.showerror("Unable to connect", f"Unable to connect to {HOST}:{PORT}")
        return

    username = username_textbox.get()
    if username != '':
        client.sendall(username.encode())
    else:
        messagebox.showerror("Invalid username", "Username cannot be empty")

    threading.Thread(target=listen_for_messages_from_server, args=(client,), daemon=True).start()

    username_textbox.config(state=tk.DISABLED)
    username_button.config(state=tk.DISABLED)

def send_message():
    message = message_textbox.get()
    if message != '':
        client.sendall(message.encode())
        message_textbox.delete(0, tk.END)
    else:
        messagebox.showerror("Empty message", "Message cannot be empty")

root = tk.Tk()
root.geometry("600x600")
root.title("Messenger Client")

# Grid structure
root.grid_rowconfigure(0, weight=0)  # top bar (fixed height)
root.grid_rowconfigure(1, weight=1)  # middle grows
root.grid_rowconfigure(2, weight=0)  # bottom bar (fixed height)
root.grid_columnconfigure(0, weight=1)

# ------------------ Frames ------------------
top_frame = tk.Frame(root, bg=DARK_GREY)
top_frame.grid(row=0, column=0, sticky="ew")

middle_frame = tk.Frame(root, bg=MEDIUM_GREY)
middle_frame.grid(row=1, column=0, sticky="nsew")

bottom_frame = tk.Frame(root, bg=DARK_GREY)
bottom_frame.grid(row=2, column=0, sticky="ew")

# ------------------ Top frame ------------------
username_label = tk.Label(top_frame, text="Enter username:", font=FONT, bg=DARK_GREY, fg=WHITE)
username_label.pack(side=tk.LEFT, padx=10, pady=10)

username_textbox = tk.Entry(top_frame, font=FONT, bg=MEDIUM_GREY, fg=WHITE)
username_textbox.pack(side=tk.LEFT, pady=10)

username_button = tk.Button(top_frame, text="Join", font=BUTTON_FONT, bg=OCEAN_BLUE, fg=WHITE, command=connect)
username_button.pack(side=tk.LEFT, padx=10, pady=10)

# ------------------ Bottom frame ------------------
message_textbox = tk.Entry(bottom_frame, font=FONT, bg=MEDIUM_GREY, fg=WHITE)
message_textbox.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.X, expand=True)

message_button = tk.Button(bottom_frame, text="Send", font=BUTTON_FONT, bg=OCEAN_BLUE, fg=WHITE, command=send_message)
message_button.pack(side=tk.LEFT, padx=10, pady=10)

# ------------------ Middle frame ------------------
message_box = scrolledtext.ScrolledText(middle_frame, font=SMALL_FONT, bg=MEDIUM_GREY, fg=WHITE)
message_box.config(state=tk.DISABLED)
message_box.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

def listen_for_messages_from_server(client):
    while True:
        try:
            message = client.recv(2048).decode('utf-8')
            if message:
                username, content = message.split("~", 1)
                add_message(f"[{username}] {content}")
            else:
                break
        except:
            break

def main():
    root.mainloop()

if __name__ == '__main__':
    main()
