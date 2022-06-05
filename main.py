import pygame
import math
pygame.init()

# Настраиваем окно игры
WIDTH, HEIGHT = 700, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Solar system Simulation")

FONT = pygame.font.SysFont('conicsans', 16)

BG_COLOR = (0, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
DARK_GREY = (80, 78, 81)
WHITE = (255, 255, 255)

# создаем шаблон для планет
class Planet:
    AU = 149.6e6 * 1000 # астрономические единицы или что-то типа того
    G = 6.67428e-11 # гравитационная постоянная для расчетов
    SCALE = 200 / AU # 1AU = 100 pixels
    TIMESTEP = 3600*12 # 1 day

    # задаем основные параметры планеты
    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass

        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0

        self.x_vel = 0
        self.y_vel = 0

    # рисуем
    def draw(self, win):
        x = self.x * self.SCALE + WIDTH/2
        y = self.y * self.SCALE + HEIGHT/2

        # рисуем орбиту
        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2
                updated_points.append((x, y))

            pygame.draw.lines(win, self.color, False, updated_points, 2)

        pygame.draw.circle(win, self.color, (x, y), self.radius)

        # пишем расстояние до солнца
        if not self.sun:
            distance_text = FONT.render(f'{round(self.distance_to_sun/1000, 2)} km', 1, WHITE)
            win.blit(distance_text, (x - distance_text.get_width()/2, y -distance_text.get_height()/2))

    # каким-то сложным способом высчитываем силы, действующие на планеты от солнца и от других планет
    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x**2 + distance_y**2)

        if other.sun:
            self.distance_to_sun = distance

        force = self.G * self.mass * other.mass / distance**2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y

    # передвигаем планету, согласно разным силам
    def update_position(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue
            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))

# основная функция
def main():
    run = True
    clock = pygame.time.Clock() # скорость программы

    # создаем планеты и солнце
    sun = Planet(0, 0, 30, YELLOW, 1.98892 * 10**30)
    sun.sun = True

    earth = Planet(-1 * Planet.AU, 0, 16, BLUE, 5.9742 * 10**24)
    earth.y_vel = 29.783 * 1000

    mars = Planet(-1.524 * Planet.AU, 0, 12, RED, 6.39 * 10**23)
    mars.y_vel = 24.077 * 1000

    mercury = Planet(0.387 * Planet.AU, 0, 8, DARK_GREY, 3.30 * 10**23)
    mercury.y_vel = -47.4 * 1000

    venus = Planet(0.723 * Planet.AU, 0, 14, WHITE, 4.8685 * 10**24)
    venus.y_vel = -35.02 * 1000

    planets = [sun, earth, mars, mercury, venus]

    while run:
        clock.tick(60)
        # закрашиваем в нужный нам цвет
        WIN.fill(BG_COLOR)

        # Если нажали на закрыть окно, то выходим из цикла
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # туть мы все рисуем
        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN)


        pygame.display.update()

    pygame.quit()

main()

# конец
# весь код взял туть - https://www.youtube.com/watch?v=WTLPmUHTPqo&t=271s