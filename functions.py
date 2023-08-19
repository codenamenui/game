import pygame, os

game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "assets")

def font(size):
    return pygame.font.Font(os.path.join(img_folder, "font.ttf"), size)

def path(path):
    file_path = img_folder
    for f in path.split("/"):
        file_path = os.path.join(file_path, f)
    return file_path

