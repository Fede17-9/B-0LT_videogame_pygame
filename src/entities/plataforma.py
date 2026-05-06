import pygame
import os

class Plataforma(pygame.sprite.Sprite):
    def __init__(self, x, y, ancho=None, alto=None, imagen_nombre="plataforma.png"): 
        super().__init__()
        
        # Construimos la ruta dinámica
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        ruta_imagen = os.path.join(base_path, 'assets', 'images', imagen_nombre)
        
        try:
            self.image = pygame.image.load(ruta_imagen).convert_alpha()
            if ancho and alto:
                self.image = pygame.transform.scale(self.image, (ancho, alto))
        except pygame.error:
            # Fallback si la imagen no existe
            self.image = pygame.Surface((ancho or 120, alto or 40))
            self.image.fill((100, 100, 100))
            
        self.rect = self.image.get_rect()
        self.rect.x = round(x)
        self.rect.y = round(y)