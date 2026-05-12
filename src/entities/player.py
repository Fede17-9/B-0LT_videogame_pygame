<<<<<<< HEAD
"""
Módulo que define la clase Player para el personaje principal B-OLT.
Gestiona animaciones, física de movimiento, colisiones y sistema de vida.
"""

import os
import pygame
from src.utils.constants import SCREEN_HEIGHT


class Player(pygame.sprite.Sprite):
    """
    Representa al jugador B-OLT en el mundo del juego.
    """

    def __init__(self):
        """
        Inicializa al jugador, carga sus assets y configura sus propiedades físicas.
        """
        super().__init__()

        # 1. Carga de Imágenes con Rutas Robustas
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        images_path = os.path.join(base_path, 'assets', 'images')

        try:
            self.atlas_main = pygame.image.load(
                os.path.join(images_path, 'B-OLT2.png')).convert_alpha()
            self.atlas_jump = pygame.image.load(
                os.path.join(images_path, 'BOLT_JUMP2.png')).convert_alpha()

            # DASH2 con manejo de transparencia (ColorKey Negro)
            self.atlas_dash = pygame.image.load(
                os.path.join(images_path, 'DASH2.png')).convert()
            self.atlas_dash.set_colorkey((0, 0, 0))
        except (pygame.error, FileNotFoundError) as e:
            print(f"Error cargando atlas del jugador: {e}")
            # Superficie de emergencia si fallan los archivos
            self.atlas_main = pygame.Surface((1024, 1024))
            self.atlas_main.fill((255, 0, 255))
            self.atlas_jump = self.atlas_main
            self.atlas_dash = self.atlas_main

        # 2. Configuración de Animación
        self.anim_map = {
            'idle': {'atlas': self.atlas_main, 'row': 0, 'frames': 8},
            'run':  {'atlas': self.atlas_main, 'row': 1, 'frames': 8},
            'jump': {'atlas': self.atlas_jump, 'row': 0, 'frames': 8},
            'dash': {'atlas': self.atlas_dash, 'row': 0, 'frames': 8}
        }

        self.state = 'idle'
        self.frame_index = 0
        self.facing_right = True
        self.on_ground = False

        # --- SISTEMA DE VIDA ---
        self.health = 3
        self.invulnerable = False
        self.last_hit_time = 0
        self.invulnerability_duration = 1500  # 1.5 segundos de parpadeo

        # Inicializar imagen y rect
        self.image = self._get_current_frame()
        self.rect = self.image.get_rect()

        # 3. Física y Vectores
        self.pos = pygame.math.Vector2(100, SCREEN_HEIGHT - 50)
        self.vel = pygame.math.Vector2(0, 0)
        self.acc = pygame.math.Vector2(0, 0)

        self.GRAVITY = 0.8
        self.FRICTION = -0.12  # Suavizado un poco para mejor control
        self.ACC_SPEED = 0.60
        self.JUMP_POWER = -16

        # Dash
        self.is_dashing = False
        self.dash_speed = 12
        self.dash_duration = 150
        self.last_dash_time = 0
        self.dash_cooldown = 800

    def _get_current_frame(self):
        """
        Extrae y procesa el frame actual según el estado y la vida.

        Returns:
            pygame.Surface: El frame procesado para renderizar.
        """
        try:
            config = self.anim_map[self.state]
            atlas = config['atlas']
            fila = config['row']
            idx = int(self.frame_index) % config['frames']

            medida_grid = 128
            off_x, off_y = 5, 10
            ancho_v, alto_v = 122, 122

            rect_recorte = pygame.Rect(
                (idx * medida_grid) + off_x,
                (fila * medida_grid) + off_y,
                ancho_v,
                alto_v
            )

            # Seguridad para no salirse del atlas
            if (rect_recorte.right > atlas.get_width() or
                    rect_recorte.bottom > atlas.get_height()):
                rect_recorte = pygame.Rect(
                    off_x,
                    (fila * medida_grid) + off_y,
                    ancho_v,
                    alto_v
                )

            frame = atlas.subsurface(rect_recorte).copy()
            frame = pygame.transform.scale(frame, (90, 90))

            # --- EFECTO VISUAL DE DAÑO (PARPADEO) ---
            if self.invulnerable:
                # Alterna transparencia cada 100ms
                if (pygame.time.get_ticks() // 100) % 2 == 0:
                    frame.set_alpha(100)
                else:
                    frame.set_alpha(255)

            if not self.facing_right:
                frame = pygame.transform.flip(frame, True, False)

            return frame
        except (pygame.error, ValueError):
            surface = pygame.Surface((90, 90))
            surface.fill((255, 0, 255))
            return surface

    def recibir_danio(self):
        """
        Maneja la pérdida de vida y activa invulnerabilidad temporal.
        """
        now = pygame.time.get_ticks()
        if not self.invulnerable and self.health > 0:
            self.health -= 1
            self.invulnerable = True
            self.last_hit_time = now

            # Pequeño empuje de retroceso al recibir daño
            self.vel.y = -8
            self.vel.x = -6 if self.facing_right else 6
            print(f"¡B-OLT herido! Vida restante: {self.health}")

    def _update_invulnerability(self):
        """
        Controla el tiempo que B-OLT permanece parpadeando.
        """
        if self.invulnerable:
            now = pygame.time.get_ticks()
            if now - self.last_hit_time > self.invulnerability_duration:
                self.invulnerable = False

    def _change_state(self, new_state):
        """
        Cambia el estado de animación del jugador.

        Args:
            new_state (str): El nuevo estado de animación.
        """
        if self.state != new_state:
            self.state = new_state
            self.frame_index = 0

    def update(self, plataformas):
        """
        Actualiza la lógica del jugador: física, colisiones y animaciones.

        Args:
            plataformas (pygame.sprite.Group): Grupo de plataformas con las que colisionar.
        """
        now = pygame.time.get_ticks()
        self._update_invulnerability()

        # Aplicar Gravedad constante
        self.acc = pygame.math.Vector2(0, self.GRAVITY)

        keys = pygame.key.get_pressed()

        # 1. Movimiento Horizontal (Solo si no está en Dash)
        if not self.is_dashing:
            if keys[pygame.K_LEFT]:
                self.acc.x = -self.ACC_SPEED
                self.facing_right = False
            elif keys[pygame.K_RIGHT]:
                self.acc.x = self.ACC_SPEED
                self.facing_right = True

            # Fricción para frenado suave
            self.acc.x += self.vel.x * self.FRICTION
            self.vel.x += self.acc.x
            if abs(self.vel.x) < 0.1:
                self.vel.x = 0

        # 2. Aplicar Física al Vector de Posición
        self.pos.x += self.vel.x
        self.vel.y += self.acc.y
        self.pos.y += self.vel.y

        # 3. Colisiones de Suelo y Plataformas
        self.on_ground = False

        # Suelo de la pantalla
        if self.pos.y >= SCREEN_HEIGHT - 50:
            self.pos.y = SCREEN_HEIGHT - 50
            self.vel.y = 0
            self.on_ground = True

        # Plataformas (Unidireccionales: solo colisiona al caer)
        if self.vel.y >= 0:
            self.rect.midbottom = (int(self.pos.x), int(self.pos.y) + 1)
            hits = pygame.sprite.spritecollide(self, plataformas, False)

            if hits:
                plat = hits[0]
                if self.pos.y <= plat.rect.top + self.vel.y + 2:
                    self.pos.y = plat.rect.top
                    self.vel.y = 0
                    self.on_ground = True

        # 4. Habilidad de Dash
        if keys[pygame.K_LSHIFT] and not self.is_dashing:
            if now - self.last_dash_time > self.dash_cooldown:
                self.is_dashing = True
                self.last_dash_time = now
                self.vel.x = (self.dash_speed if self.facing_right
                              else -self.dash_speed)
                self.vel.y = 0  # El dash cancela la caída temporalmente

        if self.is_dashing and now - self.last_dash_time > self.dash_duration:
            self.is_dashing = False

        # 5. Máquina de Estados para Animaciones
        if not self.on_ground:
            self._change_state('jump')
        elif self.is_dashing:
            self._change_state('dash')
        elif abs(self.vel.x) > 0.8:
            self._change_state('run')
        else:
            self._change_state('idle')

        # 6. Control de Velocidad de Animación
        v_anim = {'run': 0.2, 'jump': 0.12, 'dash': 0.4, 'idle': 0.12}
        self.frame_index += v_anim.get(self.state, 0.1)

        # Ciclo de frames
        if self.frame_index >= self.anim_map[self.state]['frames']:
            if self.state == 'jump':
                # Mantiene el último frame del salto en el aire
                self.frame_index = self.anim_map['jump']['frames'] - 1
            else:
                self.frame_index = 0

        # 7. Renderizado Final y Rectificación del Rect
        self.image = self._get_current_frame()
        self.rect.midbottom = (round(self.pos.x), round(self.pos.y))

    def jump(self):
        """
        Realiza la acción de salto si el jugador está en el suelo.
        """
        if self.on_ground:
            self.vel.y = self.JUMP_POWER
            self.on_ground = False
            self._change_state('jump')
=======
import pygame
import os
from src.utils.constants import SCREEN_HEIGHT, SCREEN_WIDTH

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        # 1. Carga de Imágenes con Rutas Robustas
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        images_path = os.path.join(base_path, 'assets', 'images')
        
        try:
            self.atlas_main = pygame.image.load(os.path.join(images_path, 'B-OLT2.png')).convert_alpha()
            self.atlas_jump = pygame.image.load(os.path.join(images_path, 'BOLT_JUMP2.png')).convert_alpha()
            
            # DASH2 con manejo de transparencia (ColorKey Negro)
            self.atlas_dash = pygame.image.load(os.path.join(images_path, 'DASH2.png')).convert()
            self.atlas_dash.set_colorkey((0, 0, 0))
        except Exception as e:
            print(f"Error cargando atlas del jugador: {e}")
            # Superficie de emergencia si fallan los archivos
            self.atlas_main = pygame.Surface((1024, 1024))
            self.atlas_main.fill((255, 0, 255))
            self.atlas_jump = self.atlas_main
            self.atlas_dash = self.atlas_main

        # 2. Configuración de Animación
        self.anim_map = {
            'idle': {'atlas': self.atlas_main, 'row': 0, 'frames': 8},
            'run':  {'atlas': self.atlas_main, 'row': 1, 'frames': 8},
            'jump': {'atlas': self.atlas_jump, 'row': 0, 'frames': 8}, 
            'dash': {'atlas': self.atlas_dash, 'row': 0, 'frames': 8}
        }
        
        self.state = 'idle'
        self.frame_index = 0
        self.facing_right = True
        self.on_ground = False
        
        # --- SISTEMA DE VIDA ---
        self.health = 3
        self.invulnerable = False
        self.last_hit_time = 0
        self.invulnerability_duration = 1500 # 1.5 segundos de parpadeo
        
        # Inicializar imagen y rect
        self.image = self._get_current_frame()
        self.rect = self.image.get_rect()
        
        # 3. Física y Vectores
        self.pos = pygame.math.Vector2(100, SCREEN_HEIGHT - 50)
        self.vel = pygame.math.Vector2(0, 0)
        self.acc = pygame.math.Vector2(0, 0)
        
        self.GRAVITY = 0.8
        self.FRICTION = -0.12 # Suavizado un poco para mejor control
        self.ACC_SPEED = 0.60
        self.JUMP_POWER = -16
        
        # Dash
        self.is_dashing = False
        self.dash_speed = 12
        self.dash_duration = 150 
        self.last_dash_time = 0
        self.dash_cooldown = 800

    def _get_current_frame(self):
        """Extrae y procesa el frame actual según el estado y la vida."""
        try:
            config = self.anim_map[self.state]
            atlas = config['atlas']
            fila = config['row']
            idx = int(self.frame_index) % config['frames']

            medida_grid = 128
            off_x, off_y = 5, 10
            ancho_v, alto_v = 122, 122

            rect_recorte = pygame.Rect((idx * medida_grid) + off_x, (fila * medida_grid) + off_y, ancho_v, alto_v)
            
            # Seguridad para no salirse del atlas
            if rect_recorte.right > atlas.get_width() or rect_recorte.bottom > atlas.get_height():
                 rect_recorte = pygame.Rect(off_x, (fila * medida_grid) + off_y, ancho_v, alto_v)

            frame = atlas.subsurface(rect_recorte).copy()
            frame = pygame.transform.scale(frame, (90, 90))
            
            # --- EFECTO VISUAL DE DAÑO (PARPADEO) ---
            if self.invulnerable:
                # Alterna transparencia cada 100ms
                if (pygame.time.get_ticks() // 100) % 2 == 0:
                    frame.set_alpha(100)
                else:
                    frame.set_alpha(255)

            if not self.facing_right:
                frame = pygame.transform.flip(frame, True, False)
                
            return frame
        except Exception:
            surface = pygame.Surface((90, 90))
            surface.fill((255, 0, 255)) 
            return surface

    def recibir_danio(self):
        """Maneja la pérdida de vida y activa invulnerabilidad temporal."""
        now = pygame.time.get_ticks()
        if not self.invulnerable and self.health > 0:
            self.health -= 1
            self.invulnerable = True
            self.last_hit_time = now
            
            # Pequeño empuje de retroceso al recibir daño
            self.vel.y = -8 
            self.vel.x = -6 if self.facing_right else 6
            print(f"¡B-OLT herido! Vida restante: {self.health}")

    def _update_invulnerability(self):
        """Controla el tiempo que B-OLT permanece parpadeando."""
        if self.invulnerable:
            now = pygame.time.get_ticks()
            if now - self.last_hit_time > self.invulnerability_duration:
                self.invulnerable = False

    def _change_state(self, new_state):
        if self.state != new_state:
            self.state = new_state
            self.frame_index = 0

    def update(self, plataformas):
        now = pygame.time.get_ticks()
        self._update_invulnerability()
        
        # Aplicar Gravedad constante
        self.acc = pygame.math.Vector2(0, self.GRAVITY)
        
        keys = pygame.key.get_pressed()
        
        # 1. Movimiento Horizontal (Solo si no está en Dash)
        if not self.is_dashing:
            if keys[pygame.K_LEFT]:
                self.acc.x = -self.ACC_SPEED
                self.facing_right = False
            elif keys[pygame.K_RIGHT]:
                self.acc.x = self.ACC_SPEED
                self.facing_right = True
            
            # Fricción para frenado suave
            self.acc.x += self.vel.x * self.FRICTION
            self.vel.x += self.acc.x
            if abs(self.vel.x) < 0.1: self.vel.x = 0

        # 2. Aplicar Física al Vector de Posición
        self.pos.x += self.vel.x
        self.vel.y += self.acc.y
        self.pos.y += self.vel.y

        # 3. Colisiones de Suelo y Plataformas
        self.on_ground = False 

        # Suelo de la pantalla
        if self.pos.y >= SCREEN_HEIGHT - 50:
            self.pos.y = SCREEN_HEIGHT - 50
            self.vel.y = 0
            self.on_ground = True

        # Plataformas (Unidireccionales: solo colisiona al caer)
        if self.vel.y >= 0:
            self.rect.midbottom = (int(self.pos.x), int(self.pos.y) + 1)
            hits = pygame.sprite.spritecollide(self, plataformas, False)
            
            if hits:
                plat = hits[0]
                if self.pos.y <= plat.rect.top + self.vel.y + 2:
                    self.pos.y = plat.rect.top
                    self.vel.y = 0
                    self.on_ground = True

        # 4. Habilidad de Dash
        if keys[pygame.K_LSHIFT] and not self.is_dashing:
            if now - self.last_dash_time > self.dash_cooldown:
                self.is_dashing = True
                self.last_dash_time = now
                self.vel.x = self.dash_speed if self.facing_right else -self.dash_speed
                self.vel.y = 0 # El dash cancela la caída temporalmente

        if self.is_dashing and now - self.last_dash_time > self.dash_duration:
            self.is_dashing = False

        # 5. Máquina de Estados para Animaciones
        if not self.on_ground: 
            self._change_state('jump')
        elif self.is_dashing:
            self._change_state('dash')
        elif abs(self.vel.x) > 0.8: 
            self._change_state('run')
        else:
            self._change_state('idle')  

        # 6. Control de Velocidad de Animación
        v_anim = {'run': 0.2, 'jump': 0.12, 'dash': 0.4, 'idle': 0.12}
        self.frame_index += v_anim.get(self.state, 0.1)

        # Ciclo de frames
        if self.frame_index >= self.anim_map[self.state]['frames']:
            if self.state == 'jump':
                # Mantiene el último frame del salto en el aire
                self.frame_index = self.anim_map['jump']['frames'] - 1
            else:
                self.frame_index = 0
            
        # 7. Renderizado Final y Rectificación del Rect
        self.image = self._get_current_frame()
        self.rect.midbottom = (round(self.pos.x), round(self.pos.y))

    def jump(self):
        """Acción de salto."""
        if self.on_ground:
            self.vel.y = self.JUMP_POWER
            self.on_ground = False
            self._change_state('jump')
>>>>>>> f5d0c78a63262b0423309515dd3bfe18dae89ce1
