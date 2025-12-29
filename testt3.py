

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
    # .convert('1') garantit que l'image est en Noir et Blanc pur pour l'e-paper
    image_path = os.path.join(picdir, 'frame1.bmp')
    image = Image.open(image_path).convert('1')
    draw = ImageDraw.Draw(image)
    
    draw.text((1, 1), "Gardevoir", font=font15, fill=0)
   

    # 3. Affichage
    logging.info("Affichage de l'image...")
    epd.display(epd.getbuffer(image))
    
    # 4. Mise en veille (crucial pour la durée de vie de l'écran)
    epd.sleep()
    logging.info("Terminé.")

except Exception as e:
    logging.error(f"Erreur : {e}")

except KeyboardInterrupt:
    logging.info("Arrêt du script.")
    sys.exit()