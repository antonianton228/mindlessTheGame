import pygame
from inicialising import init

def running():
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                print(run)
                return

def main():
    init()
    running()


if __name__ == "__main__":
    main()
