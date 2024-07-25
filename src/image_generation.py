from PIL import Image, ImageDraw, ImageFont
import numpy as np
from tqdm import tqdm
import json

def generate_spotlight(dimensions, center, radius, color):
    img = Image.new('RGB', dimensions, color=(0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    for x in range(dimensions[0]):
        for y in range(dimensions[1]):
            # Calculate distance to the spotlight center
            dist = np.sqrt((center[0] - x) ** 2 + (center[1] - y) ** 2)
            if dist < radius:
                # Calculate intensity based on distance to center
                intensity = 1 - (dist / radius)
                # Calculate new color based on intensity
                new_color = tuple(int(c * intensity + img.getpixel((x, y))[i] * (1 - intensity)) for i, c in enumerate(color)) 
                draw.point((x, y), fill=new_color)
    return img

def generate_thumbnail():
    dimensions = (480, 320)
    background_color = (0, 0, 0)
    teams = json.load(open('src/assets/teams.json'))
    
    img = Image.new('RGB', dimensions, color=background_color)
    
    # Team colors
    color1 = teams[0]['color']
    color2 = teams[1]['color']
    
    # Generate spotlights
    spotlight1 = generate_spotlight(dimensions, (dimensions[0] * 0.1, dimensions[1]), dimensions[0] * 0.5, color1)
    spotlight2 = generate_spotlight(dimensions, (dimensions[0] * 0.9, dimensions[1]), dimensions[0] * 0.5, color2)
    
    # Blend spotlights with background
    img = Image.blend(img, spotlight1, alpha=0.5)
    img = Image.blend(img, spotlight2, alpha=0.5)
    
    
    # Cartes d'équipes
    team1_card = Image.open(teams[0]['card'])
    team2_card = Image.open(teams[1]['card'])
    
    # Redimensionnement des cartes d'équipes
    new_size = (int(dimensions[0] * 0.25), int(team1_card.height * (dimensions[0] * 0.25) / team1_card.width))
    team1_card = team1_card.resize(new_size)
    team2_card = team2_card.resize(new_size)
    
    # Positionnement des cartes d'équipes
    vertical_center = (dimensions[1] - team1_card.height) // 2
    position_1 = (int(dimensions[0] * 0.2 - team1_card.width / 2), vertical_center)
    position_2 = (int(dimensions[0] * 0.8 - team2_card.width / 2), vertical_center)
    
    img.paste(team1_card, position_1)
    img.paste(team2_card, position_2)
    
    # Overlay 
    overlay = Image.open('src/assets/overlay.png')
    img.paste(overlay, (0, 0), overlay)
    
    img.show()  # Or save the image using img.save('path_to_save.jpg')

generate_thumbnail()