import pyglet
import pymunk
import scipy.optimize, numpy
from sys import argv

from game_elements.window import Game
from AI_controller import Learner

NUM_FEATURES = 5

def single_round(parameters):
    #space = pymunk.Space()
    game = Game(space = space, run_pyglet = False, load = None)
    while True:
        game.update(1/60.0)
        if game.learner.current_iteration == 0:
            return game.learner.last_performance*-1

if __name__ == '__main__':
        space = pymunk.Space()

        if len(argv) < 2:
            print "Modo: "
            print "     python __init__.py [learn|evaluate] <arquivo de pesos>"
            print "         learn: aplica o algoritmo de aprendizado (pode receber pesos ou gerar pesos iniciais aleatorios)"
            print "         evaluate: exibe o jogo, permite avaliar os pesos encontrados"
            print "         arquivo de pesos: deve conter os pesps iniciais para as features do sistema"
        else:
            if argv[1] == "learn":
                if len(argv) == 3:
                    game = Game(space = space, run_pyglet = False, load = argv[2])
                else:
                    print "\n\nGerando pesos aleatorios."
                    game = Game(space = space, run_pyglet = False, load = None)
                while True:
                    game.update(1/60.0)
            elif argv[1] == "evaluate":
                if len(argv) == 3:
                    window = Game(space = space, run_pyglet = True, load = argv[2])
                else:
                    print "\nArquivo de pesos deve ser informado."
                    exit()
                pyglet.app.run()
            elif argv[1] == "minimize":
                params = numpy.random.normal(0, 1, 3*NUM_FEATURES)
                print params
                scipy.optimize.minimize(single_round, params, method = 'Powell')
                print params
            else:
                print "Parametro invalido."
