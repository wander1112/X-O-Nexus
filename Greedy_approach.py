import tkinter as tk

import random



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

        self.vertices.append(Vertex(val))



    def addEdge(self, origin, dest, val):

        self.edgeList.append(Edge(origin, dest, val))



    def updatevalue(self, idx, value):

        self.vertices[idx].val = value



def createList():

    g = Graph()

    for _ in range(9):

        g.addVertex("")

    edges = [

        (1,2,1),(2,3,1),(3,6,2),(6,9,2),

        (7,8,3),(8,9,3),(1,4,4),(4,7,4),

        (1,5,8),(5,9,8),(2,5,7),(5,8,7),

        (3,5,6),(5,7,6),(4,5,5),(5,6,5)
    ]

    for u, v, w in edges:

        g.addEdge(u, v, w)

    return g



graph_list = [createList() for _ in range(9)]

big_boardgraph = createList()



def add_label(val, f_index):

    for widget in sf[f_index-1].winfo_children():

        if isinstance(widget, tk.Label):

            widget.destroy()

    tk.Label(sf[f_index-1], text=val, font=("Arial",38,"bold"), bg="#f7e7ce").place(x=0,y=0,height=160,width=180)



def show_big_winner(winner):

    disable_button()

    popup = tk.Toplevel(w)

    popup.title("Game Over")

    popup.geometry("300x160")

    popup.resizable(False, False)

    popup.config(bg="#f7e7ce")

    msg = f"Player {winner} won the big board!" if winner in ["X","O"] else "It's a Draw!"

    tk.Label(popup, text=msg, font=("Arial",14,"bold"), bg="#f7e7ce").pack(pady=20)

    tk.Button(popup, text="Play Again", font=("Arial",12,"bold"), bg="#0078FF", fg="white", relief="flat", command=lambda:(popup.destroy(),reset_game())).pack(pady=5)

    tk.Button(popup, text="Exit", font=("Arial",12,"bold"), bg="#FF4C4C", fg="white", relief="flat", command=w.destroy).pack(pady=5)





WINNING_LINES = [

    [1,2,3],[4,5,6],[7,8,9],

    [1,4,7],[2,5,8],[3,6,9],

    [1,5,9],[3,5,7]

]



def dfs_check_line(boardgraph, line, index, symbol):

    if index == 3:

        return True

    if boardgraph.vertices[line[index]-1].val != symbol:

        return False

    return dfs_check_line(boardgraph, line, index+1, symbol)



def big_board_check_winner():

    for symbol in ["X","O"]:

        for line in WINNING_LINES:

            if dfs_check_line(big_boardgraph, line, 0, symbol):

                show_big_winner(symbol)

                return True

    if all(v.val in ["X","O","-"] for v in big_boardgraph.vertices):

        show_big_winner("-")

        return True

    return False



def sb_checkwinner(f_index):

    boardgraph = graph_list[f_index-1]

    if big_boardgraph.vertices[f_index-1].val in ["X","O","-"]:

        return True

    for symbol in ["X","O"]:

        for line in WINNING_LINES:

            if dfs_check_line(boardgraph, line, 0, symbol):

                big_boardgraph.updatevalue(f_index-1, symbol)

                add_label(symbol, f_index)

                return True

    if all(v.val in ["X","O"] for v in boardgraph.vertices):

        big_boardgraph.updatevalue(f_index-1, "-")

        add_label("-", f_index)

        return True

    return False



def add_value(f_index, b_index, value):

    graph_list[f_index-1].updatevalue(b_index-1, value)



def display_values():

    for i in range(9):

        for j in range(9):

            buttons[i][j].config(text=graph_list[i].vertices[j].val)



def disable_button():

    for row in buttons:

        for btn in row:

            btn.config(state="disabled")



def enable_button(f_index):

    for i in range(9):

        buttons[f_index][i].config(state="normal" if graph_list[f_index].vertices[i].val=="" else "disabled")



def enable_all_valid_boards():

    for i in range(9):

        if big_boardgraph.vertices[i].val=="":

            enable_button(i)



def displaymove(a, v, f):

    if v == "notallowed":

        move_label.config(text=f"CPU played F{f+1} C{a+1}. Make a move in any unoccupied frame.")

    else: 

        move_label.config(text=f"CPU played F{f+1} C{a+1}. Your next move should be in F{a+1}.")



def cpu_move(b_index):

    playframe = graph_list[b_index-1]

    f = b_index - 1



    # if target board already won or draw

    if big_boardgraph.vertices[f].val == "X" or big_boardgraph.vertices[f].val == "O" or big_boardgraph.vertices[f].val == "-":



        valid = []

        for i in range(9):

            if big_boardgraph.vertices[i].val == "":

                for v in graph_list[i].vertices:

                    if v.val == "":

                        valid.append(i)

                        break



        if len(valid) == 0:

            return None



        f = random.choice(valid)

        playframe = graph_list[f]



    # First pass: block player X

    for e1 in playframe.edgeList:

        for e2 in playframe.edgeList:

            if e1.val == e2.val and e1.dest == e2.origin:

                u = e1.origin - 1

                v = e1.dest - 1

                w = e2.dest - 1



                x_count = 0

                empty_index = -1



                if playframe.vertices[u].val == "X":

                    x_count += 1

                if playframe.vertices[v].val == "X":

                    x_count += 1

                if playframe.vertices[w].val == "X":

                    x_count += 1



                if playframe.vertices[u].val == "":

                    empty_index = u

                if playframe.vertices[v].val == "":

                    empty_index = v

                if playframe.vertices[w].val == "":

                    empty_index = w



                if x_count == 2 and empty_index != -1:

                    playframe.updatevalue(empty_index, "O")

                    return empty_index, f



    # Second pass: try to win with O

    for e1 in playframe.edgeList:

        for e2 in playframe.edgeList:

            if e1.val == e2.val and e1.dest == e2.origin:

                u = e1.origin - 1

                v = e1.dest - 1

                w = e2.dest - 1



                o_count = 0

                empty_index = -1



                if playframe.vertices[u].val == "O":

                    o_count += 1

                if playframe.vertices[v].val == "O":

                    o_count += 1

                if playframe.vertices[w].val == "O":

                    o_count += 1



                if playframe.vertices[u].val == "":

                    empty_index = u

                if playframe.vertices[v].val == "":

                    empty_index = v

                if playframe.vertices[w].val == "":

                    empty_index = w



                if o_count == 2 and empty_index != -1:

                    playframe.updatevalue(empty_index, "O")

                    return empty_index, f



    # take center

    if playframe.vertices[4].val == "":

        playframe.updatevalue(4, "O")

        return 4, f



    corners = []

    for i in [0, 2, 6, 8]:

        if playframe.vertices[i].val == "":

            corners.append(i)



    if len(corners) > 0:

        c = random.choice(corners)

        playframe.updatevalue(c, "O")

        return c, f



    empty = []

    for i in range(9):

        if playframe.vertices[i].val == "":

            empty.append(i)

    

    if len(empty) > 0:

        c = random.choice(empty)

        playframe.updatevalue(c, "O")

        return c, f



    return None





def cpu_turn(b_index):

    result=cpu_move(b_index)

    if not result:

        big_board_check_winner()

        return

    a,f=result

    display_values()

    sb_checkwinner(f+1)

    if big_board_check_winner():

        return

    if big_boardgraph.vertices[a].val in ["X","O","-"]:

        enable_all_valid_boards()

        displaymove(a, "notallowed", f)

    else:

        enable_button(a)

        displaymove(a, "allowed", f)



def clicked(f_index,b_index):

    if graph_list[f_index-1].vertices[b_index-1].val!="":

        return

    if big_boardgraph.vertices[f_index-1].val in ["X","O","-"]:

        return

    disable_button()

    add_value(f_index,b_index,"X")

    display_values()

    sb_checkwinner(f_index)

    if big_board_check_winner():

        return

    w.after(1000,lambda:cpu_turn(b_index))


def reset_game():

    global graph_list,big_boardgraph

    graph_list=[createList() for _ in range(9)]

    big_boardgraph=createList()

    for r in buttons:

        for b in r:

            b.config(text="",state="normal")

    for f in sf:

        for wdg in f.winfo_children():

            if isinstance(wdg,tk.Label):

                wdg.destroy()

    move_label.config(text="You start! Make your move anywhere.")


w=tk.Tk()

w.geometry("1024x720")

w.title("X-O Nexus")

w.resizable(False,False)



f_bg = tk.Frame(w, bd=2, relief="ridge", bg="#f7e7ce")

f_bg.place(x=0, y=0, height=720, width=1024)



l1 = tk.Label(w, text="X-O Nexus", font=("Arial", 24, "bold"), bg="#f7e7ce")

l1.place(x=437, y=40)


sf=[]

buttons=[]

for i in range(9):

    f=tk.Frame(f_bg,bg="white",bd=2,relief="ridge")

    f.place(x=238+(i%3)*183,y=110+(i//3)*162,width=180,height=160)

    sf.append(f)

    row=[]

    for j in range(9):

        btn=tk.Button(f,font=("Arial",12,"bold"),width=5,height=2,command=lambda fi=i+1,bi=j+1:clicked(fi,bi))

        btn.place(x=(j%3)*60,y=(j//3)*52)

        row.append(btn)

    buttons.append(row)

tk.Label(w, bg="#4e0707").place(x=420, y=112, width=5, height=482)

tk.Label(w, bg="#4e0707").place(x=603, y=112, width=5, height=482)

tk.Label(w, bg="#4e0707").place(x=238, y=270, width=550, height=5)

tk.Label(w, bg="#4e0707").place(x=238, y=432, width=549, height=5)

tk.Label(w, bg="#4e0707").place(x=238, y=112, width=5, height=482)

tk.Label(w, bg="#4e0707").place(x=787, y=112, width=5, height=486)

tk.Label(w, bg="#4e0707").place(x=238, y=112, width=550, height=5)

tk.Label(w, bg="#4e0707").place(x=238, y=594, width=553, height=5)



move_label=tk.Label(f_bg, text="You start! Make your move anywhere.", font=("Arial",16,"bold"), bg="#f7e7ce")

move_label.place(x=0,y=620,width=1024)


tk.Button(w, text="RESET", font=("Arial",14,"bold"), relief="groove", command=reset_game).place(x=462,y=665)

w.mainloop()
