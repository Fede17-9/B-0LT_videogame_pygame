import pygame  # <--- ESTA ES LA LÍNEA QUE FALTA
from src.core.game import Game
from src.ui.menu import MenuInicio
from src.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT

def main(): 
    pygame.init()
    # Definimos la pantalla una sola vez
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    # 1. Menú de Inicio
    menu = MenuInicio(screen)
    menu.ejecutar() 

    # 2. El juego inicia SOLO una vez cuando el menú termina
    game = Game()
    game.run()  

if __name__ == "__main__":
    main()