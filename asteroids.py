"""
File: asteroids.py
Original Author: Br. Burton
Completed by Roberto Villanueva
This program implements the asteroids game.
"""
import random
import math
import arcade

# These are Global constants to use throughout the game
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

BULLET_RADIUS = 30
BULLET_SPEED = 10
BULLET_LIFE = 40

SHIP_TURN_AMOUNT = 3
SHIP_THRUST_AMOUNT = 0.25
SHIP_RADIUS = 30

INITIAL_ROCK_COUNT = 5

BIG_ROCK_SPIN = 1
BIG_ROCK_SPEED = 1.5
BIG_ROCK_RADIUS = 15

MEDIUM_ROCK_SPIN = -2
MEDIUM_ROCK_RADIUS = 5

SMALL_ROCK_SPIN = 5
SMALL_ROCK_RADIUS = 2


class Point:
    def __init__(self):
        self.x = 0.0
        self.y = 0.0


class Velocity:
    def __init__(self):
        self.dx = 0
        self.dy = 0


class FlyingObject:
    def __init__(self, img):
        self.center = Point()
        self.velocity = Velocity()
        self.alive = True
        self.img = img
        self.texture = arcade.load_texture(img)
        self.width = self.texture.width
        self.height = self.texture.height
        self.radius = 0
        self.angle = 0
        self.speed = 0
        self.direction = 0

    def advance(self):
        self.wrap()
        self.center.y += self.velocity.dy
        self.center.x += self.velocity.dx

    def is_alive(self):
        return self.alive

    def draw(self):
        arcade.draw_texture_rectangle(self.center.x, self.center.y, self.width, self.height, self.texture, self.angle,
                                      255)

    def wrap(self):
        if self.center.x > SCREEN_WIDTH:
            self.center.x -= SCREEN_WIDTH
        if self.center.x < 0:
            self.center.x += SCREEN_WIDTH
        if self.center.y > SCREEN_HEIGHT:
            self.center.y -= SCREEN_HEIGHT
        if self.center.y < 0:
            self.center.y += SCREEN_HEIGHT


class Bullet(FlyingObject):
    def __init__(self, ship_angle, ship_x, ship_y):
        super().__init__("images/laserBlue01.png")
        self.radius = BULLET_RADIUS
        self.life = BULLET_LIFE
        self.speed = BULLET_SPEED
        self.angle = ship_angle + 90
        self.center.x = ship_x
        self.center.y = ship_y

    def fire(self):
        self.velocity.dx -= math.sin(math.radians(self.angle - 90)) * BULLET_SPEED
        self.velocity.dy += math.cos(math.radians(self.angle - 90)) * BULLET_SPEED

    def advance(self):
        super().advance()
        self.life -= 1
        if self.life <= 0:
            self.alive = False


class Ship(FlyingObject):
    def __init__(self):
        super().__init__("images/playerShip1_orange.png")
        self.angle = 1
        self.center.x = (SCREEN_WIDTH / 2)
        self.center.y = (SCREEN_HEIGHT / 2)
        self.radius = SHIP_RADIUS

    def left(self):
        self.angle += SHIP_TURN_AMOUNT

    def right(self):
        self.angle -= SHIP_TURN_AMOUNT

    def thrust(self):
        self.velocity.dx -= math.sin(math.radians(self.angle)) * SHIP_THRUST_AMOUNT
        self.velocity.dy += math.cos(math.radians(self.angle)) * SHIP_THRUST_AMOUNT

    def neg_thrust(self):
        self.velocity.dx += math.sin(math.radians(self.angle)) * SHIP_THRUST_AMOUNT
        self.velocity.dy -= math.cos(math.radians(self.angle)) * SHIP_THRUST_AMOUNT


class Asteroid(FlyingObject):
    def __init__(self, img):
        super().__init__(img)


class SmallRock(Asteroid):
    def __init__(self):
        super().__init__("images/meteorGrey_small1.png")
        self.radius = SMALL_ROCK_RADIUS

    def advance(self):
        super().advance()
        self.angle += SMALL_ROCK_SPIN

    def break_apart(self, asteroids):
        self.alive = False


class MediumRock(Asteroid):
    def __init__(self):
        super().__init__("images/meteorGrey_med1.png")
        self.radius = MEDIUM_ROCK_RADIUS

    def advance(self):
        super().advance()
        self.angle += MEDIUM_ROCK_SPIN

    def break_apart(self, asteroids):
        small = SmallRock()
        small.center.x = self.center.x
        small.center.y = self.center.y
        small.velocity.dy = self.velocity.dy + random.randint(0, 2)
        small.velocity.dx = self.velocity.dx + random.randint(0, 2)

        small2 = SmallRock()
        small2.center.x = self.center.x
        small2.center.y = self.center.y
        small2.velocity.dy = self.velocity.dy - random.randint(0, 2)
        small2.velocity.dx = self.velocity.dx - random.randint(0, 2)

        asteroids.append(small2)
        asteroids.append(small)
        self.alive = False


class LargeRock(Asteroid):
    def __init__(self):
        super().__init__("images/meteorGrey_big1.png")
        self.radius = BIG_ROCK_RADIUS
        self.center.x = random.randint(1, 50)
        self.center.y = random.randint(1, 150)
        self.direction = random.randint(1, 50)
        self.speed = BIG_ROCK_SPEED
        self.velocity.dx = math.cos(math.radians(self.direction)) * self.speed
        self.velocity.dy = math.sin(math.radians(self.direction)) * self.speed

    def advance(self):
        super().advance()
        self.angle += BIG_ROCK_SPIN

    def break_apart(self, asteroids):
        med1 = MediumRock()
        med1.center.x = self.center.x
        med1.center.y = self.center.y
        med1.velocity.dy = self.velocity.dy + random.randint(0, 2)
        med1.velocity.dx = self.velocity.dx - random.randint(0, 2)

        med2 = MediumRock()
        med2.center.x = self.center.x
        med2.center.y = self.center.y
        med2.velocity.dy = self.velocity.dy - random.randint(0, 2)
        med2.velocity.dx = self.velocity.dx + random.randint(0, 2)

        small1 = SmallRock()
        small1.center.x = self.center.x
        small1.center.y = self.center.y
        small1.velocity.dy = self.velocity.dy + random.randint(0, 2)
        small1.velocity.dx = self.velocity.dx - random.randint(0, 2)

        asteroids.append(med1)
        asteroids.append(med2)
        asteroids.append(small1)
        self.alive = False


class Game(arcade.Window):
    """
    This class handles all the game callbacks and interaction
    This class will then call the appropriate functions of
    each of the above classes.
    You are welcome to modify anything in this class.
    """

    def __init__(self, width, height):
        """
        Sets up the initial conditions of the game
        :param width: Screen width
        :param height: Screen height
        """
        super().__init__(width, height)
        arcade.set_background_color(arcade.color.BLACK)
        self.laser_sound = arcade.load_sound("sounds/laser.mp3")
        self.explosion_sound = arcade.load_sound("sounds/collision.mp3")
        self.game_over_sound = arcade.load_sound("sounds/game_over.mp3")
        self.music = arcade.load_sound("sounds/music.mp3")

        self.setup()

    def setup(self):
        """
        I use this method to restart the game. If the ship is dead or there are no more asteroids, I call this
        function to set up everything to their original values. That's why most attributes are here and not in the
        __init__() function. __init__() calls this function to start the game.
        """
        self.held_keys = set()

        self.asteroids = []
        for i in range(INITIAL_ROCK_COUNT):
            bigAst = LargeRock()
            self.asteroids.append(bigAst)

        self.ship = Ship()
        self.bullets = []

        self.game_over = False
        self.win = False
        arcade.play_sound(self.music, 0.1)

    def check_game_over(self):
        """
        Checks if the ship is alive. If it's not, then the game is over.
        """
        if not self.ship.alive:
            self.game_over = True
        else:
            self.game_over = False

        return self.game_over

    def check_win(self):
        """
        Checks if there are no more asteroids. If there are no asteroids, the player wins!!!
        """
        if len(self.asteroids) == 0:
            self.win = True
        else:
            self.win = False
        return self.win

    def on_draw(self):
        """
        Called automatically by the arcade framework.
        Handles the responsibility of drawing all elements.
        """

        # clear the screen to begin drawing
        arcade.start_render()

        for asteroid in self.asteroids:
            asteroid.draw()

        for bullet in self.bullets:
            bullet.draw()

        self.ship.draw()

        if self.game_over:
            """Let the player know the game is over."""
            img = "images/game_over.jpg"
            texture = arcade.load_texture(img)
            width = texture.width
            height = texture.height
            alpha = 255  # For transparency, 1 means not transparent
            angle = 0
            arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, width, height, texture, angle, alpha)

        if self.win:
            """Let the player know when he wins."""
            img = "images/win.jpg"
            texture = arcade.load_texture(img)
            width = texture.width
            height = texture.height
            alpha = 255  # For transparency, 1 means not transparent
            angle = 0
            arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, width, height, texture, angle, alpha)

        self.draw_instructions()

    def draw_instructions(self):
        text = "You are the ship's pilot! Save your crew from the asteroids!!!"
        start_x = 120
        start_y = 10
        if self.ship.alive and len(self.asteroids) > 0:
            arcade.draw_text(text, start_x, start_y, font_size=18, color=arcade.color.BARN_RED)

    def remove_not_alive_objects(self):
        for bullet in self.bullets:
            if not bullet.is_alive():
                self.bullets.remove(bullet)

        for asteroid in self.asteroids:
            if not asteroid.alive:
                self.asteroids.remove(asteroid)

    def check_collisions(self):
        for bullet in self.bullets:
            for asteroid in self.asteroids:
                if bullet.alive and asteroid.alive:
                    distance_x = abs(asteroid.center.x - bullet.center.x)
                    distance_y = abs(asteroid.center.y - bullet.center.y)
                    max_distance = asteroid.radius + bullet.radius
                    if distance_x < max_distance and distance_y < max_distance:
                        # we have a collision, do something
                        asteroid.break_apart(self.asteroids)
                        bullet.alive = False
                        asteroid.alive = False
                        arcade.play_sound(self.explosion_sound, 0.05)

        for asteroid in self.asteroids:
            if self.ship.alive and asteroid.alive:
                distance_x = abs(asteroid.center.x - self.ship.center.x)
                distance_y = abs(asteroid.center.y - self.ship.center.y)
                max_distance = asteroid.radius + self.ship.radius
                if distance_x < max_distance and distance_y < max_distance:
                    # we have a collision, do something
                    self.ship.alive = False
                    self.music.stop()
                    arcade.play_sound(self.game_over_sound, 0.1)
                    arcade.play_sound(self.explosion_sound, 0.1)

    def update(self, delta_time):
        """
        Update each object in the game.
        :param delta_time: tells us how much time has actually elapsed
        """
        self.check_keys()

        for asteroid in self.asteroids:
            asteroid.advance()

        for bullet in self.bullets:
            bullet.advance()

        self.remove_not_alive_objects()
        self.check_collisions()
        self.ship.advance()

        # this functions is constantly checking if the game has ended.
        self.check_game_over()
        self.check_win()

    def check_keys(self):
        """
        This function checks for keys that are being held down.
        You will need to put your own method calls in here.
        """
        if arcade.key.LEFT in self.held_keys:
            self.ship.left()

        if arcade.key.RIGHT in self.held_keys:
            self.ship.right()

        if arcade.key.UP in self.held_keys:
            self.ship.thrust()

        if arcade.key.DOWN in self.held_keys:
            self.ship.neg_thrust()

    def on_key_press(self, key: int, modifiers: int):
        """
        Puts the current key in the set of keys that are being held.
        You will need to add things here to handle firing the bullet.
        """
        if self.ship.alive:
            self.held_keys.add(key)

            if key == arcade.key.SPACE:
                bullet = Bullet(self.ship.angle, self.ship.center.x, self.ship.center.y)
                self.bullets.append(bullet)
                bullet.fire()
                arcade.play_sound(self.laser_sound, 0.05)

        # Let the player restart the game in case he has won or lost.
        if self.game_over or self.win:
            if key == arcade.key.ENTER:
                self.music.stop()
                self.setup()

    def on_key_release(self, key: int, modifiers: int):
        """
        Removes the current key from the set of held keys.
        """
        if key in self.held_keys:
            self.held_keys.remove(key)


# Creates the game and starts it going
window = Game(SCREEN_WIDTH, SCREEN_HEIGHT)
arcade.run()
