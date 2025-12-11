import tkinter as tk
from tkinter import messagebox

import random
# Classes

class Vertex:
    def _init_(self, val):
        self.val = val


class Edge:
    def _init_(self, origin, dest, val):
        self.val = val
        self.origin = origin
        self.dest = dest


class Graph:
    def _init_(self):
        global edgelist,vertices
        self.vertices = []
        self.edgeList = []

    def addVertex(self, val):
        v = Vertex(val)
        self.vertices.append(v)

    def addEdge(self, origin, dest, val):
        e = Edge(origin, dest, val)
        self.edgeList.append(e)

    def updatevalue(self,vet,value):
        self.vertices[vet].val=value
        

def createList():
    g = Graph()
    

    for i in range(1, 10):
        g.addVertex("")  

    e = [(1,2,1),(2,3,1),(3,6,2),(6,9,2),(7,8,3),(8,9,3),
         (1,4,4),(4,7,4),(1,5,8),(5,9,8),(2,5,7),(5,8,7),
         (3,5,6),(5,7,6),(4,5,5),(5,6,5)]
    for u,v,w in e:
        g.addEdge(u,v,w)

    return g


graph_list = []
for i in range(1,10):
    graph_list.append(createList())

big_boardgraph=createList()
def add_label(val,f_index):
      
    l = tk.Label(sf[f_index-1], text=f"{val}", font=("Arial", 38, "bold"), bg="#f7e7ce")
    l.place(x=0, y=0,height=160,width=180)

def sb_checkwinner(f_index):
    boardgraph = graph_list[f_index-1]
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
                print("winner")
                big_boardgraph.updatevalue(f_index,v_val)
                add_label(v_val,f_index)
                return True            
    return False


def add_value(f_index, b_index,value):  
    boardgraph=graph_list[f_index-1]
    boardgraph.updatevalue(b_index-1,value)


def display_values():
    for board_index in range(9):
        for cell_index in range(9):
            buttons[board_index][cell_index].config(
                text=graph_list[board_index].vertices[cell_index].val
            )



def enable_button_all(f_index):
        for i in buttons:
         for j in i:
            j.config(state="normal")
        for i in  buttons[f_index]:
            i.config(state="disabled")



def disable_button():
    global buttons
    for i in buttons:
        for j in i:
            j.config(state="disabled")

#def greedy():
    #if there is a win condition, play the winning move
        #win condition  there is an edge in the graph with a value and a vertex is free
    #else, random
        #if valid move, then proceed
        #else, call random again
    #return the move


def cpu_move(b_index):
    playframe = graph_list[b_index-1]
    if big_boardgraph.vertices[b_index-1] in ["X","O"]:
        pass
    # Try to win or block
    for e1 in playframe.edgeList:
        for e2 in playframe.edgeList:
            if e1.val != e2.val:
                continue
            if e1.dest != e2.origin:
                continue
            u = e1.origin
            v = e1.dest
            w = e2.dest

            u_val = playframe.vertices[u-1].val
            v_val = playframe.vertices[v-1].val
            w_val = playframe.vertices[w-1].val

            # Case 1: u == v -> play w
            if u_val == v_val and u_val in ["X","O"]:
                if w_val not in ["X","O"]:
                    playframe.updatevalue(w-1, "O")
                    return w-1

            # Case 2: v == w -> play u
            if v_val == w_val and v_val in ["X","O"]:
                if u_val not in ["X","O"]:
                    playframe.updatevalue(u-1, "O")
                    return u-1

            # Case 3: u == w -> play v
            if u_val == w_val and u_val in ["X","O"]:
                if v_val not in ["X","O"]:
                    playframe.updatevalue(v-1, "O")
                    return v-1

    # Random move
    empty_positions = [
        i for i, v in enumerate(playframe.vertices)
        if v.val not in ("X", "O")
    ]

    if empty_positions:
        choice = random.choice(empty_positions)
        playframe.updatevalue(choice, "O")
        return choice

    return None


def enable_button(f_index):
       
        for i in  buttons[f_index]:
            i.config(state="normal")
       





def clicked(f_index, b_index):
    #funtions that should be implemented
    #disable the button once the user clicked 
    #check for the winner (calling the function)
    #cpus move
    #update the enable buttons 
    
    disable_button()
    
    add_value(f_index,b_index,"X")
    display_values()
    sb_checkwinner(f_index)
    global cpu_index
    a=cpu_move(b_index)
    sb_checkwinner(b_index)
    enable_button(a)
    display_values()
    

    




        

# UI -------------------------------------------------------------

w = tk.Tk()
w.geometry("1024x720")
w.title("X-O Nexus")

f_bg = tk.Frame(w, bd=2, relief="ridge", bg="#f7e7ce")
f_bg.place(x=0, y=0, height=720, width=1024)

l1 = tk.Label(w, text="X-O Nexus", font=("Arial", 24, "bold"), bg="#f7e7ce")
l1.place(x=425, y=50)

sf = []
buttons = []

a = 200
bpos = 200
c = 200

for i in range(1, 10):
    if i in [1, 2, 3]:
        f_s = tk.Frame(f_bg, bd=2, relief="ridge", bg="white")
        f_s.place(x=a, y=130, height=160, width=180)
        a += 183
        sf.append(f_s)

    elif i in [4, 5, 6]:
        f_s = tk.Frame(f_bg, bd=2, relief="ridge", bg="white")
        f_s.place(x=bpos, y=292, height=160, width=180)
        bpos += 183
        sf.append(f_s)

    elif i in [7, 8, 9]:
        f_s = tk.Frame(f_bg, bd=2, relief="ridge", bg="white")
        f_s.place(x=c, y=454, height=160, width=180)
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
tk.Label(w, bg="#4e0707").place(x=382, y=132, width=5, height=482)
tk.Label(w, bg="#4e0707").place(x=565, y=132, width=5, height=482)
tk.Label(w, bg="#4e0707").place(x=200, y=290, width=550, height=5)
tk.Label(w, bg="#4e0707").place(x=200, y=452, width=549, height=5)

tk.Label(w, bg="#4e0707").place(x=200, y=132, width=5, height=482)
tk.Label(w, bg="#4e0707").place(x=749, y=132, width=5, height=486)
tk.Label(w, bg="#4e0707").place(x=200, y=132, width=550, height=5)
tk.Label(w, bg="#4e0707").place(x=200, y=614, width=553, height=5)

w.resizable(False, False)
w.mainloop()
