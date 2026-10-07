"""
renderer: all pygame drawing lives here, kept separate from game logic.
"""

import pygame

WIDTH, HEIGHT = 700, 500
WINDOW_SIZE = (WIDTH, HEIGHT)

COLOR_BG = (25, 30, 45)
COLOR_BASKET = (150, 110, 70)
COLOR_BASKET_BOOST = (255, 215, 60)
COLOR_TEXT = (255, 255, 255)


def draw_scene(surface, basket, objects):
    surface.fill(COLOR_BG)
    for obj in objects:
        pygame.draw.circle(surface, obj.color, (int(obj.x), int(obj.y)), obj.radius)
    basket_color = COLOR_BASKET_BOOST if basket.boosted_frames > 0 else COLOR_BASKET
    pygame.draw.rect(surface, basket_color, basket.get_rect(), border_radius=6)


def draw_text(surface, font, text, pos, color=COLOR_TEXT):
    surface.blit(font.render(text, True, color), pos)


def draw_banner(surface, font, text):
    surf = font.render(text, True, (255, 220, 80))
    rect = surf.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2))
    surface.blit(surf, rect)
