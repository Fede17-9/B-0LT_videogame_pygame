import pygame
import os
import sys

class TutorialScreen:
    def __init__(self, screen, next_state_callback):
        self.screen = screen
        self.on_finished = next_state_callback
        
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.img_dir = os.path.join(current_dir, "..", "..", "assets", "images")
        self.sound_dir = os.path.join(current_dir, "..", "..", "assets", "sounds") # Ruta de sonidos
        
        # 1. Cargar las 4 imágenes del tutorial
        self.frames = []
        for i in range(1, 5):
            path = os.path.join(self.img_dir, f'tutorial{i}.jpg')
            if os.path.exists(path):
                img = pygame.image.load(path).convert()
                img = pygame.transform.scale(img, (screen.get_width(), screen.get_height()))
                self.frames.append(img)
            else:
                print(f"Error: No se encontró {path}")

        self.current_frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_speed = 500  
        self.running = True

        # Configuración de fuente pixelada
        self.font = pygame.font.SysFont("Arial", 24) 
        font_path = os.path.join(current_dir, "..", "..", "assets", "fonts", "PixelFont.ttf")
        if os.path.exists(font_path):
            self.font = pygame.font.Font(font_path, 20)

    def iniciar_musica(self):
        """Método para arrancar la melodía del tutorial"""
        path_musica = os.path.join(self.sound_dir, 'tutorial.mp3')
        if os.path.exists(path_musica):
            pygame.mixer.music.load(path_musica)
            pygame.mixer.music.set_volume(0.3) # Volumen suave para no distraer
            pygame.mixer.music.play(-1)        # En bucle
        else:
            print(f"Aviso: No se encontró {path_musica}")

    def actualizar(self, events):
        # Animación de las imágenes
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_speed:
            if len(self.frames) > 0:
                self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.last_update = now

        # Manejo de eventos
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # Desvanecer música antes de entrar al laberinto
                    pygame.mixer.music.fadeout(1000) 
                    self.on_finished() 

    def dibujar(self):
        if len(self.frames) > 0:
            self.screen.blit(self.frames[self.current_frame], (0, 0))
        else:
            self.screen.fill((0, 0, 0))

        # Dibujar frase con parpadeo
        texto = self.font.render("OPRIME ENTER PARA JUGAR", True, (130, 255, 130))
        rect_texto = texto.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() - 50))
        
        if (pygame.time.get_ticks() // 500) % 2 == 0:
            self.screen.blit(texto, rect_texto)