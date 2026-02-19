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
    color     = "#FAB95B"       if highlighted else "white"
    btn_color = "#FAB95B"       if highlighted else "SystemButtonFace"
    lbl_bg    = "#FAB95B"       if highlighted else "#547792"
    bd        = 4               if highlighted else 2
    relief    = "solid"         if highlighted else "ridge"

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


def is_frame_playable(board_index_0based):

    if big_boardgraph.vertices[board_index_0based].val in ["X", "O", "-"]:
        return False
    return any(v.val == "" for v in graph_list[board_index_0based].vertices)


def displaymove(next_frame_0based, free_choice, frame_played_0based):
    cpu_frame_display = frame_played_0based + 1
    cpu_cell_display  = next_frame_0based + 1

    if free_choice:
        move_label.config(
            text=f"CPU played F{cpu_frame_display} C{cpu_cell_display}. "
                 f"Make a move in any unoccupied frame."
        )
    else:
        move_label.config(
            text=f"CPU played F{cpu_frame_display} C{cpu_cell_display}. "
                 f"Your next move should be in F{next_frame_0based + 1}."
        )

# Timer functions

def update_timer():
    global time_remaining, timer_running, timer_job

    if not timer_running:
        return

    if time_remaining > 0:
        time_remaining -= 1

        if time_remaining <= 5:
            timer_label.config(text=f"Time: {time_remaining}s", fg="#FF4C4C")
        elif time_remaining <= 10:
            timer_label.config(text=f"Time: {time_remaining}s", fg="#FFA500")
        else:
            timer_label.config(text=f"Time: {time_remaining}s", fg="#E1EBEE")

        timer_job = w.after(1000, update_timer)
    else:
        timer_label.config(text="Time's up!", fg="#FF4C4C")
        stop_timer()
        time_up_forfeit()


def start_timer():
    global time_remaining, timer_running, timer_job

    stop_timer()
    time_remaining = TURN_TIME_LIMIT
    timer_running = True
    timer_label.config(text=f"Time: {time_remaining}s", fg="#E1EBEE")
    update_timer()


def stop_timer():
    global timer_running, timer_job

    timer_running = False
    if timer_job:
        w.after_cancel(timer_job)
        timer_job = None


def time_up_forfeit():
    global current_player_frame

    disable_button()
    move_label.config(text="Time's up! CPU gets a free move in your frame.")

    if current_player_frame is not None:
        target_frame = current_player_frame
    else:
        valid_boards = [i for i in range(9)
                        if big_boardgraph.vertices[i].val == ""
                        and any(v.val == "" for v in graph_list[i].vertices)]
        if valid_boards:
            target_frame = random.choice(valid_boards) + 1
        else:
            return

    w.after(1500, lambda: cpu_turn(target_frame))


# Divide and Conquer

def dmin(a):
    if len(a) == 1:
        return a[0]
    m = len(a) // 2
    l = dmin(a[:m])
    r = dmin(a[m:])
    return l if l < r else r


def dmax(a):
    if len(a) == 1:
        return a[0]
    m = len(a) // 2
    l = dmax(a[:m])
    r = dmax(a[m:])
    return l if l > r else r


def eval_state():
    score = 0

    for s in ["O", "X"]:
        for line in WINNING_LINES:
            if dac_check_line(big_boardgraph, line, s):
                return 1000 if s == "O" else -1000

    for i in range(9):
        val = big_boardgraph.vertices[i].val
        if val == "O":
            score += 100
        elif val == "X":
            score -= 100

    return score


def sim_move(f, c, sym):
    original_big_board_val = big_boardgraph.vertices[f].val

    graph_list[f].vertices[c].val = sym

    won_small = False

    if original_big_board_val == "":
        for s in ["X", "O"]:
            for line in WINNING_LINES:
                if dac_check_line(graph_list[f], line, s):
                    big_boardgraph.vertices[f].val = s
                    won_small = True
                    break
            if won_small:
                break

        if not won_small:
            if all(v.val in ["X", "O"] for v in graph_list[f].vertices):
                big_boardgraph.vertices[f].val = "-"

    return won_small, original_big_board_val


def undo_move(f, c, original_big_board_val):
    graph_list[f].vertices[c].val = ""
    big_boardgraph.vertices[f].val = original_big_board_val


def rec(b_index, depth, turn):
    if depth == 0:
        return eval_state()

    sc = []
    frames = []

    if big_boardgraph.vertices[b_index].val == "":
        frames.append(b_index)
    else:
        for i in range(9):
            if big_boardgraph.vertices[i].val == "":
                frames.append(i)

    for f in frames:
        for c in range(9):
            if graph_list[f].vertices[c].val == "":
                won_small, orig_val = sim_move(f, c, "O" if turn else "X")
                next_board = c

                if won_small:
                    s = rec(next_board, depth - 1, turn)
                else:
                    s = rec(next_board, depth - 1, not turn)

                sc.append(s)
                undo_move(f, c, orig_val)

    if not sc:
        return eval_state()

    return dmax(sc) if turn else dmin(sc)


def snapshot_state():

    big_snap = [v.val for v in big_boardgraph.vertices]
    small_snap = [[v.val for v in g.vertices] for g in graph_list]
    return big_snap, small_snap


def restore_state(big_snap, small_snap):

    for i, val in enumerate(big_snap):
        big_boardgraph.vertices[i].val = val
    for gi, board_snap in enumerate(small_snap):
        for ci, val in enumerate(board_snap):
            graph_list[gi].vertices[ci].val = val


def cpu_move_dc(b_index):
    best = -999
    mv = None

    big_snap, small_snap = snapshot_state()

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
                won_small, orig_val = sim_move(f, c, "O")
                next_board = c

                if won_small:
                    s = rec(next_board, 2, True)
                else:
                    s = rec(next_board, 2, False)

                undo_move(f, c, orig_val)

                if s > best:
                    best = s
                    mv = (c, f)

    restore_state(big_snap, small_snap)

    return mv


def user_hint(b_index):
    best = 999
    mv = None

    big_snap, small_snap = snapshot_state()

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
                won_small, orig_val = sim_move(f, c, "X")
                next_board = c

                if won_small:
                    s = rec(next_board, 2, False)
                else:
                    s = rec(next_board, 2, True)

                undo_move(f, c, orig_val)

                if s < best:
                    best = s
                    mv = (c, f)

    restore_state(big_snap, small_snap)

    return mv


def show_hint():
    forced_boards = []
    for i in range(9):
        if sf[i].cget("bg") == "#FAB95B":
            forced_boards.append(i + 1)

    if not forced_boards:
        move_label.config(text="No valid hint available.")
        return

    forced_board = forced_boards[0]
    move = user_hint(forced_board)

    if move:
        cell, frame = move
        move_label.config(text=f"Hint: Try Frame {frame+1}, Cell {cell+1}")
    else:
        move_label.config(text="No possible hint.")



def cpu_turn(b_index):

    stop_timer()
    global current_player_frame

    move = cpu_move_dc(b_index)

    if not move:
        big_board_check_winner()
        return

    cell, frame = move      

    frame_was_already_closed = big_boardgraph.vertices[frame].val in ["X", "O", "-"]

    graph_list[frame].updatevalue(cell, "O")
    display_values()

    sb_checkwinner(frame + 1)   # updates big_boardgraph if newly won/tied

    if big_board_check_winner():
        return

    # Momentum rule fires ONLY if this move itself newly closed the small board
    frame_is_now_closed = big_boardgraph.vertices[frame].val in ["X", "O", "-"]
    newly_closed = (not frame_was_already_closed) and frame_is_now_closed

    if newly_closed:
        w.after(800, lambda: cpu_turn(cell + 1))
        return

    next_frame_0 = cell

    if is_frame_playable(next_frame_0):
        highlight_frame(next_frame_0)
        enable_button(next_frame_0)
        current_player_frame = next_frame_0 + 1
        displaymove(next_frame_0, False, frame)
    else:
        enable_all_valid_boards()
        current_player_frame = None
        displaymove(next_frame_0, True, frame)

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


# UI setup 

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
).place(x=412, y=665)

tk.Button(
    w, text="HINT", font=("Arial", 14, "bold"),
    relief="groove", command=show_hint
).place(x=522, y=665)

# Timer display
timer_label = tk.Label(
    f_bg, text=f"Time: {TURN_TIME_LIMIT}s",
    font=("Arial", 18, "bold"), bg="#547792", fg="#E1EBEE"
)
timer_label.place(x=50, y=80)

move_label = tk.Label(
    f_bg, text="You start! Make your move anywhere.",
    font=("Arial", 14, "bold"), bg="#547792", fg="#E1EBEE",
    wraplength=800
)
move_label.place(x=112, y=615, width=800, height=40)

enable_all_valid_boards()
start_timer()

w.mainloop()
