"""
Módulo que define la clase Puerta para la transición entre niveles.
Gestiona los estados de bloqueado, listo y abierto mediante animaciones.
"""

import os
import pygame


class Puerta(pygame.sprite.Sprite):
    """
    Representa la puerta de salida de un nivel.
    """

    def __init__(self, x, y):
        """
        Inicializa la puerta.

        Args:
            x (int): Posición inicial en el eje X.
            y (int): Posición inicial en el eje Y.
        """
        super().__init__()
        # --- AUDIO ---
        ruta_sonido = os.path.join("assets", "sounds", "puerta.mp3")
        try:
            self.sonido_puerta = pygame.mixer.Sound(ruta_sonido)
        except (pygame.error, FileNotFoundError):
            self.sonido_puerta = None

        # --- IMAGEN ---
        try:
            self.sheet = pygame.image.load(
                "assets/images/puerta.PNG").convert_alpha()
        except (pygame.error, FileNotFoundError):
            self.sheet = pygame.Surface((500, 200))
            self.sheet.fill((50, 50, 50))

        self.frames = []
        ancho_frame = self.sheet.get_width() / 5
        alto_total = self.sheet.get_height()

        for i in range(5):
            rect = pygame.Rect(
                int(i * ancho_frame), 0, int(ancho_frame), alto_total)
            frame = self.sheet.subsurface(rect)
            self.frames.append(pygame.transform.scale(frame, (120, 200)))

        self.frame_index = 0
        self.state = "BLOQUEADA"
        self.anim_speed = 0.15
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x, y)

    def desbloquear(self):
        """
        Cambia el estado de la puerta de bloqueada a lista para abrir.
        """
        if self.state == "BLOQUEADA":
            self.state = "LISTA"
            self.frame_index = 1

    def abrir(self):
        """
        Inicia el proceso de apertura de la puerta.
        """
        if self.state != "ABIERTA":
            self.state = "ABIERTA"
            if self.sonido_puerta:
                self.sonido_puerta.play()

    def update(self):
        """
        Actualiza el frame de animación según el estado de la puerta.
        """
        if self.state == "BLOQUEADA":
            self.frame_index = 0
        elif self.state == "LISTA":
            self.frame_index = 1
        elif self.state == "ABRIENDO":
            self.frame_index += self.anim_speed
            if self.frame_index >= len(self.frames):
                self.frame_index = len(self.frames) - 1
                self.state = "ABIERTA"

        self.image = self.frames[int(self.frame_index)]
