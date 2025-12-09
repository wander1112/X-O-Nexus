import tkinter as tk
from tkinter import messagebox

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

#    def display(self):
#        for e in self.edgeList:
#            print(f"{e.origin} --{e.val}--> {e.dest}")


def createList():
    g = Graph()
    for i in range(1, 10):
        g.addVertex(i)
    e = [(1,2,1),(2,3,1),(3,6,2),(6,9,2),(7,8,3),(8,9,3),(1,4,4),(4,7,4),(1,5,8),(5,9,8),(2,5,7),(5,8,7),(3,5,6),(5,7,6),(4,5,5),(5,6,5)]
    for u,v,w in e:
        g.addEdge(u,v,w)
    return g

graph_list = []
for i in range(1,10):
    graph_list.append(createList())

def clicked(f_index, b_index):
    return


# UI

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

    # === FIX: Use a different variable name (not b) ===
    btn_list = []

    d = 0
    f = 0
    g = 0

    for j in range(1, 10):
        if j in [1, 2, 3]:
            f_sb = tk.Button(f_s, width=5, height=2, font=("Arial", 12, "bold"),  command=lambda f_index=i, b_index=j:clicked(f_index,b_index))
            f_sb.place(x=d, y=0)
            d += 60
            btn_list.append(f_sb)

        elif j in [4, 5, 6]:
            f_sb = tk.Button(f_s, width=5, height=2, font=("Arial", 12, "bold"),  command=lambda f_index=i, b_index=j:clicked(f_index,b_index))
            f_sb.place(x=f, y=52)
            f += 60
            btn_list.append(f_sb)

        elif j in [7, 8, 9]:
            f_sb = tk.Button(f_s, width=5, height=2, font=("Arial", 12, "bold"),  command=lambda f_index=i, b_index=j:clicked(f_index,b_index))
            f_sb.place(x=g, y=104)
            g += 60
            btn_list.append(f_sb)

    buttons.append(btn_list)

l1 = tk.Label(w, bg="#4e0707")
l1.place(x=382, y=132, width=5, height=482)
l2 = tk.Label(w, bg="#4e0707")
l2.place(x=565, y=132, width=5, height=482)
l3 = tk.Label(w, bg="#4e0707")
l3.place(x=200, y=290, width=550, height=5)
l4 = tk.Label(w, bg="#4e0707")
l4.place(x=200, y=452, width=549, height=5)


l1 = tk.Label(w, bg="#4e0707")
l1.place(x=200, y=132, width=5, height=482)
l2 = tk.Label(w, bg="#4e0707")
l2.place(x=749, y=132, width=5, height=486)
l3 = tk.Label(w, bg="#4e0707")
l3.place(x=200, y=132, width=550, height=5)
l4 = tk.Label(w, bg="#4e0707")
l4.place(x=200, y=614, width=553, height=5)

w.resizable(False, False)
w.mainloop()

