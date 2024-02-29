import csv
import os

import pygame
from pygame import Surface

from app.elements.Button import Button


class LevelEditor:
    def __init__(self, data_dir: str, screen: Surface, screen_width, screen_height):
        self.scroll_speed = 1
        self.LOWER_MARGIN = 100
        self.SIDE_MARGIN = 300
        self.SCREEN_WIDTH = screen_width
        self.SCREEN_HEIGHT = screen_height
        self.data_dir = data_dir
        self.tile_folder = data_dir + "tiles"
        self.tile_list = []
        self.ROWS = 16
        self._scroll = 0
        self.current_tile = 0
        self.TILE_SIZE = self.SCREEN_HEIGHT // self.ROWS
        self.MAX_COLS = 150
        self.screen = screen
        self.MAIN_COLOR = "#c27360"
        self.world_data = []
        self.buttons = []
        self.scroll_left = False
        self.scroll_right = False

    def tile_add(self):
        for i in os.listdir(self.tile_folder):
            if os.path.isfile(os.path.join(self.tile_folder, i)):
                img = pygame.image.load(f"{self.tile_folder}/{i}").convert_alpha()
                img = pygame.transform.scale(img, (self.TILE_SIZE, self.TILE_SIZE))
                self.tile_list.append(img)

        return self.tile_list

    def draw_background(self, sky_box, layer_1, layer_2, layer_3):
        self.screen.fill(self.MAIN_COLOR)
        width = sky_box.get_width()
        for x in range(4):
            self.screen.blit(sky_box, ((x * width) - self._scroll * 0.5, 0))
            self.screen.blit(
                layer_3,
                (
                    (x * width) - self._scroll * 0.6,
                    self.SCREEN_HEIGHT - layer_3.get_height() - 300,
                ),
            )
            self.screen.blit(
                layer_1,
                (
                    (x * width) - self._scroll * 0.7,
                    self.SCREEN_HEIGHT - layer_1.get_height() - 150,
                ),
            )
            self.screen.blit(
                layer_2,
                (
                    (x * width) - self._scroll * 0.8,
                    self.SCREEN_HEIGHT - layer_2.get_height(),
                ),
            )

    def draw_grid(self):
        for c in range(self.MAX_COLS + 1):
            pygame.draw.line(
                self.screen,
                (255, 255, 255),
                (c * self.TILE_SIZE - self._scroll, 0),
                (c * self.TILE_SIZE - self._scroll, self.SCREEN_HEIGHT),
            )
        for c in range(self.ROWS + 1):
            pygame.draw.line(
                self.screen,
                (255, 255, 255),
                (0, c * self.TILE_SIZE),
                (self.SCREEN_WIDTH, c * self.TILE_SIZE),
            )

    def draw_world(self):
        for y, row in enumerate(self.world_data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    self.screen.blit(
                        self.tile_list[tile],
                        (x * self.TILE_SIZE - self._scroll, y * self.TILE_SIZE),
                    )

    def sync(self):
        for row in range(self.ROWS):
            r = [-1] * self.MAX_COLS
            self.world_data.append(r)

        for tile in range(0, self.MAX_COLS):
            self.world_data[self.ROWS - 1][tile] = 0

    def draw_text(self, text: str, font: pygame.font, text_col, x, y):
        img = font.render(text, True, text_col)
        self.screen.blit(img, x, y)

    def load_buttons(self):
        self.load_button_icon = pygame.image.load(f"{self.data_dir}img/load_button.png")
        self.save_button_icon = pygame.image.load(f"{self.data_dir}img/save_button.png")
        self.button_col = 0
        self.button_row = 0

        for i in range(len(self.tile_list)):
            asset_button = Button(
                self.SCREEN_WIDTH + (75 * self.button_col) + 50,
                75 * self.button_row + 50,
                self.tile_list[i],
                1,
            )
            self.buttons.append(asset_button)
            self.button_col += 1
            if self.button_col == 3:
                self.button_row += 1
                self.button_col = 0

    def tile_buttons_sync(self):
        for button_count, i in enumerate(self.buttons):
            if i.draw(self.screen):
                self.current_tile = button_count

        pygame.draw.rect(
            self.screen, "#6e34eb", self.buttons[self.current_tile].rect, 3
        )

        save_button = Button(
            self.SCREEN_WIDTH // 2,
            self.SCREEN_HEIGHT + self.LOWER_MARGIN - 50,
            self.save_button_icon,
            1,
        )
        load_button = Button(
            self.SCREEN_WIDTH // 2 + 200,
            self.SCREEN_HEIGHT + self.LOWER_MARGIN - 50,
            self.load_button_icon,
            1,
        )

        if load_button.draw(self.screen):
            self._scroll = 0
            with open("level_data.csv", newline="") as csvfile:
                reader = csv.reader(csvfile, delimiter=",")
                for x, row in enumerate(reader):
                    for y, tile in enumerate(row):
                        self.world_data[x][y] = int(tile)
        if save_button.draw(self.screen):

            with open("level_data.csv", "w", newline="") as csvfile:
                writer = csv.writer(csvfile, delimiter=",")
                for row in self.world_data:
                    writer.writerow(row)

    def panel_draw(self):
        pygame.draw.rect(
            self.screen,
            self.MAIN_COLOR,
            (self.SCREEN_WIDTH, 0, self.SIDE_MARGIN, self.SCREEN_HEIGHT),
        )

    def get_buttons(self):
        return self.buttons

    def scroll(self):
        if self.scroll_left and self._scroll > 0:
            self._scroll -= 5 * self.scroll_speed
        if (
            self.scroll_right
            and self._scroll < (self.MAX_COLS * self.TILE_SIZE) - self.SCREEN_WIDTH
        ):
            self._scroll += 5 * self.scroll_speed

    def get_scroll(self):
        return self._scroll

    def pos_scroll(self, pos):
        x = (pos[0] + self._scroll) // self.TILE_SIZE
        y = pos[1] // self.TILE_SIZE

        if pos[0] < self.SCREEN_WIDTH and pos[1] < self.SCREEN_HEIGHT:
            if pygame.mouse.get_pressed()[0] == 1:
                if self.world_data[y][x] != self.current_tile:
                    self.world_data[y][x] = self.current_tile
            if pygame.mouse.get_pressed()[2] == 1:
                self.world_data[y][x] = -1
