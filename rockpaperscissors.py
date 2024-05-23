import tkinter as tk
from tkinter import messagebox
import random
from collections import deque
from PIL import Image, ImageTk

# Constants
CHOICES = ["Kertas", "Batu", "Gunting"]
WINNING_COMBOS = {
    "Kertas": "Batu",
    "Batu": "Gunting",
    "Gunting": "Kertas"
}

# Stack and Queue implementations
class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        return None

    def is_empty(self):
        return len(self.items) == 0

    def get_items(self):
        return self.items

class Queue:
    def __init__(self):
        self.items = deque()

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        if not self.is_empty():
            return self.items.popleft()
        return None

    def is_empty(self):
        return len(self.items) == 0

# Game Logic
class RockPaperScissorsGame:
    def __init__(self):
        self.history = Stack()
        self.queue = Queue()
        self.player_score = 0
        self.computer_score = 0

    def determine_winner(self, player, computer):
        if player == computer:
            return "Hasil: Seri"
        elif WINNING_COMBOS[player] == computer:
            self.player_score += 1
            return "Hasil: Kamu Menang!"
        else:
            self.computer_score += 1
            return "Hasil: Kamu Kalah"

    def play_round(self, player_choice):
        computer_choice = random.choice(CHOICES)
        result = self.determine_winner(player_choice, computer_choice)
        self.history.push((player_choice, computer_choice, result))
        self.queue.enqueue(result)
        return player_choice, computer_choice, result

# Main Game Class with GUI
class RockPaperScissorsGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Game Kertas Batu Gunting")

        self.game = RockPaperScissorsGame()
        self.player_name = None

        if not self.load_images():
            messagebox.showerror("Error", "Failed to load images. Exiting application.")
            self.root.destroy()
            return

        self.create_name_entry()

    def load_images(self):
        try:
            self.images = {
                "Kertas": ImageTk.PhotoImage(Image.open("kertas.png")),
                "Batu": ImageTk.PhotoImage(Image.open("batu.png")),
                "Gunting": ImageTk.PhotoImage(Image.open("gunting.png")),
                "WelcomeIcon": ImageTk.PhotoImage(Image.open("welcome_icon.png"))  # Add an icon for the welcome button
            }
            return True
        except Exception as e:
            print(f"Error loading images: {e}")
            return False

    def create_name_entry(self):
        self.name_label = tk.Label(self.root, text="Masukkan Nama Anda:", font=("Helvetica", 14))
        self.name_label.pack(pady=20)

        self.name_entry = tk.Entry(self.root, font=("Helvetica", 12), bd=2, relief="solid")
        self.name_entry.pack(pady=10)

        self.name_button = tk.Button(
            self.root,
            image=self.images["WelcomeIcon"],
            compound=tk.LEFT,
            command=self.start_game,
            bg="green",
            fg="white",
            font=("Helvetica", 12, "bold"),
            padx=10,
            pady=5
        )
        self.name_button.pack(pady=10)

    def start_game(self):
        self.player_name = self.name_entry.get()
        if not self.player_name:
            messagebox.showwarning("Peringatan", "Nama tidak boleh kosong!")
        else:
            self.name_label.pack_forget()
            self.name_entry.pack_forget()
            self.name_button.pack_forget()
            self.create_widgets()
            self.show_greeting()

    def create_widgets(self):
        self.label = tk.Label(self.root, text="Pilih Kertas, Batu, atau Gunting:", font=("Helvetica", 14))
        self.label.pack(pady=10)

        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=20)

        self.buttons = []
        for choice in CHOICES:
            button = tk.Button(self.button_frame, image=self.images[choice], borderwidth=5, relief="raised",
                               command=lambda ch=choice: self.play_round(ch))
            button.pack(side=tk.LEFT, padx=20, pady=20)
            button.bind("<Enter>", self.on_button_hover)
            button.bind("<Leave>", self.on_button_leave)
            button.bind("<ButtonPress-1>", self.on_button_press)
            button.bind("<ButtonRelease-1>", self.on_button_release)
            self.buttons.append(button)

        self.history_button = tk.Button(self.root, text="Lihat Riwayat", command=self.show_history, borderwidth=5, relief="raised", font=("Helvetica", 12, "bold"), bg="blue", fg="white")
        self.history_button.pack(pady=10)

        self.result_label = tk.Label(self.root, text="", font=("Helvetica", 14))
        self.result_label.pack(pady=10)

        self.score_label = tk.Label(self.root, text=f"Skor - {self.player_name}: 0 | Komputer: 0", font=("Helvetica", 14))
        self.score_label.pack(pady=10)

    def show_greeting(self):
        greeting_popup = tk.Toplevel(self.root)
        greeting_popup.title("Selamat Datang")
        greeting_popup.geometry("600x550")
        greeting_popup.configure(bg="lightblue")

        greeting_label = tk.Label(greeting_popup, text=f"Selamat datang, {self.player_name}! Selamat bermain Kertas, Batu, Gunting!", font=("Helvetica", 12), wraplength=250, justify=tk.CENTER, bg="lightblue")
        greeting_label.pack(pady=20, padx=20)

        close_button = tk.Button(greeting_popup, text="Mulai Bermain", command=greeting_popup.destroy, font=("Helvetica", 12, "bold"))
        close_button.pack(pady=10)

    def on_button_hover(self, event):
        event.widget.config(bg='lightgrey')

    def on_button_leave(self, event):
        event.widget.config(bg='SystemButtonFace')

    def on_button_press(self, event):
        event.widget.config(bg='lightblue', relief="sunken")

    def on_button_release(self, event):
        event.widget.config(bg='lightgrey', relief="raised")

    def play_round(self, player_choice):
        player_choice, computer_choice, result = self.game.play_round(player_choice)
        self.result_label.config(text=f"Kamu memilih: {player_choice}, Komputer memilih: {computer_choice}. {result}")
        self.update_score()

    def update_score(self):
        self.score_label.config(text=f"Skor - {self.player_name}: {self.game.player_score} | Komputer: {self.game.computer_score}")

    def show_history(self):
        if self.game.history.is_empty():
            messagebox.showinfo("Riwayat", "Belum ada permainan yang dimainkan.")
        else:
            history_items = self.game.history.get_items()
            history_text = "\n".join([f"Player: {p}, Computer: {c}, Result: {r}" for p, c, r in history_items])
            history_popup = tk.Toplevel(self.root)
            history_popup.title("Riwayat Permainan")
            history_popup.geometry("800x600")
            history_label = tk.Label(history_popup, text=history_text, font=("Helvetica", 12), justify=tk.LEFT)
            history_label.pack(pady=10, padx=10)
            close_button = tk.Button(history_popup, text="Tutup", command=history_popup.destroy, font=("Helvetica", 12, "bold"))
            close_button.pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = RockPaperScissorsGUI(root)
    root.mainloop()
