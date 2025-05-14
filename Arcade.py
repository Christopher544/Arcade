import pygame
ANCHO_VENTANA = 800
ALTO_VENTANA = 600

shift = 0
background_speed     = 0
ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))

class Objeto(pygame.sprite.Sprite):
    def __init__(self, posicion_x:int=0,posicion_y:int=0,ancho:int=0, alto:int=0, imagen:str="",velocidad:int=0):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(imagen),(ancho, alto))
        self.rect = self.image.get_rect()
        self.rect.x = posicion_x
        self.rect.y = posicion_y
        self.velocidad = velocidad

    def dibujar(self):
        ventana.blit(self.image, (self.rect.x, self.rect.y))
class Jugador(Objeto):
    def __init__(self, posicion_x:int=0, posicion_y:int=0, ancho:int=0, alto:int=0, imagen:str="", velocidad:int=0):
        super().__init__(posicion_x, posicion_y, ancho, alto, imagen, velocidad)
        self.contador_salto = 2  # Initialize jump counter

    def mover(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.velocidad
            background_speed = -5
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.velocidad
            background_speed = 0
        #if not keys[pygame.K_LEFT] or keys[pygame.K_a] or keys[pygame.K_RIGHT] or keys[pygame.K_d]:


        
    def gravedad(self, plataformas):
        en_el_suelo = False
        gravedad = 5
        self.rect.y += gravedad
        for plataforma in plataformas:
            if self.rect.colliderect(plataforma.rect):
                en_el_suelo = True
                self.rect.y = plataforma.rect.top - self.rect.height
                self.contador_salto = 2  # Reset jump counter when on the ground
                break
        if not en_el_suelo:
            self.contador_salto = max(0, self.contador_salto)  # Ensure counter doesn't go negative

    def saltar(self):
        if self.contador_salto > 0:  # Allow jump only if counter > 0
            self.rect.y -= 100
            self.contador_salto -= 1  # Decrease jump counter

class Plataforma(pygame.sprite.Sprite):
    def __init__(self, posicion_x:int=0,posicion_y:int=0,ancho:int=0, alto:int=0, color:tuple = (0,0,0),velocidad:int=0):
        super().__init__()
        self.image = pygame.Surface((ancho, alto))
        self.image.fill(color)

        self.rect = self.image.get_rect()
        self.rect.x = posicion_x
        self.rect.y = posicion_y

    def crear_plataforma(self):
        ventana.blit(self.image, (self.rect.x, self.rect.y))

reloj = pygame.time.Clock()
run = True

jugador =  Jugador(0, 0, 50, 50, 'mario.png', 5)

plataforma1 = Plataforma(0, 100, 200, 5, (255,255,0))
plataforma2 = Plataforma(400, 200, 200, 5, (255,87,0))
plataforma3 = Plataforma(0, 600, ANCHO_VENTANA, 5, (255,0,0))
plataformas = pygame.sprite.Group()
plataformas.add(plataforma1)
plataformas.add(plataforma2)
plataformas.add(plataforma3)
fondo = pygame.transform.scale(pygame.image.load('mariofondo.jpg'), (ANCHO_VENTANA, ALTO_VENTANA))
while run:

    shift += background_speed
    local_shift = shift % ANCHO_VENTANA 
    ventana.blit(fondo, (local_shift, 0))
    if local_shift != 0:
        ventana.blit(fondo, (local_shift - ANCHO_VENTANA, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                jugador.saltar()
    borde_izquierdo = ANCHO_VENTANA/8
    borde_derecho = ANCHO_VENTANA - borde_izquierdo
    if jugador.rect.x > borde_derecho:
        jugador.rect.x = borde_derecho
        shift -= jugador.velocidad *1.5
    elif jugador.rect.x < borde_izquierdo:
        jugador.rect.x = borde_izquierdo
        shift += jugador.velocidad *1.5
    
    
    jugador.dibujar()
    jugador.mover()
    jugador.gravedad(plataformas)
    for plataforma in plataformas:
        plataforma.crear_plataforma()
    pygame.display.update()
    reloj.tick(60)



