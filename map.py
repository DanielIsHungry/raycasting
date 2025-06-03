import tkinter as tk
import random

GRID_WIDTH = 100
GRID_HEIGHT = 20
TILE_SIZE = 20

class MapEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Doom Map Editor")
        self.canvas = tk.Canvas(root, width=GRID_WIDTH*TILE_SIZE, height=GRID_HEIGHT*TILE_SIZE, bg="white")
        self.canvas.pack()

        self.tiles = set()
        self.dragged_tiles = set()
        self.drawing = True  # True = add wall, False = remove wall

        self.canvas.bind("<Button-1>", self.start_drag)
        self.canvas.bind("<B1-Motion>", self.drag_tile)
        self.canvas.bind("<ButtonRelease-1>", self.end_drag)

        self.output = tk.Text(root, height=5, width=50)
        self.output.pack()

        btn_frame = tk.Frame(root)
        btn_frame.pack()

        copy_btn = tk.Button(btn_frame, text="Copy to Clipboard", command=self.copy_to_clipboard)
        copy_btn.pack(side=tk.LEFT)

        maze_btn = tk.Button(btn_frame, text="Generate Maze", command=self.generate_maze)
        maze_btn.pack(side=tk.LEFT)

        self.draw_grid()

    def draw_grid(self):
        for x in range(0, GRID_WIDTH*TILE_SIZE, TILE_SIZE):
            for y in range(0, GRID_HEIGHT*TILE_SIZE, TILE_SIZE):
                self.canvas.create_rectangle(x, y, x+TILE_SIZE, y+TILE_SIZE, outline="gray")

    def get_tile_pos(self, event):
        return (event.x // TILE_SIZE, event.y // TILE_SIZE)

    def draw_tile(self, pos):
        if pos in self.dragged_tiles:
            return
        self.dragged_tiles.add(pos)

        x1, y1 = pos[0]*TILE_SIZE, pos[1]*TILE_SIZE
        x2, y2 = x1 + TILE_SIZE, y1 + TILE_SIZE

        if self.drawing:
            self.tiles.add(pos)
            self.canvas.create_rectangle(x1, y1, x2, y2, fill="black", outline="gray")
        else:
            self.tiles.discard(pos)
            self.canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="gray")

        self.update_output()

    def start_drag(self, event):
        pos = self.get_tile_pos(event)
        self.drawing = pos not in self.tiles
        self.dragged_tiles = set()
        self.draw_tile(pos)

    def drag_tile(self, event):
        pos = self.get_tile_pos(event)
        self.draw_tile(pos)

    def end_drag(self, event):
        self.dragged_tiles.clear()

    def update_output(self):
        self.output.delete("1.0", tk.END)
        lines = ["{"]
        for t in sorted(self.tiles):
            lines.append(f"    {t},")
        lines.append("}")
        self.output.insert(tk.END, "".join(lines))

    def copy_to_clipboard(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.output.get("1.0", tk.END))
        self.root.update()

    def redraw_tiles(self):
        self.canvas.delete("all")
        self.draw_grid()
        for pos in self.tiles:
            x1, y1 = pos[0] * TILE_SIZE, pos[1] * TILE_SIZE
            x2, y2 = x1 + TILE_SIZE, y1 + TILE_SIZE
            self.canvas.create_rectangle(x1, y1, x2, y2, fill="black", outline="gray")

    def generate_maze(self):
        cols = GRID_WIDTH // 2
        rows = GRID_HEIGHT // 2
        visited = set()

        def carve(x, y):
            visited.add((x, y))
            directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
            random.shuffle(directions)

            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < cols and 0 <= ny < rows and (nx, ny) not in visited:
                    wall_x = x + nx + 1
                    wall_y = y + ny + 1
                    self.tiles.add((x * 2 + 1, y * 2 + 1))
                    self.tiles.add((nx * 2 + 1, ny * 2 + 1))
                    self.tiles.add((wall_x, wall_y))
                    carve(nx, ny)

        self.tiles.clear()
        carve(0, 0)
        self.redraw_tiles()
        self.update_output()

if __name__ == "__main__":
    root = tk.Tk()
    app = MapEditor(root)
    root.mainloop()
