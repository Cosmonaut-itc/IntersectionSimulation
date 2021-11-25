import numpy as np
# Model design
import agentpy as ap

class Vehicle(ap.Agent):
    # TODO: agregar metodo para moverse en neighbors con la tag carretera
    # TODO: agregar metodo para interactuar con los distintos estados del semaforo
    def setup(self):
        self.pos = [0,0]
        self.grid = self.model.grid
        self.road = 2
        self.side = [1, 0]
        self.speed = 1
        self.max_speed = 20

    def position(self):
        self.pos = self.grid.positions[self]

    def direction(self):
        if self.pos[1] == 0:
            self.side = [0, 1]

    def movement(self):
        self.grid.move_by(self, [self.speed * self.side[0], self.speed * self.side[1]])

    def speed_update(self):
        next_car = self.grid.positions[self]

        min_dist = 100000000
        for car in self.model.vehicles:
            if car != self:
                same_dir = self.side[0]*car.side[0] + self.side[1]*car.side[1]

                car_pos = self.grid.positions[car]

                road_pos = (car_pos[0] - same_dir[0])*self.side[0] + (car_pos[1] - same_dir[1]) * self.side[1]



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
            car.position()
            car.direction()
            car.movement()

    def end(self):
        pass


parameters = {
    'Vehicles': 2,
    'steps': 5,
}

sample = ap.Sample(parameters, n=30)
# Perform experiment
exp = ap.Experiment(IntersectionModel, sample, iterations=40)
results = exp.run()
