import random
import sys
import time

from utils import Environment, Graph
import pygame

if __name__ == '__main__':

    dims = (1280, 720)
    start = (100, 100)
    goal = (1000, 560)

    if len(sys.argv) != 2:
        raise Exception('Invalid Number of Arguments')

    obstacles = []

    if sys.argv[1] == '--random' or sys.argv[1] == '-r':
        counter = 0

        while counter < 35:
            obstacle = (random.uniform(0, dims[0] - 50), random.uniform(0, dims[1] - 50), 50, 50)
            rect = pygame.Rect(obstacle)

            if pygame.Rect.collidepoint(rect, start) or pygame.Rect.collidepoint(rect, goal):
                continue

            obstacles.append(obstacle)
            counter += 1

    elif sys.argv[1] == '--blocked' or sys.argv[1] == '-b':
        obstacles.append((600, 0, 50, 720))

    elif sys.argv[1] == '--narrow' or sys.argv[1] == '-n':
        obstacles = [
            (600, 0, 50, 550),
            (600, 570, 50, 150)
        ]

    elif sys.argv[1] == '--standard' or sys.argv[1] == '-s':
        obstacles = [
            (500, 20, 50, 500),
            (20, 300, 400, 50),
            (650, 200, 200, 50),
            (850, 200, 50, 450)
        ]

    else:
        raise Exception('Invalid Argument')

    pygame.init()

    environment_map = Environment(start, goal, dims, obstacles)
    rrt_graph = Graph(environment_map.env, start, goal, dims, obstacles)

    pygame.display.update()
    pygame.event.clear()
    pygame.event.wait(5)

    time.sleep(1)

    event = pygame.event.Event(pygame.KEYDOWN)
    pygame.event.post(event)

    execute = True
    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if execute:
                counter = 0
                while not rrt_graph.goal_reached and counter < 1000:
                    if counter % 10 == 0:
                        rrt_graph.bias()
                    else:
                        rrt_graph.add_vertex()
                    counter += 1
                    pygame.display.update()

                if rrt_graph.goal_reached:
                    rrt_graph.highlight_path_to_goal()
                    pygame.display.update()

                execute = False
