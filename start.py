import pygame
from gamelib import menu


if __name__ == '__main__':
    pygame.init()
    pygame.mouse.set_visible(0)
    pygame.display.set_caption("JUMP!")
    size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
    screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
    #screen = pygame.display.set_mode((740, 580))
    m = menu.Menu(screen)
    m.loop()
	
