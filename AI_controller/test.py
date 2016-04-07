
import pymunk
import scipy
from game_elements.window import Game
from .state import State
from . import MAX_STEPS

def run_episode(params):
    game = Game(space = pymunk.Space(), numpy_test = True, load = None)
    game.learner.controller.parameters = params
    while game.learner.current_iteration < MAX_STEPS and not game.out_of_screen():
        game.learner.current_iteration += 1
        impulse = game.learner.controller.take_action(State(game.get_pole_angle(),
                                                    game.angular_velocity,
                                                    game.lone_wheel.x))
        game.wheel_impulse(impulse)
        game.update(1/60.0)
    game.learner.controller.update(game.epoch, game.learner.get_performance())
    return game.learner.get_performance()

def save_params(params):
    result = open('params.txt', 'w+')
    for w in params:
        result.write(str(w) + '\n')
