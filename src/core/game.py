import pygame
import sys
import os
from src.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, COLOR_BG, GAME_TITLE, COLOR_PRIMARY
from src.entities.player import Player
from src.ui.story import StoryScreen
from src.ui.tutorial import TutorialScreen
from src.entities.escenario import EscenarioNivel1, EscenarioNivel2 
from src.entities.plataforma import Plataforma
from src.entities.item import Bateria 
from src.entities.puerta import Puerta 
from src.entities.enemy import Enemy 

class Game:
    def __init__(self):
        # Inicialización del mixer
        pygame.mixer.pre_init(44100, -16, 2, 512)
        pygame.mixer.init()

        self.screen = pygame.display.get_surface()
        if self.screen is None:
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
            
        pygame.display.set_caption(GAME_TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = "STORY" 
        self.nivel_actual = 1

        # --- ENTIDADES ---
        self.player = Player()
        self.background = EscenarioNivel1(self.screen) 
        
        self.plataformas = pygame.sprite.Group()
        self.baterias = pygame.sprite.Group()
        self.enemigos = pygame.sprite.Group() 
        self._configurar_objetos_nivel_1()

        # --- GESTORES DE PANTALLAS ---
        self.story_manager = StoryScreen(self.screen, self._finalizar_historia)
        self.tutorial_manager = TutorialScreen(self.screen, self._finalizar_tutorial)
        
        # --- ANIMACIÓN GAME OVER ---
        self.game_over_frames = []
        self.go_index = 0
        self.go_speed = 0.15 
        self._cargar_assets_gameover()

        # Música inicial
        self.story_manager.iniciar_musica()

    def _finalizar_historia(self):
        self.state = "TUTORIAL"
        self.tutorial_manager.iniciar_musica()

    def _finalizar_tutorial(self):
        self.state = "PLAYING"
        pygame.mixer.music.stop()
        self.background.iniciar_musica()

    def _cargar_nivel_2(self):
        """Configuración del Sector B."""
        print("Accediendo al Sector B...")
        self.nivel_actual = 2
        self.background = EscenarioNivel2(self.screen) 
        self.player.rect.x = 80 
        self.player.rect.y = SCREEN_HEIGHT - 160
        
        self.plataformas.empty()
        p1 = Plataforma(270, 625, 180, 35, imagen_nombre="plataforma2.png")
        p2 = Plataforma(600, 480, 180, 35, imagen_nombre="plataforma2.png")
        p3 = Plataforma(800, 370, 180, 35, imagen_nombre="plataforma2.png")
        self.plataformas.add(p1, p2, p3)

        self.puerta = Puerta(900, 410) 
        self.baterias.empty()
        self.score = 0
        self.baterias.add(Bateria(270, 450), Bateria(650, 330), Bateria(1200, 600))
        self.enemigos.empty()
        # Enemigo del Sector B con rango controlado para no caerse
        self.enemigos.add(Enemy(1000, 635, rango=60),Enemy(200, 635, rango=60) )

    def _cargar_assets_gameover(self):
        path = os.path.join("assets", "images")
        for i in range(1, 6):
            try:
                img = pygame.image.load(os.path.join(path, f"gameover{i}.jpg")).convert_alpha()
                img = pygame.transform.scale(img, (SCREEN_WIDTH, SCREEN_HEIGHT))
                self.game_over_frames.append(img)
            except:
                pass

    def _configurar_objetos_nivel_1(self):
        self.plataformas.empty()
        self.enemigos.empty()
        mesa_central = Plataforma(638, 530, 160, 75)
        self.mesa_final = Plataforma(850, 480, 180, 95, imagen_nombre="plataforma2.png")
        self.plataformas.add(mesa_central, self.mesa_final)
        self.puerta = Puerta(940, 525) 
        self.baterias.empty()
        self.score = 0 
        self.baterias.add(Bateria(638, 450), Bateria(1150, 550), Bateria(400, 650))
        self.enemigos.add(Enemy(1150, SCREEN_HEIGHT - 110, rango=100))

    def _reiniciar_juego(self):
        self.nivel_actual = 1
        self.player = Player()
        self.background = EscenarioNivel1(self.screen)
        self._configurar_objetos_nivel_1()
        self.state = "PLAYING"
        pygame.mixer.music.stop()
        self.background.iniciar_musica()

    def run(self):
        while self.running:
            self.clock.tick(FPS) 
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                if self.state == "GAME_OVER":
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        self._reiniciar_juego()

            if self.state == "STORY":
                self.story_manager.actualizar(events)
                self.story_manager.dibujar()
            elif self.state == "TUTORIAL":
                self.tutorial_manager.actualizar(events)
                self.tutorial_manager.dibujar()
            elif self.state == "PLAYING":
                self._handle_events(events)
                self._update() 
                self._draw()
            elif self.state == "GAME_OVER":
                self._dibujar_game_over()
            pygame.display.flip()

    def _handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if self.state == "PLAYING" and event.key == pygame.K_SPACE:
                    self.player.jump()

    def _update(self):
        if self.state == "PLAYING":
            self.background.actualizar() 
            self.player.update(self.plataformas)

            # --- LIMITAR B-OLT A LOS BORDES CON RESPUESTA INMEDIATA ---
            if self.player.rect.left < 0:
                self.player.rect.left = 0
                if hasattr(self.player, 'vel_x'): self.player.vel_x = 0
            
            if self.player.rect.right > SCREEN_WIDTH:
                self.player.rect.right = SCREEN_WIDTH
                if hasattr(self.player, 'vel_x'): self.player.vel_x = 0
            # ---------------------------------------------------------

            self.baterias.update()
            self.enemigos.update() 
            self.puerta.update() 

            col_enemigo = pygame.sprite.spritecollide(self.player, self.enemigos, False)
            if col_enemigo:
                self.player.recibir_danio()
                if self.player.health <= 0:
                    self.state = "GAME_OVER"
                    self.go_index = 0
                    pygame.mixer.music.stop()
                    ruta_musica_go = os.path.join("assets", "sounds", "8BitJam.mp3")
                    if os.path.exists(ruta_musica_go):
                        pygame.mixer.music.load(ruta_musica_go)
                        pygame.mixer.music.play(-1)
                    return

            colisiones_bat = pygame.sprite.spritecollide(self.player, self.baterias, False)
            for bat in colisiones_bat:
                self.score += 1
                bat.recolectar() 
            
            if self.score >= 3:
                if self.puerta.state == "BLOQUEADA":
                    self.puerta.desbloquear()
                if self.puerta.state == "LISTA" and self.player.rect.colliderect(self.puerta.rect):
                    self.puerta.abrir()

            if self.puerta.state == "ABIERTA" and self.player.rect.colliderect(self.puerta.rect):
                if self.nivel_actual == 1:
                    self._cargar_nivel_2()
                else:
                    self.running = False

    def _draw(self):
        if self.state == "PLAYING":
            self.background.dibujar() 
            self.plataformas.draw(self.screen)
            self.screen.blit(self.puerta.image, self.puerta.rect)
            self.baterias.draw(self.screen)
            self.enemigos.draw(self.screen)
            self.screen.blit(self.player.image, self.player.rect)
            self._dibujar_interfaz()

    def _dibujar_interfaz(self):
        font = pygame.font.SysFont("Arial", 25, bold=True)
        color_e = (0, 255, 255) if self.score >= 3 else (255, 255, 255)
        text_e = font.render(f"ENERGÍA: {self.score}/3", True, color_e)
        self.screen.blit(text_e, (20, 20))
        salud_color = (255, 50, 50)
        corazones = "I" * self.player.health
        text_s = font.render(f"B-OLT VIDA: {corazones}", True, salud_color)
        self.screen.blit(text_s, (20, 50))

    def _dibujar_game_over(self):
        if self.game_over_frames:
            self.go_index += self.go_speed
            if self.go_index >= len(self.game_over_frames):
                self.go_index = 0
            frame_actual = self.game_over_frames[int(self.go_index)]
            self.screen.blit(frame_actual, (0, 0))
        else:
            self.screen.fill((0, 0, 0))