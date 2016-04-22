# -*- coding: utf-8 -*-
import numpy
import math
import random
from .state import State
import random
import datetime, time

class Controller:
    def __init__(self, game, load, state):
        self.initialize_parameters(game, load, state)
        self.last_parameters = self.parameters
        self.last_performance = 0

    def initialize_parameters(self, game, load,state):
        self.state = state
        if load == None:
            self.parameters = numpy.random.normal(0, 1, 3*len(self.compute_features()))
        else:
            params = open(load, 'r')
            weights = params.read().split("\n")
            self.parameters = [float(x.strip()) for x in weights[0:-1]]


    def output(self, episode, performance):
       print "Performance do episodio #%d: %d" % (episode, performance)
       if episode > 0 and episode % 10 == 0:
           output = open("./params/%s.txt" % datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d%H%M%S'), "w+")
           for parameter in self.parameters:
               output.write(str(parameter) + "\n")

#--------------------------------------------------------------------------------------------------------

    #FUNCAO A SER COMPLETADA. Deve utilizar os pesos para calcular as funções de preferência Q para cada ação e retorna
    #-1 caso a ação desejada seja esquerda, +1 caso seja direita, e 0 caso seja ação nula
    def take_action(self, state):
        self.state = state
        features = self.compute_features()
        parameters = self.parameters

        e = parameters[0] * features[0] + parameters[1] * features[1] + parameters[2] * features[1]
        
        n = parameters[2] * features[0] + parameters[3] * features[1] + parameters[4] * features[1]
        
        d = parameters[5] * features[0] + parameters[6] * features[1] + parameters[7] * features[1]
        
        if d > e and d > n: #melhor = direita
            return 1
        elif e > n: #melhor = esquerda
            return -1
        else: #melhor = ficar parado
            return 0

    #FUNCAO A SER COMPLETADA. Deve calcular features expandidas do estados (Dica: deve retornar um vetor)
    def compute_features(self):
        features = []

        x = self.state.wheel_x
        vel = self.state.angular_velocity
        ang = self.state.rod_angle

        features.append(x)
        features.append(vel)
        features.append(ang)

        return features

        
    #FUNCAO A SER COMPLETADA. Deve atualizar a propriedade self.parameters
    def update(self, episode, performance): #SIMULATED ANNEALING
        temperature = (10000/(episode+1))
        if performance > self.last_performance: #se for melhor, salva o novo, senão, depende da probabilidade/temperatura
                self.last_parameters = self.parameters
                self.last_performance = performance
        else:
            if temperature > 0:
                diff = performance - self.last_performance
                prob = math.e**(diff/temperature)
                if (round(random.uniform(0,1),5) <= prob): #será considerado, mesmo sendo pior; senão, não será atualizado
                    self.last_parameters = self.parameters
                    self.last_performance = performance

        disturb = numpy.random.normal(0, 1, 3*len(self.compute_features()))
        #disturb *= 0.1
        self.parameters += disturb
