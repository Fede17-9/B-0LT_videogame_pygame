"""
Módulo principal para iniciar el videojuego B-0LT.
Este script inicializa Pygame, configura la pantalla y gestiona la transición
entre el menú de inicio y el bucle principal del juego.
"""

import pygame
from src.core.game import Game
from src.ui.menu import MenuInicio
from src.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT


def main():
    """
    Función principal que orquesta el inicio del juego.
    """
    # Inicializar todos los módulos de pygame
    pygame.init()

    # Configurar la ventana principal
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # 1. Ejecutar el Menú de Inicio
    menu = MenuInicio(screen)
    menu.ejecutar()

    # 2. Iniciar el juego principal una vez que el menú termina
    game = Game()
    game.run()


if __name__ == "__main__":
    main()