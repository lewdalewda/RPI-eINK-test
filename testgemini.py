#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
import logging
import time
import traceback
from PIL import Image, ImageDraw, ImageFont

# --- Configuration des chemins (identique à votre fichier original) ---
# Cela permet de trouver les librairies 'lib' et 'pic' même après avoir déplacé le script
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

from waveshare_epd import epd2in13_V4

logging.basicConfig(level=logging.DEBUG)

try:
    logging.info("Demo Formes Geometriques")
    
    # Initialisation de l'écran
    epd = epd2in13_V4.EPD()
    logging.info("Initialisation et nettoyage...")
    epd.init()
    epd.Clear(0xFF) # 0xFF = Blanc

    if 1:
        # Création de l'image vide (blanche)
        # Note : On inverse height et width pour dessiner en mode paysage
        image = Image.new('1', (epd.height, epd.width), 255) 
        draw = ImageDraw.Draw(image)

        logging.info("Dessin des formes...")

        # --- DESSIN DES FORMES ---
        # Syntaxe : draw.rectangle((x1, y1, x2, y2), outline=0)
        # 0 = Noir, 255 = Blanc
        # x1, y1 = Coin haut gauche
        # x2, y2 = Coin bas droit

        # 1. Le Rectangle (x=10 à x=70)
        draw.rectangle((10, 30, 70, 80), outline=0)
        
        # 2. Le Carré (x=90 à x=140 -> 50x50 pixels)
        draw.rectangle((90, 30, 140, 80), outline=0)

        # 3. Le Rond (x=160 à x=210)
        # Pour faire un rond parfait, la zone (bounding box) doit être un carré
        draw.ellipse((160, 30, 210, 80), outline=0)

        # (Optionnel) Ajout de texte pour légender
        # On utilise une police par défaut si Font.ttc n'est pas trouvé, sinon celle du dossier pic
        try:
            font15 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 15)
        except:
            font15 = ImageFont.load_default()
            
        draw.text((10, 90), 'Rect', font=font15, fill=0)
        draw.text((90, 90), 'Carre', font=font15, fill=0)
        draw.text((160, 90), 'Rond', font=font15, fill=0)

        # Rotation si nécessaire (décommenter si l'écran est à l'envers)
        # image = image.rotate(180) 

        # Envoi de l'image vers l'écran
        epd.display(epd.getbuffer(image))
        
        # Pause pour laisser le temps de voir (et éviter un refresh trop rapide qui abîme l'écran)
        time.sleep(5)
        
        # Mise en veille de l'écran (important pour la durée de vie)
        logging.info("Mise en veille...")
        epd.Sleep()

except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd2in13_V4.epdconfig.module_exit(cleanup=True)
    exit()