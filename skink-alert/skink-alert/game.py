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
import random
from threading import Thread
import httplib

import simplejson

import pygame
from pygame.locals import *
from text_rect import *
from context import AlertContext

LOGO_HEIGHT = 136
MESSAGE_OFFSET_VERT = 60

class Game(object):

    def __init__(self):
        self.initialize()
        self.ctx = AlertContext.current()
        self.resources = Resources()
        self.resources.preload()
        self.is_failing = False

    def log(self, message):
        if self.ctx.debug_mode:
            print message

    def initialize(self):
        pygame.init()

    def show(self):
        if self.ctx.debug_mode:
            vert_res=400
            horiz_res=800
            full_screen = False
        else:
            vert_res = self.ctx.height
            horiz_res = self.ctx.width
            full_screen = self.ctx.full_screen

        if full_screen:
            self.window = pygame.display.set_mode((horiz_res, vert_res), pygame.FULLSCREEN)
        else:
            self.window = pygame.display.set_mode((horiz_res, vert_res))
            
        pygame.display.set_caption('Skink Alert')
        self.screen = pygame.display.get_surface()
        self.display_message("Retrieving...", self.ctx.unknown_bg, self.ctx.unknown_font)

    def loop(self):
        event_handler = EventHandler(self)
        while True:
            try:
                Monitor.get_last_status(self.process_response)
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

    def process_response(self, response_object):
        errors = []
        error_number = 0
        for project in response_object["projects"]:
            if project["lastBuild"]:
                build = project["lastBuild"]
                if build["status"] != "SUCCESS":
                    error_number += 1
                    errors.append("FAILURE #%d\n    Project:%s\n    Committer:%s\nDate: %s\n\n" % (error_number, project["name"], build["commitCommitter"], build["commitCommitterDate"]))

        if not errors:
            self.display_message("ALL BUILDS GREEN", self.ctx.success_bg, self.ctx.success_font)
            self.is_failing = False
        else:
            self.display_message("BUILD FAILING:\n%s" % "\n".join(errors), self.ctx.broken_bg, self.ctx.broken_font)
            if not self.is_failing:
                self.resources.play_broken_build_sound()
                self.is_failing = True

    def display_message(self, message, rgb, text_color):
        self.resources.print_bg(rgb, self.screen)
        self.resources.print_message(message, text_color, rgb, self.screen)
        self.resources.print_logo_image(self.screen)
        self.resources.print_exit_message(text_color, rgb, self.screen)
        pygame.display.flip()

class EventHandler(object):
    def __init__(self, game):
        self.game = game
        self.ctx = AlertContext.current()

    def process_events(self, events):
        #no events raised.
        if not events: return None

        for event in events:
            if self.check_for_quit(event):
                return "QUIT"
            if self.ctx.debug_mode and event.type == KEYDOWN:
                if event.unicode == 's':
                    self.resources.play_broken_build_sound()
            return event

    def check_for_quit(self, event):
        if event.type == QUIT:
            return True
        elif event.type == KEYDOWN:
            if event.unicode == self.ctx.exit_key:
                return True
        return False

class Resources(object):
    def __init__(self):
        self.ctx = AlertContext.current()

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

        fullname = self.ctx.path_for_audio_file(self.ctx.audio_broken)
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
        pygame.display.flip()

    def print_message(self, message, text_color, background_color, screen):
        if pygame.font:
            font = pygame.font.Font(None, self.ctx.font_size)
            display_info = pygame.display.Info()
            screen_width = display_info.current_w
            screen_height = display_info.current_h
            rect = pygame.Rect((0, LOGO_HEIGHT + MESSAGE_OFFSET_VERT, screen_width, screen_height - LOGO_HEIGHT - MESSAGE_OFFSET_VERT))
            rendered_text = render_textrect(message, font, rect, text_color, background_color, 1)
            if rendered_text:
                screen.blit(rendered_text, rect.topleft)

    def print_bg(self, rgb, screen):
        background = pygame.Surface(screen.get_size())
        background = background.convert()
        background.fill(rgb)
        screen.blit(background, (0,0))

    def print_exit_message(self, text_color, background_color, screen):
        font = pygame.font.Font(None, self.ctx.font_size)
        display_info = pygame.display.Info()
        screen_width = display_info.current_w
        screen_height = display_info.current_h
        rect = pygame.Rect((0, screen_height - 30, screen_width, 30))
        rendered_text = render_textrect("Press %s to QUIT" % self.ctx.exit_key, font, rect, text_color, background_color, 1)
        if rendered_text:
            screen.blit(rendered_text, rect.topleft)

class Monitor(object):
    is_retrieving = False

    @classmethod
    def get_last_status(cls, callback):
        ctx = AlertContext.current()
        if cls.is_retrieving: return
        cls.is_retrieving = False
        cls.callback = callback
        thread = Thread(target = cls.connect_and_retrieve_status)
        thread.start()

    @classmethod
    def connect_and_retrieve_status(cls):
        ctx = AlertContext.current()
        try:
            cls.is_retrieving = True
            time.sleep(3)
            conn = httplib.HTTPConnection(ctx.skink_address)
            url = "/status?_=%d" % (random.random() * 1000)
            conn.request("GET", url)
            r1 = conn.getresponse()
            json = r1.read()
        except Exception, message:
            #intentionally swallow since it does not matter why the connection was refused.
            cls.is_retrieving = False
            return

        json = json.replace("'","\"")
        json_object = simplejson.loads(json)
        if cls.callback:
            cls.callback(json_object)

        cls.is_retrieving = False
