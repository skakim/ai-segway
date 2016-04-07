from .controller import Controller
from .state      import State
MAX_STEPS = 10000
VISUALIZE = True
NUM_EPISODES = 20

class Learner:
    def __init__(self, game, load):
        self.current_iteration = 0
        self.last_performance = 0
        game.toggle_visualization(VISUALIZE)
        self.controller = Controller(game, load, State(game.get_pole_angle(),
                                                    game.angular_velocity,
                                                    game.lone_wheel.x))

    def step(self, game):
        if (self.current_iteration == MAX_STEPS or game.out_of_screen()):
            self.controller.output(game.epoch, self.get_performance())
            if not game.run_pyglet:
                self.controller.update(game.epoch, self.get_performance())
            game.reset(self.get_performance())
            self.last_performance = self.get_performance()
            self.current_iteration = 0
            # if game.epoch == NUM_EPISODES:
            #     exit()
        else:
            self.current_iteration += 1
            impulse = self.controller.take_action(State(game.get_pole_angle(),
                                                        game.angular_velocity,
                                                        game.lone_wheel.x))
            game.wheel_impulse(impulse)

    def get_performance(self):
        performance = 2*MAX_STEPS + 2*(self.current_iteration - MAX_STEPS)
        return performance
