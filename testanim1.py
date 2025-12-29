
import time
import sys
import os
import logging
from PIL import Image, ImageDraw, ImageFont

# Configuration des chemins pour trouver les librairies Waveshare
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')

if os.path.exists(libdir):
    sys.path.append(libdir)

from waveshare_epd import epd2in13_V4

# Configuration minimale des logs pour voir si ça avance
logging.basicConfig(level=logging.INFO)



try:
    font15 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 15)
    # 1. Préparation de l'écran
    epd = epd2in13_V4.EPD()
    epd.init()
    epd.Clear(0xFF) # Efface l'écran (blanc)

    # 2. Préparation de l'image
    images = []
    for i in range(1, 3):  # Va de 1 à 4
            nom_fichier = f'frame{i}.bmp'
            chemin = os.path.join(picdir, nom_fichier)
            logging.info(f"Chargement de {nom_fichier}...")
       
            img = Image.open(chemin).convert('1')
            images.append(img)
    
    while True:
        

        for i in len(images):
        
            img = images[i]
            draw = ImageDraw.Draw(img)
            draw.text((1, 1), "Gardevoir", font=font15, fill=0)
            
            epd.displayPartial(epd.getbuffer(img)) 
    
            time.sleep(3)
   




# 3. Affichage
  
   
    # 4. Mise en veille (crucial pour la durée de vie de l'écran)
    epd.sleep()
    logging.info("Terminé.")

except Exception as e:
    logging.error(f"Erreur : {e}")

except KeyboardInterrupt:
    logging.info("Arrêt du script.")
    sys.exit()