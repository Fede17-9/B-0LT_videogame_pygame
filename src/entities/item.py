import pygame
import os

class Bateria(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        ruta_sonido = os.path.join("assets", "sounds", "bateria.mp3")
        try:
            self.sonido_recolectar = pygame.mixer.Sound(ruta_sonido)
            self.sonido_recolectar.set_volume(0.6)
        except:
            print("No se pudo cargar bateria.mp3")
            self.sonido_recolectar = None

        # --- IMAGEN ---
        try:
            self.sheet = pygame.image.load("assets/images/bateria.png").convert_alpha()
        except pygame.error:
            self.sheet = pygame.Surface((320, 40))
            self.sheet.fill((0, 255, 0))

        self.frames = []
        ancho_frame = self.sheet.get_width() // 8
        alto_total = self.sheet.get_height()
        
        for i in range(8):
            rect_recorte = pygame.Rect(i * ancho_frame, 0, ancho_frame, alto_total)
            frame = self.sheet.subsurface(rect_recorte)
            self.frames.append(pygame.transform.scale(frame, (50, 80)))
            
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x, y)
        self.anim_speed = 0.15 

    def recolectar(self):
        if self.sonido_recolectar:
            self.sonido_recolectar.play()
        self.kill() # Elimina el sprite del grupo

    def update(self):
        self.frame_index += self.anim_speed
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]