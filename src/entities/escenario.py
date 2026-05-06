import pygame
import os  # <--- ESTA ES LA LÍNEA QUE FALTA

class EscenarioNivel1:
    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.frames = []
        # Corregimos la carpeta de 'audio' a 'sounds'
        self.ruta_musica = os.path.join("assets", "sounds", "TechnoJazz.mp3")
        
        try:
            for i in range(1, 6):
                nombre_archivo = f"assets/images/fondo{i}LV1.jpg"
                imagen = pygame.image.load(nombre_archivo).convert()
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