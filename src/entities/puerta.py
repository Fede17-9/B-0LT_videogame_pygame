import pygame
import os

class Puerta(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # --- AUDIO ---
        ruta_sonido = os.path.join("assets", "sounds", "puerta.mp3")
        try:
            self.sonido_puerta = pygame.mixer.Sound(ruta_sonido)
        except:
            self.sonido_puerta = None

        # --- IMAGEN ---
        self.sheet = pygame.image.load("assets/images/puerta.PNG").convert_alpha()
        self.frames = []
        ancho_frame = self.sheet.get_width() / 5 
        alto_total = self.sheet.get_height()
        
        for i in range(5):
            rect = pygame.Rect(int(i * ancho_frame), 0, int(ancho_frame), alto_total)
            frame = self.sheet.subsurface(rect)
            self.frames.append(pygame.transform.scale(frame, (120, 200)))

        self.frame_index = 0
        self.state = "BLOQUEADA" 
        self.anim_speed = 0.15 # Asegúrate de tener definida esta variable
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x, y)

    def desbloquear(self):
        if self.state == "BLOQUEADA":
            self.state = "LISTA"
            self.frame_index = 1 

    def abrir(self):
        if self.state != "ABIERTA":
            self.state = "ABIERTA"
            if self.sonido_puerta:
                self.sonido_puerta.play()

    def update(self):
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