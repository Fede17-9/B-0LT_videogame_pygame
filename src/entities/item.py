"""
Módulo que define la clase Bateria para los items recolectables.
Gestiona la animación del item y el sonido al ser recolectado.
"""

import os
import pygame


class Bateria(pygame.sprite.Sprite):
    """
    Representa una batería que el jugador puede recolectar para ganar energía.
    """

    def __init__(self, x, y):
        """
        Inicializa la batería.

        Args:
            x (int): Posición inicial en el eje X.
            y (int): Posición inicial en el eje Y.
        """
        super().__init__()
        ruta_sonido = os.path.join("assets", "sounds", "bateria.mp3")
        try:
            self.sonido_recolectar = pygame.mixer.Sound(ruta_sonido)
            self.sonido_recolectar.set_volume(0.6)
        except (pygame.error, FileNotFoundError):
            print("No se pudo cargar bateria.mp3")
            self.sonido_recolectar = None

        # --- IMAGEN ---
        try:
            self.sheet = pygame.image.load(
                "assets/images/bateria.png").convert_alpha()
        except (pygame.error, FileNotFoundError):
            self.sheet = pygame.Surface((320, 40))
            self.sheet.fill((0, 255, 0))

        self.frames = []
        ancho_frame = self.sheet.get_width() // 8
        alto_total = self.sheet.get_height()

        for i in range(8):
            rect_recorte = pygame.Rect(
                i * ancho_frame, 0, ancho_frame, alto_total)
            frame = self.sheet.subsurface(rect_recorte)
            self.frames.append(pygame.transform.scale(frame, (50, 80)))

        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x, y)
        self.anim_speed = 0.15

    def recolectar(self):
        """
        Reproduce el sonido de recolección y elimina el item.
        """
        if self.sonido_recolectar:
            self.sonido_recolectar.play()
        self.kill()

    def update(self):
        """
        Actualiza la animación de la batería.
        """
        self.frame_index += self.anim_speed
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]
