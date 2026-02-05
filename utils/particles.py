import arcade
import random
import math


class Particle:
    def __init__(self, x, y, vx, vy, life, size, color, shape="circle", gravity=0.0, spin=0.0):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.life = max(0.05, life)
        self.age = 0.0
        self.size = size
        self.color = color
        self.shape = shape
        self.gravity = gravity
        self.spin = spin
        self.angle = random.uniform(0, 360)

    def update(self, dt):
        self.age += dt
        if self.age >= self.life:
            return False
        self.vy -= self.gravity * dt
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.vx *= 0.96
        self.vy *= 0.96
        self.angle = (self.angle + self.spin * dt) % 360
        return True

    def draw(self):
        alpha = max(0, 1.0 - self.age / self.life)
        if len(self.color) == 4:
            color = (self.color[0], self.color[1], self.color[2], int(self.color[3] * alpha))
        else:
            color = (self.color[0], self.color[1], self.color[2], int(255 * alpha))

        if self.shape == "diamond":
            half = self.size / 2
            points = [
                (self.x, self.y + half),
                (self.x + half, self.y),
                (self.x, self.y - half),
                (self.x - half, self.y),
            ]
            arcade.draw_polygon_filled(points, color)
        elif self.shape == "spark":
            length = self.size * 1.4
            angle_rad = math.radians(self.angle)
            dx = math.cos(angle_rad) * length
            dy = math.sin(angle_rad) * length
            arcade.draw_line(self.x - dx, self.y - dy, self.x + dx, self.y + dy, color, max(1, int(self.size / 3)))
        else:
            arcade.draw_circle_filled(self.x, self.y, self.size / 2, color)


class ParticleSystem:
    def __init__(self, max_particles=240):
        self.particles = []
        self.max_particles = max_particles

    def emit(self, x, y, count=8, speed=80, spread=math.pi, life=0.35, size=4, color=(255, 200, 120), shape="circle"):
        for _ in range(count):
            angle = random.uniform(-spread / 2, spread / 2)
            velocity = random.uniform(speed * 0.5, speed)
            vx = math.cos(angle) * velocity
            vy = math.sin(angle) * velocity
            p = Particle(
                x,
                y,
                vx,
                vy,
                life=random.uniform(life * 0.7, life * 1.2),
                size=random.uniform(size * 0.7, size * 1.3),
                color=color,
                shape=shape,
                gravity=30,
                spin=random.uniform(-160, 160),
            )
            self._add(p)

    def emit_melee_swing(self, x, y, angle_rad, radius, color=(255, 200, 120)):
        count = random.randint(10, 16)
        arc = math.radians(80)
        for _ in range(count):
            a = angle_rad + random.uniform(-arc / 2, arc / 2)
            dist = radius * random.uniform(0.6, 1.0)
            px = x + math.cos(a) * dist
            py = y + math.sin(a) * dist
            speed = random.uniform(60, 120)
            vx = math.cos(a) * speed
            vy = math.sin(a) * speed
            shape = random.choice(["spark", "diamond", "circle"])
            p = Particle(
                px,
                py,
                vx,
                vy,
                life=random.uniform(0.18, 0.32),
                size=random.uniform(3, 7),
                color=color,
                shape=shape,
                gravity=40,
                spin=random.uniform(-220, 220),
            )
            self._add(p)

    def emit_hit(self, x, y, color=(255, 120, 120)):
        self.emit(
            x,
            y,
            count=random.randint(6, 10),
            speed=90,
            spread=math.pi * 2,
            life=0.25,
            size=4,
            color=color,
            shape=random.choice(["spark", "diamond"]),
        )

    def _add(self, particle):
        self.particles.append(particle)
        if len(self.particles) > self.max_particles:
            self.particles = self.particles[-self.max_particles :]

    def update(self, dt):
        if not self.particles:
            return
        alive = []
        for p in self.particles:
            if p.update(dt):
                alive.append(p)
        self.particles = alive

    def draw(self):
        for p in self.particles:
            p.draw()
