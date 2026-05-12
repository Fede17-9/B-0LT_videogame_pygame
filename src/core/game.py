"""
Módulo principal del motor del juego B-0LT.
Gestiona el bucle principal, la carga de niveles, colisiones y estados del juego.
"""

import os
import pygame
from src.utils.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, GAME_TITLE
)
from src.entities.player import Player
from src.ui.story import StoryScreen
from src.ui.tutorial import TutorialScreen
from src.entities.escenario import (
    EscenarioNivel1, EscenarioNivel2, EscenarioNivel3, EscenarioNivel4
)
from src.entities.plataforma import Plataforma
from src.entities.item import Bateria
from src.entities.puerta import Puerta
from src.entities.enemy import Enemy
from src.entities.FlyingEnemy import FlyingEnemy


class Game:
    """
    Clase principal que orquesta toda la lógica del videojuego.
    """

    def __init__(self):
        """
        Inicializa el motor del juego, carga assets y configura el estado inicial.
        """
        # Inicialización del mixer
        pygame.mixer.pre_init(44100, -16, 2, 512)
        pygame.mixer.init()

        self.screen = pygame.display.get_surface()
        if self.screen is None:
            self.screen = pygame.display.set_mode(
                (SCREEN_WIDTH, SCREEN_HEIGHT))

        pygame.display.set_caption(GAME_TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = "STORY"
        self.nivel_actual = 1

        # --- SISTEMA DE TIEMPO Y PUNTAJE ---
        self.start_ticks = 0
        self.high_score = self._cargar_max_score()
        self.score_total = 0

        # --- ENTIDADES ---
        self.player = Player()
        self.background = EscenarioNivel1(self.screen)

        self.plataformas = pygame.sprite.Group()
        self.baterias = pygame.sprite.Group()
        self.enemigos = pygame.sprite.Group()
        self._configurar_objetos_nivel_1()

        # --- GESTORES DE PANTALLAS ---
        self.story_manager = StoryScreen(self.screen, self._finalizar_historia)
        self.tutorial_manager = TutorialScreen(
            self.screen, self._finalizar_tutorial)

        # --- ANIMACIONES Y CRÉDITOS ---
        self.game_over_frames = []
        self.go_index = 0
        self.go_speed = 0.15

        self.final_frames = []
        self.final_index = 0
        self.final_speed = 0.08

        self.credits_frames = []
        self.credits_index = 0
        self.credits_speed = 0.06
        self.mostrar_creditos = False
        self.timer_final30 = 0
        self.creditos_texto_y = SCREEN_HEIGHT

        self._cargar_assets_gameover()
        self._cargar_assets_final()
        self._cargar_assets_creditos()

        self.story_manager.iniciar_musica()

    def _cargar_max_score(self):
        """
        Carga el récord histórico de tiempo desde un archivo.

        Returns:
            int: El mejor tiempo guardado o 9999 si no existe.
        """
        try:
            if os.path.exists("highscore.txt"):
                with open("highscore.txt", "r") as f:
                    contenido = f.read().strip()
                    return (int(contenido) if contenido and
                            int(contenido) > 0 else 9999)
            return 9999
        except (IOError, ValueError):
            return 9999

    def _guardar_max_score(self, nuevo_record):
        """
        Guarda un nuevo récord de tiempo en el archivo.

        Args:
            nuevo_record (int): El nuevo tiempo a guardar.
        """
        try:
            with open("highscore.txt", "w") as f:
                f.write(str(nuevo_record))
        except IOError as e:
            print(f"Error al guardar highscore: {e}")

    def _finalizar_historia(self):
        """Transiciona de la historia al tutorial."""
        self.state = "TUTORIAL"
        self.tutorial_manager.iniciar_musica()

    def _finalizar_tutorial(self):
        """Transiciona del tutorial al inicio del juego."""
        self.state = "PLAYING"
        self.start_ticks = pygame.time.get_ticks()
        pygame.mixer.music.stop()
        self.background.iniciar_musica()

    def _cargar_assets_gameover(self):
        """Carga los frames de la animación de Game Over."""
        path = os.path.join("assets", "images")
        for i in range(1, 6):
            try:
                img = pygame.image.load(
                    os.path.join(path, f"gameover{i}.jpg")).convert_alpha()
                img = pygame.transform.scale(img, (SCREEN_WIDTH, SCREEN_HEIGHT))
                self.game_over_frames.append(img)
            except pygame.error:
                pass

    def _cargar_assets_final(self):
        """Carga los frames de la animación final."""
        path = os.path.join("assets", "images", "final")
        for i in range(1, 31):
            try:
                img_path = os.path.join(path, f"final{i}.jpg")
                if os.path.exists(img_path):
                    img = pygame.image.load(img_path).convert()
                    img = pygame.transform.scale(
                        img, (SCREEN_WIDTH, SCREEN_HEIGHT))
                    self.final_frames.append(img)
            except pygame.error as e:
                print(f"Error cargando fotograma final {i}: {e}")

    def _cargar_assets_creditos(self):
        """Carga los fondos para la pantalla de créditos."""
        path = os.path.join("assets", "images", "final")
        for i in range(1, 4):
            try:
                img = pygame.image.load(
                    os.path.join(path, f"creditos{i}.jpg")).convert()
                img = pygame.transform.scale(img, (SCREEN_WIDTH, SCREEN_HEIGHT))
                self.credits_frames.append(img)
            except pygame.error:
                pass

    def _configurar_objetos_nivel_1(self):
        """Configura las plataformas, enemigos e items del Nivel 1."""
        self.plataformas.empty()
        self.enemigos.empty()
        mesa_central = Plataforma(638, 530, 160, 75)
        self.mesa_final = Plataforma(
            850, 480, 180, 95, imagen_nombre="plataforma2.png")
        self.plataformas.add(mesa_central, self.mesa_final)
        self.puerta = Puerta(940, 525)
        self.baterias.empty()
        self.score = 0
        self.baterias.add(Bateria(638, 450), Bateria(
            1150, 550), Bateria(400, 650))
        self.enemigos.add(Enemy(1150, SCREEN_HEIGHT - 110, rango=100))

    def _cargar_nivel_2(self):
        """Configura el Nivel 2."""
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
        self.baterias.add(Bateria(270, 450), Bateria(
            650, 330), Bateria(1200, 600))
        self.enemigos.empty()
        self.enemigos.add(Enemy(1000, 635, rango=60),
                          Enemy(200, 635, rango=60))
        helicotero = FlyingEnemy(600, 300, rango=200, velocidad=3)
        self.enemigos.add(helicotero)

    def _cargar_nivel_3(self):
        """Configura el Nivel 3."""
        self.nivel_actual = 3
        self.background = EscenarioNivel3(self.screen)
        self.player.rect.x = 80
        self.player.rect.y = SCREEN_HEIGHT - 160
        self.plataformas.empty()

        plats = [
            Plataforma(300, 550, 180, 35, imagen_nombre="plataforma2.png"),
            Plataforma(600, 480, 180, 35, imagen_nombre="plataforma2.png"),
            Plataforma(950, 440, 180, 35, imagen_nombre="plataforma2.png")
        ]
        # Generar plataformas de suelo
        for x in range(20, 1200, 110):
            plats.append(Plataforma(x, 675, 180, 35,
                         imagen_nombre="plataforma2.png"))

        self.plataformas.add(*plats)

        self.puerta = Puerta(1050, 480)
        self.baterias.empty()
        self.score = 0
        self.baterias.add(Bateria(400, 655), Bateria(
            600, 330), Bateria(1000, 600))

        self.enemigos.empty()
        self.enemigos.add(FlyingEnemy(400, 250, rango=150, velocidad=4))
        self.enemigos.add(FlyingEnemy(980, 250, rango=200, velocidad=3))
        self.enemigos.add(Enemy(1000, 635, rango=80), Enemy(400, 635, rango=80))

    def _cargar_nivel_4(self):
        """Configura el Nivel 4."""
        self.nivel_actual = 4
        self.background = EscenarioNivel4(self.screen)
        self.player.rect.x = 50
        self.player.rect.y = SCREEN_HEIGHT - 160
        self.plataformas.empty()

        plats = [
            Plataforma(200, 580, 150, 35, imagen_nombre="plataforma2.png"),
            Plataforma(450, 480, 150, 35, imagen_nombre="plataforma2.png"),
            Plataforma(700, 380, 150, 35, imagen_nombre="plataforma2.png")
        ]
        for x in range(20, 1200, 110):
            plats.append(Plataforma(x, 675, 180, 35,
                         imagen_nombre="plataforma2.png"))

        self.plataformas.add(*plats)

        self.puerta = Puerta(1200, 715)
        self.baterias.empty()
        self.score = 0
        self.baterias.add(Bateria(200, 500), Bateria(
            700, 300), Bateria(1100, 600))

        self.enemigos.empty()
        self.enemigos.add(Enemy(300, 635, rango=70), Enemy(
            610, 635, rango=70), Enemy(1110, 635, rango=55))
        self.enemigos.add(FlyingEnemy(300, 380, rango=250, velocidad=5))
        self.enemigos.add(FlyingEnemy(800, 170, rango=100, velocidad=4))

    def _activar_final(self):
        """Calcula el tiempo final y activa la secuencia de ending."""
        self.score_total = (pygame.time.get_ticks() - self.start_ticks) // 1000
        self.state = "ENDING"
        pygame.mixer.music.stop()
        ruta_musica_final = os.path.join("assets", "sounds", "final.mp3")
        if os.path.exists(ruta_musica_final):
            pygame.mixer.music.load(ruta_musica_final)
            pygame.mixer.music.play(0)

    def _reiniciar_juego(self):
        """Reinicia todas las variables para volver a jugar."""
        self.nivel_actual = 1
        self.player = Player()
        self.score_total = 0
        self.start_ticks = pygame.time.get_ticks()
        self.background = EscenarioNivel1(self.screen)
        self._configurar_objetos_nivel_1()
        self.state = "PLAYING"
        pygame.mixer.music.stop()
        self.background.iniciar_musica()

    def run(self):
        """Inicia el bucle principal del juego."""
        while self.running:
            self.clock.tick(FPS)
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.KEYDOWN:
                    if self.state == "GAME_OVER":
                        if event.key == pygame.K_RETURN:
                            self._reiniciar_juego()

                    elif self.state == "ENDING":
                        if event.key == pygame.K_s:
                            self.creditos_texto_y = -5000

                        if event.key == pygame.K_RETURN:
                            if self.creditos_texto_y < 0:
                                self.running = False

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
            elif self.state == "ENDING":
                self._dibujar_final()

            pygame.display.flip()

    def _handle_events(self, events):
        """Maneja eventos específicos del estado de juego."""
        for event in events:
            if event.type == pygame.KEYDOWN:
                if self.state == "PLAYING" and event.key == pygame.K_SPACE:
                    self.player.jump()

    def _update(self):
        """Actualiza toda la lógica de los objetos en juego."""
        if self.state == "PLAYING":
            self.background.actualizar()
            self.player.update(self.plataformas)

            # Límites de pantalla
            if self.player.rect.left < 0:
                self.player.rect.left = 0
            if self.player.rect.right > SCREEN_WIDTH:
                self.player.rect.right = SCREEN_WIDTH

            self.baterias.update()
            self.enemigos.update()
            self.puerta.update()

            # Colisión con enemigos
            if pygame.sprite.spritecollide(self.player, self.enemigos, False):
                self.player.recibir_danio()
                if self.player.health <= 0:
                    self.state = "GAME_OVER"
                    pygame.mixer.music.stop()
                    ruta_musica_go = os.path.join(
                        "assets", "sounds", "8BitJam.mp3")
                    if os.path.exists(ruta_musica_go):
                        pygame.mixer.music.load(ruta_musica_go)
                        pygame.mixer.music.play(-1)
                    return

            # Recolección de baterías
            col_bat = pygame.sprite.spritecollide(
                self.player, self.baterias, True)
            for _ in col_bat:
                self.score += 1

            # Lógica de la Puerta
            if self.score >= 3:
                if self.puerta.state == "BLOQUEADA":
                    self.puerta.desbloquear()

                if (self.puerta.state == "LISTA" and
                        self.player.rect.colliderect(self.puerta.rect)):
                    self.puerta.abrir()

            # Transición de niveles
            if (self.puerta.state == "ABIERTA" and
                    self.player.rect.colliderect(self.puerta.rect)):
                pygame.time.delay(100)

                if self.nivel_actual == 1:
                    self._cargar_nivel_2()
                elif self.nivel_actual == 2:
                    self._cargar_nivel_3()
                elif self.nivel_actual == 3:
                    self._cargar_nivel_4()
                elif self.nivel_actual == 4:
                    self._activar_final()
                return

    def _draw(self):
        """Renderiza todos los elementos del juego."""
        self.background.dibujar()
        self.plataformas.draw(self.screen)
        self.screen.blit(self.puerta.image, self.puerta.rect)
        self.baterias.draw(self.screen)
        self.enemigos.draw(self.screen)
        self.screen.blit(self.player.image, self.player.rect)
        self._dibujar_interfaz()

    def _dibujar_interfaz(self):
        """Dibuja la UI (vida, energía, tiempo) durante el juego."""
        segundos_pasados = (pygame.time.get_ticks() - self.start_ticks) // 1000
        font = pygame.font.SysFont("Arial", 25, bold=True)
        text_t = font.render(f"TIEMPO: {segundos_pasados}s", True, (255, 255, 0))
        self.screen.blit(text_t, (20, 20))
        color_e = (0, 255, 255) if self.score >= 3 else (255, 255, 255)
        text_e = font.render(f"ENERGÍA: {self.score}/3", True, color_e)
        self.screen.blit(text_e, (20, 50))
        text_s = font.render(
            f"B-OLT VIDA: {'I' * self.player.health}", True, (255, 50, 50))
        self.screen.blit(text_s, (20, 80))

    def _dibujar_game_over(self):
        """Renderiza la animación de fin de juego."""
        if self.game_over_frames:
            self.go_index += self.go_speed
            if self.go_index >= len(self.game_over_frames):
                self.go_index = 0
            self.screen.blit(self.game_over_frames[int(self.go_index)], (0, 0))
        else:
            self.screen.fill((0, 0, 0))

    def _dibujar_final(self):
        """Renderiza la secuencia final y los créditos."""
        if not self.final_frames:
            return
        indice_actual = int(self.final_index)

        if not self.mostrar_creditos:
            self.screen.blit(self.final_frames[indice_actual], (0, 0))
            if indice_actual < len(self.final_frames) - 1:
                # Pausas dramáticas en frames específicos
                if (indice_actual + 1) in [20, 22, 24]:
                    self.final_index += self.final_speed * 0.27
                else:
                    self.final_index += self.final_speed
            else:
                self.final_index = len(self.final_frames) - 1
                self.timer_final30 += 1
                if self.timer_final30 > 180:
                    self.mostrar_creditos = True
        else:
            if self.credits_frames:
                self.credits_index += self.credits_speed
                if self.credits_index >= len(self.credits_frames):
                    self.credits_index = 0
                self.screen.blit(
                    self.credits_frames[int(self.credits_index)], (0, 0))
            self._dibujar_texto_creditos()

    def _dibujar_texto_creditos(self):
        """Dibuja el texto de los créditos con desplazamiento vertical."""
        fuente_sub = pygame.font.SysFont("Arial", 26, bold=True)
        fuente_nombres = pygame.font.SysFont("Arial", 22)

        creditos = [
            ("DIRECCIÓN Y PRODUCCIÓN", "B-OLT: El Despertar del Sector B"),
            ("Directores del Proyecto", "Isac Velásquez / Juan Federico Pulido"),
            ("", ""),
            ("DESARROLLO TÉCNICO", ""),
            ("Programación y Lógica", "Juan Federico Pulido & Isac Velásquez"),
            ("Arquitectura de Niveles", "Isac Velásquez / Juan Federico Pulido"),
            ("", ""),
            ("ARTE Y NARRATIVA", ""),
            ("Diseño de Personajes y Arte", "Isac Velásquez"),
            ("Historia y Guion Original", "Juan Federico Pulido"),
            ("", ""),
            ("AGRADECIMIENTOS", ""),
            ("Música y Sonido", "Juan Federico Pulido"),
            ("Especiales", "A todos los que ayudaron a B-OLT")
        ]

        self.creditos_texto_y -= 0.8
        y_offset = self.creditos_texto_y

        for titulo, nombres in creditos:
            txt_t = fuente_sub.render(titulo, True, (0, 255, 255))
            txt_n = fuente_nombres.render(nombres, True, (255, 255, 255))
            self.screen.blit(txt_t, (SCREEN_WIDTH // 2 + 50, y_offset))
            self.screen.blit(txt_n, (SCREEN_WIDTH // 2 + 50, y_offset + 30))
            y_offset += 90

        if y_offset < 0:
            self._pantalla_despedida_final()
        else:
            msg = "Presiona S para saltar"
            skip_txt = fuente_nombres.render(msg, True, (150, 150, 150))
            self.screen.blit(skip_txt, (20, SCREEN_HEIGHT - 40))

    def _pantalla_despedida_final(self):
        """Muestra el mensaje final y el récord histórico."""
        self.screen.blit(self.final_frames[-1], (0, 0))
        f = pygame.font.SysFont("Arial", 30, bold=True)
        f_small = pygame.font.SysFont("Arial", 25)

        if self.score_total < self.high_score:
            msg_record = f"¡NUEVO RÉCORD DE TIEMPO: {self.score_total}s!"
            color_score = (0, 255, 0)
            self._guardar_max_score(self.score_total)
        else:
            msg_record = f"Mejor Tiempo Histórico: {self.high_score}s"
            color_score = (255, 255, 255)

        txt_puntos = f_small.render(
            f"Tu Tiempo: {self.score_total} segundos", True, (255, 255, 255))
        txt_record = f_small.render(msg_record, True, color_score)
        t = f.render("FIN DE LA TRANSMISIÓN - ENTER PARA SALIR",
                     True, (255, 255, 255))

        r = t.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        rp = txt_puntos.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
        rr = txt_record.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))

        self.screen.blit(t, r)
        self.screen.blit(txt_puntos, rp)
        self.screen.blit(txt_record, rr)
