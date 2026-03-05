import random
import tkinter as tk

pattern_cache = {}
BOARD_SIZE = 3
WINNING_LINES = []

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

def createList(N):  # O(N^2)
    g = Graph()
    for _ in range(N * N):
        g.addVertex("")
    winning_lines = []
    for r in range(N):
        winning_lines.append([r * N + c + 1 for c in range(N)])
    for c in range(N):
        winning_lines.append([r * N + c + 1 for r in range(N)])
    winning_lines.append([i * N + i + 1 for i in range(N)])
    winning_lines.append([(i + 1) * N - i for i in range(N)])
    for line in winning_lines:
        for i in range(len(line) - 1):
            g.addEdge(line[i], line[i + 1], 1)
    return g, winning_lines

graph_list = []
for i in range(BOARD_SIZE * BOARD_SIZE):
    g, WINNING_LINES = createList(BOARD_SIZE)
    graph_list.append(g)
big_boardgraph, _ = createList(BOARD_SIZE)

TURN_TIME_LIMIT = 16
timer_running = False
time_remaining = TURN_TIME_LIMIT
timer_job = None
current_player_frame = None

# ── Line check (DFS over graph edges) ────────────────────────────────────────
def check_line(boardgraph, line, symbol):
    line_set = set(line)
    visited = set()
    stack = [line[0]]  # start DFS from the first cell in the winning line

    while stack:
        node = stack.pop()
        if node in visited:
            continue
        visited.add(node)

        # If this cell doesn't match the symbol, the line is not a win
        if boardgraph.vertices[node - 1].val != symbol:
            return False

        # Push unvisited neighbours that belong to this winning line
        for edge in boardgraph.edgeList:
            if edge.origin == node and edge.dest in line_set and edge.dest not in visited:
                stack.append(edge.dest)

    # Win only if every cell in the line was reached and matched
    return visited == line_set

# ── Board helpers ─────────────────────────────────────────────────────────────
def sb_checkwinner(f_index):
    boardgraph = graph_list[f_index - 1]
    if big_boardgraph.vertices[f_index - 1].val in ["X", "O", "-"]:
        return True
    for symbol in ["X", "O"]:
        for line in WINNING_LINES:
            if check_line(boardgraph, line, symbol):
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
            if check_line(big_boardgraph, line, symbol):
                show_big_winner(symbol)
                return True
    if all(v.val in ["X", "O", "-"] for v in big_boardgraph.vertices):
        show_big_winner("-")
        return True
    return False

# ── Simulation helpers ────────────────────────────────────────────────────────
def sim_move(f, c, sym):  # O(1)
    original_big_board_val = big_boardgraph.vertices[f].val
    graph_list[f].vertices[c].val = sym
    won_small = False
    if original_big_board_val == "":
        for s in ["X", "O"]:
            for line in WINNING_LINES:
                if check_line(graph_list[f], line, s):
                    big_boardgraph.vertices[f].val = s
                    won_small = True
                    break
            if won_small:
                break
        if not won_small:
            if all(v.val in ["X", "O"] for v in graph_list[f].vertices):
                big_boardgraph.vertices[f].val = "-"
    return won_small, original_big_board_val

def undo_move(f, c, original_big_board_val):  # O(1)
    graph_list[f].vertices[c].val = ""
    big_boardgraph.vertices[f].val = original_big_board_val

def snapshot_state():  # O(81)
    big_snap = [v.val for v in big_boardgraph.vertices]
    small_snap = [[v.val for v in g.vertices] for g in graph_list]
    return big_snap, small_snap

def restore_state(big_snap, small_snap):  # O(81)
    for i, val in enumerate(big_snap):
        big_boardgraph.vertices[i].val = val
    for gi, board_snap in enumerate(small_snap):
        for ci, val in enumerate(board_snap):
            graph_list[gi].vertices[ci].val = val

# ── DP pattern compression ────────────────────────────────────────────────────
def compress_board_pattern(boardgraph):
    patterns = []
    for line in WINNING_LINES:
        x = o = e = 0
        for pos in line:
            val = boardgraph.vertices[pos - 1].val
            if val == "X":      x += 1
            elif val == "O":    o += 1
            else:               e += 1
        patterns.append((x, o, e))
    return patterns

def compress_game_pattern():
    all_patterns = []
    all_patterns.extend(compress_board_pattern(big_boardgraph))
    for g in graph_list:
        all_patterns.extend(compress_board_pattern(g))
    unique_patterns = sorted(set(all_patterns))
    return tuple(unique_patterns)

# ── DP eval & minimax ─────────────────────────────────────────────────────────
def eval_state():
    score = 0
    for s in ["O", "X"]:
        for line in WINNING_LINES:
            if check_line(big_boardgraph, line, s):
                return 1000 if s == "O" else -1000
    for i in range(9):
        val = big_boardgraph.vertices[i].val
        if val == "O":   score += 100
        elif val == "X": score -= 100
    return score

def rec(b_index, depth, turn):
    key = (compress_game_pattern(), b_index, turn, depth)
    if key in pattern_cache:
        return pattern_cache[key]
    if depth == 0:
        val = eval_state()
        pattern_cache[key] = val
        return val
    scores = []
    frames = ([b_index] if big_boardgraph.vertices[b_index].val == ""
              else [i for i in range(9) if big_boardgraph.vertices[i].val == ""])
    for f in frames:
        for c in range(9):
            if graph_list[f].vertices[c].val == "":
                symbol = "O" if turn else "X"
                won_small, orig_val = sim_move(f, c, symbol)
                s = rec(c, depth - 1, turn if won_small else not turn)
                undo_move(f, c, orig_val)
                scores.append(s)
    if not scores:
        val = eval_state()
    else:
        val = max(scores) if turn else min(scores)
    pattern_cache[key] = val
    return val

# ── DP CPU move ───────────────────────────────────────────────────────────────
def cpu_move_dp(b_index):
    best = -9999
    best_move = None
    frames = ([b_index - 1] if big_boardgraph.vertices[b_index - 1].val == ""
              else [i for i in range(9) if big_boardgraph.vertices[i].val == ""])
    for f in frames:
        for c in range(9):
            if graph_list[f].vertices[c].val == "":
                won_small, orig_val = sim_move(f, c, "O")
                s = rec(c, 2, True if won_small else False)
                undo_move(f, c, orig_val)
                if s > best:
                    best = s
                    best_move = (c, f)
    return best_move

# ── Hint (DP version) ─────────────────────────────────────────────────────────
def user_hint(b_index):
    best = 999
    mv = None
    big_snap, small_snap = snapshot_state()
    frames = ([b_index - 1] if big_boardgraph.vertices[b_index - 1].val == ""
              else [i for i in range(BOARD_SIZE * BOARD_SIZE)
                    if big_boardgraph.vertices[i].val == ""])
    for f in frames:
        for c in range(BOARD_SIZE * BOARD_SIZE):
            if graph_list[f].vertices[c].val == "":
                won_small, orig_val = sim_move(f, c, "X")
                s = rec(c, 1, False if won_small else True)
                undo_move(f, c, orig_val)
                if s < best:
                    best = s
                    mv = (c, f)
    restore_state(big_snap, small_snap)
    return mv

def show_hint():
    forced_board = None
    for i in range(BOARD_SIZE * BOARD_SIZE):
        if sf[i].cget("bg") == "#FAB95B":
            forced_board = i + 1
            break
    if forced_board is None:
        move_label.config(text="No valid hint available.")
        return
    move = user_hint(forced_board)
    if move:
        cell, frame = move
        move_label.config(text=f"Hint: Try the highlighted yellow frame, Cell {cell+1}")
    else:
        move_label.config(text="No possible hint.")

# ── UI helpers ────────────────────────────────────────────────────────────────
def add_label(val, f_index):
    for widget in sf[f_index - 1].winfo_children():
        if isinstance(widget, tk.Label):
            widget.destroy()
    tk.Label(sf[f_index - 1], text=val, font=("Arial", 38, "bold"),
             bg="#547792", fg="white").place(x=0, y=0, height=160, width=180)

def show_big_winner(winner):
    stop_timer()
    disable_button()
    popup = tk.Toplevel(w)
    popup.title("Game Over")
    popup.geometry("300x160")
    popup.resizable(False, False)
    popup.config(bg="#547792")
    msg = f"Player {winner} won the big board!" if winner in ["X", "O"] else "It's a Draw!"
    tk.Label(popup, text=msg, font=("Arial", 14, "bold"), bg="#547792", fg="white").pack(pady=20)
    tk.Button(popup, text="Play Again", font=("Arial", 12, "bold"), bg="#0078FF", fg="white",
              relief="flat", command=lambda: (popup.destroy(), reset_game())).pack(pady=5)
    tk.Button(popup, text="Exit", font=("Arial", 12, "bold"), bg="#FF4C4C", fg="white",
              relief="flat", command=w.destroy).pack(pady=5)

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
    color     = "#FAB95B" if highlighted else "white"
    btn_color = "#FAB95B" if highlighted else "SystemButtonFace"
    lbl_bg    = "#FAB95B" if highlighted else "#547792"
    bd        = 4         if highlighted else 2
    relief    = "solid"   if highlighted else "ridge"
    sf[board_index].config(bg=color, bd=bd, relief=relief)
    for btn in buttons[board_index]:
        btn.config(bg=btn_color)
    for widget in sf[board_index].winfo_children():
        if isinstance(widget, tk.Label):
            widget.config(bg=lbl_bg)

def reset_frame_colors():
    for i in range(BOARD_SIZE * BOARD_SIZE):
        set_frame_highlight(i, False)

def highlight_frame(board_index):
    reset_frame_colors()
    set_frame_highlight(board_index, True)

def enable_all_valid_boards():
    reset_frame_colors()
    for i in range(BOARD_SIZE * BOARD_SIZE):
        if big_boardgraph.vertices[i].val == "":
            set_frame_highlight(i, True)
            enable_button(i)

def display_values():
    for bi in range(BOARD_SIZE * BOARD_SIZE):
        for ci in range(BOARD_SIZE * BOARD_SIZE):
            buttons[bi][ci].config(text=graph_list[bi].vertices[ci].val)

def displaymove(a, v, f):
    cpu_frame = f + 1
    cpu_cell  = a + 1
    if v == "notallowed":
        move_label.config(text=f"CPU played F{cpu_frame} C{cpu_cell}. Your next move should be in the highlighted yellow frame(s).")
    else:
        move_label.config(text=f"CPU played F{cpu_frame} C{cpu_cell}. Your next move should be in the highlighted yellow frame.")

# ── Timer ─────────────────────────────────────────────────────────────────────
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

# ── CPU turn ──────────────────────────────────────────────────────────────────
def cpu_turn(b_index):
    stop_timer()
    global current_player_frame
    move = cpu_move_dp(b_index)
    if not move:
        big_board_check_winner()
        return
    cell, frame = move
    frame_was_already_closed = big_boardgraph.vertices[frame].val in ["X", "O", "-"]
    graph_list[frame].updatevalue(cell, "O")
    display_values()
    sb_checkwinner(frame + 1)
    if big_board_check_winner():
        return
    frame_is_now_closed = big_boardgraph.vertices[frame].val in ["X", "O", "-"]
    newly_closed = (not frame_was_already_closed) and frame_is_now_closed
    if newly_closed:
        w.after(800, lambda: cpu_turn(cell + 1))
        return
    target_frame_closed = big_boardgraph.vertices[cell].val in ["X", "O", "-"]
    target_has_no_moves = all(v.val != "" for v in graph_list[cell].vertices)
    if target_frame_closed or target_has_no_moves:
        enable_all_valid_boards()
        displaymove(cell, "notallowed", frame)
        current_player_frame = None
    else:
        highlight_frame(cell)
        enable_button(cell)
        displaymove(cell, "allowed", frame)
        current_player_frame = cell + 1
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
    if won:
        enable_all_valid_boards()
        start_timer()
        return
    w.after(1000, lambda: cpu_turn(b_index))

def reset_game():
    global graph_list, big_boardgraph
    stop_timer()
    pattern_cache.clear()
    graph_list = []
    for _ in range(BOARD_SIZE * BOARD_SIZE):
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

# ── UI build ──────────────────────────────────────────────────────────────────
w = tk.Tk()
w.geometry("1024x720")
w.title("X-O Nexus  [Dynamic Programming Mode]")
w.resizable(False, False)
f_bg = tk.Frame(w, bd=2, relief="ridge", bg="#547792")
f_bg.place(x=0, y=0, height=720, width=1024)
tk.Label(w, text="X-O Nexus  [DP]", font=("Arial", 24, "bold"),
         bg="#547792", fg="#E1EBEE").place(x=415, y=40)
sf = []
buttons = []
base_x, base_y = 238, 110
for i in range(BOARD_SIZE * BOARD_SIZE):
    frame = tk.Frame(f_bg, bd=2, relief="ridge", bg="white")
    frame.place(x=base_x + (i % 3) * 183, y=base_y + (i // 3) * 162, width=180, height=160)
    sf.append(frame)
    btns = []
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            idx = r * BOARD_SIZE + c + 1
            btn = tk.Button(frame, width=5, height=2, font=("Arial", 12, "bold"),
                            command=lambda f=i+1, b=idx: clicked(f, b))
            btn.place(x=c * 60, y=r * 52)
            btns.append(btn)
    buttons.append(btns)
# Grid lines
for cfg in [
    (420,112,5,482),(603,112,5,482),(238,270,550,5),(238,432,549,5),
    (238,112,5,482),(787,112,5,486),(238,112,550,5),(238,594,553,5)]:
    tk.Label(w, bg="#003153").place(x=cfg[0], y=cfg[1], width=cfg[2], height=cfg[3])
tk.Button(w, text="RESET", font=("Arial", 14, "bold"), relief="groove",
          command=reset_game).place(x=462, y=665)
tk.Button(w, text="HINT",  font=("Arial", 14, "bold"), relief="groove",
          command=show_hint).place(x=562, y=665)
timer_label = tk.Label(f_bg, text=f"Time: {TURN_TIME_LIMIT}s",
                       font=("Arial", 18, "bold"), bg="#547792", fg="#E1EBEE")
timer_label.place(x=50, y=80)
move_label = tk.Label(f_bg, text="You start! Make your move anywhere.",
                      font=("Arial", 16, "bold"), bg="#547792", fg="#E1EBEE")
move_label.place(x=512, y=620, anchor="center")
enable_all_valid_boards()
start_timer()
w.mainloop()
