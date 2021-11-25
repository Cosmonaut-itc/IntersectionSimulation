import numpy as np
# Model design
import agentpy as ap

# Visualization
import matplotlib.pyplot as plt
import seaborn as sns
import IPython


# TODO : generar en diferentes tiempos los carros

class Vehicle(ap.Agent):
    # TODO: corregir el metodo de movement para que el carro deje de moverse solamente cuando este adyacente al semaforo y este esté en rojo.
    # TODO: agregar que el carro se pare cuando tiene un carro en frente parado
    def setup(self):
        self.grid = self.model.grid
        self.pos = [0, 0]
        self.road = 2
        self.side = [1, 0]
        self.speed = 1
        self.crossed = False

    def direction(self):
        self.pos = self.grid.positions[self]
        if self.pos[1] == 0:
            self.side = [0, 1]

    def movement(self):
        self.direction()
        '''
        for stop in self.model.stop_sign:
            if stop.pos[0] - 1 == self.pos[0] or stop.pos[1] - 1 == self.pos[1]:
                if stop.status == 1:
                    self.grid.move_by(self, [self.speed * self.side[0], self.speed * self.side[1]])
                elif stop.status == 0:
                    self.grid.move_by(self, [self.speed * self.side[0], self.speed * self.side[1]])
        '''
        self.grid.move_by(self, [self.speed * self.side[0], self.speed * self.side[1]])


class StopSign(ap.Agent):
    # TODO: Agregar metodo que calcule el cambio de estados del semaforo dependiendo de la cantidad de carros.
    def setup(self):
        self.status = 1
        self.road = 3
        self.grid = self.model.grid
        self.pos = [0, 0]

    def positions(self):
        self.pos = self.grid.positions[self]


class Roads(ap.Agent):
    def setup(self):
        self.road = 1
        self.condition = 1


class IntersectionModel(ap.Model):
    def setup(self):
        # Define the grid. Hard coded 10x10
        self.grid = ap.Grid(self, [10] * 2, track_empty=True)

        # Define the agents
        n_vehicles = self.p['Vehicles']
        n_roads = 20

        # Define the agents representing the vehicles
        self.vehicles = ap.AgentList(self, n_vehicles, Vehicle)

        # Define the agents representing the road and the stop sign
        self.road = ap.AgentList(self, n_roads, Roads)
        self.stop_sign = ap.AgentList(self, 2, StopSign)

        # Creates the atribute grid in both agent vehicles in order to acces values like position
        self.vehicles.grid = self.grid

        # Location array, creates an array of tuples representing the location of the road tiles in the grid
        road_pos = []
        for i in range(20):
            if i <= 9:
                road_pos.append((i, 4))
            else:
                road_pos.append((4, i - 10))

        # Add agents to the grid in their respective position
        self.grid.add_agents(self.road, road_pos)  # for loop adds road in order to do an intersection
        self.grid.add_agents(self.vehicles, positions=[(0, 4), (4, 0)])
        self.grid.add_agents(self.stop_sign, positions=[(3, 5), (5, 3)])

    def step(self):
        # TODO: agregar logica para la interaccion entre el objeto semaforo y objeto vehiculo
        moving_cars_1 = self.vehicles

        for car in moving_cars_1:
            car.movement()

    def end(self):
        pass


parameters = {
    'Vehicles': 2,
    'steps': 20,
}


def animation_plot(model, ax):
    attr_grid = model.grid.attr_grid('road')
    color_dict = {0: '#d5e5d5', 1: '#e5e5e5', 2: '#d62c2c', 3: '#FFFF00', None: '#7FC97F'}  # '#d5e5d5' '#d62c2c'
    ap.gridplot(attr_grid, ax=ax, color_dict=color_dict, convert=True)


fig, ax = plt.subplots()
model = IntersectionModel(parameters)
animation = ap.animate(model, fig, ax, animation_plot)
IPython.display.HTML(animation.to_jshtml(fps=30))
