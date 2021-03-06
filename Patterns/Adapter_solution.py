class MappingAdapter:
    def __init__(self, adaptee):
        self.adaptee = adaptee

    def lighten(self, grid):
        lights, obtacles = self.__find_all(grid)
        height, width = len(grid[0]), len(grid)
        self.adaptee.set_dim((height, width))
        self.adaptee.set_lights(lights)
        self.adaptee.set_obstacles(obtacles)
        return self.adaptee.generate_lights()

    def __find_all(self, grid):
        lights = []
        obtacles = []
        for i, j in enumerate(grid):
            for k, g in enumerate(j):
                if g == 1:
                    lights.append((k, i))
                if g == -1:
                    obtacles.append((k, i))
        return lights, obtacles


if __name__ == '__main__':
    class Light:
        def __init__(self, dim):
            self.dim = dim
            self.grid = [[0 for i in range(dim[0])] for _ in range(dim[1])]
            self.lights = []
            self.obstacles = []

        def set_dim(self, dim):
            self.dim = dim
            self.grid = [[0 for i in range(dim[0])] for _ in range(dim[1])]

        def set_lights(self, lights):
            self.lights = lights
            self.generate_lights()

        def set_obstacles(self, obstacles):
            self.obstacles = obstacles
            self.generate_lights()

        def generate_lights(self):
            return self.grid.copy()

    class System:
        def __init__(self):
            self.map = self.grid = [[0 for i in range(30)] for _ in range(20)]
            self.map[5][7] = 1  # Источники света
            self.map[5][2] = -1  # Стены

        def get_lightening(self, light_mapper):
            self.lightmap = light_mapper.lighten(self.map)
            # for i in self.lightmap:
            #     print(i)

    sys = System()
    sys.get_lightening(MappingAdapter(Light))
