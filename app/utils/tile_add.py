import os

import pygame.image


def tile_add(folder: str, tile_list: list, tile_size: int):
    for i in os.listdir(folder):
        if os.path.isfile(os.path.join(folder, i)):
            img = pygame.image.load(f"{folder}/{i}").convert_alpha()
            img = pygame.transform.scale(img, (tile_size, tile_size))
            tile_list.append(img)

    return tile_list
