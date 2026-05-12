<<<<<<< HEAD
"""
Módulo que define las clases para los escenarios de los diferentes niveles.
Utiliza una clase base para gestionar la animación de fondos y la música.
"""

import os
import pygame


class BaseEscenario:
    """
    Clase base para gestionar fondos animados y música de nivel.
    """

    def __init__(self, pantalla, prefijo_fondo, num_frames, color_filtro,
                 velocidad_animacion=150, ruta_musica=None):
        """
        Inicializa el escenario base.

        Args:
            pantalla (pygame.Surface): La superficie de la pantalla.
            prefijo_fondo (str): Prefijo del nombre de archivo de fondo.
            num_frames (int): Número de frames de animación.
            color_filtro (tuple): Color RGBA para el filtro de oscuridad.
            velocidad_animacion (int): Milisegundos entre frames.
            ruta_musica (str): Ruta al archivo de música.
        """
        self.pantalla = pantalla
        self.frames = []
        self.ruta_musica = ruta_musica

        try:
            for i in range(1, num_frames + 1):
                nombre_archivo = f"assets/images/{prefijo_fondo}{i}.jpg"
                if not os.path.exists(nombre_archivo):
                    # Reintentar con otro patrón común si falla
                    nombre_archivo = f"assets/images/{prefijo_fondo}{i}.jpg"

                imagen = pygame.image.load(nombre_archivo).convert()
                imagen = pygame.transform.scale(
                    imagen, (pantalla.get_width(), pantalla.get_height()))

                # Aplicar filtro de atmósfera
                filtro = pygame.Surface(imagen.get_size()).convert_alpha()
                filtro.fill(color_filtro)
                imagen.blit(filtro, (0, 0))
                self.frames.append(imagen)

        except (pygame.error, FileNotFoundError) as e:
            print(f"Error al cargar los fondos {prefijo_fondo}: {e}")
            self.frames = [pygame.Surface((pantalla.get_width(),
                                           pantalla.get_height()))]
            self.frames[0].fill((30, 30, 30))

        self.indice_actual = 0
        self.ultima_actualizacion = pygame.time.get_ticks()
        self.velocidad_animacion = velocidad_animacion

    def iniciar_musica(self):
        """
        Carga e inicia la reproducción de la música del nivel.
        """
        if not self.ruta_musica or not os.path.exists(self.ruta_musica):
            return
        try:
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
            pygame.mixer.music.load(self.ruta_musica)
            pygame.mixer.music.set_volume(1.0)
            pygame.mixer.music.play(-1)
        except (pygame.error, Exception) as e:
            print(f"Error al reproducir música: {e}")

    def actualizar(self):
        """
        Actualiza el frame de animación del fondo.
        """
        tiempo_ahora = pygame.time.get_ticks()
        if (tiempo_ahora - self.ultima_actualizacion >
                self.velocidad_animacion):
            self.indice_actual = (self.indice_actual + 1) % len(self.frames)
            self.ultima_actualizacion = tiempo_ahora

    def dibujar(self):
        """
        Dibuja el fondo actual en la pantalla.
        """
        self.pantalla.blit(self.frames[self.indice_actual], (0, 0))


class EscenarioNivel1(BaseEscenario):
    """Escenario para el Nivel 1."""

    def __init__(self, pantalla):
        ruta_musica = os.path.join("assets", "sounds", "TechnoJazz.mp3")
        super().__init__(
            pantalla,
            prefijo_fondo="fondo",
            num_frames=5,
            color_filtro=(0, 0, 0, 140),
            ruta_musica=ruta_musica
        )

    def _corregir_nombres(self):
        # Sobreescribir para manejar el sufijo LV1 si es necesario
        pass

    # Re-implementamos el constructor para manejar los nombres específicos
    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.frames = []
        self.ruta_musica = os.path.join("assets", "sounds", "TechnoJazz.mp3")
=======
import pygame
import os  # <--- ESTA ES LA LÍNEA QUE FALTA

class EscenarioNivel1:
    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.frames = []
        # Corregimos la carpeta de 'audio' a 'sounds'
        self.ruta_musica = os.path.join("assets", "sounds", "TechnoJazz.mp3")
        
>>>>>>> f5d0c78a63262b0423309515dd3bfe18dae89ce1
        try:
            for i in range(1, 6):
                nombre_archivo = f"assets/images/fondo{i}LV1.jpg"
                imagen = pygame.image.load(nombre_archivo).convert()
<<<<<<< HEAD
                imagen = pygame.transform.scale(
                    imagen, (pantalla.get_width(), pantalla.get_height()))
                filtro = pygame.Surface(imagen.get_size()).convert_alpha()
                filtro.fill((0, 0, 0, 140))
                imagen.blit(filtro, (0, 0))
                self.frames.append(imagen)
        except pygame.error:
            self.frames = [pygame.Surface((pantalla.get_width(),
                                           pantalla.get_height()))]
            self.frames[0].fill((30, 30, 30))
        self.indice_actual = 0
        self.ultima_actualizacion = pygame.time.get_ticks()
        self.velocidad_animacion = 150


class EscenarioNivel2(BaseEscenario):
    """Escenario para el Nivel 2."""

    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.frames = []
        try:
            for i in range(1, 7):
                nombre_archivo = f"assets/images/fondo{i}LV2.jpg"
                imagen = pygame.image.load(nombre_archivo).convert()
                imagen = pygame.transform.scale(
                    imagen, (pantalla.get_width(), pantalla.get_height()))
                filtro = pygame.Surface(imagen.get_size()).convert_alpha()
                filtro.fill((10, 20, 40, 130))
                imagen.blit(filtro, (0, 0))
                self.frames.append(imagen)
        except pygame.error:
            self.frames = [pygame.Surface((pantalla.get_width(),
                                           pantalla.get_height()))]
            self.frames[0].fill((10, 20, 30))
        self.indice_actual = 0
        self.ultima_actualizacion = pygame.time.get_ticks()
        self.velocidad_animacion = 180


class EscenarioNivel3(BaseEscenario):
    """Escenario para el Nivel 3."""

    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.frames = []
        try:
            for i in range(1, 7):
                nombre_archivo = f"assets/images/fondo{i}LV3.jpg"
                imagen = pygame.image.load(nombre_archivo).convert()
                imagen = pygame.transform.scale(
                    imagen, (pantalla.get_width(), pantalla.get_height()))
                filtro = pygame.Surface(imagen.get_size()).convert_alpha()
                filtro.fill((5, 5, 15, 160))
                imagen.blit(filtro, (0, 0))
                self.frames.append(imagen)
        except pygame.error:
            self.frames = [pygame.Surface((pantalla.get_width(),
                                           pantalla.get_height()))]
            self.frames[0].fill((5, 5, 10))
        self.indice_actual = 0
        self.ultima_actualizacion = pygame.time.get_ticks()
        self.velocidad_animacion = 120


class EscenarioNivel4(BaseEscenario):
    """Escenario para el Nivel 4."""

    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.frames = []
        try:
            for i in range(1, 6):
                nombre_archivo = f"assets/images/fondo{i}LV4.jpg"
                imagen = pygame.image.load(nombre_archivo).convert()
                imagen = pygame.transform.scale(
                    imagen, (pantalla.get_width(), pantalla.get_height()))
                filtro = pygame.Surface(imagen.get_size()).convert_alpha()
                filtro.fill((20, 5, 5, 150))
                imagen.blit(filtro, (0, 0))
                self.frames.append(imagen)
        except pygame.error:
            self.frames = [pygame.Surface((pantalla.get_width(),
                                           pantalla.get_height()))]
            self.frames[0].fill((20, 10, 10))
        self.indice_actual = 0
        self.ultima_actualizacion = pygame.time.get_ticks()
        self.velocidad_animacion = 140
=======
                imagen = pygame.transform.scale(imagen, (pantalla.get_width(), pantalla.get_height()))
                
                filtro = pygame.Surface(imagen.get_size()).convert_alpha()
                filtro.fill((0, 0, 0, 140)) 
                imagen.blit(filtro, (0, 0))
                self.frames.append(imagen)
                
        except pygame.error as e:
            print(f"Error al cargar los fondos LV1: {e}")
            self.frames = [pygame.Surface((pantalla.get_width(), pantalla.get_height()))]
            self.frames[0].fill((30, 30, 30))

        self.indice_actual = 0
        self.ultima_actualizacion = pygame.time.get_ticks()
        self.velocidad_animacion = 150 

    def iniciar_musica(self):
        print(f"--- Intento de reproducción: {self.ruta_musica} ---")
        
        if not os.path.exists(self.ruta_musica):
            print(f"CRÍTICO: No se encuentra el archivo en: {os.path.abspath(self.ruta_musica)}")
            return

        try:
            # 1. Detenemos cualquier rastro de audio previo para liberar el canal
            pygame.mixer.music.stop()
            pygame.mixer.music.unload() 
            
            # 2. Cargamos el archivo
            pygame.mixer.music.load(self.ruta_musica)
            
            # 3. Forzamos el volumen (a veces se queda en 0.0 internamente)
            pygame.mixer.music.set_volume(1.0) 
            
            # 4. Reproducir en bucle
            pygame.mixer.music.play(-1)
            
            # 5. Verificación final
            if pygame.mixer.music.get_busy():
                print(">>> ÉXITO: El mixer informa que la música está sonando.")
            else:
                print(">>> AVISO: El mixer cargó el archivo pero NO hay actividad de sonido.")
                
        except Exception as e:
            print(f"Error fatal al reproducir música: {e}")

    def actualizar(self):
        tiempo_ahora = pygame.time.get_ticks()
        if tiempo_ahora - self.ultima_actualizacion > self.velocidad_animacion:
            self.indice_actual = (self.indice_actual + 1) % len(self.frames)
            self.ultima_actualizacion = tiempo_ahora

    def dibujar(self):
        self.pantalla.blit(self.frames[self.indice_actual], (0, 0))

# --- NUEVA CLASE PARA EL NIVEL 2 ---
class EscenarioNivel2:
    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.frames = []
        
        try:
            # Aquí usamos el rango hasta 7 (para cargar fondo1LV2 hasta fondo6LV2)
            for i in range(1, 7):
                nombre_archivo = f"assets/images/fondo{i}LV2.jpg"
                imagen = pygame.image.load(nombre_archivo).convert()
                imagen = pygame.transform.scale(imagen, (pantalla.get_width(), pantalla.get_height()))
                
                # FILTRO PERSONALIZADO PARA NIVEL 2 (Más frío/azulado)
                filtro = pygame.Surface(imagen.get_size()).convert_alpha()
                # Usamos un azul muy oscuro (10, 20, 40) en lugar de negro puro
                filtro.fill((10, 20, 40, 130)) 
                
                imagen.blit(filtro, (0, 0))
                self.frames.append(imagen)
                
        except pygame.error as e:
            print(f"Error al cargar los fondos LV2: {e}")
            self.frames = [pygame.Surface((pantalla.get_width(), pantalla.get_height()))]
            self.frames[0].fill((10, 20, 30)) # Azul oscuro por si falla

        self.indice_actual = 0
        self.ultima_actualizacion = pygame.time.get_ticks()
        # Puedes hacer que el laboratorio "palpite" más rápido o lento ajustando esto:
        self.velocidad_animacion = 180 

    def actualizar(self):
        tiempo_ahora = pygame.time.get_ticks()
        if tiempo_ahora - self.ultima_actualizacion > self.velocidad_animacion:
            self.indice_actual = (self.indice_actual + 1) % len(self.frames)
            self.ultima_actualizacion = tiempo_ahora

    def dibujar(self):
        self.pantalla.blit(self.frames[self.indice_actual], (0, 0))
>>>>>>> f5d0c78a63262b0423309515dd3bfe18dae89ce1
