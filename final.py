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

# Timer globals
TURN_TIME_LIMIT = 21
timer_running = False
time_remaining = TURN_TIME_LIMIT
timer_job = None
current_player_frame = None


def merge_sort_moves(arr):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort_moves(arr[:mid])
    right = merge_sort_moves(arr[mid:])

    return merge(left, right)


def merge(left, right):
    result = []
    i = j = 0

    # Descending order (highest score first)
    while i < len(left) and j < len(right):
        if left[i][0] >= right[j][0]:  
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    # Remaining elements
    result.extend(left[i:])
    result.extend(right[j:])

    return result


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
        return helper(start, mid) and helper(mid + 1, end)
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
        bg="#547792",
        fg="white"
    ).place(x=0, y=0, height=160, width=180)


def show_big_winner(winner):
    stop_timer()
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
            bg="#547792",
            fg="white"
        ).pack(pady=20)
    else:
        tk.Label(
            popup,
            text="It's a Draw!",
            font=("Arial", 14, "bold"),
            bg="#547792",
            fg="white"
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


def set_frame_highlight(board_index, highlighted):
    """Apply or remove highlight colour from a frame, its buttons, and any overlay label."""
    color     = "#FAB95B"        if highlighted else "white"
    btn_color = "#FAB95B"        if highlighted else "SystemButtonFace"
    lbl_bg    = "#FAB95B"        if highlighted else "#547792"
    bd        = 4                if highlighted else 2
    relief    = "solid"          if highlighted else "ridge"

    sf[board_index].config(bg=color, bd=bd, relief=relief)

    for btn in buttons[board_index]:
        btn.config(bg=btn_color)

    for widget in sf[board_index].winfo_children():
        if isinstance(widget, tk.Label):
            widget.config(bg=lbl_bg)


def reset_frame_colors():
    for i in range(9):
        set_frame_highlight(i, False)


def highlight_frame(board_index):
    reset_frame_colors()
    set_frame_highlight(board_index, True)


def enable_all_valid_boards():
    reset_frame_colors()
    for i in range(9):
        if big_boardgraph.vertices[i].val == "":
            set_frame_highlight(i, True)
            enable_button(i)


def display_values():
    for bi in range(9):
        for ci in range(BOARD_SIZE * BOARD_SIZE):
            buttons[bi][ci].config(text=graph_list[bi].vertices[ci].val)


def displaymove(a, v, f):
    if v == "notallowed":
        move_label.config(
            text=f"CPU played F{f+1} C{a+1}. Make a move in any unoccupied frame."
        )
    else:
        move_label.config(
            text=f"CPU played F{f+1} C{a+1}. Your next move should be in F{a+1}."
        )


# ══════════════════════════════════════════════════════════════════════════════
# TIMER FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════════

def update_timer():
    """Update the timer display every second."""
    global time_remaining, timer_running, timer_job
    
    if not timer_running:
        return
    
    if time_remaining > 0:
        time_remaining -= 1
        
        # Update timer display with color coding
        if time_remaining <= 5:
            timer_label.config(text=f"Time: {time_remaining}s", fg="#FF4C4C")  # Red
        elif time_remaining <= 10:
            timer_label.config(text=f"Time: {time_remaining}s", fg="#FFA500")  # Orange
        else:
            timer_label.config(text=f"Time: {time_remaining}s", fg="#E1EBEE")  # Normal
        
        # Schedule next update
        timer_job = w.after(1000, update_timer)
    else:
        # Time's up! CPU wins the turn
        timer_label.config(text="Time's up!", fg="#FF4C4C")
        stop_timer()
        time_up_forfeit()


def start_timer():
    """Start the turn timer for player."""
    global time_remaining, timer_running, timer_job
    
    stop_timer()  # Stop any existing timer
    time_remaining = TURN_TIME_LIMIT
    timer_running = True
    timer_label.config(text=f"Time: {time_remaining}s", fg="#E1EBEE")
    update_timer()


def stop_timer():
    """Stop the timer."""
    global timer_running, timer_job
    
    timer_running = False
    if timer_job:
        w.after_cancel(timer_job)
        timer_job = None


def time_up_forfeit():
    """Handle what happens when player runs out of time."""
    global current_player_frame
    
    disable_button()
    move_label.config(text="Time's up! CPU gets a free move in your frame.")
    
    # CPU plays in the frame where the player should have played
    if current_player_frame is not None:
        # Player had a specific frame to play in
        target_frame = current_player_frame
    else:
        # Player could play anywhere, pick a random valid board
        valid_boards = [i for i in range(9) 
                        if big_boardgraph.vertices[i].val == "" 
                        and any(v.val == "" for v in graph_list[i].vertices)]
        if valid_boards:
            target_frame = random.choice(valid_boards) + 1
        else:
            return
    
    # CPU makes its move in the target frame
    w.after(1500, lambda: cpu_turn(target_frame))


# ══════════════════════════════════════════════════════════════════════════════


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


def cpu_move_dc(b_index):

    best = -999
    mv = None

    frames = []

    if big_boardgraph.vertices[b_index - 1].val == "":
        frames.append(b_index - 1)
    else:
        for i in range(9):
            if big_boardgraph.vertices[i].val == "":
                frames.append(i)

    for f in frames:
        for c in range(9):

            if graph_list[f].vertices[c].val == "":

                won_small = sim_move(f, c, "O")

                next_board = c

                if won_small:
                    s = rec(next_board, 2, True)
                else:
                    s = rec(next_board, 2, False)

                undo_move(f, c)

                if s > best:
                    best = s
                    mv = (c, f)

    return mv


def cpu_turn(b_index):
    stop_timer()
    global current_player_frame

    move = cpu_move(b_index)
    if not move:
        big_board_check_winner()
        return

    cell, frame = move
    display_values()

    won = sb_checkwinner(frame + 1)

    if big_board_check_winner():
        return

    if won:
        w.after(800, lambda: cpu_turn(cell + 1))
        return

    if big_boardgraph.vertices[cell].val in ["X", "O", "-"]:
        enable_all_valid_boards()
        displaymove(cell, "notallowed", frame)
        current_player_frame = None  # Player can play anywhere
    else:
        highlight_frame(cell)
        enable_button(cell)
        displaymove(cell, "allowed", frame)
        current_player_frame = cell + 1  # Player must play in this specific frame
    
    start_timer()


def clicked(f_index, b_index):
    if graph_list[f_index - 1].vertices[b_index - 1].val != "":
        return

    if big_boardgraph.vertices[f_index - 1].val in ["X", "O", "-"]:
        return

    stop_timer()
    disable_button()
    graph_list[f_index - 1].updatevalue(b_index - 1, "X")
    display_values()

    won = sb_checkwinner(f_index)

    if big_board_check_winner():
        return

    # Momentum Rule
    if won:
        enable_all_valid_boards()
        start_timer()
        return

    w.after(1000, lambda: cpu_turn(b_index))


def reset_game():
    global graph_list, big_boardgraph

    stop_timer()

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
    start_timer()


# ── UI setup ──────────────────────────────────────────────────────────────────

w = tk.Tk()
w.geometry("1024x720")
w.title("X-O Nexus")
w.resizable(False, False)

f_bg = tk.Frame(w, bd=2, relief="ridge", bg="#547792")
f_bg.place(x=0, y=0, height=720, width=1024)

tk.Label(w, text="X-O Nexus", font=("Arial", 24, "bold"),
         bg="#547792", fg="#E1EBEE").place(x=437, y=40)

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

# Big-board grid lines
tk.Label(w, bg="#003153").place(x=420, y=112, width=5, height=482)
tk.Label(w, bg="#003153").place(x=603, y=112, width=5, height=482)
tk.Label(w, bg="#003153").place(x=238, y=270, width=550, height=5)
tk.Label(w, bg="#003153").place(x=238, y=432, width=549, height=5)
tk.Label(w, bg="#003153").place(x=238, y=112, width=5,   height=482)
tk.Label(w, bg="#003153").place(x=787, y=112, width=5,   height=486)
tk.Label(w, bg="#003153").place(x=238, y=112, width=550, height=5)
tk.Label(w, bg="#003153").place(x=238, y=594, width=553, height=5)

tk.Button(
    w, text="RESET", font=("Arial", 14, "bold"),
    relief="groove", command=reset_game
).place(x=462, y=665)

# Timer display
timer_label = tk.Label(
    f_bg, text=f"Time: {TURN_TIME_LIMIT}s",
    font=("Arial", 18, "bold"), bg="#547792", fg="#E1EBEE"
)
timer_label.place(x=50, y=80)

move_label = tk.Label(
    f_bg, text="You start! Make your move anywhere.",
    font=("Arial", 16, "bold"), bg="#547792", fg="#E1EBEE"
)
move_label.place(x=180, y=620)

enable_all_valid_boards()
start_timer()

w.mainloop()
