import pygame
from typing import Callable, Union
from random import randint

try:
    from .logger import Log
except ImportError:
    try:
        from logger import Log
    except ImportError:
        print("FATAL: Can't find 'logger.py' dependency.")
        exit()

log = Log("screen.py")

class cache:
    surface: list = []
    rect: list = []


class config:
    # DEFAULT VALUES
    width: int = 1280
    height: int = 720


    def disp_set_mode():
        return pygame.display.set_mode(size=(config.width, config.height), flags=pygame.SRCALPHA)


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
                log.error("Too many attempts to generate ID")
                return -1




def init(screen_width: int = config.width, screen_height: int = config.height):
    if screen_width < 0 or screen_height < 0:
        log.error("Screen size cannot be negative")
        return
    if screen_width != config.width:
        config.width = screen_width
    if screen_height != config.height:
        config.height = screen_height
    return config.disp_set_mode()




def update(surface: pygame.Surface):
    pygame.draw.rect(surface, pygame.Color(0, 0, 0), (0, 0, config.width, config.height)) #black bg

    removal_cache = []
    for r in cache.rect:
        if r[0] < 0:
            pygame.draw.rect(r[1], pygame.Color(0, 0, 0, 0), r[3])
            removal_cache.append(r)
        else:
            pygame.draw.rect(r[1], r[2], r[3])

    if len(removal_cache) > 0:
        for r in removal_cache:
            cache.rect.remove(r)

    i = len(cache.surface)
    while i > 0:
        i = i - 1
        surface.blit(cache.surface[i][0], (0, 0))

    pygame.display.flip()




class add:
    def rect(surface: pygame.Surface, color: pygame.Color, rect: pygame.Rect, event: Callable = None):
        found = False
        for s in cache.surface:
            if s[0] == surface:
                found = True
        if not found:
            log.error("Surface must be defined first")
            return
        ID = config.generate_id(cache.rect)
        if ID < 0:
            return
        cache.rect.append([ID, surface, color, rect, event])
        return ID
    

    def surface(layer: int = None):
        if layer == None:
            layer = 0
            if len(cache.surface) > 0:
                for s in cache.surface:
                    if s[1] > layer:
                        layer = s[1]
                layer = layer + 1
        elif layer < 0:
            log.error("Layer must be greater than -1")
            return
        
        surface = pygame.Surface(pygame.display.get_surface().get_size(), pygame.SRCALPHA)
        surface.fill((0, 0, 0, 0))
        cache.surface.append([surface, layer])

        adjust = True
        while adjust:
            adjust = False
            i = 0
            for s in cache.surface:
                i = i + 1
                if len(cache.surface) > i and s[1] < cache.surface[i][1]:
                    adjust = True
                    cache.surface.insert(i-1, cache.surface.pop(i))

        return surface
                



class remove:
    def __new__(self, object: Union[int, pygame.Surface]):
        if type(object) == int:
            return remove.item(object)
        else:
            return remove.surface(object)


    def surface(surface: pygame.Surface):
        for s in cache.surface:
            if s[0] == surface:
                cache.surface.remove(surface)
                for r in cache.rect:
                    if r[1] == surface:
                        cache.rect.remove(r)
                return True
        return False


    def item(ID: int):
        index = 0
        for r in cache.rect:
            if r[0] == ID:
                cache.rect[index][0] = -1
                return True
            index = index + 1
        return False




class event:
    def mouse_over(event):
        x = event.pos[0]
        y = event.pos[1]

        for s in cache.surface:
            for i in cache.rect:
                if i[1] == s[0]:
                    pos = i[3]
                    if x >= pos.x and x <= pos.x + pos.w:
                        if y >= pos.y and y <= pos.y + pos.h:
                            return i[0]