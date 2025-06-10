import pygame
import random
from abc import ABC, abstractmethod

class Particle(ABC):
    def __init__(self):
        self.pos = pygame.Vector2(0, 0)
        self.velocity = pygame.Vector2(0, 0)
        self.lifetime = 0
        self.max_lifetime = 0
        self.active = False
        self.color = (255, 255, 255)
        self.size = 1
        self.rect = pygame.Rect(0, 0, self.size * 2, self.size * 2)

    def reset(self, pos, velocity, lifetime, color, size):
        self.active = True
        self.pos = pos.copy()
        self.velocity = velocity.copy()
        self.lifetime = 0
        self.max_lifetime = lifetime
        self.color = color
        self.size = size
        self.rect = pygame.Rect(int(pos.x) - size, int(pos.y) - size, size * 2, size * 2)

    def draw(self, surface):
        if self.active:
            pygame.draw.circle(surface, self.color, (int(self.pos.x), int(self.pos.y)), self.size)

    @abstractmethod
    def update(self, d_time, bounds=None):
        pass

    def is_inside_bounds(self, bounds):
        if isinstance(bounds, pygame.Rect):
            return bounds.collidepoint(self.pos.x, self.pos.y)
        elif isinstance(bounds, list):  # Polygon
            return self.point_in_polygon(self.pos, bounds)
        return True

    def point_in_polygon(self, point, polygon):
        x, y = point
        n = len(polygon)
        inside = False
        px, py = polygon[0]
        for i in range(n + 1):
            sx, sy = polygon[i % n]
            if y > min(py, sy):
                if y <= max(py, sy):
                    if x <= max(px, sx):
                        if py != sy:
                            xinters = (y - py) * (sx - px) / (sy - py) + px
                        if px == sx or x <= xinters:
                            inside = not inside
            px, py = sx, sy
        return inside

class WaterDroplet(Particle):
    def __init__(self):
        super().__init__()
        self.gravity = 1700  # 1700 pixel/giây²

    def update(self, d_time, bounds=None):
        if not self.active:
            return
        self.lifetime += d_time
        if self.lifetime >= self.max_lifetime:
            self.active = False
            return
        self.velocity.y += self.gravity * d_time
        self.pos += self.velocity * d_time
        self.rect.center = (int(self.pos.x), int(self.pos.y))
        if bounds and not self.is_inside_bounds(bounds):
            self.active = False

class DustParticle(Particle):
    def update(self, d_time, bounds=None):
        if not self.active:
            return
        self.lifetime += d_time
        if self.lifetime >= self.max_lifetime:
            self.active = False
            return
        self.pos += self.velocity * d_time
        self.rect.center = (int(self.pos.x), int(self.pos.y))
        # Thêm chuyển động ngẫu nhiên
        self.velocity += pygame.Vector2(
            random.uniform(-5, 5) * d_time,
            random.uniform(-5, 5) * d_time
        )
        if bounds and not self.is_inside_bounds(bounds):
            self.active = False

class ParticlePool:
    def __init__(self, initial_size=100):
        self.particles = []
        self.types = {"dust": DustParticle, "water": WaterDroplet}
        self.initial_size = initial_size
        # Khởi tạo pool
        for _ in range(initial_size // 2):
            self.particles.append(DustParticle())
            self.particles.append(WaterDroplet())

    def get_particle(self, particle_type):
        # Tìm particle không hoạt động
        for particle in self.particles:
            if not particle.active and isinstance(particle, self.types[particle_type]):
                return particle
        # Tạo mới nếu thiếu
        new_particle = self.types[particle_type]()
        self.particles.append(new_particle)
        return new_particle

    def update(self, d_time, bounds=None):
        for particle in self.particles:
            if particle.active:
                particle.update(d_time, bounds)

    def draw(self, surface):
        for particle in self.particles:
            if particle.active:
                particle.draw(surface)

class ParticleSystem:
    def __init__(self, pool_size=100):
        self.pool = ParticlePool(pool_size)
        self.screen_height = 720  # Điều chỉnh theo game
        self.screen_width = 1280  # Điều chỉnh theo game
        self.dust_timer = 0
        self.water_timers = {}  # {id: timer}
        self.dust_interval = 0.1  # Bụi mỗi 0.1s
        self.water_interval = 0.5  # Giọt nước mỗi 0.5s
        self.dust_polygon = None
        self.water_positions = {}  # {id: Vector2}

    def start_dust_effect(self, polygon):
        self.dust_polygon = polygon

    def stop_dust_effect(self):
        self.dust_polygon = None

    def add_water_spawn(self, spawn_id, x, y):
        self.water_positions[spawn_id] = pygame.Vector2(x, y)
        self.water_timers[spawn_id] = 0

    def remove_water_spawn(self, spawn_id):
        self.water_positions.pop(spawn_id, None)
        self.water_timers.pop(spawn_id, None)

    def spawn_dust(self, polygon, count=3):
        for _ in range(count):
            particle = self.pool.get_particle("dust")
            if particle:
                min_x = min(p[0] for p in polygon)
                max_x = max(p[0] for p in polygon)
                min_y = min(p[1] for p in polygon)
                max_y = max(p[1] for p in polygon)
                pos = pygame.Vector2(
                    random.uniform(min_x, max_x),
                    random.uniform(min_y, max_y)
                )
                while not particle.point_in_polygon(pos, polygon):
                    pos = pygame.Vector2(
                        random.uniform(min_x, max_x),
                        random.uniform(min_y, max_y)
                    )
                velocity = pygame.Vector2(
                    random.uniform(-20, 20),
                    random.uniform(-20, 20)
                )
                particle.reset(
                    pos=pos,
                    velocity=velocity,
                    lifetime=random.uniform(0.5, 1.5),
                    color=(255, 245, 200),  # Vàng nhạt lung linh
                    size=random.randint(1, 2)
                )

    def spawn_water_droplet(self, x, y, count=2):
        for _ in range(count):
            particle = self.pool.get_particle("water")
            if particle:
                pos = pygame.Vector2(x + random.uniform(-10, 10), y)
                velocity = pygame.Vector2(
                    random.uniform(-20, 20),
                    random.uniform(0, 50)
                )
                particle.reset(
                    pos=pos,
                    velocity=velocity,
                    lifetime=2,
                    color=(100, 150, 255),
                    size=3
                )

    def update(self, d_time, dust_bounds=None):
        self.dust_timer += d_time
        if self.dust_polygon and self.dust_timer >= self.dust_interval:
            self.spawn_dust(self.dust_polygon, count=3)
            self.dust_timer = 0

        for spawn_id in self.water_timers:
            self.water_timers[spawn_id] += d_time
            if self.water_timers[spawn_id] >= self.water_interval:
                pos = self.water_positions[spawn_id]
                self.spawn_water_droplet(pos.x, pos.y, count=2)
                self.water_timers[spawn_id] = 0

        self.pool.update(d_time, dust_bounds if dust_bounds else self.dust_polygon)

    def draw(self, surface):
        self.pool.draw(surface)

# Cách sử dụng
"""
from particle_system import ParticleSystem
particle_system = ParticleSystem(pool_size=100)
# Bụi
polygon = [(300, 200), (400, 200), (400, 300), (300, 300)]
particle_system.start_dust_effect(polygon)
# Nhiều điểm giọt nước
particle_system.add_water_spawn(1, x=500, y=100)
particle_system.add_water_spawn(2, x=600, y=150)
# Trong vòng lặp game
particle_system.update(d_time, dust_bounds=polygon)
particle_system.draw(screen)
# Dừng
particle_system.stop_dust_effect()
particle_system.remove_water_spawn(1)
"""