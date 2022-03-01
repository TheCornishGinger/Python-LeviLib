import pygame, os
from typing import Callable, Union
from random import randint
from datetime import datetime

class groups:
    surface: list = []
    rect: list = []


class config:
    # DEFAULT VALUES
    width: int = 1280
    height: int = 720
    log_file: str = "log.txt"


    def disp_set_mode():
        return pygame.display.set_mode(size=(config.width, config.height), flags=pygame.SRCALPHA)


    def error(log: str):
        time = datetime.now().strftime("%H:%M:%S")
        log = "[" + time + "] ERROR: " + log
        print(log)
        if not os.path.exists(os.getcwd()):
            try: 
                open(config.log_file, mode="x").close()
            except IOError:
                print("FATAL: file error.")
                return
        try:
            f = open(config.log_file, mode="r", encoding="utf-8")
            prefix = f.read()
            f.close()
            f = open(config.log_file, mode="w", encoding="utf-8")
            f.write(prefix + "\n" + log)
            f.close()
        except IOError:
            print("FATAL: file error.")


    def generate_id(list: list):
        attempt = 0
        while True:
            fail = False
            id = randint(1000, 9999)
            for item in list:
                if item[0] == id:
                    fail = True
            attempt = attempt + 1
            if not fail:
                return id
            if attempt > 100:
                config.error("Too many attempts to generate ID")
                return -1


def init(screen_width: int = config.width, screen_height: int = config.height):
    if screen_width < 0 or screen_height < 0:
        config.error("Screen size cannot be negative")
        return
    if screen_width != config.width:
        config.width = screen_width
    if screen_height != config.height:
        config.height = screen_height
    return config.disp_set_mode()


def update(surface: pygame.Surface):
    pygame.draw.rect(surface, pygame.Color(0, 0, 0), (0, 0, config.width, config.height))

    for r in groups.rect:
        if r[0] < 0:
            pygame.draw.rect(r[1], pygame.Color(0, 0, 0, 0), r[3])
            groups.rect.pop(groups.rect.index(r))
        else:
            pygame.draw.rect(r[1], r[2], r[3])

    i = len(groups.surface)
    while i > 0:
        i = i - 1
        surface.blit(groups.surface[i][0], (0, 0))

    print("-=-UPDATE-=-")
    for i in groups.rect:
        print("<> ", i[0])
    pygame.display.flip()
    print("-=-=-=-=-=-")


class add:
    def rect(surface: pygame.Surface, color: pygame.Color, rect: pygame.Rect, event: Callable = None):
        found = False
        for s in groups.surface:
            if s[0] == surface:
                found = True
        if not found:
            config.error("Surface must be defined first")
            return
        ID = config.generate_id(groups.rect)
        if ID < 0:
            return
        groups.rect.append([ID, surface, color, rect, event])
        return ID
    

    def surface(layer: int = None):
        if layer == None:
            layer = 0
            if len(groups.surface) > 0:
                for s in groups.surface:
                    if s[1] > layer:
                        layer = s[1]
                layer = layer + 1

        elif layer < 0:
            config.error("Layer must be greater than -1")
            return
        
        surface = pygame.Surface(pygame.display.get_surface().get_size(), pygame.SRCALPHA)
        surface.fill((0, 0, 0, 0))
        groups.surface.append([surface, layer])

        adjust = True
        while adjust:
            adjust = False
            i = 0
            for s in groups.surface:
                i = i + 1
                if len(groups.surface) > i and s[1] < groups.surface[i][1]:
                    adjust = True
                    groups.surface.insert(i-1, groups.surface.pop(i))

        return surface
                

class remove:
    def __new__(self, object: Union[int, pygame.Surface]):
        if type(object) == int:
            return remove.item(object)
        else:
            return remove.surface(object)


    def surface(surface: pygame.Surface):
        for s in groups.surface:
            if s[0] == surface:
                groups.surface.remove(surface)
                for r in groups.rect:
                    if r[1] == surface:
                        groups.rect.remove(r)
                return True
        return False

    def item(ID: int):
        index = 0
        for r in groups.rect:
            if r[0] == ID:
                groups.rect[index][0] = -1
                return True
            index = index + 1
        return False

class event:
    def mouse_down(event):
        x = event.pos[0]
        y = event.pos[1]

        for s in groups.surface:
            for i in groups.rect:
                if i[1] == s[0]:
                    pos = i[3]
                    if x >= pos.x and x <= pos.x + pos.w:
                        if y >= pos.y and y <= pos.y + pos.h:
                            return i[0]

    def mouse_down_old(event: pygame.event.Event):
        x = event.pos[0]
        y = event.pos[1]
        for item in groups.rect:
            pos = item[3]
            if item[4] and x >= pos.x and x <= pos.x + pos.w:
                if y >= pos.y and y <= pos.y + pos.h:
                    item[4]()
        return # DO THIS

    def mouse_up(event):
        return # DO THIS