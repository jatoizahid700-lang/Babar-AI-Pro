import tkinter as tk
from tkinter import scrolledtext

class ChatBot:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("ChatBot")
        self.window.geometry("400x600")
        self.window.configure(bg="#2f4f7f")

        self.chat_log = scrolledtext.ScrolledText(self.window, width=40, height=20, bg="#f0f0f0", fg="#2f4f7f")
        self.chat_log.pack(padx=10, pady=10)

        self.input_field = tk.Entry(self.window, width=30, bg="#f0f0f0", fg="#2f4f7f")
        self.input_field.pack(padx=10, pady=10)

        self.send_button = tk.Button(self.window, text="Send", command=self.send_message, bg="#4CAF50", fg="#ffffff")
        self.send_button.pack(padx=10, pady=10)

        self.clear_button = tk.Button(self.window, text="Clear", command=self.clear_chat, bg="#e74c3c", fg="#ffffff")
        self.clear_button.pack(padx=10, pady=10)

    def send_message(self):
        user_input = self.input_field.get()
        self.chat_log.insert(tk.END, "User: " + user_input + "\n")
        self.input_field.delete(0, tk.END)

        response = self.generate_response(user_input)
        self.chat_log.insert(tk.END, "Bot: " + response + "\n")

    def generate_response(self, user_input):
        if user_input == "hello":
            return "Hi, how are you?"
        elif user_input == "goodbye":
            return "See you later!"
        else:
            return "I didn't understand that."

    def clear_chat(self):
        self.chat_log.delete(1.0, tk.END)

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    chatbot = ChatBot()
    chatbot.run()
