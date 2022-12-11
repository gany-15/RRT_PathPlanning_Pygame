import pygame
import random
import math


class Environment:
    def __init__(self, start, goal, dims, obstacles):
        self.start = start
        self.goal = goal
        self.width, self.height = dims
        self.obstacles = obstacles

        pygame.display.set_caption('Path Planning in Search Space using Rapidly exploring Random Trees')
        self.env = pygame.display.set_mode((self.width, self.height))

        env_fill_colour = (235, 235, 235)
        self.env.fill(env_fill_colour)

        self.vertex_radius = 5
        self.vertex_size = 5

        self.obstacles = obstacles

        self.draw_env()
        self.draw_obstacles()

    def draw_env(self):
        pygame.draw.circle(self.env, (100, 255, 100), self.start, self.vertex_radius, self.vertex_size)
        pygame.draw.circle(self.env, (255, 100, 100), self.goal, self.vertex_radius, self.vertex_size)

    def draw_obstacles(self):
        for obstacle in self.obstacles:
            pygame.draw.rect(self.env, (50, 50, 50), obstacle)


class Graph:
    def __init__(self, env, start, goal, dims, obstacles):
        self.env = env
        self.start = start
        self.goal = goal
        self.width, self.height = dims
        self.obstacles = obstacles
        self.vertices: list[tuple[tuple, tuple, int]] = [ (tuple(start), tuple(), 0) ]
        self.goal_reached = False

    def add_vertex(self):
        while True:
            x = random.uniform(0, self.width)
            y = random.uniform(0, self.height)

            nearest_vertex = ()
            distance = 9999
            index = -1

            for i, vertex in enumerate(self.vertices):
                dist = math.dist(vertex[0], (x, y))
                if dist < distance:
                    distance = dist
                    nearest_vertex = vertex[0]
                    index = i

            if math.dist(nearest_vertex, (x, y)) > 100:
                continue

            if self.in_free_space(nearest_vertex, (x, y)):
                self.vertices.append(((x, y), nearest_vertex, index))
                pygame.draw.circle(self.env, (0, 0, 255), (x, y), 3)
                pygame.draw.line(self.env, (200, 200, 200), nearest_vertex, (x, y))
                return

    def in_free_space(self, vertex, new_vert):
        for obstacle in self.obstacles:
            rect = pygame.Rect(obstacle)
            if rect.collidepoint(new_vert):
                return False
            elif rect.clipline(vertex, new_vert):
                return False
        return True

    def highlight_path_to_goal(self):
        vert = self.vertices[-1]
        while vert[0] != self.start:
            pygame.draw.line(self.env, (50, 200, 50), vert[0], vert[1], 3)
            vert = self.vertices[vert[2]]

    def bias(self):
        nearest_to_goal = ()
        distance = 9999
        index = -1
        for i, vertex in enumerate(self.vertices):
            dist = math.dist(vertex[0], self.goal)
            if dist < distance:
                distance = dist
                nearest_to_goal = vertex[0]
                index = i

        self.vertices.append(self.vertices[index])

        if math.dist(nearest_to_goal, self.goal) <= 100 and self.in_free_space(nearest_to_goal, self.goal):
            self.vertices.append((nearest_to_goal, self.goal, index))
            pygame.draw.line(self.env, (150, 150, 150), nearest_to_goal, self.goal)
            self.goal_reached = True

        else:
            while True:
                x = random.uniform(max(0, nearest_to_goal[0] - 50), min(self.width, nearest_to_goal[0] + 50))
                y = random.uniform(max(0, nearest_to_goal[1] - 50), min(self.height, nearest_to_goal[1] + 50))

                if self.in_free_space(nearest_to_goal, (x, y)):
                    self.vertices.append(((x, y), nearest_to_goal, index))
                    pygame.draw.circle(self.env, (0, 0, 255), (x, y), 3)
                    pygame.draw.line(self.env, (200, 200, 200), nearest_to_goal, (x, y))
                    return
