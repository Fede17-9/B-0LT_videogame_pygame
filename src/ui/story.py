<<<<<<< HEAD
"""
Módulo que define la clase StoryScreen para la narrativa del juego.
Presenta viñetas animadas con efectos de fundido y música ambiental.
"""

import os
import pygame
import pygame_menu


class StoryScreen:
    """
    Gestiona la pantalla de historia, mostrando viñetas secuencialmente.
    """

    def __init__(self, screen, next_state_callback):
        """
        Inicializa la pantalla de historia.

        Args:
            screen (pygame.Surface): Superficie de la pantalla principal.
            next_state_callback (callable): Función a llamar al terminar.
        """
        self.screen = screen
        self.on_finished = next_state_callback

        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.img_dir = os.path.join(
            current_dir, "..", "..", "assets", "images")
        self.sound_dir = os.path.join(
            current_dir, "..", "..", "assets", "sounds")

        # 1. Cargar las viñetas
        self.vinetas = []
        for i in range(1, 7):
            path = os.path.join(self.img_dir, f'viñeta{i}.jpg')
            if os.path.exists(path):
                img = pygame.image.load(path).convert()
                img = pygame.transform.scale(
                    img, (screen.get_width(), screen.get_height()))
                self.vinetas.append({"img": img, "visible": False, "alpha": 0})
            else:
                print(f"Error: No se encontró la imagen en {path}")

        self.index_actual = 0
        self.last_update = pygame.time.get_ticks()
        self.delay = 1000
        self.all_shown = False

        # 2. Configuración del Menú Transparente
        mi_tema = pygame_menu.themes.THEME_DARK.copy()
        mi_tema.background_color = (0, 0, 0, 0)
        mi_tema.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_NONE
        mi_tema.widget_font = pygame_menu.font.FONT_8BIT
        mi_tema.widget_font_size = 20
        mi_tema.widget_font_color = (130, 255, 130)

        self.menu = pygame_menu.Menu(
            '', screen.get_width(), screen.get_height(), theme=mi_tema)
        self.btn_skip = self.menu.add.button('SALTAR INTRO', self._saltar_todo)
        self.btn_jugar = self.menu.add.button('JUGAR', self._finalizar)
        self.btn_jugar.hide()

    def iniciar_musica(self):
        """
        Carga e inicia la música ambiental para la historia.
        """
        path_musica = os.path.join(self.sound_dir, 'Story.mp3')
        if os.path.exists(path_musica):
            pygame.mixer.music.load(path_musica)
            # Un poco más alto para la historia
            pygame.mixer.music.set_volume(0.6)
            pygame.mixer.music.play(-1)
        else:
            print(f"Error: No se encontró el archivo de audio {path_musica}")

    def _saltar_todo(self):
        """
        Muestra todas las viñetas instantáneamente y habilita el botón de jugar.
        """
        for vineta in self.vinetas:
            vineta["visible"] = True
            vineta["alpha"] = 255
            vineta["img"].set_alpha(255)
        self.all_shown = True
        self.btn_skip.hide()
        self.btn_jugar.show()

    def _finalizar(self):
        """
        Finaliza la secuencia de historia y transiciona al siguiente estado.
        """
        # Desvanecer la música antes de pasar al tutorial
        pygame.mixer.music.fadeout(1000)
        self.on_finished()

    def actualizar(self, events):
        """
        Actualiza la lógica de transición de viñetas y efectos de alpha.

        Args:
            events (list): Lista de eventos de Pygame.
        """
        now = pygame.time.get_ticks()

        if not self.all_shown:
            if self.index_actual < len(self.vinetas):
                if now - self.last_update > self.delay:
                    self.vinetas[self.index_actual]["visible"] = True
                    self.index_actual += 1
                    self.last_update = now
            else:
                self.all_shown = True
                self.btn_skip.hide()
                self.btn_jugar.show()

        for vineta in self.vinetas:
            if vineta["visible"] and vineta["alpha"] < 255:
                vineta["alpha"] += 15
                if vineta["alpha"] > 255:
                    vineta["alpha"] = 255
                vineta["img"].set_alpha(vineta["alpha"])

        if self.menu.is_enabled():
            self.menu.update(events)

    def dibujar(self):
        """
        Renderiza las viñetas visibles y los botones del menú.
        """
        # Fondo base por si alguna imagen falla
        self.screen.fill((0, 0, 0))

        # Dibujamos las viñetas acumuladas
        for vineta in self.vinetas:
            if vineta["visible"]:
                self.screen.blit(vineta["img"], (0, 0))

        # Dibujamos el menú (botones) al frente
        if self.menu.is_enabled():
            self.menu.draw(self.screen)
=======
import pygame
import os
import pygame_menu

class StoryScreen:
    def __init__(self, screen, next_state_callback):
        self.screen = screen
        self.on_finished = next_state_callback
        
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.img_dir = os.path.join(current_dir, "..", "..", "assets", "images")
        self.sound_dir = os.path.join(current_dir, "..", "..", "assets", "sounds")
        
        # 1. Cargar las viñetas
        self.vinetas = []
        for i in range(1, 7):
            path = os.path.join(self.img_dir, f'viñeta{i}.jpg')
            if os.path.exists(path):
                img = pygame.image.load(path).convert()
                img = pygame.transform.scale(img, (screen.get_width(), screen.get_height()))
                self.vinetas.append({"img": img, "visible": False, "alpha": 0})
            else:
                print(f"Error: No se encontró la imagen en {path}")

        self.index_actual = 0
        self.last_update = pygame.time.get_ticks()
        self.delay = 1000 
        self.all_shown = False

        # 2. Configuración del Menú Transparente
        mi_tema = pygame_menu.themes.THEME_DARK.copy()
        mi_tema.background_color = (0, 0, 0, 0) 
        mi_tema.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_NONE 
        mi_tema.widget_font = pygame_menu.font.FONT_8BIT
        mi_tema.widget_font_size = 20
        mi_tema.widget_font_color = (130, 255, 130)

        self.menu = pygame_menu.Menu('', screen.get_width(), screen.get_height(), theme=mi_tema)
        self.btn_skip = self.menu.add.button('SALTAR INTRO', self._saltar_todo)
        self.btn_jugar = self.menu.add.button('JUGAR', self._finalizar)
        self.btn_jugar.hide()

    def iniciar_musica(self):
        """Llamar a este método desde Game.py al cambiar al estado STORY"""
        path_musica = os.path.join(self.sound_dir, 'Story.mp3')
        if os.path.exists(path_musica):
            pygame.mixer.music.load(path_musica)
            pygame.mixer.music.set_volume(0.6) # Un poco más alto para la historia
            pygame.mixer.music.play(-1)
        else:
            print(f"Error: No se encontró el archivo de audio {path_musica}")

    def _saltar_todo(self):
        for vineta in self.vinetas:
            vineta["visible"] = True
            vineta["alpha"] = 255
            vineta["img"].set_alpha(255)
        self.all_shown = True
        self.btn_skip.hide()
        self.btn_jugar.show()

    def _finalizar(self):
        # Desvanecer la música antes de pasar al tutorial
        pygame.mixer.music.fadeout(1000)
        self.on_finished()

    def actualizar(self, events):
        now = pygame.time.get_ticks()
        
        if not self.all_shown:
            if self.index_actual < len(self.vinetas):
                if now - self.last_update > self.delay:
                    self.vinetas[self.index_actual]["visible"] = True
                    self.index_actual += 1
                    self.last_update = now
            else:
                self.all_shown = True
                self.btn_skip.hide()
                self.btn_jugar.show()

        for vineta in self.vinetas:
            if vineta["visible"] and vineta["alpha"] < 255:
                vineta["alpha"] += 15
                if vineta["alpha"] > 255: vineta["alpha"] = 255
                vineta["img"].set_alpha(vineta["alpha"])

        if self.menu.is_enabled():
            self.menu.update(events)

    def dibujar(self):
        self.screen.fill((0, 0, 0))
        for vineta in self.vinetas:
            if vineta["visible"]:
                self.screen.blit(vineta["img"], (0, 0))
        
        if self.menu.is_enabled():
            self.menu.draw(self.screen)

    def dibujar(self):
        # Fondo base por si alguna imagen falla
        self.screen.fill((0, 0, 0))
        
        # Dibujamos las viñetas (la última activa queda encima o se van acumulando)
        for vineta in self.vinetas:
            if vineta["visible"]:
                self.screen.blit(vineta["img"], (0, 0))
        
        # Dibujamos el menú (botones) al final para que estén al frente
        if self.menu.is_enabled():
            self.menu.draw(self.screen)
>>>>>>> f5d0c78a63262b0423309515dd3bfe18dae89ce1
