import pygame
import random
import os
import math
from PIL import Image, ImageSequence # Importa a biblioteca Pillow

# --- Constantes do Jogo ---
# (O restante das suas constantes permaneceria aqui, igual ao arquivo original)
# Tamanho da tela
WIDTH, HEIGHT = 900, 500
SCREEN_TITLE = "Doctor Stone Game - Versão Melhorada"

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ORANGE = (255, 100, 0)
RED = (255, 0, 0)
GREEN = (0, 200, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255) 
TRANSPARENT_RED = (255, 0, 0, 100)

# Velocidades
PLAYER_VEL = 5
FIREBALL_SPEED = 12
BACKGROUND_SCROLL_SPEED = 1 
MONKEY_SPEED_BASE = 2
BOAR_SPEED_BASE = 2.7
GIANT_SPEED_BASE = 1

# Cooldowns e Durações
FIREBALL_COOLDOWN_BASE = 500
RAPID_FIRE_DURATION = 5000
DAMAGE_INVULNERABILITY_TIME = 1500
EXPLOSION_DURATION = 300
FLOATING_TEXT_DURATION = 1200
COMBO_RESET_TIME = 1500
SUPER_STRENGTH_DURATION = 7000 
FIREBALL_BASE_DAMAGE = 2
SUPER_STRENGTH_DAMAGE_MULTIPLIER = 2

# Caminhos das imagens (diretamente do diretório do script)
BACKGROUND_IMG_PATH = "background.png" # Alterado para .jpg
SENKU_IMG_PATH = "senku.png"
FIREBALL_RIGHT_IMG_PATH = "fireball.png"
FIREBALL_LEFT_IMG_PATH = "fireball.png" 
MONKEY_IMG_PATH = "monkey.png"
BOAR_IMG_PATH = "boar.png"
GIANT_IMG_PATH = "giant.png"
SENKU_STONE_IMG_PATH = "senku_stone.png"
RAPID_FIRE_POWERUP_IMG_PATH = "coca.png"
BANANA_POWERUP_IMG_PATH = "banana.png"
SUPER_STRENGTH_POWERUP_IMG_PATH = "muscle.png" 
LOAD_SCREEN_GIF_PATH = "load_screen.gif"

# Tamanhos dos elementos
PLAYER_SIZE = (150, 150)
FIREBALL_SIZE = (70, 70)
MONKEY_SIZE = (70, 70)
BOAR_SIZE = (90, 90)
GIANT_SIZE = (120, 120)
ITEM_SIZE = (50, 50)
EXPLOSION_SIZE = (100, 100)
PARTICLE_SIZE = 5

# Pontuações
SCORE_MONKEY = 10
SCORE_BOAR = 25
SCORE_GIANT = 75
SCORE_SENKU_STONE = 50
SCORE_BANANA = 30

# Dano dos Inimigos
MONKEY_DAMAGE = 1
BOAR_DAMAGE = 1
GIANT_DAMAGE = 2

# Vidas
MAX_LIVES = 5

# Configurações das Fases (AJUSTADO PARA MELHOR GAMEPLAY)
### PHASES: Aqui você define 'target_defeated' para cada fase.
# Configurações das Fases (AJUSTADO PARA MELHOR GAMEPLAY E MAIOR DURAÇÃO)
PHASES = {
    1: {"monkeys": 4, "boars": 0, "giants": 0, "items": 1, 
        "target_defeated": 10,  # Aumentado de 6 para 10 (mais inimigos para derrotar)
        "spawn_freq_min": 1800,  # Aumentado de 1300 (inimigos aparecem um pouco mais devagar)
        "spawn_freq_max": 3500,  # Aumentado de 2800 (intervalo maior para ظهور de inimigos)
        "monkey_speed_multiplier": 1.0, "boar_speed_multiplier": 1.0, "giant_speed_multiplier": 1.0},
    2: {"monkeys": 5, "boars": 2, "giants": 0, "items": 1, 
        "target_defeated": 15,  # Aumentado de 8 para 15
        "spawn_freq_min": 1500,  # Aumentado de 1100
        "spawn_freq_max": 3000,  # Aumentado de 2500
        "monkey_speed_multiplier": 1.1, "boar_speed_multiplier": 1.05, "giant_speed_multiplier": 1.0},
    # ... você pode aplicar ajustes semelhantes para as outras fases (3, 4, 5)
    3: {"monkeys": 6, "boars": 3, "giants": 1, "items": 2, 
        "target_defeated": 18, # Exemplo: aumentado de 12
        "spawn_freq_min": 1200, # Exemplo: aumentado de 900
        "spawn_freq_max": 2800, # Exemplo: aumentado de 2200
        "monkey_speed_multiplier": 1.2, "boar_speed_multiplier": 1.1, "giant_speed_multiplier": 1.05},
    4: {"monkeys": 7, "boars": 4, "giants": 2, "items": 2, 
        "target_defeated": 22, # Exemplo: aumentado de 15
        "spawn_freq_min": 1000, # Exemplo: aumentado de 800
        "spawn_freq_max": 2500, # Exemplo: aumentado de 2000
        "monkey_speed_multiplier": 1.3, "boar_speed_multiplier": 1.15, "giant_speed_multiplier": 1.1},
    5: {"monkeys": 8, "boars": 5, "giants": 3, "items": 3, 
        "target_defeated": 30, # Exemplo: aumentado de 20
        "spawn_freq_min": 900,  # Exemplo: aumentado de 700
        "spawn_freq_max": 2200, # Exemplo: aumentado de 1800
        "monkey_speed_multiplier": 1.45, "boar_speed_multiplier": 1.25, "giant_speed_multiplier": 1.2}
}

ITEM_SPAWN_INTERVAL_MIN = 4000 
ITEM_SPAWN_INTERVAL_MAX = 8000

# --- Constantes para Cenas de Diálogo ---
DIALOGUE_GIF_SIZE = (200, 200)
DIALOGUE_BOX_HEIGHT = 120

# --- Recursos dos Diálogos por Fase ---
DIALOGUES_RESOURCES = {
      1: {
        "char1_gif_path": "senku-falando.gif", 
        "char2_gif_path": "kohaku.gif", 
        "audio_path": "dialogue_phase1.ogg",  
        "script": [
            {"char": 1, "text": "Senku: Finalmente! Hora de começar a coletar ciência!"},
            {"char": 2, "text": "Kohaku: Não se esqueça dos perigos, Senku. Macacos e javalis por toda parte."},
            {"char": 1, "text": "Senku: Kukuku, com minhas invenções, estaremos dez bilhões por cento seguros!"},
            {"char": 2, "text": "Kohaku: Mas como vamos começar????? "},
            {"char": 1, "text": "Senku: Não se preocupe, Kohaku! Vamos usar a minha mais nova invenção"},
            {"char": 2, "text": "Kohaku: O que é essa sua nova invenção?"},
            {"char": 1, "text": "Senku: É uma maquina que nos ira ajudar a salvar o mundo!"},
            {"char": 2, "text": "Kohaku: Isso parece incrível! Vamos lá!"},
            {"char": 1, "text": "Senku: Sim! Vamos começar a aventura!"}

        ]
    },
   2: { 
        "char1_gif_path": "char1_phase2.gif",
        "char2_gif_path": "char2_phase2.gif",
        "audio_path": "dialogue_phase2.ogg",
        "script": [
            {"char": 1, "text": "Texto da fase 2, personagem 1."},
            {"char": 2, "text": "Texto da fase 2, personagem 2."},
        ]
    }
} 

# --- Inicialização do Pygame ---
pygame.init()
pygame.mixer.init()

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(SCREEN_TITLE)
FONT = pygame.font.SysFont("comicsans", 36)
BIG_FONT = pygame.font.SysFont("comicsans", 72)
SMALL_FONT = pygame.font.SysFont("comicsans", 24)

# --- Carregamento e Escalonamento de Imagens ---
# (Suas funções load_and_scale_image e load_gif_frames e o carregamento de recursos permaneceriam aqui)
def load_and_scale_image(path, size=None):
    if not os.path.exists(path):
        print(f"Erro: Imagem não encontrada em {path}. Usando placeholder.")
        placeholder = pygame.Surface(size if size else (50, 50), pygame.SRCALPHA)
        if "fireball" in path: placeholder.fill(ORANGE)
        elif "monkey" in path or "boar" in path or "giant" in path: placeholder.fill(RED)
        else: placeholder.fill(GREEN)
        return placeholder
    try:
        img = pygame.image.load(path)
        if path.lower().endswith('.png'): 
            img = img.convert_alpha()
        else:
            img = img.convert() 
        if size:
            img = pygame.transform.scale(img, size)
        return img
    except pygame.error as e:
        print(f"Erro ao carregar imagem {path}: {e}. Usando placeholder.")
        placeholder = pygame.Surface(size if size else (50, 50), pygame.SRCALPHA)
        placeholder.fill(BLUE) 
        return placeholder

def load_gif_frames(gif_path, size=None):
    frames = []
    if not os.path.exists(gif_path):
        print(f"Erro: GIF não encontrado em {gif_path}. Retornando placeholder.")
        placeholder_surface = pygame.Surface(size if size else (50,50), pygame.SRCALPHA)
        placeholder_surface.fill((100,100,100, 128))
        if size: pygame.draw.rect(placeholder_surface, WHITE, (0,0,size[0],size[1]), 2)
        frames.append(placeholder_surface)
        return frames
    try:
        gif = Image.open(gif_path)
        for frame in ImageSequence.Iterator(gif):
            frame = frame.convert("RGBA")
            pygame_frame = pygame.image.fromstring(frame.tobytes(), frame.size, frame.mode)
            if size: pygame_frame = pygame.transform.scale(pygame_frame, size)
            frames.append(pygame_frame)
    except Exception as e:
        print(f"Erro ao carregar o GIF {gif_path}: {e}. Usando placeholder.")
        placeholder_surface = pygame.Surface(size if size else (50,50), pygame.SRCALPHA)
        placeholder_surface.fill((100,100,100, 128))
        if size: pygame.draw.rect(placeholder_surface, WHITE, (0,0,size[0],size[1]), 2)
        frames.append(placeholder_surface)
        return frames
    if not frames:
        print(f"Nenhum frame carregado do GIF {gif_path}. Usando placeholder.")
        placeholder_surface = pygame.Surface(size if size else (50,50), pygame.SRCALPHA)
        placeholder_surface.fill((100,100,100, 128))
        if size: pygame.draw.rect(placeholder_surface, WHITE, (0,0,size[0],size[1]), 2)
        frames.append(placeholder_surface)
    return frames

BACKGROUND_IMG = load_and_scale_image(BACKGROUND_IMG_PATH, (WIDTH, HEIGHT))
SENKU_IMG_ORIGINAL = load_and_scale_image(SENKU_IMG_PATH, PLAYER_SIZE)
FIREBALL_IMG_RIGHT = load_and_scale_image(FIREBALL_RIGHT_IMG_PATH, FIREBALL_SIZE)
FIREBALL_IMG_LEFT = load_and_scale_image(FIREBALL_LEFT_IMG_PATH, FIREBALL_SIZE)
if FIREBALL_IMG_LEFT.get_width() <= 50 and FIREBALL_IMG_LEFT.get_height() <=50 : 
    FIREBALL_IMG_LEFT = pygame.transform.flip(FIREBALL_IMG_RIGHT, True, False)
MONKEY_IMG = load_and_scale_image(MONKEY_IMG_PATH, MONKEY_SIZE)
BOAR_IMG = load_and_scale_image(BOAR_IMG_PATH, BOAR_SIZE)
GIANT_IMG = load_and_scale_image(GIANT_IMG_PATH, GIANT_SIZE)
SENKU_STONE_IMG = load_and_scale_image(SENKU_STONE_IMG_PATH, ITEM_SIZE)
RAPID_FIRE_POWERUP_IMG = load_and_scale_image(RAPID_FIRE_POWERUP_IMG_PATH, ITEM_SIZE)
BANANA_POWERUP_IMG = load_and_scale_image(BANANA_POWERUP_IMG_PATH, ITEM_SIZE)
SUPER_STRENGTH_POWERUP_IMG = load_and_scale_image(SUPER_STRENGTH_POWERUP_IMG_PATH, ITEM_SIZE)
LOAD_SCREEN_GIF_FRAMES = load_gif_frames(LOAD_SCREEN_GIF_PATH, (WIDTH, HEIGHT))

# --- Função Auxiliar para Renderizar Texto Multilinha ---
def render_text_multiline(surface, text, pos, font, color, max_width, line_height_offset=0):
    words = [word.split(' ') for word in text.splitlines()]
    space_width = font.size(' ')[0]
    x_start, y_start = pos
    y = y_start
    current_line_height = font.get_linesize() + line_height_offset
    for line_words in words:
        x = x_start
        for i, word in enumerate(line_words):
            word_surface = font.render(word, True, color)
            word_width, _ = word_surface.get_size()
            if x + word_width > x_start + max_width:
                x = x_start
                y += current_line_height
            surface.blit(word_surface, (x, y))
            x += word_width
            if i < len(line_words) - 1: x += space_width
        y += current_line_height

# --- Classes dos Elementos do Jogo ---
# (Suas classes Player, Fireball, Enemy, Monkey, Boar, Giant, Item, etc. permaneceriam aqui)
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = SENKU_IMG_ORIGINAL
        self.rect = self.image.get_rect(topleft=(x, y))
        self.direction = "right"
        self.last_fireball_time = 0
        self.lives = MAX_LIVES
        self.is_invulnerable = False
        self.invulnerable_start_time = 0
        self.is_rapid_fire = False
        self.rapid_fire_start_time = 0
        self.hit_combo = 0
        self.last_hit_time = 0
        self.has_super_strength = False 
        self.super_strength_start_time = 0 

    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.x -= PLAYER_VEL; self.direction = "left"
        if keys[pygame.K_RIGHT]:
            self.x += PLAYER_VEL; self.direction = "right"
        if keys[pygame.K_UP]: self.y -= PLAYER_VEL
        if keys[pygame.K_DOWN]: self.y += PLAYER_VEL
        self.x = max(0, min(self.x, WIDTH - self.rect.width))
        self.y = max(0, min(self.y, HEIGHT - self.rect.height))
        self.rect.topleft = (self.x, self.y)

    def draw(self, window):
        display_image = pygame.transform.flip(self.image, True, False) if self.direction == "left" else self.image
        if self.is_invulnerable and pygame.time.get_ticks() % 200 < 100: pass
        else: window.blit(display_image, (self.x, self.y))
        if self.has_super_strength and pygame.time.get_ticks() % 300 < 150: 
            aura_surface = pygame.Surface(PLAYER_SIZE, pygame.SRCALPHA)
            aura_surface.fill((255,0,0,50)) 
            window.blit(aura_surface, (self.x, self.y))

    def shoot(self, current_time):
        cooldown = FIREBALL_COOLDOWN_BASE / 2 if self.is_rapid_fire else FIREBALL_COOLDOWN_BASE
        if current_time - self.last_fireball_time >= cooldown:
            y_pos = self.y + self.rect.height // 2 - FIREBALL_SIZE[1] // 2
            if self.direction == "right":
                fireball = Fireball(self.x + self.rect.width, y_pos, "right")
            else:
                fireball = Fireball(self.x - FIREBALL_SIZE[0], y_pos, "left")
            
            fireball.damage = FIREBALL_BASE_DAMAGE
            if self.has_super_strength:
                fireball.damage *= SUPER_STRENGTH_DAMAGE_MULTIPLIER
            
            self.last_fireball_time = current_time
            return fireball
        return None

    def take_damage(self, current_time, damage_amount=1):
        if not self.is_invulnerable:
            self.lives -= damage_amount
            self.is_invulnerable = True
            self.invulnerable_start_time = current_time
            self.hit_combo = 0
            return True
        return False

    def gain_life(self):
        if self.lives < MAX_LIVES:
            self.lives += 1; return True
        return False

    def activate_rapid_fire(self, current_time):
        self.is_rapid_fire = True
        self.rapid_fire_start_time = current_time

    def activate_super_strength(self, current_time): 
        self.has_super_strength = True
        self.super_strength_start_time = current_time

    def update_powerups_and_combo(self, current_time):
        if self.is_invulnerable and current_time - self.invulnerable_start_time >= DAMAGE_INVULNERABILITY_TIME:
            self.is_invulnerable = False
        if self.is_rapid_fire and current_time - self.rapid_fire_start_time >= RAPID_FIRE_DURATION:
            self.is_rapid_fire = False
        if self.has_super_strength and current_time - self.super_strength_start_time >= SUPER_STRENGTH_DURATION: 
            self.has_super_strength = False
        if self.hit_combo > 0 and current_time - self.last_hit_time >= COMBO_RESET_TIME:
            self.hit_combo = 0

    def increment_combo(self, current_time):
        self.hit_combo += 1
        self.last_hit_time = current_time

class Fireball:
    def __init__(self, x, y, direction):
        self.rect = pygame.Rect(x, y, FIREBALL_SIZE[0], FIREBALL_SIZE[1])
        self.speed = FIREBALL_SPEED if direction == "right" else -FIREBALL_SPEED
        self.image = FIREBALL_IMG_RIGHT if direction == "right" else FIREBALL_IMG_LEFT
        self.damage = FIREBALL_BASE_DAMAGE 

    def move(self):
        self.rect.x += self.speed

    def draw(self, window):
        window.blit(self.image, self.rect.topleft)

class Enemy:
    def __init__(self, x, y, size, image, speed, health, damage_output): 
        self.rect = pygame.Rect(x, y, size[0], size[1])
        self.image = image
        self.speed = speed
        self.health = health
        self.max_health = health
        self.damage_output = damage_output 
        self.last_hit_time = 0
        self.is_hit_effect_active = False

    def draw(self, window):
        if self.is_hit_effect_active and pygame.time.get_ticks() - self.last_hit_time < 100:
            flash_surface = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)
            flash_surface.fill((255, 255, 255, 128))
            window.blit(flash_surface, self.rect.topleft)
        else:
            self.is_hit_effect_active = False
            window.blit(self.image, self.rect.topleft)
        if self.max_health > 1: 
            bar_width = self.rect.width * (self.health / self.max_health)
            pygame.draw.rect(window, RED, (self.rect.x, self.rect.y - 10, self.rect.width, 5))
            pygame.draw.rect(window, GREEN, (self.rect.x, self.rect.y - 10, bar_width, 5))

    def take_hit(self, damage_amount, current_time): 
        self.health -= damage_amount
        self.last_hit_time = current_time
        self.is_hit_effect_active = True
        return self.health <= 0

class Monkey(Enemy):
    def __init__(self, current_speed):
        super().__init__(random.randint(WIDTH, WIDTH + 100),
                         random.randint(50, HEIGHT - MONKEY_SIZE[1] - 50), 
                         MONKEY_SIZE, MONKEY_IMG, current_speed, 1, MONKEY_DAMAGE)
    def move(self): self.rect.x -= self.speed

class Boar(Enemy):
    def __init__(self, current_speed):
        super().__init__(random.randint(WIDTH, WIDTH + 200),
                         random.randint(50, HEIGHT - BOAR_SIZE[1] - 50),
                         BOAR_SIZE, BOAR_IMG, current_speed, 3, BOAR_DAMAGE) 
    def move(self, player_rect):
        if self.rect.centery < player_rect.centery: self.rect.y += self.speed * 0.25
        elif self.rect.centery > player_rect.centery: self.rect.y -= self.speed * 0.25
        self.rect.x -= self.speed
        self.rect.y = max(0, min(self.rect.y, HEIGHT - self.rect.height))

class Giant(Enemy):
    def __init__(self, current_speed, player_rect): 
        super().__init__(random.randint(WIDTH + 50, WIDTH + 300),
                         random.randint(50, HEIGHT - GIANT_SIZE[1] - 50),
                         GIANT_SIZE, GIANT_IMG, current_speed, 8, GIANT_DAMAGE) 
    def move(self, player_rect):
        if self.rect.centery < player_rect.centery: self.rect.y += self.speed * 0.6
        elif self.rect.centery > player_rect.centery: self.rect.y -= self.speed * 0.6
        self.rect.x -= self.speed * 0.7 
        self.rect.y = max(0, min(self.rect.y, HEIGHT - self.rect.height))

class Item:
    def __init__(self, x, y, image, effect_type):
        self.rect = pygame.Rect(x, y, ITEM_SIZE[0], ITEM_SIZE[1])
        self.image = image
        self.effect = effect_type
    def move(self): self.rect.x -= BACKGROUND_SCROLL_SPEED + 1 
    def draw(self, window): window.blit(self.image, self.rect.topleft)

class SenkuStone(Item):
    def __init__(self): super().__init__(random.randint(WIDTH, WIDTH + 100), random.randint(0, HEIGHT - ITEM_SIZE[1]), SENKU_STONE_IMG, "score")
class RapidFirePowerup(Item):
    def __init__(self): super().__init__(random.randint(WIDTH, WIDTH + 100), random.randint(0, HEIGHT - ITEM_SIZE[1]), RAPID_FIRE_POWERUP_IMG, "rapid_fire")
class BananaPowerup(Item):
    def __init__(self): super().__init__(random.randint(WIDTH, WIDTH + 100), random.randint(0, HEIGHT - ITEM_SIZE[1]), BANANA_POWERUP_IMG, "banana")
class SuperStrengthPowerup(Item): 
    def __init__(self): super().__init__(random.randint(WIDTH, WIDTH + 100), random.randint(0, HEIGHT - ITEM_SIZE[1]), SUPER_STRENGTH_POWERUP_IMG, "super_strength")

class FloatingText:
    def __init__(self, x, y, text, color, font_size=24):
        self.text = text
        self.color = color
        self.start_time = pygame.time.get_ticks()
        self.position = [x, y]
        self.font = pygame.font.SysFont("comicsans", font_size)

    def update(self, current_time):
        elapsed_time = current_time - self.start_time
        if elapsed_time < FLOATING_TEXT_DURATION:
            self.position[1] -= 1.5 
            alpha = max(0, 255 - int(255 * (elapsed_time / FLOATING_TEXT_DURATION)))
            return True, self.color[:3] + (alpha,) if len(self.color) == 4 else self.color + (alpha,)
        return False, None

    def draw(self, window):
        is_active, color_with_alpha = self.update(pygame.time.get_ticks())
        if is_active:
            text_surface = self.font.render(self.text, True, color_with_alpha)
            if len(color_with_alpha) == 3 : 
                 temp_surf = pygame.Surface(text_surface.get_size(), pygame.SRCALPHA)
                 temp_surf.blit(text_surface, (0,0))
                 temp_surf.set_alpha(color_with_alpha[3] if len(color_with_alpha) > 3 else 255) 
                 window.blit(temp_surf, self.position)
            else: 
                 window.blit(text_surface, self.position)

class Particle:
    def __init__(self, x, y, color, radius_range, vel_range, lifetime_range):
        self.x = x
        self.y = y
        self.color = color
        self.radius = random.uniform(radius_range[0], radius_range[1])
        self.x_vel = random.uniform(vel_range[0], vel_range[1])
        self.y_vel = random.uniform(vel_range[0], vel_range[1])
        self.lifetime = random.randint(lifetime_range[0], lifetime_range[1])
        self.initial_lifetime = self.lifetime

    def update(self):
        self.x += self.x_vel
        self.y += self.y_vel
        self.radius = max(0, self.radius * (self.lifetime / self.initial_lifetime))
        self.lifetime -= 1
        return self.lifetime > 0 and self.radius > 0.5 

    def draw(self, window):
        if self.radius > 0.5: 
            pygame.draw.circle(window, self.color, (int(self.x), int(self.y)), int(self.radius))

class Explosion:
    def __init__(self, x, y, num_particles=25, color=ORANGE, particle_radius_range=(2,6), particle_vel_range=(-3.5, 3.5), particle_lifetime_range=(20,50)):
        self.center_x, self.center_y = x + EXPLOSION_SIZE[0]//2, y + EXPLOSION_SIZE[1]//2
        self.start_time = pygame.time.get_ticks()
        self.particles = []
        self.duration = EXPLOSION_DURATION 
        self.color = color

        for _ in range(num_particles):
            self.particles.append(Particle(self.center_x, self.center_y, self.color,
                                           particle_radius_range, particle_vel_range, particle_lifetime_range))
        self.flash_radius = EXPLOSION_SIZE[0] // 3
        self.flash_alpha = 200

    def update_and_draw(self, window, current_time): 
        elapsed = current_time - self.start_time
        if elapsed >= self.duration and not self.particles:
            return False 

        for p in self.particles[:]:
            if p.update():
                p.draw(window)
            else:
                self.particles.remove(p)

        if elapsed < self.duration / 2: 
            current_flash_radius = self.flash_radius * (1 - (elapsed / (self.duration / 2)))
            current_flash_alpha = self.flash_alpha * (1 - (elapsed / (self.duration / 2)))
            if current_flash_radius > 0 and current_flash_alpha > 0:
                s = pygame.Surface((current_flash_radius * 2, current_flash_radius * 2), pygame.SRCALPHA)
                pygame.draw.circle(s, self.color[:3] + (int(current_flash_alpha),) , (current_flash_radius, current_flash_radius), current_flash_radius)
                window.blit(s, (self.center_x - current_flash_radius, self.center_y - current_flash_radius))
        
        return True 

# --- Funções de Tela e Jogo ---
# (Suas funções start_screen, pause_menu, game_over_screen, display_phase_info, display_dialogue_scene permaneceriam aqui)
def start_screen():
    if not LOAD_SCREEN_GIF_FRAMES or len(LOAD_SCREEN_GIF_FRAMES) == 0 or (len(LOAD_SCREEN_GIF_FRAMES) == 1 and LOAD_SCREEN_GIF_FRAMES[0].get_width() <= 50):
        WIN.fill(BLACK)
        title = BIG_FONT.render(SCREEN_TITLE, True, WHITE)
        instruction = FONT.render("Pressione qualquer tecla para começar", True, WHITE)
        WIN.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 50))
        WIN.blit(instruction, (WIDTH // 2 - instruction.get_width() // 2, HEIGHT // 2))
        pygame.display.update()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); exit()
                if event.type == pygame.KEYDOWN: waiting = False
        return

    frame_index = 0
    last_frame_time = pygame.time.get_ticks()
    frame_delay = 100 # ms
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); exit()
            if event.type == pygame.KEYDOWN: waiting = False; return
        current_time = pygame.time.get_ticks()
        if current_time - last_frame_time > frame_delay:
            frame_index = (frame_index + 1) % len(LOAD_SCREEN_GIF_FRAMES)
            last_frame_time = current_time
        WIN.blit(LOAD_SCREEN_GIF_FRAMES[frame_index], (0, 0))
        instruction_text = FONT.render("Pressione qualquer tecla para iniciar", True, WHITE)
        text_rect = instruction_text.get_rect(center=(WIDTH // 2, HEIGHT - 50))
        text_bg = pygame.Surface((text_rect.width + 20, text_rect.height + 10), pygame.SRCALPHA)
        text_bg.fill((0, 0, 0, 150))
        WIN.blit(text_bg, (text_rect.x - 10, text_rect.y - 5))
        WIN.blit(instruction_text, text_rect)
        pygame.display.update()

def pause_menu():
    paused_text = BIG_FONT.render("PAUSADO", True, WHITE)
    resume_text = FONT.render("Pressione 'P' para continuar", True, WHITE)
    quit_text = FONT.render("Pressione 'Q' para sair", True, WHITE)
    s = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA); s.fill((0, 0, 0, 150)); WIN.blit(s, (0,0))
    WIN.blit(paused_text, (WIDTH // 2 - paused_text.get_width() // 2, HEIGHT // 2 - 100))
    WIN.blit(resume_text, (WIDTH // 2 - resume_text.get_width() // 2, HEIGHT // 2 - 20))
    WIN.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, HEIGHT // 2 + 30))
    pygame.display.update()
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p: paused = False
                elif event.key == pygame.K_q: pygame.quit(); exit()

def game_over_screen(score):
    WIN.fill(BLACK)
    game_over_text = BIG_FONT.render("GAME OVER", True, RED)
    final_score_text = FONT.render(f"Pontuação Final: {score}", True, WHITE)
    restart_instruction = FONT.render("Pressione R para Reiniciar ou Q para Sair", True, WHITE)
    WIN.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 70))
    WIN.blit(final_score_text, (WIDTH // 2 - final_score_text.get_width() // 2, HEIGHT // 2 - 20))
    WIN.blit(restart_instruction, (WIDTH // 2 - restart_instruction.get_width() // 2, HEIGHT // 2 + 30))
    pygame.display.update()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r: return "restart"
                if event.key == pygame.K_q: pygame.quit(); exit()
    return "quit"

def display_phase_info(phase_num):
    WIN.fill(BLACK)
    phase_text = BIG_FONT.render(f"Fase {phase_num}", True, WHITE)
    WIN.blit(phase_text, (WIDTH // 2 - phase_text.get_width() // 2, HEIGHT // 2 - 50))
    pygame.display.update()
    pygame.time.delay(1500) 

def display_dialogue_scene(dialogue_config, current_phase_number):
    if not dialogue_config: return
    char1_gif_frames = []
    char2_gif_frames = []
    dialogue_audio = None
    if dialogue_config.get("char1_gif_path"): char1_gif_frames = load_gif_frames(dialogue_config["char1_gif_path"], DIALOGUE_GIF_SIZE)
    if dialogue_config.get("char2_gif_path"): char2_gif_frames = load_gif_frames(dialogue_config["char2_gif_path"], DIALOGUE_GIF_SIZE)
    if dialogue_config.get("audio_path"):
        audio_path = dialogue_config["audio_path"]
        if os.path.exists(audio_path):
            try: dialogue_audio = pygame.mixer.Sound(audio_path); dialogue_audio.play()
            except pygame.error as e: print(f"Erro áudio {audio_path}: {e}"); dialogue_audio = None
        else: print(f"Áudio não encontrado: {audio_path}")
    script = dialogue_config.get("script", [])
    has_content = script or dialogue_audio or \
                  (char1_gif_frames and not (len(char1_gif_frames)==1 and char1_gif_frames[0].get_width() <=50)) or \
                  (char2_gif_frames and not (len(char2_gif_frames)==1 and char2_gif_frames[0].get_width() <=50))
    if not has_content:
        if dialogue_audio: dialogue_audio.stop()
        return

    current_line_index = 0; anim_frame_char1 = 0; anim_frame_char2 = 0
    last_gif_update_time = pygame.time.get_ticks(); gif_frame_duration = 100
    dialogue_running = True; clock = pygame.time.Clock()
    pos_char1_gif = (50, HEIGHT // 2 - DIALOGUE_GIF_SIZE[1] // 2 - DIALOGUE_BOX_HEIGHT // 2)
    pos_char2_gif = (WIDTH - DIALOGUE_GIF_SIZE[0] - 50, HEIGHT // 2 - DIALOGUE_GIF_SIZE[1] // 2 - DIALOGUE_BOX_HEIGHT // 2)
    dialogue_box_rect = pygame.Rect(40, HEIGHT - DIALOGUE_BOX_HEIGHT - 40, WIDTH - 80, DIALOGUE_BOX_HEIGHT)
    text_area_start_pos = (dialogue_box_rect.x + 20, dialogue_box_rect.y + 15)
    text_max_width = dialogue_box_rect.width - 40

    while dialogue_running:
        current_time = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if dialogue_audio: dialogue_audio.stop()
                pygame.quit(); exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    if script and current_line_index < len(script) - 1: current_line_index += 1
                    else: dialogue_running = False
                elif event.key == pygame.K_ESCAPE: dialogue_running = False
        if current_time - last_gif_update_time > gif_frame_duration:
            if char1_gif_frames: anim_frame_char1 = (anim_frame_char1 + 1) % len(char1_gif_frames)
            if char2_gif_frames: anim_frame_char2 = (anim_frame_char2 + 1) % len(char2_gif_frames)
            last_gif_update_time = current_time
        if not script and dialogue_audio and dialogue_audio.get_num_channels() == 0: dialogue_running = False
        
        WIN.fill(BLACK)
        if char1_gif_frames and not (len(char1_gif_frames)==1 and char1_gif_frames[0].get_width() <=50) : WIN.blit(char1_gif_frames[anim_frame_char1], pos_char1_gif)
        else: pygame.draw.rect(WIN, (50,50,50), (*pos_char1_gif, *DIALOGUE_GIF_SIZE)); WIN.blit(SMALL_FONT.render("GIF P1", True, WHITE), (pos_char1_gif[0]+10, pos_char1_gif[1]+10))
        if char2_gif_frames and not (len(char2_gif_frames)==1 and char2_gif_frames[0].get_width() <=50): WIN.blit(char2_gif_frames[anim_frame_char2], pos_char2_gif)
        else: pygame.draw.rect(WIN, (50,50,50), (*pos_char2_gif, *DIALOGUE_GIF_SIZE)); WIN.blit(SMALL_FONT.render("GIF P2", True, WHITE), (pos_char2_gif[0]+10, pos_char2_gif[1]+10))
        
        pygame.draw.rect(WIN, (30, 30, 70), dialogue_box_rect); pygame.draw.rect(WIN, WHITE, dialogue_box_rect, 3)
        if script and current_line_index < len(script):
            current_speech = script[current_line_index]
            speaker_name_text = "Personagem 1: " if current_speech["char"] == 1 else "Personagem 2: "
            full_text_line = speaker_name_text + current_speech["text"]
            render_text_multiline(WIN, full_text_line, text_area_start_pos, SMALL_FONT, WHITE, text_max_width, line_height_offset=3)
        
        skip_text_surface = SMALL_FONT.render("ENTER/ESPAÇO para avançar | ESC para pular", True, YELLOW)
        WIN.blit(skip_text_surface, (WIDTH // 2 - skip_text_surface.get_width() // 2, HEIGHT - 30))
        pygame.display.update()
        clock.tick(30)
    if dialogue_audio: dialogue_audio.stop()

def main_game_loop():
    player = Player(WIDTH // 2 - PLAYER_SIZE[0] // 2, HEIGHT - PLAYER_SIZE[1] - 30) 
    monkeys, boars, giants, items, fireballs, explosions, floating_texts, all_particles = [],[],[],[],[],[],[],[]
    score = 0
    current_phase = 1
    
    dialogue_data = DIALOGUES_RESOURCES.get(current_phase)
    if dialogue_data: 
        display_dialogue_scene(dialogue_data, current_phase)
    display_phase_info(current_phase)

    background_x = 0
    clock = pygame.time.Clock()
    last_spawn_times = {"monkey": 0, "boar": 0, "giant": 0, "item": 0}
    ### total_enemies_defeated_in_phase: Contador de inimigos derrotados na fase atual.
    total_enemies_defeated_in_phase = 0

    while True: 
        clock.tick(60)
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return score, "quit_event" 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    new_fireball = player.shoot(current_time)
                    if new_fireball:
                        fireballs.append(new_fireball)
                        for _ in range(3):
                            all_particles.append(Particle(new_fireball.rect.centerx, new_fireball.rect.centery, ORANGE, (1,3), (-1,1,-1,1), (10,20) ))
                if event.key == pygame.K_p: 
                    pause_menu() 

        player.update_powerups_and_combo(current_time)
        ### current_phase_config: Carrega as configurações da fase atual, incluindo 'target_defeated'.
        current_phase_config = PHASES.get(current_phase, PHASES[len(PHASES)])

        ### CONDIÇÃO PRINCIPAL PARA MUDAR DE FASE:
        # Compara o total de inimigos derrotados com o alvo da fase.
        if total_enemies_defeated_in_phase >= current_phase_config.get("target_defeated", 999):
            current_phase += 1 # Avança para a próxima fase
            if current_phase > len(PHASES): # Vitória
                WIN.blit(BIG_FONT.render("VOCÊ VENCEU!", True, GREEN), (WIDTH//2 - BIG_FONT.size("VOCÊ VENCEU!")[0]//2, HEIGHT//2 - 50))
                pygame.display.update()
                pygame.time.delay(3000) 
                return score, "victory" 
            
            else: # Próxima fase
                dialogue_data = DIALOGUES_RESOURCES.get(current_phase)
                if dialogue_data: 
                    display_dialogue_scene(dialogue_data, current_phase)
                display_phase_info(current_phase)
                ### Zera o contador de inimigos para a nova fase.
                total_enemies_defeated_in_phase = 0
                monkeys.clear(); boars.clear(); giants.clear(); items.clear(); fireballs.clear()
                explosions.clear(); floating_texts.clear(); all_particles.clear()
                last_spawn_times = {"monkey": 0, "boar": 0, "giant": 0, "item": 0}

        background_x = (background_x - BACKGROUND_SCROLL_SPEED) % WIDTH
        WIN.blit(BACKGROUND_IMG, (background_x - WIDTH, 0))
        WIN.blit(BACKGROUND_IMG, (background_x, 0))

        keys = pygame.key.get_pressed()
        player.move(keys)

        for fb in fireballs[:]:
            fb.move()
            if fb.rect.right < 0 or fb.rect.left > WIDTH: 
                if fb in fireballs: fireballs.remove(fb)

        spawn_freq_min = current_phase_config.get("spawn_freq_min", 1000)
        spawn_freq_max = current_phase_config.get("spawn_freq_max", 3000)
        
        phase_speeds = {
            "monkey": MONKEY_SPEED_BASE * current_phase_config.get("monkey_speed_multiplier", 1.0),
            "boar": BOAR_SPEED_BASE * current_phase_config.get("boar_speed_multiplier", 1.0),
            "giant": GIANT_SPEED_BASE * current_phase_config.get("giant_speed_multiplier", 1.0)
        }
        if len(monkeys) < current_phase_config.get("monkeys",0) and current_time - last_spawn_times["monkey"] > random.randint(spawn_freq_min, spawn_freq_max):
            monkeys.append(Monkey(phase_speeds["monkey"])); last_spawn_times["monkey"] = current_time
        if len(boars) < current_phase_config.get("boars",0) and current_time - last_spawn_times["boar"] > random.randint(int(spawn_freq_min*1.2), int(spawn_freq_max*1.2)):
            boars.append(Boar(phase_speeds["boar"])); last_spawn_times["boar"] = current_time
        if len(giants) < current_phase_config.get("giants",0) and current_time - last_spawn_times["giant"] > random.randint(int(spawn_freq_min*1.8), int(spawn_freq_max*1.8)):
            giants.append(Giant(phase_speeds["giant"], player.rect)); last_spawn_times["giant"] = current_time

        if len(items) < current_phase_config.get("items",0) and current_time - last_spawn_times["item"] > random.randint(ITEM_SPAWN_INTERVAL_MIN, ITEM_SPAWN_INTERVAL_MAX):
            choice = random.randint(1, 100)
            if choice <= 30: items.append(SenkuStone())
            elif choice <= 55: items.append(BananaPowerup())
            elif choice <= 80: items.append(RapidFirePowerup())
            else: items.append(SuperStrengthPowerup())
            last_spawn_times["item"] = current_time

        for m in monkeys: m.move()
        for b in boars: b.move(player.rect)
        for g in giants: g.move(player.rect)
        for i in items[:]: 
            i.move()
            if i.rect.right < 0 : 
                if i in items: items.remove(i)

        for p in all_particles[:]:
            if not p.update(): 
                if p in all_particles: all_particles.remove(p)
        for exp in explosions[:]:
            if not exp.update_and_draw(WIN, current_time): 
                if exp in explosions: explosions.remove(exp)

        for enemy_list in [monkeys, boars, giants]:
            for enemy in enemy_list[:]:
                for fb in fireballs[:]:
                    if fb.rect.colliderect(enemy.rect):
                        if fb in fireballs: fireballs.remove(fb)
                        for _ in range(5): all_particles.append(Particle(fb.rect.centerx, fb.rect.centery, YELLOW, (2,4), (-2,2,-2,2), (15,30)))
                        if enemy.take_hit(fb.damage, current_time):
                            if enemy in enemy_list: enemy_list.remove(enemy) 
                            score_val = 0
                            if isinstance(enemy, Monkey): score_val = SCORE_MONKEY
                            elif isinstance(enemy, Boar): score_val = SCORE_BOAR
                            elif isinstance(enemy, Giant): score_val = SCORE_GIANT
                            
                            score_gained = score_val * (1 + player.hit_combo * 0.15)
                            score += int(score_gained)
                            ### Incrementa o contador quando um inimigo é derrotado.
                            total_enemies_defeated_in_phase += 1
                            explosions.append(Explosion(enemy.rect.x, enemy.rect.y))
                            floating_texts.append(FloatingText(enemy.rect.centerx, enemy.rect.y, f"+{int(score_gained)}", YELLOW, 28))
                            player.increment_combo(current_time)
                        break 

        for enemy_list in [monkeys, boars, giants]:
            for enemy in enemy_list[:]: 
                if player.rect.colliderect(enemy.rect):
                    if player.take_damage(current_time, enemy.damage_output):
                        for _ in range(10): all_particles.append(Particle(player.rect.centerx, player.rect.centery, RED, (3,7), (-2.5,2.5,-2.5,2.5), (25,50)))
                        if player.lives <= 0:
                            return score, "game_over" 
                    
                    if not isinstance(enemy, Giant):
                        if enemy in enemy_list: 
                             enemy_list.remove(enemy)
        
        for item in items[:]:
            if player.rect.colliderect(item.rect):
                if item in items: items.remove(item)
                item_color = GREEN; extra_text = ""
                if item.effect == "score": score += SCORE_SENKU_STONE
                elif item.effect == "banana":
                    if player.gain_life(): score += SCORE_BANANA; extra_text = "+1 Vida!"
                    else: score += SCORE_BANANA // 2
                elif item.effect == "rapid_fire": player.activate_rapid_fire(current_time); item_color = ORANGE; extra_text = "Tiro Rápido!"
                elif item.effect == "super_strength": player.activate_super_strength(current_time); item_color = RED; extra_text = "Super Força!"
                
                floating_texts.append(FloatingText(item.rect.centerx, item.rect.y, extra_text if extra_text else f"+{ (SCORE_SENKU_STONE if item.effect == 'score' else 0) }", item_color, 30))
                for _ in range(15): all_particles.append(Particle(item.rect.centerx, item.rect.centery, item_color, (2,5), (-2,2,-2,2), (20,40)))
                break

        player.draw(WIN)
        for fb in fireballs: fb.draw(WIN)
        for m in monkeys: m.draw(WIN)
        for b in boars: b.draw(WIN)
        for g in giants: g.draw(WIN)
        for i in items: i.draw(WIN)
        for p in all_particles: p.draw(WIN)
        for ft in floating_texts[:]:
            is_active, _ = ft.update(current_time)
            if is_active: ft.draw(WIN)
            else: 
                if ft in floating_texts: floating_texts.remove(ft)

        score_text = FONT.render(f"Recursos: {score}", True, WHITE)
        WIN.blit(score_text, (10, 5))
        
        lives_text = FONT.render(f"Vidas: {player.lives}", True, WHITE)
        WIN.blit(lives_text, (10, 40))

        phase_text_render = FONT.render(f"Fase: {current_phase}", True, WHITE)
        WIN.blit(phase_text_render, (WIDTH - phase_text_render.get_width() - 10, 5))

        cd_bar_len = 100
        cd_actual = (FIREBALL_COOLDOWN_BASE / 2 if player.is_rapid_fire else FIREBALL_COOLDOWN_BASE)
        cd_percent = min((current_time - player.last_fireball_time) / cd_actual, 1) if cd_actual > 0 else 1
        pygame.draw.rect(WIN, WHITE, (WIDTH - 120, 40, cd_bar_len, 10), 1)
        pygame.draw.rect(WIN, ORANGE, (WIDTH - 119, 41, (cd_bar_len-2)*cd_percent , 8))
        
        powerup_y_offset = 70
        if player.is_rapid_fire:
            rf_text = SMALL_FONT.render(f"Tiro Rápido: {max(0, (RAPID_FIRE_DURATION - (current_time - player.rapid_fire_start_time))//1000)}s", True, ORANGE)
            WIN.blit(rf_text, (WIDTH - rf_text.get_width() - 10, powerup_y_offset)); powerup_y_offset += 25
        if player.has_super_strength:
            ss_text = SMALL_FONT.render(f"Super Força: {max(0, (SUPER_STRENGTH_DURATION - (current_time - player.super_strength_start_time))//1000)}s", True, RED)
            WIN.blit(ss_text, (WIDTH - ss_text.get_width() - 10, powerup_y_offset)); powerup_y_offset += 25

        if player.hit_combo > 1:
            combo_text = BIG_FONT.render(f"{player.hit_combo}x COMBO!", True, YELLOW)
            WIN.blit(combo_text, (WIDTH // 2 - combo_text.get_width() // 2, 10))

        pygame.display.update()
    
    # Este 'return score' só seria alcançado se o loop 'while True' fosse quebrado
    # de uma forma não prevista pelos 'return score, status' dentro do loop.
    # No fluxo normal, o jogo encerra através desses retornos (game_over, victory, quit_event).
    return score


# --- Fluxo Principal do Jogo ---
if __name__ == "__main__":
    start_screen()
    while True:
        final_score, status = main_game_loop() # Espera dois valores de retorno
        if status == "game_over":
            action = game_over_screen(final_score)
            if action == "quit":
                break
        elif status == "victory" or status == "quit_event":
            break
    pygame.quit()
    exit()