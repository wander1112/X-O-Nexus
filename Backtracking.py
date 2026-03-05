import random
import tkinter as tk


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

def dac_check_line(boardgraph, line, symbol):  # O(N)
    def helper(start, end):
        if start == end:
            return boardgraph.vertices[line[start] - 1].val == symbol
        mid = (start + end) // 2
        return helper(start, mid) and helper(mid + 1, end)
    return helper(0, len(line) - 1)

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



def sb_checkwinner(f_index):  # O(1)
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

def big_board_check_winner():  # O(N)
    for symbol in ["X", "O"]:
        for line in WINNING_LINES:
            if dac_check_line(big_boardgraph, line, symbol):
                show_big_winner(symbol)
                return True
    if all(v.val in ["X", "O", "-"] for v in big_boardgraph.vertices):
        show_big_winner("-")
        return True
    return False

# functions to be added (in progress)

def sim_move(f, c, sym):  # O(1)
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

def undo_move(f, c, original_big_board_val):  # O(1)
    graph_list[f].vertices[c].val = ""
    big_boardgraph.vertices[f].val = original_big_board_val

def snapshot_state():  # O(81)
    big_snap = [v.val for v in big_boardgraph.vertices]
    small_snap = [[v.val for v in g.vertices] for g in graph_list]
    return big_snap, small_snap

# restore state


def score_small_board(boardgraph, cpu="O", user="X"):
    score = 0
    for line in WINNING_LINES:
        cpu_count = user_count = empty_count = 0
        for pos in line:
            val = boardgraph.vertices[pos - 1].val
            if val == cpu:      cpu_count += 1
            elif val == user:   user_count += 1
            else:               empty_count += 1
        if cpu_count == 3:                       score += 100
        elif user_count == 3:                    score -= 100
        elif cpu_count == 2 and empty_count == 1:  score += 10
        elif user_count == 2 and empty_count == 1: score -= 10
        elif cpu_count == 1 and empty_count == 2:  score += 1
        elif user_count == 1 and empty_count == 2: score -= 1
    return score

small_board_scores = [0] * 9

def update_all_small_board_scores():
    for i in range(9):
        if big_boardgraph.vertices[i].val == "":
            small_board_scores[i] = score_small_board(graph_list[i])
        else:
            small_board_scores[i] = -9999


# eval state dc


# branch and bound 

# cpu move bb

# rec_dc

# user_hint

#show hint

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

# cpu turn 

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
    update_all_small_board_scores()
    if big_board_check_winner():
        return
    w.after(1000, lambda: cpu_turn(b_index))

def reset_game():
    global graph_list, big_boardgraph
    stop_timer()
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
w.title("X-O Nexus  [D&C + Branch & Bound]")
w.resizable(False, False)
f_bg = tk.Frame(w, bd=2, relief="ridge", bg="#547792")
f_bg.place(x=0, y=0, height=720, width=1024)
tk.Label(w, text="X-O Nexus  [D&C + B&B]", font=("Arial", 24, "bold"),
         bg="#547792", fg="#E1EBEE").place(x=385, y=40)
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
