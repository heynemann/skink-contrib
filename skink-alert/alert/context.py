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
from ConfigParser import ConfigParser
from os.path import dirname, abspath, join
root_path = abspath(join(dirname(__file__), "../"))
sys.path.insert(0, root_path)

class AlertContext:
    instance = None
    @classmethod
    def current(cls):
        if not cls.instance:
            cls.instance = cls()
            config = ConfigParser()
            config.read(join(root_path, "config.ini"))

            #General
            cls.instance.debug_mode = config.get("General", "debug_mode").lower() == "true"
            cls.instance.full_screen = config.get("General", "full_screen").lower() == "true"
            cls.instance.width = int(config.get("General", "width"))
            cls.instance.height = int(config.get("General", "height"))
            cls.exit_key = config.get("General","exit_key")

            #Skink Server
            cls.instance.skink_address = config.get("SkinkServer","skink_address")

            #Layout
            cls.instance.font_size = int(config.get("Layout","font_size"))

            unknown_bg_red = int(config.get("Layout","unknown_bg_red"))
            unknown_bg_green = int(config.get("Layout","unknown_bg_green"))
            unknown_bg_blue = int(config.get("Layout","unknown_bg_blue"))
            unknown_font_red = int(config.get("Layout","unknown_font_red"))
            unknown_font_green = int(config.get("Layout","unknown_font_green"))
            unknown_font_blue = int(config.get("Layout","unknown_font_blue"))
            cls.instance.unknown_bg = (unknown_bg_red, unknown_bg_green, unknown_bg_blue)
            cls.instance.unknown_font = (unknown_font_red, unknown_font_green, unknown_font_blue)

            broken_bg_red = int(config.get("Layout","broken_bg_red"))
            broken_bg_green = int(config.get("Layout","broken_bg_green"))
            broken_bg_blue = int(config.get("Layout","broken_bg_blue"))
            broken_font_red = int(config.get("Layout","broken_font_red"))
            broken_font_green = int(config.get("Layout","broken_font_green"))
            broken_font_blue = int(config.get("Layout","broken_font_blue"))
            cls.instance.broken_bg = (broken_bg_red, broken_bg_green, broken_bg_blue)
            cls.instance.broken_font = (broken_font_red, broken_font_green, broken_font_blue)

            success_bg_red = int(config.get("Layout","success_bg_red"))
            success_bg_green = int(config.get("Layout","success_bg_green"))
            success_bg_blue = int(config.get("Layout","success_bg_blue"))
            success_font_red = int(config.get("Layout","success_font_red"))
            success_font_green = int(config.get("Layout","success_font_green"))
            success_font_blue = int(config.get("Layout","success_font_blue"))
            cls.instance.success_bg = (success_bg_red, success_bg_green, success_bg_blue)
            cls.instance.success_font = (success_font_red, success_font_green, success_font_blue)

            #Audio
            cls.instance.audio_root = config.get("Audio","audio_root")
            cls.instance.audio_broken = config.get("Audio","audio_broken")
            
        return cls.instance
    
    @classmethod
    def path_for_audio_file(cls, audio_file):
        ctx = cls.current()
        if ctx.audio_root.startswith("/"):
            return abspath(join(ctx.audio_root, audio_file))
        else:
            return abspath(join(root_path, ctx.audio_root, audio_file))
