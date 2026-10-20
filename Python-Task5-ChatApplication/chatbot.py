import tkinter as tk
from tkinter import scrolledtext
from datetime import datetime
import random

def get_bot_reply(message):
    text = message.lower().strip()
    if not text:
        return "Please type a message so I can help."
    if any(word in text for word in ["hello", "hi", "hey", "namaste"]):
        return random.choice(["Hello! How can I help you today?", "Hi there! What would you like to talk about?", "Namaste! Ask me a simple question."])
    if "your name" in text or "who are you" in text:
        return "I am PyBot, a simple Python chatbot."
    if "how are you" in text:
        return "I am doing well, thank you! How can I help?"
    if "time" in text:
        return "The current time is " + datetime.now().strftime("%I:%M %p") + "."
    if "date" in text or "today" in text:
        return "Today's date is " + datetime.now().strftime("%d %B %Y") + "."
    if "python" in text:
        return "Python is a popular programming language used for automation, data analysis, AI, and web development."
    if "help" in text:
        return "Ask my name, the time, today's date, or ask me about Python."
    if "thank you" in text or "thanks" in text:
        return "You're welcome! Happy to help."
    if "bye" in text or "goodbye" in text or "exit" in text:
        return "Goodbye! Have a nice day."
    if "joke" in text:
        return "Why do programmers prefer dark mode? Because light attracts bugs!"
    return "I am a beginner rule-based chatbot, so I do not know that answer yet. Try asking about my name, time, date, Python, or type 'help'."

class PyBotApp:
    def __init__(self, root):
        self.root = root
        root.title("PyBot - Python Chatbot")
        root.geometry("680x600")
        root.minsize(520, 450)
        root.configure(bg="#eef4f8")

        header = tk.Frame(root, bg="#153e5c", padx=18, pady=16)
        header.pack(fill="x")
        tk.Label(header, text="PyBot", font=("Arial", 21, "bold"), bg="#153e5c", fg="white").pack(anchor="w")
        tk.Label(header, text="Your simple Python assistant", font=("Arial", 10), bg="#153e5c", fg="#d9edf7").pack(anchor="w")

        self.chat = scrolledtext.ScrolledText(root, wrap=tk.WORD, state="disabled", font=("Arial", 11), bg="white", fg="#1e293b", padx=12, pady=12, bd=0)
        self.chat.pack(fill="both", expand=True, padx=16, pady=(16, 10))
        self.chat.tag_config("user", foreground="#075985", font=("Arial", 10, "bold"))
        self.chat.tag_config("bot", foreground="#0f766e", font=("Arial", 10, "bold"))
        self.chat.tag_config("body", foreground="#1e293b")

        bottom = tk.Frame(root, bg="#eef4f8", padx=16, pady=12)
        bottom.pack(fill="x")
        self.message_var = tk.StringVar()
        self.entry = tk.Entry(bottom, textvariable=self.message_var, font=("Arial", 11), relief="solid", bd=1)
        self.entry.pack(side="left", fill="x", expand=True, ipady=10, padx=(0, 8))
        self.entry.bind("<Return>", lambda event: self.send_message())
        tk.Button(bottom, text="Send", command=self.send_message, bg="#087f8c", fg="white", activebackground="#066b75", font=("Arial", 10, "bold"), relief="flat", padx=20, pady=9).pack(side="left")
        tk.Button(bottom, text="Clear", command=self.clear_chat, bg="#dbe7ef", fg="#153e5c", relief="flat", padx=14, pady=9).pack(side="left", padx=(8, 0))
        self.add_message("PyBot", "Hello! I'm PyBot. Type 'help' to see what I can do.")
        self.entry.focus_set()

    def add_message(self, speaker, message):
        self.chat.configure(state="normal")
        self.chat.insert(tk.END, f"{speaker}: ", "user" if speaker == "You" else "bot")
        self.chat.insert(tk.END, message + "\n\n", "body")
        self.chat.configure(state="disabled")
        self.chat.see(tk.END)

    def send_message(self):
        message = self.message_var.get().strip()
        if not message:
            return
        self.message_var.set("")
        self.add_message("You", message)
        self.root.after(250, lambda: self.add_message("PyBot", get_bot_reply(message)))

    def clear_chat(self):
        self.chat.configure(state="normal")
        self.chat.delete("1.0", tk.END)
        self.chat.configure(state="disabled")
        self.add_message("PyBot", "Chat cleared. How can I help?")

if __name__ == "__main__":
    root = tk.Tk()
    app = PyBotApp(root)
    root.mainloop()
