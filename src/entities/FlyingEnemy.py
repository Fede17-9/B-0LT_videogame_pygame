"""
Módulo que define la clase FlyingEnemy para los enemigos voladores.
Gestiona el movimiento oscilatorio y patrullaje aéreo.
"""

import math
import os
import pygame


class FlyingEnemy(pygame.sprite.Sprite):
    """
    Representa un enemigo volador con movimiento sinusoidal y patrullaje.
    """

    def __init__(self, x, y, rango=100, velocidad=2):
        """
        Inicializa al enemigo volador.

        Args:
            x (int): Posición inicial en el eje X.
            y (int): Posición inicial en el eje Y.
            rango (int): Distancia máxima de patrullaje horizontal.
            velocidad (int): Velocidad de movimiento horizontal.
        """
        super().__init__()
        self.frames = []
        self._cortar_sprite_sheet()
        self.index = 0
        self.image = self.frames[self.index]
        self.rect = self.image.get_rect(topleft=(x, y))

        # Configuración de patrulla
        self.pos_inicial_x = x
        self.pos_inicial_y = y
        self.rango = rango
        self.velocidad = velocidad
        self.direccion = 1
        self.contador_flotado = 0

    def _cortar_sprite_sheet(self):
        """
        Divide la hoja de sprites en frames individuales.
        """
        path = os.path.join("assets", "images", "enemigo2.png")
        try:
            sheet = pygame.image.load(path).convert_alpha()

            # Ajuste de dimensiones:
            # Dividimos el ancho total entre 8 (columnas)
            ancho_frame = sheet.get_width() // 8

            # Alto limitado para evitar capturar partes no deseadas
            alto_frame = 105

            for i in range(8):
                recorte = pygame.Surface((ancho_frame, alto_frame),
                                         pygame.SRCALPHA)
                recorte.blit(sheet, (0, 0),
                             (i * ancho_frame, 0, ancho_frame, alto_frame))

                # Escalamos al tamaño final para el juego
                image_final = pygame.transform.scale(recorte, (64, 64))
                self.frames.append(image_final)

        except (pygame.error, FileNotFoundError) as e:
            print(f"Error al ajustar recorte de enemigo2.png: {e}")
            surf = pygame.Surface((64, 64), pygame.SRCALPHA)
            surf.fill((200, 100, 0))
            self.frames.append(surf)

    def update(self):
        """
        Actualiza la animación y el movimiento del enemigo volador.
        """
        # Animación de frames
        self.index += 0.15
        if self.index >= len(self.frames):
            self.index = 0
        self.image = self.frames[int(self.index)]

        # Patrullaje Horizontal
        self.rect.x += self.velocidad * self.direccion
        if abs(self.rect.x - self.pos_inicial_x) >= self.rango:
            self.direccion *= -1
            # Voltear frames para que mire en la dirección del movimiento
            self.frames = [pygame.transform.flip(f, True, False)
                           for f in self.frames]

        # Movimiento Vertical (Flotado Sinusoidal)
        self.contador_flotado += 0.05
        self.rect.y = (self.pos_inicial_y +
                       math.sin(self.contador_flotado) * 15)
