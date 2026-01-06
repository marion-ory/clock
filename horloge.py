import time as time_library
from time import strftime
import keyboard
import pygame

# INITIALISATION AUDIO
pygame.mixer.init()

# VARIABLES GLOBALES
heure_manuelle = None
heure_alarme = None
alarme_declenchee = False
is_24_hour_format = True
en_pause = False

def afficher_heure(heure):
    global heure_manuelle
    heure_manuelle = heure

def regler_alarme(heure_choisie):
    global heure_alarme, alarme_declenchee
    heure_alarme = heure_choisie
    alarme_declenchee = False

def choisir_mode_affichage(mode):
    global is_24_hour_format
    if mode == "12h":
        is_24_hour_format = False
    elif mode == "24h":
        is_24_hour_format = True

def gerer_pause(e):
    global en_pause
    en_pause = not en_pause
    
    if en_pause:
        try:
            pygame.mixer.music.load("stop.mp3")
            pygame.mixer.music.play()
        except:
            pass

        ascii_dio = r"""
                ⢷⡀⠀⠀⠀⠀⠀⠀⠀⣾⠀⢸⣰⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡀⠀⠀⠀⠀⠉⠳⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⠈⠉
                ⣨⡇⠀⠀⠀⠀⠀⠀⠀⣿⠀⢸⠃⠀⠀⠀⠀⠀⠀⠀⢀⠀⠀⠀⢀⠀⠀⠀⢻⡄⠀⠀⠀⠀⠀⠘⢶⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⠴
                ⢰⠏⠀⠀⠀⠀⠀⠀⠀⠀⣿⡀⠘⣧⠀⠀⠀⠀⠀⠻⣷⣿⠀⠀⠀⠸⣿⡀⠀⠀⠻⣆⠀⠀⠀⠀⠀⠀⠙⠦⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠒
                ⢰⣦⡀⠀⠀⠀⠀⠀⠀⢀⠈⠛⢀⣸⣿⠀⢠⣄⡀⠀⢻⠙⢷⣄⡀⠀⢹⡽⢦⡀⠀⠹⣦⠀⠀⠀⠀⠀⠀⠀⠈⠻⢤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢧
      ⢻⡦⠤⣤⡤⠴⠛⠁⠀⠀⠀⠀⠀⣤⡼⣷⣧⠀⣟⣿⡀⢸⠋⢳⡀⠸⡆⠀⢙⣿⣦⡀⠹⡄⠙⠳⠤⣌⣿⡛⣛⠛⠛⠛⠛⠛⠉⠉⢉⣃⠀⠀⠀⠀⠀⠀⠀⠀⠈
      ⠈⠻⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣧⢹⣿⢿⡟⠘⣇⢸⠀⠀⢻⠀⡇⡴⠋⣸⠏⠙⠳⢽⣦⠀⠀⠈⠉⠛⣽⣷⠄⠀⠀⠀⣠⡴⠋⢉⣹⡆⠀⠀⠀⠀⠀⠀⠀
      ⠀⠀⠈⠉⠉⣿⠄⠀⠀⠀⠀⢰⣄⠀⠸⡇⡿⠀⠀⠀⢻⣼⡄⠀⠈⣷⠿⢁⣴⠃⣀⣠⢄⣒⣿⣿⠟⠀⠀⠀⠈⠛⠓⣶⠀⡟⠋⢠⡼⠋⠉⡇⠀⠀⠀⠀⠀⠀⠀
      ⠀⠀⠀⠀⡼⢻⡷⠀⠀⠀⣶⠀⢻⡄⣰⣿⠇⠀⠰⡀⠸⣿⣇⣰⡾⣿⣤⣾⣵⣾⡽⠿⠟⣹⡟⠁⠀⠀⠀⠀⠀⠀⠀⢸⣠⡇⠀⢸⠛⢳⡄⢹⡄⠀⠀⠀⠀⠀⠀
      ⠀⠀⠀⢸⢡⣿⡃⠀⠀⠀⠹⡇⣸⣧⡿⣿⢦⣀⡀⣧⠀⣯⣽⣧⡴⣿⣿⡿⠛⢽⣋⣿⣶⡋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣿⠀⠀⣸⡄⣠⡇⠈⣧⠀⠀⠀⠀⠀⣠
      ⠀⠀⠀⠸⢿⢸⣇⠀⢠⡆⠀⣧⡿⣿⡷⠿⣶⣌⡛⢿⡄⠘⢋⣽⣺⣽⣿⠟⠒⠒⠾⠟⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠰⠿⠀⠀⣿⣼⠋⠀⢠⡿⠀⠀⠀⠠⠼⢥
                ⠀⠀⠉⣳⣿⡇⠀⡿⠀⠙⣷⣹⣯⣿⢽⣶⣧⠀⠈⠉⠉⠈⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠇⠀⢀⣼⠃⠀⠀⠀⠀⣴⠊
                ⣤⣶⣞⣩⠿⡇⣴⠦⣤⠀⠘⣏⠹⠿⠟⠉⣿⣰⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣤⣄⣀⣰⠟⠁⠀⠀⠀⠀⠀⠈⢆
                ⠀⠀⠀⠀⠀⣿⡟⣞⡟⣦⡀⢻⡄⠀⠀⠀⣷⡇⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⢹⠈⠁⠀⠀⠀⠀⠀⠀⢸⠒⢎
                ⠀⠀⠀⠀⠀⠻⠁⠸⣿⠀⠙⠿⡇⠀⠀⠀⠻⣦⡈⠻⠛⠶⠀⠀⠀⠀⠀⠀⠀⠀⣦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⠇⠸⣇⠀⠀⠀⠀⠀⠀⠀⠈⢇⠀
                ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⡄⠀⠀⠀⠁⠀⠀⠀⠀⣀⣠⣤⡤⢤⣤⣼⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠀⠀⠙⣆⢦⠀⠀⠀⠀⠀⠀⠈⣆
                ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⡄⠀⠀⠀⡟⣥⠶⠶⢋⣩⣤⠴⣞⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⠀⠀⠙⢿⠀⢸⠀⠀⠀⠀⠀⠈
                ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⣦⠀⠀⠁⠻⣶⠟⠉⣠⠶⠋⠉⠀⠀⣸⠇⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⢟⡅⠀⠀⢀⡾⢠⡟⠀⠀⠀⠀⠀⠀
                ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢳⣄⠀⠀⠈⣷⣾⠁⠀⠀⠀⠀⣠⣾⠀⠀⠀⠀⠀⠀⠀⢀⣴⠟⠁⣸⠁⠀⠀⣼⡷⠛⣇⠀⠀⠀⠀⠀⠀
                ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢧⡀⠀⢸⣛⡒⠲⠶⠚⣋⡵⠋⠀⠀⠀⠀⠀⢀⡴⠛⠁⠀⢀⡏⠀⠀⠚⠋⠀⠀⠹⣤⠤⠤⠤⢠⠤
                ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⣆⠀⠉⠉⠑⠒⣋⣭⠄⠀⠀⠀⠀⢀⡴⠋⠀⠀⠀⠀⣾⠀⠀⠀⠀⠀⠀⠀⠀⢻⡤⢤⣄⡼⠃
      ⣀⣴⡖⠛⠙⢧⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⢧⠀⠈⠉⠉⠉⠀⠀⠀⠀⣀⡴⠋⠀⠀⠀⠀⠀⢸⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⢳⣠⠞⠁⠀
      ⠫⡟⠁⠀⠀⠀⠈⢷⡀⠀⢀⣤⠶⠒⠋⠉⠛⣷⠀⠀⠀⠀⠀⠀⠀⠀⠘⣧⠀⠀⠀⠀⠀⣀⣠⠞⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣠⠴⠖⠉⢀⣠⡴⠚
      ⠿⠤⠤⠤⠤⣤⠀⠈⣧⣰⠟⠁⠀⠀⠀⢀⣴⠿⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⠤⠟⣛⣷⣶⠒⢻⡏⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⡤⠤⠴⠒⠛⠋⠉⠀⢀⣀⡤⠞⠋⠀⠀⠀
                ⢸⡀⠀⢸⡁⠀⠀⠀⢀⡴⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⣞⢉⡴⠖⠛⠉⠁⠹⡆⢸⡇⠀⠀⣀⡤⠴⠒⠛⠉⠉⠀⠀⠀⣀⣀⣠⠤⠔⠚⠉⠁⠀⠀⠀⠀⠀⠀
      ⠦⡀⠀⠀⠀⢸⠃⢀⡴⠳⢦⡀⢠⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣯⣉⠙⠒⠲⠦⢤⡀⠀⢱⠸⣇⢀⡼⠁⢀⣠⡤⠴⠒⠒⠒⠋⠉⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
      ⠀⢸⠁⠀⠀⠀⢸⡾⠛⠀⠀⠈⢻⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⡏⠉⠉⠓⠲⣄⠻⡄⠘⡆⣸⠟⢀⣠⡤⠴⠒⠒⠒⠋⠉⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
      ⠀⢨⠀⠀⠀⠀⣸⠇⠀⠀⠀⣼⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⠀⠀⠀⠀⠈⣷⠹⣆⡼⠁⣠⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
      ⠀⢸⡄⢀⣠⡾⠁⠀⠀⠀⣰⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡞⠀⠀⠀⠀⠀⠀⢀⡿⠁⡼⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
      ⠀⢸⡟⠉⠉⠀⠀⠀⠀⣠⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣠⣤⠤⠤⠤⠴⢧⡀⠀⠀⠀⠀⠀⡼⠁⡼⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
      ⠰⠏⠀⠀⠀⠀⠀⠀⣰⠏⠀⠀⠀⠀⠀⣀⣤⠤⠖⠚⠉⠉⠀⠀⠀⠀⠀⠀⠀⠙⣦⡀⠀⠀⢠⡇⣸⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                ⠀⠀⠀⣴⠃⠀⢀⣠⠴⠞⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢳⡄⣀⣼⣶⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                ⢀⣾⡥⠖⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⢚⣯⠷⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                ⣀⣀⣴⡛⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡴⣿⡟⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        """
        print(ascii_dio)
        print("\n[PAUSE] ZA WARUDO !!!!  ")
    else:
        try:
            pygame.mixer.music.load("start.mp3")
            pygame.mixer.music.play()
        except:
            pass
        print("\n[LECTURE] Le temps reprend son cours.")

def horloge():
    global alarme_declenchee

    # Activation du contrôle clavier (Espace)
    keyboard.on_press_key("space", gerer_pause)

    try:
        print("--- HORLOGE DIGITALE ---")
        print("Commandes : [Espace] pour Pause/Lecture | [Ctrl+C] pour Quitter")
        
        while True:
            if not en_pause:
                h = int(strftime("%H"))
                m = int(strftime("%M"))
                s = int(strftime("%S"))

                # Comparaison de l'heure actuelle avec l'alarme configurée
                if heure_alarme and (h, m, s) == heure_alarme and not alarme_declenchee:
                    alarme_declenchee = True
                    print(f"\n[ALARME] Debout L'ancienne ! Il est {h:02d}:{m:02d}:{s:02d}")
                    
                    try:
                        pygame.mixer.music.load("alarme.mp3")
                        pygame.mixer.music.play()
                    except:
                        print("[ERREUR] Impossible de lire le fichier mp3 :/")

                # Mise en forme de l'heure uniquement
                current_time_format = "%H:%M:%S" if is_24_hour_format else "%I:%M:%S %p"
                current_time = strftime(current_time_format)
                
                print(f"Heure: {current_time}", end="\r")
            
            time_library.sleep(1)
            
    except KeyboardInterrupt:
        print("\nHorloge arrêtée avec succès.")

# LANCEMENT ET CONFIGURATION
print("--- CONFIGURATION DE L'HORLOGE ---")

format_choisi = input("Format d'affichage (12h ou 24h) : ").strip().lower()
choisir_mode_affichage(format_choisi)

print("\nRéglage de l'alarme :")
h_alarme = int(input("Heure (0-23) : "))
m_alarme = int(input("Minutes (0-59) : "))
s_alarme = int(input("Secondes (0-59) : "))

regler_alarme((h_alarme, m_alarme, s_alarme))

print("\nLancement de l'horloge...")
horloge()