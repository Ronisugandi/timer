import tkinter as tk
from tkinter import messagebox
import time
import threading
import pygame
import os

class TimerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("🤖 Futuristic Timer")
        self.master.geometry("400x360")
        self.master.configure(bg="#0f0f1e")
        self.master.resizable(False, False)

        # Inisialisasi pygame untuk suara
        pygame.mixer.init()

        # Font fallback
        self.font_path = os.path.join(os.path.dirname(__file__), "Orbitron-Regular.ttf")
        if os.path.exists(self.font_path):
            try:
                import tkinter.font as tkFont
                self.custom_font = tkFont.Font(file=self.font_path, size=30)
                self.label_font = tkFont.Font(file=self.font_path, size=12)
            except Exception:
                self.custom_font = ("Courier New", 36, "bold")
                self.label_font = ("Courier New", 12, "bold")
        else:
            self.custom_font = ("Courier New", 36, "bold")
            self.label_font = ("Courier New", 12, "bold")

        self.remaining_time = 0
        self.running = False
        self.paused = False

        self.timer_label = tk.Label(master, text="00:00:00", font=self.custom_font, fg="#00ffe1", bg="#0f0f1e")
        self.timer_label.pack(pady=20)

        self.input_frame = tk.Frame(master, bg="#0f0f1e")
        self.input_frame.pack(pady=10)

        self.hour_entry = self.create_time_input("Jam", 0)
        self.minute_entry = self.create_time_input("Menit", 1)
        self.second_entry = self.create_time_input("Detik", 2)

        self.button_frame = tk.Frame(master, bg="#0f0f1e")
        self.button_frame.pack(pady=15)

        self.start_btn = tk.Button(self.button_frame, text="▶ Start", command=self.start_timer, font=self.label_font,
                                   bg="#1c1c2b", fg="#00ffcc", activebackground="#00ffcc", activeforeground="#1c1c2b", width=10)
        self.start_btn.grid(row=0, column=0, padx=5)

        self.pause_btn = tk.Button(self.button_frame, text="⏸ Pause", command=self.pause_timer, font=self.label_font,
                                   bg="#1c1c2b", fg="#ffaa00", activebackground="#ffaa00", activeforeground="#1c1c2b", width=10)
        self.pause_btn.grid(row=0, column=1, padx=5)

        self.reset_btn = tk.Button(self.button_frame, text="⏹ Reset", command=self.reset_timer, font=self.label_font,
                                   bg="#1c1c2b", fg="#ff4444", activebackground="#ff4444", activeforeground="#1c1c2b", width=10)
        self.reset_btn.grid(row=0, column=2, padx=5)

        self.status_label = tk.Label(master, text="", font=self.label_font, fg="#8888aa", bg="#0f0f1e")
        self.status_label.pack(pady=5)

    def create_time_input(self, label_text, column):
        tk.Label(self.input_frame, text=label_text, font=self.label_font, bg="#0f0f1e", fg="#00ffe1").grid(row=0, column=column)
        entry = tk.Entry(self.input_frame, width=5, font=self.label_font, bg="#1f1f2e", fg="#00ffe1", justify="center", insertbackground="#00ffe1")
        entry.grid(row=1, column=column, padx=10)
        entry.insert(0, "0")
        return entry

    def start_timer(self):
        if self.running:
            return
        try:
            hours = int(self.hour_entry.get())
            minutes = int(self.minute_entry.get())
            seconds = int(self.second_entry.get())
            self.remaining_time = hours * 3600 + minutes * 60 + seconds
        except ValueError:
            messagebox.showerror("Invalid input", "Masukkan angka yang valid untuk jam, menit, dan detik.")
            return

        if self.remaining_time <= 0:
            messagebox.showwarning("Kosong", "Masukkan waktu lebih dari 0 detik.")
            return

        self.running = True
        self.paused = False
        self.status_label.config(text="⏳ Timer dimulai.")
        threading.Thread(target=self.run_timer, daemon=True).start()

    def pause_timer(self):
        if not self.running:
            return
        self.paused = not self.paused
        status = "⏸ Dijeda." if self.paused else "▶ Dilanjutkan."
        self.status_label.config(text=status)

    def reset_timer(self):
        self.running = False
        self.paused = False
        self.remaining_time = 0
        self.timer_label.config(text="00:00:00")
        self.status_label.config(text="⏹ Direset.")

    def run_timer(self):
        while self.remaining_time > 0 and self.running:
            if not self.paused:
                time.sleep(1)
                self.remaining_time -= 1
                hrs, rem = divmod(self.remaining_time, 3600)
                mins, secs = divmod(rem, 60)
                self.timer_label.config(text=f"{hrs:02}:{mins:02}:{secs:02}")
        if self.remaining_time == 0 and self.running:
            self.timer_label.config(text="00:00:00")
            self.status_label.config(text="✅ Waktu habis!")
            self.running = False
            threading.Thread(target=self.play_alarm_sound, daemon=True).start()
            messagebox.showinfo("⏰ Timer", "Waktu habis!")

    def play_alarm_sound(self):
        try:
            pygame.mixer.music.load("alarm.mp3")
            pygame.mixer.music.play()
        except Exception as e:
            messagebox.showerror("Error", f"Gagal memutar suara alarm: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TimerApp(root)
    root.mainloop()
