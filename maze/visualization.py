'''This module implements visualization solving of the maze '''
import tkinter as tk
from PIL import ImageTk, Image
from maze import Maze

def resize_image(path: str, size):
    '''Return resized image by entered path'''
    image = Image.open(path)
    image = image.resize((size, size), Image.ANTIALIAS)
    new_img = ImageTk.PhotoImage(image)
    return new_img

def draw_maze(maze):
    '''
    Draw maze solution by tkinter
    Each cell has its own specific color:
    * black - wall
    * white - unvisited cell
    * green - founded path
    * red - visited cells that are not included in the path
    '''
    root = tk.Tk()
    root.title('Maze')
    matrix = maze.array
    rows = matrix.num_rows()
    cols = matrix.num_cols()
    root.geometry(f"{round(500*(cols/rows))}x500")
    size = 500/rows

    for i in range(rows):
        for j in range(cols):
            mark = matrix[i, j].mark
            if mark == '*':
                color = 'black'
            elif mark == 'x':
                color = '#66ff66'
            elif mark == 'o':
                color = '#ff4d4d'
            else:
                color = 'white'

            cell = tk.Text(bg=color)
            if matrix[i, j] == maze.start:
                start = resize_image('images/start.png', round(size))
                cell.image_create("current", image=start)

            elif matrix[i, j] == maze.end:
                img = resize_image('images/finish.png', round(size))
                cell.image_create("current", image=img)
            cell.place(x=j*size,y=i*size)

    root.mainloop()

def main(path: str):
    '''Main function'''
    maze = Maze(path)
    maze.find_path()
    draw_maze(maze)

if __name__ == '__main__':
    main('big_maze.txt')
