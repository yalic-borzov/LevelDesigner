import os

import pygame

from app.LevelEditor.LevelEditor import LevelEditor

pygame.init()
main_clock = pygame.time.Clock()
screen_height = 640
screen_width = 800
screen = pygame.display.set_mode((screen_width + 300, screen_height + 100))
level = 1
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = f"{BASE_DIR}/data/"

sky_box = pygame.image.load(f"data/img/sky-box-{level}.png").convert_alpha()
layer_1 = pygame.image.load(f"data/img/layer1-{level}.png").convert_alpha()
layer_2 = pygame.image.load(f"data/img/layer2-{level}.png").convert_alpha()
layer_3 = pygame.image.load(f"data/img/layer3-{level}.png").convert_alpha()
if __name__ == "__main__":
    editor = LevelEditor(
        data_dir=DATA_DIR,
        screen=screen,
        screen_width=screen_width,
        screen_height=screen_height,
    )
    editor.tile_add()
    editor.sync()
    editor.load_buttons()
    running = True
    while running:
        main_clock.tick(60)
        editor.draw_background(sky_box, layer_1, layer_2, layer_3)
        editor.draw_grid()
        editor.draw_world()
        editor.panel_draw()
        editor.tile_buttons_sync()
        editor.scroll()
        pos = pygame.mouse.get_pos()
        editor.pos_scroll(pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    editor.scroll_left = True
                if event.key == pygame.K_RIGHT:
                    editor.scroll_right = True
                if event.key == pygame.K_RSHIFT:
                    editor.scroll_speed = 5
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    editor.scroll_left = False
                if event.key == pygame.K_RIGHT:
                    editor.scroll_right = False
                if event.key == pygame.K_RSHIFT:
                    editor.scroll_speed = 1

        pygame.display.update()

    pygame.quit()
