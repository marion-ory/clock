import tkinter as tk
from tkinter import ttk, messagebox
import datetime
import time
import pygame  # Utilisé ici pour l'alarme ET le son de la vidéo
from tkvideo import tkvideo

# INITIALISATION AUDIO
pygame.mixer.init()

# Configuration
is_24_hour_format = True
alarm_time = None
pause = False
pause_click_count = 0  # Compteur pour le bouton pause

root = tk.Tk()
root.title("Horloge Interactive")

# --- AJOUT DU FOND D'ÉCRAN ---
# On charge les deux images au démarrage
image_fond1 = tk.PhotoImage(file="fond.png")
try:
    image_fond2 = tk.PhotoImage(file="fond2.png")
except:
    # Au cas où le fichier fond2.jpg pose problème avec PhotoImage (nécessite parfois PIL pour le JPG pur)
    # On garde la même par défaut ou on gère l'erreur
    image_fond2 = image_fond1 

background_label = tk.Label(root, image=image_fond1)
background_label.place(relwidth=1, relheight=1) # L'image prend toute la place
# ------------------------------

# Affichage de l'heure
label_time = tk.Label(root, font=("Arial", 40, "bold"), fg="black", bg="white")
label_time.pack(padx=20, pady=5)

# FONCTION FORMAT 12/24H
def time_format():
    global is_24_hour_format
    is_24_hour_format = not is_24_hour_format
    
    # Changement du texte du bouton
    time_format_button.config(text="Passer en 12H" if is_24_hour_format else "Passer en 24H")
    
    # CHANGEMENT DU FOND LORS DU CLIC
    if not is_24_hour_format:
        background_label.config(image=image_fond2)
    else:
        background_label.config(image=image_fond1)

# Bouton format
time_format_button = ttk.Button(root, text="Passer en 12H", command=time_format)
time_format_button.pack(pady=10)

# FONCTION LECTURE VIDÉO ET FERMETURE
def play_stop_video():
    # On crée une nouvelle fenêtre en plein écran pour la vidéo
    top = tk.Toplevel(root)
    top.attributes("-fullscreen", True)
    video_label = tk.Label(top)
    video_label.pack(expand=True, fill="both")
    
    # Lancement du SON en premier via pygame
    try:
        pygame.mixer.music.load("stopit.mp3")
        pygame.mixer.music.play()
    except:
        print("Erreur : stopit.mp3 introuvable")

    # Lancement de la VIDÉO
    player = tkvideo("stopit.mp4", video_label, loop=0, size=(root.winfo_screenwidth(), root.winfo_screenheight()))
    player.play()
    
    # On ferme tout après 19 secondes
    root.after(19000, root.destroy)

# FONCTION PRINCIPALE D'AFFICHAGE
def print_time():
    global pause
    global alarm_time

    if not pause:
        now = datetime.datetime.now()
        h = now.hour
        m = now.minute
        s = now.second
        suf = ""

        # Verifier l'alarme
        if alarm_time and h == alarm_time[0] and m == alarm_time[1] and s == 0:
            try:
                pygame.mixer.music.load("alarme.mp3")
                pygame.mixer.music.play()
            except:
                pass
            messagebox.showwarning("Rappel", "Jeannine tes médicaments !")
            alarm_time = None 

        # Conversion format 12h
        display_h = h
        if not is_24_hour_format:
            suf = " AM" if h < 12 else " PM"
            display_h = h % 12
            if display_h == 0:
                display_h = 12

        hour_string = f"{display_h:02d}:{m:02d}:{s:02d}{suf}"
        label_time.config(text=hour_string)

    # Rappel de la fonction toutes les secondes
    label_time.after(1000, print_time)

# FONCTION PAUSE / REPRISE
def rest():
    global pause
    global pause_click_count
    
    pause_click_count += 1
    
    # Se déclenche à partir de 6 clics
    if pause_click_count >= 6:
        rest_button.config(state="disabled")
        play_stop_video()
        return

    if not pause:
        pause = True
        rest_button.config(text="Reprendre")
        print("[PAUSE] ZA WARUDO !!!!")
    else:
        pause = False
        rest_button.config(text="Pause")
        print("[LECTURE] Le temps reprend son cours.")

# FONCTION REGLAGE ALARME
def set_alarm():
    global alarm_time
    try:
        h = int(entry_h.get())
        m = int(entry_m.get())
        if 0 <= h <= 23 and 0 <= m <= 59:
            alarm_time = (h, m)
            messagebox.showinfo("Alarme activée", f"Alarme réglée pour {h:02d}:{m:02d}")
        else:
            raise ValueError
    except ValueError:
        messagebox.showerror("Erreur", "Format invalide (H: 0-23, M: 0-59)")

# INTERFACE ALARME
frame_alarm = ttk.Frame(root)
frame_alarm.pack(pady=10)

ttk.Label(frame_alarm, text="H:").grid(row=0, column=0)
entry_h = ttk.Entry(frame_alarm, width=5)
entry_h.grid(row=0, column=1, padx=5)

ttk.Label(frame_alarm, text="M:").grid(row=0, column=2)
entry_m = ttk.Entry(frame_alarm, width=5)
entry_m.grid(row=0, column=3, padx=5)

alarm_button = ttk.Button(root, text="Activer l'alarme", command=set_alarm)
alarm_button.pack(pady=5)

# INTERFACE BOUTON PAUSE
rest_button = ttk.Button(root, text="Pause", command=rest)
rest_button.pack(pady=10)

# Lancement
print_time()
root.mainloop()