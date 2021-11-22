import numpy as np
# Model design
import agentpy as ap

# Visualization
import matplotlib.pyplot as plt
import seaborn as sns
import IPython


class Vehicle(ap.Agent):
    # TODO: agregar metodo para moverse en neighbors con la tag carretera
    # TODO: agregar metodo para interactuar con los distintos estados del semaforo
    def setup(self):
        self.movimiento = False
        self.grid = self.model.grid
        self.road = 2
        self.side = 0

    def movement(self):
        if self.side == 0:
            self.grid.move_by(self, (1, 0))
        elif self.side == 1:
            self.grid.move_by(self, (0, 1))


class StopSign(ap.Agent):
    # TODO: Agregar estados del semaforo: verde, amarillo, rojo.
    def setup(self):
        self.status = 1
        self.road = 3
        self.grid = self.model.grid


class Roads(ap.Agent):
    def setup(self):
        self.road = 1
        self.condition = 1


class IntersectionModel(ap.Model):

    def setup(self):
        # TODO: agregar agentes: 1.Vehiculo, 2. Carretera, 3. Semaforo

        # Define the grid. Hard coded 10x10
        self.grid = ap.Grid(self, [10] * 2, track_empty=True)

        # Define the agents
        n_vehicles = self.p['Vehicles']
        n_roads = 20

        # Define the agents representing the vehicles
        self.vehicles_1 = ap.AgentList(self, n_vehicles, Vehicle)
        self.vehicles_2 = ap.AgentList(self, n_vehicles, Vehicle)

        # Define the agents representing the road and the stop sign
        self.road = ap.AgentList(self, n_roads, Roads)
        self.stop_sign = ap.AgentList(self, 2, StopSign)

        # Creates the atribute grid in both agent vehicles in order to acces values like position
        self.vehicles_1.grid = self.grid
        self.vehicles_2.grid = self.grid

        # Defines the side of the vehicle
        self.vehicles_2.side = 1

        # Location array, creates an array of tuples representing the location of the road tiles in the grid
        road_pos = []
        for i in range(20):
            if i <= 9:
                road_pos.append((i, 4))
            else:
                road_pos.append((4, i - 10))

        # Add agents to the grid in their respective position
        self.grid.add_agents(self.road, road_pos)  # for loop adds road in order to do an intersection
        self.grid.add_agents(self.vehicles_1, positions=[(0, 4)])
        self.grid.add_agents(self.vehicles_2, positions=[(4, 0)])
        self.grid.add_agents(self.stop_sign, positions=[(3, 5), (5, 3)])

    def step(self):
        # TODO: agregar logica para la interaccion entre el objeto semaforo y objeto vehiculo
        moving_cars_1 = self.vehicles_1
        moving_cars_2 = self.vehicles_2

    def end(self):
        pass


parameters = {
    'Vehicles': 1,
    'steps': 5,
}


def animation_plot(model, ax):
    attr_grid = model.grid.attr_grid('road')
    color_dict = {0: '#d5e5d5', 1: '#e5e5e5', 2: '#d62c2c', 3: '#FFFF00', None: '#7FC97F'}  # '#d5e5d5' '#d62c2c'
    ap.gridplot(attr_grid, ax=ax, color_dict=color_dict, convert=True)


fig, ax = plt.subplots()
model = IntersectionModel(parameters)
animation = ap.animate(model, fig, ax, animation_plot)
IPython.display.HTML(animation.to_jshtml(fps=15))
