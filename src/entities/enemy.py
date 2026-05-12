<<<<<<< HEAD
"""
Módulo que define la clase Enemy para los enemigos terrestres.
Gestiona el movimiento patrullado y la animación de los enemigos.
"""

import os
import pygame


class Enemy(pygame.sprite.Sprite):
    """
    Representa un enemigo terrestre con movimiento de patrullaje.
    """

    def __init__(self, x, y, rango=50):
        """
        Inicializa al enemigo.

        Args:
            x (int): Posición inicial en el eje X.
            y (int): Posición inicial en el eje Y.
            rango (int): Distancia máxima que puede recorrer desde su origen.
        """
        super().__init__()

        base_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        ruta_img = os.path.join(base_path, 'assets', 'images', 'enemigo-1.png')

        try:
            self.atlas = pygame.image.load(ruta_img).convert_alpha()
        except (pygame.error, FileNotFoundError):
            self.atlas = pygame.Surface((700, 400), pygame.SRCALPHA)

        self.frame_width = 128
        self.frame_height = 128
        self.frames_totales = 8
        self.frame_index = 0
        self.anim_speed = 0.15

        # Posicionamiento
        self.pos_inicial_x = x
        self.rango = rango
        self.direccion = 1  # 1 para derecha, -1 para izquierda
        self.vel = 2

        self.image = self._get_frame()
        self.rect = self.image.get_rect()

        # AJUSTE DE PISO: +38 para alinear con el suelo del jugador
        self.rect.midbottom = (x, y + 38)

    def _get_frame(self):
        """
        Extrae el frame actual del atlas y aplica transformaciones.

        Returns:
            pygame.Surface: El frame procesado.
        """
        idx = int(self.frame_index) % self.frames_totales

        # --- AJUSTE DE VENTANA (MANDÍBULA) ---
        y_recorte = 80
        alto_recorte = 48

        rect_recorte = pygame.Rect(
            idx * self.frame_width,
            y_recorte,
            self.frame_width,
            alto_recorte
        )

        try:
            frame = self.atlas.subsurface(rect_recorte).copy()
            # Escalado para visualización óptima
            frame = pygame.transform.scale(frame, (75, 48))

            if self.direccion == -1:
                frame = pygame.transform.flip(frame, True, False)
            return frame
        except (pygame.error, ValueError):
            return pygame.Surface((75, 48), pygame.SRCALPHA)

    def update(self):
        """
        Actualiza el movimiento y la animación del enemigo.
        """
        # Movimiento horizontal
        self.rect.x += self.vel * self.direccion

        # --- CONTROL DE PATRULLAJE ---
        if self.rect.x > self.pos_inicial_x + self.rango:
            self.direccion = -1
        elif self.rect.x < self.pos_inicial_x - self.rango:
            self.direccion = 1

        self.frame_index += self.anim_speed
        self.image = self._get_frame()
=======
import pygame
import os

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, rango=50): # Rango más corto (50) para evitar que se salga
        super().__init__()
        
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        ruta_img = os.path.join(base_path, 'assets', 'images', 'enemigo-1.png')
        
        try:
            self.atlas = pygame.image.load(ruta_img).convert_alpha()
        except:
            self.atlas = pygame.Surface((700, 400), pygame.SRCALPHA)

        self.frame_width = 128   
        self.frame_height = 128  
        self.frames_totales = 8  
        self.frame_index = 0
        self.anim_speed = 0.15
        
        # Posicionamiento
        self.pos_inicial_x = x
        self.rango = rango
        self.direccion = 1 # Empieza hacia la derecha
        self.vel = 2
        
        self.image = self._get_frame()
        self.rect = self.image.get_rect()
        
        # AJUSTE DE PISO: +38 para que quede bien abajo en la línea de B-OLT
        self.rect.midbottom = (x, y + 38) 

    def _get_frame(self):
        idx = int(self.frame_index) % self.frames_totales
        
        # --- AJUSTE DE VENTANA (MANDÍBULA) ---
        # Bajamos el inicio a 80 para centrar el bicho
        y_recorte = 80 
        # Le damos 48 de alto para que la mandíbula inferior salga completa
        alto_recorte = 48 
        
        rect_recorte = pygame.Rect(idx * self.frame_width, y_recorte, self.frame_width, alto_recorte)
        
        try:
            frame = self.atlas.subsurface(rect_recorte).copy()
            # Escalado ligeramente más alto para que se vea el detalle de los dientes
            frame = pygame.transform.scale(frame, (75, 48)) 
            
            if self.direccion == -1:
                frame = pygame.transform.flip(frame, True, False)
            return frame
        except:
            return pygame.Surface((75, 48), pygame.SRCALPHA)

    def update(self, plataformas=None):
        # Movimiento
        self.rect.x += self.vel * self.direccion
        
        # --- CORRECCIÓN DE RANGO (PARED DERECHA) ---
        # Si el enemigo se aleja más de 'rango' píxeles de su origen, cambia de dirección.
        if self.rect.x > self.pos_inicial_x + self.rango:
            self.direccion = -1 # Obligamos a ir a la izquierda
        elif self.rect.x < self.pos_inicial_x - self.rango:
            self.direccion = 1  # Obligamos a ir a la derecha
            
        self.frame_index += self.anim_speed
        self.image = self._get_frame()
>>>>>>> f5d0c78a63262b0423309515dd3bfe18dae89ce1
