import pygame
import sys
from src.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, COLOR_BG, GAME_TITLE

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(GAME_TITLE)
        self.clock = pygame.time.Clock()
        self.running = True

    def run(self):
        """Ciclo principal del juego."""
        while self.running:
            self._handle_events()
            self._update()
            self._draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

    def _handle_events(self):
        """Manejo de eventos (teclado, ratón, cerrar ventana)."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def _update(self):
        """Actualización de la lógica del juego."""
        pass

    def _draw(self):
        """Renderizado de elementos en pantalla."""
        self.screen.fill(COLOR_BG)
        
        # Aquí se dibujarán los elementos del juego en el futuro
        
        pygame.display.flip()
