import tkinter as tk
from tkinter import ttk, messagebox
import datetime
import time
import pygame 
from tkvideo import tkvideo

# INITIALISATION AUDIO
pygame.mixer.init()

# Configuration
is_24_hour_format = True
alarm_time = None
pause = False
pause_click_count = 0  # Compteur pour le bouton pause
heure_manuelle_forcee = None # Pour stocker l'heure réglée par afficher_heure

root = tk.Tk()
root.title("Horloge Interactive")

# --- AJOUT DU FOND D'ÉCRAN ---
image_fond1 = tk.PhotoImage(file="fond.png")
try:
    image_fond2 = tk.PhotoImage(file="fond2.png")
except:
    image_fond2 = image_fond1 

background_label = tk.Label(root, image=image_fond1)
background_label.place(relwidth=1, relheight=1)
# ------------------------------

# --- ZONE D'AFFICHAGE CENTRALE (HEURE + ROUAGE) ---
frame_horloge = tk.Frame(root, bg="white", bd=2, relief="ridge")
frame_horloge.pack(pady=20)

label_time = tk.Label(frame_horloge, font=("Arial", 40, "bold"), fg="black", bg="white")
label_time.pack(side="left", padx=(20, 5), pady=5)

# Chargement de l'icône engrenage avec réduction de taille accrue
try:
    # .subsample(3, 3) divise la taille par 3.
    img_rouage = tk.PhotoImage(file="engrenage.png").subsample(3, 3)
except:
    # Si l'image n'existe pas, on met un texte simple "*"
    img_rouage = None

def ouvrir_reglages(event=None):
    # Bascule l'affichage du panneau de modification
    if frame_manual.winfo_viewable():
        frame_manual.pack_forget()
    else:
        frame_manual.pack(pady=10, padx=10)

btn_rouage = tk.Label(frame_horloge, image=img_rouage, text="⚙" if not img_rouage else "", 
                      font=("Arial", 20), bg="white", cursor="hand2")
btn_rouage.pack(side="left", padx=(5, 15))
btn_rouage.bind("<Button-1>", ouvrir_reglages)


def afficher_heure(heure):
    global heure_manuelle_forcee
    heure_manuelle_forcee = heure
    h, m, s = heure
    suf = ""
    display_h = h
    if not is_24_hour_format:
        suf = " AM" if h < 12 else " PM"
        display_h = h % 12
        if display_h == 0: display_h = 12
    hour_string = f"{display_h:02d}:{m:02d}:{s:02d}{suf}"
    label_time.config(text=hour_string)

def modifier_heure_interface():
    try:
        h = int(entry_h_man.get())
        m = int(entry_m_man.get())
        s = int(entry_s_man.get())
        if 0 <= h <= 23 and 0 <= m <= 59 and 0 <= s <= 59:
            afficher_heure((h, m, s))
            frame_manual.pack_forget() # Cache le menu après validation
        else:
            raise ValueError
    except ValueError:
        messagebox.showerror("Erreur", "Format invalide (H: 0-23, M/S: 0-59)")

def time_format():
    global is_24_hour_format
    is_24_hour_format = not is_24_hour_format
    time_format_button.config(text="Passer en 12H" if is_24_hour_format else "Passer en 24H")
    background_label.config(image=image_fond2 if not is_24_hour_format else image_fond1)

time_format_button = ttk.Button(root, text="Passer en 12H", command=time_format)
time_format_button.pack(pady=5)

def play_stop_video():
    top = tk.Toplevel(root)
    top.attributes("-fullscreen", True)
    video_label = tk.Label(top)
    video_label.pack(expand=True, fill="both")
    try:
        pygame.mixer.music.load("stopit.mp3")
        pygame.mixer.music.play()
    except:
        pass
    player = tkvideo("stopit.mp4", video_label, loop=0, size=(root.winfo_screenwidth(), root.winfo_screenheight()))
    player.play()
    root.after(20000, root.destroy)

def print_time():
    global pause, alarm_time, heure_manuelle_forcee
    if not pause:
        if heure_manuelle_forcee is None:
            now = datetime.datetime.now()
            h, m, s = now.hour, now.minute, now.second
        else:
            h, m, s = heure_manuelle_forcee
            s += 1
            if s >= 60: s = 0; m += 1
            if m >= 60: m = 0; h += 1
            if h >= 24: h = 0
            heure_manuelle_forcee = (h, m, s)

        if alarm_time and h == alarm_time[0] and m == alarm_time[1] and s == 0:
            try:
                pygame.mixer.music.load("alarme.mp3")
                pygame.mixer.music.play()
            except: pass
            messagebox.showwarning("Rappel", "Jeannine tes médicaments !")
            alarm_time = None 

        display_h = h
        suf = ""
        if not is_24_hour_format:
            suf = " AM" if h < 12 else " PM"
            display_h = h % 12 if h % 12 != 0 else 12

        label_time.config(text=f"{display_h:02d}:{m:02d}:{s:02d}{suf}")
    label_time.after(1000, print_time)

def rest():
    global pause, pause_click_count
    pause_click_count += 1
    if pause_click_count >= 6:
        rest_button.config(state="disabled")
        play_stop_video()
        return
    pause = not pause
    rest_button.config(text="Reprendre" if pause else "Pause")

def set_alarm():
    global alarm_time
    try:
        h, m = int(entry_h.get()), int(entry_m.get())
        if 0 <= h <= 23 and 0 <= m <= 59:
            alarm_time = (h, m)
            messagebox.showinfo("Alarme", f"Alarme réglée pour {h:02d}:{m:02d}")
        else: raise ValueError
    except ValueError:
        messagebox.showerror("Erreur", "Format invalide")

# INTERFACE MODIFIER L'HEURE (Cachée par défaut)
frame_manual = ttk.LabelFrame(root, text="Modifier l'heure")
# On ne le pack pas immédiatement

ttk.Label(frame_manual, text="H:").grid(row=0, column=0)
entry_h_man = ttk.Entry(frame_manual, width=4); entry_h_man.grid(row=0, column=1, padx=2)
ttk.Label(frame_manual, text="M:").grid(row=0, column=2)
entry_m_man = ttk.Entry(frame_manual, width=4); entry_m_man.grid(row=0, column=3, padx=2)
ttk.Label(frame_manual, text="S:").grid(row=0, column=4)
entry_s_man = ttk.Entry(frame_manual, width=4); entry_s_man.grid(row=0, column=5, padx=2)
ttk.Button(frame_manual, text="Valider", command=modifier_heure_interface).grid(row=1, column=0, columnspan=6, pady=5)

# INTERFACE ALARME
frame_alarm = ttk.LabelFrame(root, text="Réglage Alarme")
frame_alarm.pack(pady=10, padx=10)
entry_h = ttk.Entry(frame_alarm, width=5); entry_h.grid(row=0, column=1)
entry_m = ttk.Entry(frame_alarm, width=5); entry_m.grid(row=0, column=3)
ttk.Button(frame_alarm, text="Activer l'alarme", command=set_alarm).grid(row=1, column=0, columnspan=4, pady=5)

rest_button = ttk.Button(root, text="Pause", command=rest)
rest_button.pack(pady=10)

print_time()
root.mainloop()