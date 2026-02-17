import tkinter as tk
import random

BOARD_SIZE = 3 


class Vertex:
    def __init__(self, val):
        self.val = val


class Edge:
    def __init__(self, origin, dest, val):
        self.origin = origin
        self.dest = dest
        self.val = val


class Graph:
    def __init__(self):
        self.vertices = []
        self.edgeList = []

    def addVertex(self, val):
        self.vertices.append(Vertex(val))

    def addEdge(self, origin, dest, val):
        self.edgeList.append(Edge(origin, dest, val))

    def updatevalue(self, idx, value):
        self.vertices[idx].val = value


def createList(N):
    g = Graph()

    for _ in range(N * N):
        g.addVertex("")

    winning_lines = []

    # rows
    for r in range(N):
        winning_lines.append([r * N + c + 1 for c in range(N)])

    # columns
    for c in range(N):
        winning_lines.append([r * N + c + 1 for r in range(N)])

    # diagonals
    winning_lines.append([i * N + i + 1 for i in range(N)])
    winning_lines.append([(i + 1) * N - i for i in range(N)])

    for line in winning_lines:
        for i in range(len(line) - 1):
            g.addEdge(line[i], line[i + 1], 1)

    return g, winning_lines

graph_list = []
WINNING_LINES = []

for _ in range(9):
    g, WINNING_LINES = createList(BOARD_SIZE)
    graph_list.append(g)

big_boardgraph, _ = createList(BOARD_SIZE)



def dfs_check_line(boardgraph, line, index, symbol):
    if index == len(line):
        return True
    if boardgraph.vertices[line[index] - 1].val != symbol:
        return False
    return dfs_check_line(boardgraph, line, index + 1, symbol)



def dac_check_line(boardgraph, line, symbol):
    def helper(start, end):
        if start == end:
            return boardgraph.vertices[line[start] - 1].val == symbol

        mid = (start + end) // 2

        return (
            helper(start, mid) and
            helper(mid + 1, end)
        )

    return helper(0, len(line) - 1)


def sb_checkwinner(f_index):
    boardgraph = graph_list[f_index - 1]

    if big_boardgraph.vertices[f_index - 1].val in ["X", "O", "-"]:
        return True

    for symbol in ["X", "O"]:
        for line in WINNING_LINES:
            if dac_check_line(boardgraph, line, symbol):
                big_boardgraph.updatevalue(f_index - 1, symbol)
                add_label(symbol, f_index)
                return True

    if all(v.val in ["X", "O"] for v in boardgraph.vertices):
        big_boardgraph.updatevalue(f_index - 1, "-")
        add_label("-", f_index)
        return True

    return False


def big_board_check_winner():
    for symbol in ["X", "O"]:
        for line in WINNING_LINES:
            if dac_check_line(big_boardgraph, line, symbol):
                show_big_winner(symbol)
                return True

    if all(v.val in ["X", "O", "-"] for v in big_boardgraph.vertices):
        show_big_winner("-")
        return True

    return False

def add_label(val, f_index):
    for widget in sf[f_index - 1].winfo_children():
        if isinstance(widget, tk.Label):
            widget.destroy()

    tk.Label(
        sf[f_index - 1],
        text=val,
        font=("Arial", 38, "bold"),
        bg="#FAB95B",  # Changed: start with highlight color
        fg="white"
    ).place(x=0, y=0, height=160, width=180)


def show_big_winner(winner):
    disable_button()

    popup = tk.Toplevel(w)
    popup.title("Game Over")
    popup.geometry("300x160")
    popup.resizable(False, False)
    popup.config(bg="#547792")

    if winner in ["X", "O"]:
        tk.Label(
            popup,
            text=f"Player {winner} won the big board!",
            font=("Arial", 14, "bold"),
            bg="#547792"
        ).pack(pady=20)
    else:
        tk.Label(
            popup,
            text=f"It's a Draw!",
            font=("Arial", 14, "bold"),
            bg="#547792"
        ).pack(pady=20)

    tk.Button(
        popup,
        text="Play Again",
        font=("Arial", 12, "bold"),
        bg="#0078FF",
        fg="white",
        relief="flat",
        command=lambda: (popup.destroy(), reset_game())
    ).pack(pady=5)

    tk.Button(
        popup,
        text="Exit",
        font=("Arial", 12, "bold"),
        bg="#FF4C4C",
        fg="white",
        relief="flat",
        command=w.destroy
    ).pack(pady=5)


def disable_button():
    for row in buttons:
        for btn in row:
            btn.config(state="disabled")

def enable_button(board_index):
    for i in range(BOARD_SIZE * BOARD_SIZE):
        if graph_list[board_index].vertices[i].val == "":
            buttons[board_index][i].config(state="normal")
        else:
            buttons[board_index][i].config(state="disabled")


def reset_frame_colors():
    # Reset all frames and their contents to default (white/dark blue)
    for i, frame in enumerate(sf):
        frame.config(bg="white", bd=2, relief="ridge")
        
        # Reset buttons to default color
        for btn in buttons[i]:
            btn.config(bg="SystemButtonFace")
        
        # Reset any labels back to dark blue
        for widget in frame.winfo_children():
            if isinstance(widget, tk.Label):
                widget.config(bg="#547792")



def highlight_frame(board_index):
    reset_frame_colors()
    sf[board_index].config(bg="#FAB95B", bd=4, relief="solid")
    
    # Highlight the buttons in this frame
    for btn in buttons[board_index]:
        btn.config(bg="#FAB95B")
    
    # Also update any labels covering the frame (from won boards)
    for widget in sf[board_index].winfo_children():
        if isinstance(widget, tk.Label):
            widget.config(bg="#FAB95B")


def enable_all_valid_boards():
    reset_frame_colors()

    for i in range(9):
        if big_boardgraph.vertices[i].val == "":
            sf[i].config(bg="#FAB95B", bd=4, relief="solid")
            
            # Highlight buttons in this frame
            for btn in buttons[i]:
                btn.config(bg="#FAB95B")
            
            # Also update any labels on this frame
            for widget in sf[i].winfo_children():
                if isinstance(widget, tk.Label):
                    widget.config(bg="#FAB95B")
            
            enable_button(i)


def display_values():
    for bi in range(9):
        for ci in range(BOARD_SIZE * BOARD_SIZE):
            buttons[bi][ci].config(
                text=graph_list[bi].vertices[ci].val
            )


def displaymove(a, v, f):
    if v == "notallowed":
        move_label.config(
            text=f"CPU played F{f+1} C{a+1}. Make a move in any unoccupied frame."
        )
    else:
        move_label.config(
            text=f"CPU played F{f+1} C{a+1}. Your next move should be in F{a+1}."
        )

def evaluate_move(boardgraph, idx):

    score = 0

    boardgraph.vertices[idx].val = "O"

    for line in WINNING_LINES:
        vals = [boardgraph.vertices[i - 1].val for i in line]
        if vals.count("O") == BOARD_SIZE:
            score += 3

  
    for line in WINNING_LINES:
        vals = [boardgraph.vertices[i - 1].val for i in line]
        if vals.count("X") == BOARD_SIZE - 1 and vals.count("O") == 1:
            score += 2

    next_board = idx

  
    if big_boardgraph.vertices[next_board].val in ["X", "O", "-"]:
        score += 2
    else:
        next_boardgraph = graph_list[next_board]
        danger = 0

        for line in WINNING_LINES:
            vals = [next_boardgraph.vertices[i - 1].val for i in line]
            if vals.count("X") == BOARD_SIZE - 1 and vals.count("") == 1:
                danger += 1

        if danger == 0:
            score += 1

    boardgraph.vertices[idx].val = ""

    return score

def cpu_move(b_index):
    f = b_index - 1
    board = graph_list[f]

    if big_boardgraph.vertices[f].val in ["X", "O", "-"]:
        valid = [i for i in range(9)
                 if big_boardgraph.vertices[i].val == ""
                 and any(v.val == "" for v in graph_list[i].vertices)]
        if not valid:
            return None
        f = random.choice(valid)
        board = graph_list[f]

    for line in WINNING_LINES:
        vals = [board.vertices[i - 1].val for i in line]
        if vals.count("O") == BOARD_SIZE - 1 and vals.count("") == 1:
            idx = line[vals.index("")] - 1
            board.updatevalue(idx, "O")
            return idx, f

    for line in WINNING_LINES:
        vals = [board.vertices[i - 1].val for i in line]
        if vals.count("X") == BOARD_SIZE - 1 and vals.count("") == 1:
            idx = line[vals.index("")] - 1
            board.updatevalue(idx, "O")
            return idx, f

    center_idx = (BOARD_SIZE * BOARD_SIZE) // 2
    if board.vertices[center_idx].val == "":
        board.updatevalue(center_idx, "O")
        return center_idx, f

    if BOARD_SIZE == 3:
        corners = [i for i in [0, 2, 6, 8] if board.vertices[i].val == ""]
        if corners:
            idx = random.choice(corners)
            board.updatevalue(idx, "O")
            return idx, f

    empty = [i for i, v in enumerate(board.vertices) if v.val == ""]
    if empty:
        idx = random.choice(empty)
        board.updatevalue(idx, "O")
        return idx, f

    return None


def cpu_turn(b_index):
    move = cpu_move(b_index)
    if not move:
        big_board_check_winner()
        return

    cell, frame = move
    display_values()
    sb_checkwinner(frame + 1)

    if big_board_check_winner():
        return

    if big_boardgraph.vertices[cell].val in ["X", "O", "-"]:
        enable_all_valid_boards()
        displaymove(cell, "notallowed", frame)
    else:
        highlight_frame(cell)
        enable_button(cell)
        displaymove(cell, "allowed", frame)


def clicked(f_index, b_index):
    if graph_list[f_index - 1].vertices[b_index - 1].val != "":
        return

    if big_boardgraph.vertices[f_index - 1].val in ["X", "O", "-"]:
        return

    disable_button()
    graph_list[f_index - 1].updatevalue(b_index - 1, "X")
    display_values()

    sb_checkwinner(f_index)

    if big_board_check_winner():
        return

    w.after(1000, lambda: cpu_turn(b_index))

def reset_game():
    global graph_list, big_boardgraph

    graph_list = []
    for _ in range(9):
        g, _ = createList(BOARD_SIZE)
        graph_list.append(g)

    big_boardgraph, _ = createList(BOARD_SIZE)

    for row in buttons:
        for btn in row:
            btn.config(text="", state="normal")

    for frame in sf:
        for widget in frame.winfo_children():
            if isinstance(widget, tk.Label):
                widget.destroy()

    enable_all_valid_boards()
    move_label.config(text="You start! Make your move anywhere.")

w = tk.Tk()
w.geometry("1024x720")
w.title("X-O Nexus")
w.resizable(False, False)

f_bg = tk.Frame(w, bd=2, relief="ridge", bg="#547792")
f_bg.place(x=0, y=0, height=720, width=1024)

l1 = tk.Label(w, text="X-O Nexus", font=("Arial", 24, "bold"), bg="#547792",fg="#E1EBEE")
l1.place(x=437, y=40)

sf = []
buttons = []

base_x = 238
base_y = 110

for i in range(9):
    frame = tk.Frame(f_bg, bd=2, relief="ridge", bg="white")
    frame.place(
        x=base_x + (i % 3) * 183,
        y=base_y + (i // 3) * 162,
        width=180,
        height=160
    )
    sf.append(frame)

    btns = []
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            idx = r * BOARD_SIZE + c + 1
            btn = tk.Button(
                frame,
                width=5,
                height=2,
                font=("Arial", 12, "bold"),
                command=lambda f=i + 1, b=idx: clicked(f, b)
            )
            btn.place(x=c * 60, y=r * 52)
            btns.append(btn)

    buttons.append(btns)

tk.Label(w, bg="#003153").place(x=420, y=112, width=5, height=482)
tk.Label(w, bg="#003153").place(x=603, y=112, width=5, height=482)
tk.Label(w, bg="#003153").place(x=238, y=270, width=550, height=5)
tk.Label(w, bg="#003153").place(x=238, y=432, width=549, height=5)
tk.Label(w, bg="#003153").place(x=238, y=112, width=5, height=482)
tk.Label(w, bg="#003153").place(x=787, y=112, width=5, height=486)
tk.Label(w, bg="#003153").place(x=238, y=112, width=550, height=5)
tk.Label(w, bg="#003153").place(x=238, y=594, width=553, height=5)

tk.Button(
    w, text="RESET", font=("Arial", 14, "bold"),
    relief="groove", command=reset_game
).place(x=462, y=665)

move_label = tk.Label(
    f_bg, text="You start! Make your move anywhere.",
    font=("Arial", 16, "bold"), bg="#547792",fg="#E1EBEE"
)
move_label.place(x=180, y=620)

# Highlight all frames at game start
enable_all_valid_boards()

w.mainloop()
