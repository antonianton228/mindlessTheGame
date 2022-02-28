import pygame
from inicialising import init


def main():
    init()
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                print(run)
                return


if __name__ == "__main__":
    main()
