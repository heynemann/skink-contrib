#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Licensed under the Open Software License ("OSL") v. 3.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.opensource.org/licenses/osl-3.0.php

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
from os.path import dirname, abspath, join
root_path = abspath(join(dirname(__file__), "../"))
sys.path.insert(0, root_path)
import time

import pygame
from pygame.locals import *

RESOLUTION_VERTICAL=400
RESOLUTION_HORIZONTAL=400
FULL_SCREEN_MODE = False
DEBUG_MODE = False

RED_BG = (227,52,52)
GREEN_BG = (11,143,1)
YELLOW_BG = (255, 248, 135)

BLACK_TEXT = (0,0,0)
WHITE_TEXT = (255,255,255)

class Game(object):

    def __init__(self):
        self.initialize()
        self.resources = Resources()
        self.resources.preload()

    def log(self, message):
        if DEBUG_MODE:
            print message

    def initialize(self):
        pygame.init()

    def show(self):
        if FULL_SCREEN_MODE:
            self.window = pygame.display.set_mode((RESOLUTION_VERTICAL,RESOLUTION_HORIZONTAL), pygame.FULLSCREEN)
        else:
            self.window = pygame.display.set_mode((RESOLUTION_VERTICAL,RESOLUTION_HORIZONTAL))
        pygame.display.set_caption('Skink Alert')
        self.screen = pygame.display.get_surface()
        self.display_message("Retrieving...", YELLOW_BG, BLACK_TEXT)

    def loop(self):
        event_handler = EventHandler(self)
        while True:
            try:
                return_value = event_handler.process_events(pygame.event.get())
                if not return_value:
                    continue
                if return_value == "QUIT":
                    print "Exiting due to exit signal..."
                    return 0
                else:
                    self.log(return_value)
            except KeyboardInterrupt:
                print "Exiting due to exit signal..."
                return 0

    def display_message(self, message, rgb = GREEN_BG, text_color=WHITE_TEXT):
        self.resources.print_bg(rgb, self.screen)
        self.resources.print_message(message, text_color, self.screen)
        self.resources.print_logo_image(self.screen)
        pygame.display.update()

class EventHandler(object):
    def __init__(self, game):
        self.game = game

    def process_events(self, events):
        if not events: return None

        for event in events:
            if self.check_for_quit(event):
                return "QUIT"
            if self.check_for_sound(event):
                self.resources.play_broken_build_sound()
            if event.type == KEYDOWN:
                if event.unicode == 'r':
                    self.game.display_message("FAIL", RED_BG)
                if event.unicode == 'g':
                    self.game.display_message("SUCCESS", GREEN_BG)
            return event

    def check_for_quit(self, event):
        if event.type == QUIT:
            return True
        elif event.type == KEYDOWN:
            if event.unicode == 'q':
                return True
        return False

    def check_for_sound(self, event):
        if event.type == KEYDOWN:
            if event.unicode == 's':
                return True
        return False

class Resources(object):
    def preload(self):
        self.load_broken_build_sound()
        self.load_logo_image()

    def play_broken_build_sound(self):
        sound = self.load_broken_build_sound()
        sound.play()

    def load_broken_build_sound(self):
        class NoneSound:
            def play(self): pass

        if not pygame.mixer:
            return NoneSound()
        fullname = join(root_path, "skink-alert", "brain.wav")
        try:
            sound = pygame.mixer.Sound(fullname)
        except pygame.error, message:
            print "Cannot load sound:", fullname
            raise SystemExit, message
        return sound

    def load_logo_image(self):
        logo_surface_path = join(root_path, "skink-alert", "logo.bmp")
        self.logo_surface = pygame.image.load(logo_surface_path)

    def print_logo_image(self, screen):
        logo_position = self.logo_surface.get_rect()
        logo_width = logo_position.width
        logo_height = logo_position.height

        display_info = pygame.display.Info()
        screen_width = display_info.current_w
        screen_height = display_info.current_h

        pos_x = (screen_width / 2) - logo_width/2
        screen.blit(self.logo_surface, (pos_x,0))
        pygame.display.update()

    def print_message(self, message, text_color, screen):
        if pygame.font:
            font = pygame.font.Font(None, 72)
            text = font.render(message, 1, text_color)
            text_position = text.get_rect()
            text_width = text_position.width
            text_height = text_position.height

            display_info = pygame.display.Info()
            screen_width = display_info.current_w
            screen_height = display_info.current_h

            pos_x = (screen_width / 2) - text_width/2
            pos_y = (screen_height / 2) - text_height/2
            screen.blit(text, (pos_x,pos_y))

    def print_bg(self, rgb, screen):
        background = pygame.Surface(screen.get_size())
        background = background.convert()
        background.fill(rgb)
        screen.blit(background, (0,0))
