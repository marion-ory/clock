import tkinter as tk
from time import strftime
from ttkthemes import ThemedStyle
from tkinter import ttk, messagebox
import datetime
import time


# Configuration
is_24_hour_format = True  # On définit le format
alarm_time = None
pause = False


root = tk.Tk()  # fenetre principale
root.title("Clock test")

#  affichage de l heure
label_time = tk.Label(root, font=("Arial", 40, "bold"), fg="black")
label_time.pack(padx=20, pady=5)


# Format 12 ou 24
def time_format():
    global is_24_hour_format

    is_24_hour_format = not is_24_hour_format
    time_format_button.config(text="Passer en 12 H" if is_24_hour_format else "24 Hour")


#  bouton change format
time_format_button = ttk.Button(root, text="Passer en 12H", command=time_format)
time_format_button.pack(pady=10)


# AFFICHER L HEURE FONCTION
def print_time():
    global pause
    global alarm_time

    if pause == False:
        now = datetime.datetime.now()
        h = now.hour
        m = now.minute
        s = now.second
        suf = ""  # vide pour stocker AM PM

        # compare l alarme avec l heure actuelle
        if (
            alarm_time and h == alarm_time[0] and m == alarm_time[1]
        ):  # lis 1er puis 2eme chiffre
            messagebox.showwarning(
                "Rappel", "Jeannine tes médicaments !"
            )  # 2 attributs
            alarm_time = None  # comme break pour sortir

        if not is_24_hour_format:
            suf = "AM" if h < 12 else "PM"
            h = h % 12
            if h == 0:
                h = 12  # affiche 12 au lieu de 00.00

        current_time = (h, m, s)
        hour = f"{current_time[0]:02d}:{current_time[1]:02d}:{current_time[2]:02d}{suf}"

        label_time.config(text=hour)

        # actualise toutes les secondes (décalé aussi !)
        label_time.after(1000, print_time)


# --Def stop fonction --
def rest():
    global pause

    if pause == False:
        pause = True
        rest_button.config(text="Reprendre")
    elif pause == True:
        pause = False
        rest_button.config(text="Pause")
        print_time()  # Relance l'affichage après la pause


# REGLER L ALARME FONCTION
def set_alarm():
    global alarm_time
    try:
        h = int(entry_h.get())  # entry= boite de saisie
        m = int(entry_m.get())  # get = pour lire
        alarm_time = (h, m)
        messagebox.showinfo("Alarme activé", f"Alarme réglée pour {h:02d} : {m:02d}")

    except ValueError:
        messagebox.showinfo("Erreur ", "format HH:MM")


# --- INTERFACE DE SAISIE ALARME ---

frame_alarm = ttk.Frame(root)  # cadre dans parent frame alarm
frame_alarm.pack(pady=10)  # design cadre

ttk.Label(frame_alarm, text="H:").grid(row=0, column=0)
entry_h = ttk.Entry(frame_alarm, width=5)  # Case pour l'heure
entry_h.grid(row=0, column=1, padx=5)

ttk.Label(frame_alarm, text="M:").grid(row=0, column=2)
entry_m = ttk.Entry(frame_alarm, width=5)  # Case pour les minutes
entry_m.grid(row=0, column=3, padx=5)


#  bouton alarme
alarm_button = ttk.Button(root, text="Activer l'alarme", command=set_alarm)
alarm_button.pack(pady=10)


# ------INTERFACE DE SAISIE STOP ---

frame_rest = ttk.Frame(root)

rest_button = ttk.Button(root, text="Pause", command=rest)
rest_button.pack(pady=10)

# Lancer la fonction une première fois
print_time()
root.mainloop()
