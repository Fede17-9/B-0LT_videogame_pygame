import pygame
import os
import sys
import pygame_menu

class MenuInicio:
    def __init__(self, screen):
        self.screen = screen
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.img_dir = os.path.join(current_dir, "..", "..", "assets", "images")
        # 1. Ruta de sonidos
        self.sound_dir = os.path.join(current_dir, "..", "..", "assets", "sounds")
        
        # --- INICIALIZAR MÚSICA ---
        pygame.mixer.init()
        path_musica = os.path.join(self.sound_dir, 'lalaland.mp3')
        
        if os.path.exists(path_musica):
            pygame.mixer.music.load(path_musica)
            pygame.mixer.music.set_volume(0.4) # Volumen al 40% (ideal para piano)
            pygame.mixer.music.play(-1)        # Reproducción infinita
        else:
            print(f"Aviso: No se encontró {path_musica}")

        # 2. Cargar Animación de Fondo
        self.frames = []
        for i in range(1, 5):
            path = os.path.normpath(os.path.join(self.img_dir, f'inicio{i}.jpg'))
            if os.path.exists(path):
                img = pygame.image.load(path).convert()
                img_escalada = pygame.transform.scale(img, (self.screen.get_width(), self.screen.get_height()))
                self.frames.append(img_escalada)

        # 3. Cargar Imagen de Controles
        path_controles = os.path.join(self.img_dir, 'controles.jpg')
        self.img_controles = None
        if os.path.exists(path_controles):
            try:
                self.img_controles = pygame.image.load(path_controles).convert()
                self.img_controles = pygame.transform.scale(self.img_controles, (self.screen.get_width(), self.screen.get_height()))
            except pygame.error as e:
                print(f"No se pudo cargar controles.jpg: {e}")
        
        self.current_frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_speed = 250 
        self.activo = True
        self.mostrando_controles = False

        # 4. Configurar Menú con Estilo PIXEL ART
        self.tema = pygame_menu.themes.THEME_DARK.copy()
        self.tema.background_color = (0, 0, 0, 0)
        self.tema.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_NONE
        
        self.tema.widget_font = pygame_menu.font.FONT_8BIT
        self.tema.widget_font_size = 25
        self.tema.widget_font_color = (130, 255, 130)
        self.tema.widget_selection_effect = pygame_menu.widgets.LeftArrowSelection(
            arrow_size=(15, 25),
            blink_ms=400
        )

        self.menu = pygame_menu.Menu('', screen.get_width(), screen.get_height(), theme=self.tema)
        self.menu.add.vertical_margin(250) 
        
        self.menu.add.button('CONTROLES', self._ver_controles)
        self.menu.add.vertical_margin(10)
        self.menu.add.button('SALIR', pygame_menu.events.EXIT)

    def _iniciar_juego(self):
        # 5. Efecto de desvanecimiento de la música (1.5 segundos)
        pygame.mixer.music.fadeout(1500)
        self.activo = False 

    def _ver_controles(self):
        self.mostrando_controles = True

    def ejecutar(self):
        clock = pygame.time.Clock()
        while self.activo:
            events = pygame.event.get()
            
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if self.mostrando_controles:
                    if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                        self.mostrando_controles = False
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self._iniciar_juego()

            now = pygame.time.get_ticks()
            if now - self.last_update > self.frame_speed:
                if len(self.frames) > 0:
                    self.current_frame = (self.current_frame + 1) % len(self.frames)
                self.last_update = now

            # --- DIBUJADO ---
            if self.mostrando_controles and self.img_controles:
                self.screen.blit(self.img_controles, (0, 0))
            else:
                if len(self.frames) > 0:
                    self.screen.blit(self.frames[self.current_frame], (0, 0))
                else:
                    self.screen.fill((0, 0, 0))
                
                if self.menu.is_enabled():
                    self.menu.update(events)
                    self.menu.draw(self.screen)

            pygame.display.flip()
            clock.tick(60)