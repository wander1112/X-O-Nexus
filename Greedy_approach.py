import tkinter as tk
import random

# Classes
class Vertex:
    def __init__(self, val):
        self.val = val


class Edge:
    def __init__(self, origin, dest, val):
        self.val = val
        self.origin = origin
        self.dest = dest


class Graph:
    def __init__(self):
        self.vertices = []
        self.edgeList = []

    def addVertex(self, val):
        v = Vertex(val)
        self.vertices.append(v)

    def addEdge(self, origin, dest, val):
        e = Edge(origin, dest, val)
        self.edgeList.append(e)

    def updatevalue(self, vet, value):
        self.vertices[vet].val = value


def createList():
    g = Graph()
    
    for i in range(1, 10):
        g.addVertex("")  

    e = [(1,2,1),(2,3,1),(3,6,2),(6,9,2),(7,8,3),(8,9,3),
         (1,4,4),(4,7,4),(1,5,8),(5,9,8),(2,5,7),(5,8,7),
         (3,5,6),(5,7,6),(4,5,5),(5,6,5)]
    for u, v, w in e:
        g.addEdge(u, v, w)

    return g


# Initialize game state
graph_list = []
for i in range(1, 10):
    graph_list.append(createList())
big_boardgraph = createList()


def add_label(val, f_index):
    # Remove any existing label in this frame
    for widget in sf[f_index-1].winfo_children():
        if isinstance(widget, tk.Label):
            widget.destroy()
    
    l = tk.Label(sf[f_index-1], text=f"{val}", font=("Arial", 38, "bold"), bg="#f7e7ce")
    l.place(x=0, y=0, height=160, width=180)


def show_big_winner(winner):
    disable_button()
    
    popup = tk.Toplevel(w)
    popup.title("Game Over")
    popup.geometry("300x160")
    popup.resizable(False, False)
    popup.config(bg="#f7e7ce")

    if winner in ["X", "O"]:
        tk.Label(
            popup,
            text=f"Player {winner} won the big board!",
            font=("Arial", 14, "bold"),
            bg="#f7e7ce"
        ).pack(pady=20)
    else:
        tk.Label(
            popup,
            text=f"It's a Draw!",
            font=("Arial", 14, "bold"),
            bg="#f7e7ce"
        ).pack(pady=20)
    
    # Play Again
    tk.Button(
        popup,
        text="Play Again",
        font=("Arial", 12, "bold"),
        bg="#0078FF",
        fg="white",
        relief="flat",
        command=lambda: (popup.destroy(), reset_game())
    ).pack(pady=5)

    # Exit
    tk.Button(
        popup,
        text="Exit",
        font=("Arial", 12, "bold"),
        bg="#FF4C4C",
        fg="white",
        relief="flat",
        command=w.destroy
    ).pack(pady=5)


def bb_checkwinner():
    boardgraph = big_boardgraph
    
    # Check for three in a row
    for e1 in boardgraph.edgeList:
        for e2 in boardgraph.edgeList:
            if e1.val != e2.val:
                continue
            if e1.dest != e2.origin:
                continue

            u = e1.origin  
            v = e1.dest    
            w = e2.dest

            u_val = boardgraph.vertices[u-1].val
            v_val = boardgraph.vertices[v-1].val
            w_val = boardgraph.vertices[w-1].val

            if u_val != "" and u_val == v_val == w_val:
                show_big_winner(u_val)
                return True
    
    # Check for draw (all cells filled)
    all_filled = True
    for v in boardgraph.vertices:
        if v.val not in ["X", "O", "-"]:
            all_filled = False
            break
    
    if all_filled:
        show_big_winner("-")
        return True
    
    return False


def sb_checkwinner(f_index):
    boardgraph = graph_list[f_index-1]
    
    # Check if already won or drawn
    if big_boardgraph.vertices[f_index-1].val in ["X", "O", "-"]:
        return True
    
    # Check for three in a row
    for e1 in boardgraph.edgeList:
        for e2 in boardgraph.edgeList:
            if e1.val != e2.val:
                continue
            if e1.dest != e2.origin:
                continue

            u = e1.origin  
            v = e1.dest    
            w = e2.dest

            u_val = boardgraph.vertices[u-1].val
            v_val = boardgraph.vertices[v-1].val
            w_val = boardgraph.vertices[w-1].val

            if u_val != "" and u_val == v_val == w_val:
                big_boardgraph.updatevalue(f_index-1, v_val)
                add_label(v_val, f_index)
                return True  
    
    # Check for draw (all cells filled with X or O)
    all_filled = True
    for v in boardgraph.vertices:
        if v.val not in ["X", "O"]:
            all_filled = False
            break
    
    if all_filled:
        big_boardgraph.updatevalue(f_index-1, "-")
        add_label("-", f_index)
        return True

    return False


def add_value(f_index, b_index, value):  
    boardgraph = graph_list[f_index-1]
    boardgraph.updatevalue(b_index-1, value)


def display_values():
    for board_index in range(9):
        for cell_index in range(9):
            buttons[board_index][cell_index].config(
                text=graph_list[board_index].vertices[cell_index].val
            )


def disable_button():
    for i in buttons:
        for j in i:
            j.config(state="disabled")


def enable_button(f_index):
    for i in range(9):
        if graph_list[f_index].vertices[i].val == "":
            buttons[f_index][i].config(state="normal")
        else:
            buttons[f_index][i].config(state="disabled")


def enable_all_valid_boards():
    for board_index in range(9):
        if big_boardgraph.vertices[board_index].val == "":
            enable_button(board_index)


def cpu_move(b_index):
    playframe = graph_list[b_index-1]
    f = b_index - 1

    # If target board is won/drawn, choose any available board
    if big_boardgraph.vertices[f].val in ["X", "O", "-"]:
        valid_boards = []
        for i in range(9):
            if big_boardgraph.vertices[i].val == "":
                if any(v.val == "" for v in graph_list[i].vertices):
                    valid_boards.append(i)

        if not valid_boards:
            return None  

        f = random.choice(valid_boards)
        playframe = graph_list[f]

    # Strategy: Block player's winning move first, then try to win
    #First pass: Try to win
    for e1 in playframe.edgeList:
        for e2 in playframe.edgeList:
            if e1.val != e2.val or e1.dest != e2.origin:
                continue

            u, v, w = e1.origin, e1.dest, e2.dest
            u_val = playframe.vertices[u-1].val
            v_val = playframe.vertices[v-1].val
            w_val = playframe.vertices[w-1].val

            # Try to win with O
            if u_val == v_val == "O" and w_val == "":
                playframe.updatevalue(w-1, "O")
                return w-1, f

            if v_val == w_val == "O" and u_val == "":
                playframe.updatevalue(u-1, "O")
                return u-1, f

            if u_val == w_val == "O" and v_val == "":
                playframe.updatevalue(v-1, "O")
                return v-1, f

    #  Second  pass: Check if player (X) can win and block
    for e1 in playframe.edgeList:
        for e2 in playframe.edgeList:
            if e1.val != e2.val or e1.dest != e2.origin:
                continue

            u, v, w = e1.origin, e1.dest, e2.dest
            u_val = playframe.vertices[u-1].val
            v_val = playframe.vertices[v-1].val
            w_val = playframe.vertices[w-1].val

            # Block X's winning move
            if u_val == v_val == "X" and w_val == "":
                playframe.updatevalue(w-1, "O")
                return w-1, f

            if v_val == w_val == "X" and u_val == "":
                playframe.updatevalue(u-1, "O")
                return u-1, f

            if u_val == w_val == "X" and v_val == "":
                playframe.updatevalue(v-1, "O")
                return v-1, f

    
    # Take center if available
    if playframe.vertices[4].val == "":
        playframe.updatevalue(4, "O")
        return 4, f

    # Take a corner if available
    corners = [i for i in [0, 2, 6, 8] if playframe.vertices[i].val == ""]
    if corners:
        c = random.choice(corners)
        playframe.updatevalue(c, "O")
        return c, f

    # Take any empty cell
    empty = [i for i, v in enumerate(playframe.vertices) if v.val == ""]
    if empty:
        c = random.choice(empty)
        playframe.updatevalue(c, "O")
        return c, f

    return None


def displaymove(a, v, f):
    if v == "notallowed":
        move_label.config(
            text=f"CPU played F{f+1} C{a+1}. Make a move in any unoccupied frame."
        )
    else: 
        move_label.config(
            text=f"CPU played F{f+1} C{a+1}. Your next move should be in F{a+1}."
        )


def cpu_turn(b_index):
    result = cpu_move(b_index)
    
    if result is None:
        # No valid moves available
        bb_checkwinner()
        return

    a, f = result
    display_values()
    
    # Check if CPU won the small board
    sb_checkwinner(f+1)
    
    # Check if game is over
    if bb_checkwinner():
        return

    # Determine next player's allowed boards
    if big_boardgraph.vertices[a].val in ["X", "O", "-"]:
        # Board is won/drawn, player can play anywhere
        enable_all_valid_boards()
        displaymove(a, "notallowed", f)
    else:
        # Player must play in specific board
        enable_button(a)
        displaymove(a, "allowed", f)


def clicked(f_index, b_index):
    # Validate: cell must be empty
    if graph_list[f_index-1].vertices[b_index-1].val != "":
        return
    
    # Validate: board must not be won/drawn
    if big_boardgraph.vertices[f_index-1].val in ["X", "O", "-"]:
        return

    disable_button()
    add_value(f_index, b_index, "X")
    display_values()
    
    # Check if player won the small board
    sb_checkwinner(f_index)
    
    # Check if game is over
    if bb_checkwinner():
        return

    # CPU's turn after 1 second
    w.after(1000, lambda: cpu_turn(b_index))

    
def reset_game():
    global graph_list, big_boardgraph

    # Reset game state
    graph_list = []
    for _ in range(9):
        graph_list.append(createList())
    big_boardgraph = createList()

    # Reset all buttons
    for board in buttons:
        for btn in board:
            btn.config(text="", state="normal")

    # Remove overlay labels
    for frame in sf:
        for widget in frame.winfo_children():
            if isinstance(widget, tk.Label):
                widget.destroy()
    
    # Reset message
    move_label.config(text="You start! Make your move anywhere.")


# UI Setup
w = tk.Tk()
w.geometry("1024x720")
w.title("X-O Nexus")
w.resizable(False, False)

f_bg = tk.Frame(w, bd=2, relief="ridge", bg="#f7e7ce")
f_bg.place(x=0, y=0, height=720, width=1024)

l1 = tk.Label(w, text="X-O Nexus", font=("Arial", 24, "bold"), bg="#f7e7ce")
l1.place(x=437, y=40)

sf = []
buttons = []

# Create 9 small boards
a = 238
bpos = 238
c = 238

for i in range(1, 10):
    if i in [1, 2, 3]:
        f_s = tk.Frame(f_bg, bd=2, relief="ridge", bg="white")
        f_s.place(x=a, y=110, height=160, width=180)
        a += 183
        sf.append(f_s)
    elif i in [4, 5, 6]:
        f_s = tk.Frame(f_bg, bd=2, relief="ridge", bg="white")
        f_s.place(x=bpos, y=272, height=160, width=180)
        bpos += 183
        sf.append(f_s)
    elif i in [7, 8, 9]:
        f_s = tk.Frame(f_bg, bd=2, relief="ridge", bg="white")
        f_s.place(x=c, y=434, height=160, width=180)
        c += 183
        sf.append(f_s)
    
    btn_list = []
    d = 0
    f = 0
    g = 0
    
    for j in range(1, 10):
        if j in [1, 2, 3]:
            f_sb = tk.Button(
                f_s, width=5, height=2, font=("Arial", 12, "bold"),
                command=lambda f_index=i, b_index=j: clicked(f_index, b_index)
            )
            f_sb.place(x=d, y=0)
            d += 60
            btn_list.append(f_sb)
        elif j in [4, 5, 6]:
            f_sb = tk.Button(
                f_s, width=5, height=2, font=("Arial", 12, "bold"),
                command=lambda f_index=i, b_index=j: clicked(f_index, b_index)
            )
            f_sb.place(x=f, y=52)
            f += 60
            btn_list.append(f_sb)
        elif j in [7, 8, 9]:
            f_sb = tk.Button(
                f_s, width=5, height=2, font=("Arial", 12, "bold"),
                command=lambda f_index=i, b_index=j: clicked(f_index, b_index)
            )
            f_sb.place(x=g, y=104)
            g += 60
            btn_list.append(f_sb)
    
    buttons.append(btn_list)

# Board separators
tk.Label(w, bg="#4e0707").place(x=420, y=112, width=5, height=482)
tk.Label(w, bg="#4e0707").place(x=603, y=112, width=5, height=482)
tk.Label(w, bg="#4e0707").place(x=238, y=270, width=550, height=5)
tk.Label(w, bg="#4e0707").place(x=238, y=432, width=549, height=5)
tk.Label(w, bg="#4e0707").place(x=238, y=112, width=5, height=482)
tk.Label(w, bg="#4e0707").place(x=787, y=112, width=5, height=486)
tk.Label(w, bg="#4e0707").place(x=238, y=112, width=550, height=5)
tk.Label(w, bg="#4e0707").place(x=238, y=594, width=553, height=5)

tk.Button(
    w, text="RESET", font=("Arial", 14, "bold"), 
    relief="groove", command=reset_game
).place(x=462, y=665)

# Initialize move label
move_label = tk.Label(
    f_bg, text="\tYou start! Make your move anywhere.", 
    font=("Arial", 16, "bold"), bg="#f7e7ce"
)
move_label.place(x=250, y=620)

w.mainloop()

