from PIL import Image, ImageDraw, ImageFont
import numpy as np
from tqdm import tqdm
import json


def generate_spotlight(dimensions, center, radius, color):
    img = Image.new('RGB', dimensions, color=(0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    for x in tqdm(range(dimensions[0]), desc='Generating spotlight', position=0, leave=True):
        for y in range(dimensions[1]):
            # Dimension from center
            dist = np.sqrt((center[0] - x) ** 2 + (center[1] - y) ** 2)
            if dist < radius:
                # Calculate intensity based on distance to center
                intensity = 1 - (dist / radius)
                # Calculate new color based on intensity
                new_color = tuple(
                    int(c * intensity + img.getpixel((x, y))[i] * (1 - intensity)) for i, c in enumerate(color))
                draw.point((x, y), fill=new_color)
    return img


def generate_thumbnail(teams: list):
    dimensions = (480, 320)
    background_color = (0, 0, 0)
    teams_dic = json.load(open('./src/assets/teams.json'))
    
    for i, team in enumerate(teams):
            if team not in teams_dic:
                print(f"Team {team} not found in teams.json, using default team")
                teams[i] = "default"
    print(teams)
    
    img = Image.new('RGB', dimensions, color=background_color)
    
    # Team colors
    color1 = teams_dic[teams[0]]['color']
    color2 = teams_dic[teams[1]]['color']
    
    # Generate spotlights
    spotlight1 = generate_spotlight(dimensions, (dimensions[0] * 0.1, dimensions[1]), dimensions[0] * 0.5, color1)
    spotlight2 = generate_spotlight(dimensions, (dimensions[0] * 0.9, dimensions[1]), dimensions[0] * 0.5, color2)
    
    # Blend spotlights with background
    img = Image.blend(img, spotlight1, alpha=0.5)
    img = Image.blend(img, spotlight2, alpha=0.5)

    # Loading team cards
    team1_card = Image.open(teams_dic[teams[0]]['card'])
    team2_card = Image.open(teams_dic[teams[1]]['card'])
    
    # Card resizing to fit dimensions
    new_size = (int(dimensions[0] * 0.25), int(team1_card.height * (dimensions[0] * 0.25) / team1_card.width))
    team1_card = team1_card.resize(new_size)
    team2_card = team2_card.resize(new_size)
    
    # Card positioning
    vertical_center = (dimensions[1] - team1_card.height) // 2
    position_1 = (int(dimensions[0] * 0.2 - team1_card.width / 2), vertical_center+10)
    position_2 = (int(dimensions[0] * 0.8 - team2_card.width / 2), vertical_center+10)
    
    img.paste(team1_card, position_1, team1_card)
    img.paste(team2_card, position_2, team2_card)
    
    # Overlay 
    overlay = Image.open('./src/assets/overlay.png')
    overlay = overlay.resize(dimensions)
    img.paste(overlay, (0, 0), overlay)
    
    draw = ImageDraw.Draw(img)
    font_size = dimensions[1] // 15
    font = ImageFont.truetype('./src/assets/Valorant.ttf', font_size)
    match_time = '17:00 UTC'
    
    # Calculate text position to be at the bottom center
    text_bbox = font.getbbox(match_time)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    text_x_position = (dimensions[0] - text_width) // 2
    text_y_position = dimensions[1] - text_height - dimensions[1] // 30
    
    draw.text((text_x_position, text_y_position), match_time, font=font, fill=(255, 255, 255))
        
    return img