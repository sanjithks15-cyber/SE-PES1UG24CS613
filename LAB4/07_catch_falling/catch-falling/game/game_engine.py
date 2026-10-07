"""
GameEngine: owns the basket and all falling objects.

Starter version: basket movement and spawning both work at a basic
level (Tasks 2 and 3 ask you to improve them), there's no speed boost
yet (Task 4 builds it from scratch), and catch detection has two
known bugs (see game/collision.py and the catch-checking loop below)
that Task 1 asks you to fix.
"""

import random
import pygame

from game.basket import Basket
from game.falling_object import FallingObject
from game.collision import is_caught
from game.renderer import WIDTH, HEIGHT

MIN_SPAWN_INTERVAL_FRAMES = 30
MAX_SPAWN_INTERVAL_FRAMES = 70
MAX_OBJECTS = 5
MIN_SPAWN_DISTANCE = 80
MAX_MISSES = 5


class GameEngine:
    def __init__(self):
        self.basket = Basket(x=WIDTH / 2, y=HEIGHT - 30)
        self.objects = []
        self.frames_until_spawn = 0
        self.score = 0
        self.misses = 0
        self.game_over = False

    def _spawn_object(self):
        radius = 14
        min_x = radius
        max_x = WIDTH - radius

        if self.objects:
            previous_x = self.objects[-1].x
            valid_positions = [
                x for x in range(min_x, max_x + 1)
                if abs(x - previous_x) >= MIN_SPAWN_DISTANCE
            ]
            if not valid_positions:
                return
            x = random.choice(valid_positions)
        else:
            x = random.randint(min_x, max_x)

        self.objects.append(FallingObject(x=x, y=-radius, speed=3))

    def handle_input(self, keys_pressed):
        if self.game_over:
            return
        if keys_pressed[pygame.K_LEFT]:
            self.basket.x -= self.basket.speed
        if keys_pressed[pygame.K_RIGHT]:
            self.basket.x += self.basket.speed
        half_width = self.basket.width / 2
        self.basket.x = max(
            half_width,
            min(WIDTH - half_width, self.basket.x)
        )

    def handle_keydown(self, key):
        if self.game_over and key == pygame.K_r:
            self.__init__()
            return

        if key == pygame.K_SPACE:
            self.basket.activate_boost()

    def update(self):
        if self.game_over:
            return

        self.basket.update()

        self.frames_until_spawn -= 1
        if self.frames_until_spawn <= 0:
            if len(self.objects) < MAX_OBJECTS:
                self._spawn_object()
            self.frames_until_spawn = random.randint(
                MIN_SPAWN_INTERVAL_FRAMES,
                MAX_SPAWN_INTERVAL_FRAMES,
            )

        for obj in self.objects:
            obj.update()

        basket_rect = self.basket.get_rect()
        remaining = []
        for obj in self.objects:
            if is_caught(basket_rect, obj):
                self.score += 1
            else:
                remaining.append(obj)
        self.objects = remaining

        missed = [o for o in self.objects if o.is_past_bottom(HEIGHT)]
        if missed:
            self.objects = [o for o in self.objects if not o.is_past_bottom(HEIGHT)]
            self.misses += len(missed)
            if self.misses >= MAX_MISSES:
                self.game_over = True

    def draw(self, surface, font):
        from game import renderer
        renderer.draw_scene(surface, self.basket, self.objects)
        renderer.draw_text(surface, font, f"Score: {self.score}", (10, 10))
        renderer.draw_text(surface, font, f"Misses: {self.misses}/{MAX_MISSES}", (10, 36))

        if self.basket.boosted_frames > 0:
            boost_seconds = (self.basket.boosted_frames + 59) // 60
            renderer.draw_text(
                surface,
                font,
                f"BOOST: {boost_seconds}s",
                (10, 62),
            )

        if self.game_over:
            renderer.draw_banner(surface, font, f"Game Over! Final score: {self.score}. Press R to restart.")
