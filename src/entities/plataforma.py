<<<<<<< HEAD
"""
Módulo que define la clase Plataforma para los elementos del escenario.
Representa superficies sobre las que el jugador puede saltar.
"""

import os
import pygame


class Plataforma(pygame.sprite.Sprite):
    """
    Representa una plataforma física en el nivel.
    """

    def __init__(self, x, y, ancho=None, alto=None,
                 imagen_nombre="plataforma.png"):
        """
        Inicializa la plataforma.

        Args:
            x (int): Posición X de la plataforma.
            y (int): Posición Y de la plataforma.
            ancho (int, optional): Ancho personalizado.
            alto (int, optional): Alto personalizado.
            imagen_nombre (str): Nombre del archivo de imagen en assets.
        """
        super().__init__()

        # Construimos la ruta dinámica de assets
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        ruta_imagen = os.path.join(base_path, 'assets', 'images', imagen_nombre)

=======
import pygame
import os

class Plataforma(pygame.sprite.Sprite):
    def __init__(self, x, y, ancho=None, alto=None, imagen_nombre="plataforma.png"): 
        super().__init__()
        
        # Construimos la ruta dinámica
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        ruta_imagen = os.path.join(base_path, 'assets', 'images', imagen_nombre)
        
>>>>>>> f5d0c78a63262b0423309515dd3bfe18dae89ce1
        try:
            self.image = pygame.image.load(ruta_imagen).convert_alpha()
            if ancho and alto:
                self.image = pygame.transform.scale(self.image, (ancho, alto))
<<<<<<< HEAD
        except (pygame.error, FileNotFoundError):
            # Fallback si la imagen no existe
            self.image = pygame.Surface((ancho or 120, alto or 40))
            self.image.fill((100, 100, 100))

=======
        except pygame.error:
            # Fallback si la imagen no existe
            self.image = pygame.Surface((ancho or 120, alto or 40))
            self.image.fill((100, 100, 100))
            
>>>>>>> f5d0c78a63262b0423309515dd3bfe18dae89ce1
        self.rect = self.image.get_rect()
        self.rect.x = round(x)
        self.rect.y = round(y)