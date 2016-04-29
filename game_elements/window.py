# -*- coding: utf-8 -*-
import math, random, sys, signal, time, datetime

import AI_controller
import pyglet
from pyglet import font
from pyglet.gl import *

import pymunk
from .sprites import Cloud, Floor, GameObject, Rod
from . import constants

G_VECTOR = (0.0, -900.0)
SKY_COLOR = (65.0/255, 0.0/255, 0.0/255)


def signal_handler(signal, frame):
        print(' Finalizando...')
        sys.exit(0)


#Classe que define a captação e as ações tomadas em eventos de mouse/teclado
class GameEventHandler(object):
    def __init__(self, window):
        self.window = window
    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.D or symbol == pyglet.window.key.RIGHT:
                self.window.smiley.obj_space.body.apply_impulse(j = (15000, 0))
        if symbol == pyglet.window.key.A or symbol == pyglet.window.key.LEFT:
            self.window.smiley.obj_space.body.apply_impulse(j = (-15000, 0))
        if symbol == pyglet.window.key.W:
            self.window.toggle_wind()
        if symbol == pyglet.window.key.ESCAPE:
            exit()
        return True

#classe que define o jogo
class Game(pyglet.window.Window):
    def __init__(self, space, run_pyglet, load):

        space.gravity = (G_VECTOR[0], G_VECTOR[1])
        self.space = space
        self.epoch = 0

        if(run_pyglet):
            pyglet.window.Window.__init__(self, width = constants.W_WIDTH, height = constants.W_HEIGHT)
            self.wind = 0

        self.run_pyglet = run_pyglet

        self.push_handlers(GameEventHandler(self))
        self.batch_draw = pyglet.graphics.Batch()
        font.add_file('./resources/neon_pixel.ttf')
        neon_pixel = font.load('Neon Pixel-7')
        self.define_scenario()

        self.define_game_objects()

        signal.signal(signal.SIGINT, signal_handler)

        self.pole_angle = self.get_pole_angle()
        self.angular_velocity = 0
        self.learner = AI_controller.Learner(self, load)

        pyglet.clock.schedule(self.update)
        if not(run_pyglet):
            filename =  datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d%H%M%S')
            print "Gerando arquivo para listagem das performances (%s.txt)" % filename
            self.performances_file = open(("./performance/%s.txt" % filename), "w+")


    def define_scenario(self):
        background = pyglet.graphics.OrderedGroup(0)
        pyglet.gl.glClearColor(SKY_COLOR[0], SKY_COLOR[1], SKY_COLOR[2],1)
        self.clouds = (Cloud(batch = self.batch_draw,
                             x = constants.W_WIDTH * 0.2,
                             y = constants.W_HEIGHT * 0.8,
                             group = background),
                    Cloud(batch = self.batch_draw,
                          x = constants.W_WIDTH * 0.8,
                          y = constants.W_HEIGHT * 0.72,
                          group = background))
        self.floor = Floor(batch = self.batch_draw, space = self.space)


    def define_game_objects(self):
        self.lone_wheel = GameObject("wheel", batch = self.batch_draw,
                    space = self.space,
                    group = pyglet.graphics.OrderedGroup(1))

        self.smiley = GameObject("smiley", batch = self.batch_draw,
                             space = self.space,
                             group = pyglet.graphics.OrderedGroup(3))

        if self.run_pyglet:
            self.smiley.randomize(self.lone_wheel.randomize())

        self.smiley.obj_space.body.apply_impulse((random.randint(-10000, 10000), 0))

        rod = pymunk.PinJoint(self.lone_wheel.obj_space.body,
                              self.smiley.obj_space.body)
        self.space.add(rod)

        self.rod = Rod(batch = self.batch_draw, group = pyglet.graphics.OrderedGroup(2))

    def on_draw(self):
        self.clear()
        self.lone_wheel.rotation = self.lone_wheel.x - constants.W_WIDTH/2
        pyglet.text.Label('Death Count: %.2d' % self.epoch,
                          font_name='OptimusPrinceps',
                          font_size=120,
                          x=self.width//2, y=self.height//2,
                          anchor_x='center', anchor_y='center').draw()
        if self.visualize:
            self.batch_draw.draw()
            for i in range(0, int(math.ceil(constants.W_WIDTH / self.floor.img.width))):
                self.floor.img.blit(i * self.floor.img.width,0)



    def out_of_screen(self):
        if (self.smiley.obj_space.body.position.y <= constants.F_HEIGHT + self.smiley.obj_space.radius or
           self.lone_wheel.obj_space.body.position.x <= 0 or self.lone_wheel.obj_space.body.position.x  >= constants.W_WIDTH):
            return True
        else:
            return False


    def reset(self, performance):
        self.lone_wheel.reset()
        self.smiley.reset()
        if not(self.run_pyglet):
            self.smiley.randomize(self.lone_wheel.randomize())
            self.performances_file.write(str(performance) + "\n")
        self.epoch += 1

    def get_wheel_x(self):
        return self.lone_wheel.obj_space.body.position.x

    def get_smiley_y(self):
        return self.smiley.obj_space.body.position.y

    def get_pole_angle(self):
        if self.smiley.y == self.lone_wheel.y:
            if self.smiley.x > self.lone_wheel.x:
                arctan = 90
            else:
                arctan = -90
        else:
            if self.smiley.y > self.lone_wheel.y:
                 tan = (self.smiley.x - self.lone_wheel.x)/(self.smiley.y - self.lone_wheel.y)
                 arctan = (math.atan(tan)*180)/math.pi
            else:
                 tan = (self.smiley.x - self.lone_wheel.x)/(self.lone_wheel.y - self.smiley.y)
                 arctan = 180 - (math.atan(tan)*180)/math.pi
        return arctan

    def get_pole_angular_velocity(self):
        return (self.get_pole_angle() - self.pole_angle)*60

    def toggle_visualization(self, visualize):
        self.visualize = visualize

    def wheel_impulse(self, impulse):
        self.lone_wheel.obj_space.body.apply_impulse((impulse*5000, 0))

    def toggle_wind(self):
        if self.wind == 0:
            self.wind = random.randint(-500, 500)
        else:
            self.wind = 0

    def update(self, dt):
        self.lone_wheel.update()
        self.smiley.update()
        self.rod.update(self)
        self.smiley.obj_space.body.velocity *= 0.98
        self.lone_wheel.obj_space.body.velocity *= 0.98
        self.angular_velocity = self.get_pole_angular_velocity()
        self.learner.step(self)
        if self.run_pyglet:
            self.smiley.obj_space.body.apply_impulse((self.wind, 0))
        self.space.step(dt)
