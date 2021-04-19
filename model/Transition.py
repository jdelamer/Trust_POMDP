def execute_action(maze, position, action):
    cell = maze.cell_at(position[0], position[1])
    if cell.wall(action.direction):
        return cell
    else:
        new_position = position
        if action.direction == "S":
            new_position = [new_position[0], new_position[1] + 1]
        elif action.direction == "N":
            new_position = [new_position[0], new_position[1] - 1]
        elif action.direction == "E":
            new_position = [new_position[0] + 1, new_position[1]]
        elif action.direction == "W":
            new_position = [new_position[0] - 1, new_position[1]]
        return maze.cell_at(new_position[0], new_position[1])
