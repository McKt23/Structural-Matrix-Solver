import numpy as np
import matplotlib.pyplot as plt

# ======================================
# TRUSS GEOMETRY
# ======================================

def case1_nodes():
    nodes = []
    for i in range(6):
        nodes.append((4*i,0))   # bottom
    for i in range(6):
        nodes.append((4*i,4))   # top
    return np.array(nodes)


def case2_nodes():
    nodes = []
    for i in range(6):
        nodes.append((4*i,0))   # bottom
    for i in range(6):
        nodes.append((4*i,4))   # middle
    for i in range(6):
        nodes.append((4*i,8))   # top
    return np.array(nodes)

# ======================================
# ELEMENT CONNECTIVITY
# ======================================

def case1_elements():

    elems = []

    for i in range(5):
        elems.append((i,i+1))

    for i in range(6,11):
        elems.append((i,i+1))

    for i in range(6):
        elems.append((i,i+6))

    for i in range(5):
        elems.append((i,i+7))
        elems.append((i+1,i+6))

    return elems


def case2_elements():

    elems = []

    for r in [0,6,12]:
        for i in range(5):
            elems.append((r+i,r+i+1))

    for i in range(6):
        elems.append((i,i+6))
        elems.append((i+6,i+12))

    for i in range(5):
        elems.append((i,i+7))
        elems.append((i+1,i+6))
        elems.append((i+6,i+13))
        elems.append((i+7,i+12))

    return elems

# ======================================
# DOF NUMBERING
# ======================================

def assign_dof(order):

    dof_map = {}
    counter = 1

    for n in order:

        dof_map[(n,'x')] = counter
        counter += 1

        dof_map[(n,'y')] = counter
        counter += 1

    return dof_map

# ======================================
# GLOBAL MATRIX PATTERN
# ======================================

def assemble_pattern(num_dof,elements,dof_map):

    K = np.zeros((num_dof,num_dof))

    for (i,j) in elements:

        dofs = [
            dof_map[(i,'x')]-1,
            dof_map[(i,'y')]-1,
            dof_map[(j,'x')]-1,
            dof_map[(j,'y')]-1
        ]

        for a in dofs:
            for b in dofs:
                K[a,b] = 1

    return K

# ======================================
# BANDWIDTH
# ======================================

def bandwidth(K):

    rows,cols = np.nonzero(K)

    bw = np.max(np.abs(rows-cols))

    return bw + 1

# ======================================
# TRUSS DRAWING
# ======================================

def draw_truss(nodes,elements,dof_map,order,title):

    node_number = {node:i+1 for i,node in enumerate(order)}

    plt.figure(figsize=(10,4))

    for (i,j) in elements:

        x = [nodes[i][0],nodes[j][0]]
        y = [nodes[i][1],nodes[j][1]]

        plt.plot(x,y,'k')

    for n,(x,y) in enumerate(nodes):

        dx = dof_map[(n,'x')]
        dy = dof_map[(n,'y')]

        num = node_number[n]

        plt.scatter(x,y)

        plt.text(x,y+0.35,f"Node {num}\nDOF({dx},{dy})",ha='center')

    plt.title(title)

    plt.axis('equal')

    plt.grid(True)

    plt.show()

# ======================================
# MATRIX CONSOLE PRINT
# ======================================

def print_matrix_pattern(K,title):

    n = K.shape[0]

    print("\n" + title)

    header = "     "
    for j in range(n):
        header += f"{j+1:3}"

    print(header)

    for i in range(n):

        row = f"{i+1:3} |"

        for j in range(n):

            if K[i,j] != 0:
                row += "  X"
            else:
                row += "   "

        print(row)

# ======================================
# MATRIX FIGURE
# ======================================

def plot_matrix_pattern(K,title):

    n = K.shape[0]

    fig, ax = plt.subplots(figsize=(8,8))

    for i in range(n):
        for j in range(n):
            if K[i,j] != 0:
                ax.text(j+1,i+1,'X',ha='center',va='center')

    ax.set_xlim(0.5,n+0.5)
    ax.set_ylim(n+0.5,0.5)

    ax.set_xticks(range(1,n+1))
    ax.set_yticks(range(1,n+1))

    ax.set_xlabel("Column")
    ax.set_ylabel("Row")

    ax.set_title(title)

    ax.grid(True)

    plt.show()

# ======================================
# REVERSE CUTHILL MCKEE (MIN BANDWIDTH)
# ======================================

def rcm_order(nodes,elements):

    n = len(nodes)

    adjacency = {i:set() for i in range(n)}

    for i,j in elements:
        adjacency[i].add(j)
        adjacency[j].add(i)

    visited = [False]*n
    order = []

    degrees = {i:len(adjacency[i]) for i in adjacency}

    start = min(degrees,key=degrees.get)

    queue = [start]

    while queue:

        node = queue.pop(0)

        if visited[node]:
            continue

        visited[node] = True

        order.append(node)

        neighbors = list(adjacency[node])
        neighbors.sort(key=lambda x:len(adjacency[x]))

        for nb in neighbors:
            if not visited[nb]:
                queue.append(nb)

    order.reverse()

    return order

# ======================================
# CASE 1
# ======================================

nodes1 = case1_nodes()
elems1 = case1_elements()

# ---------- CASE1-A ----------

order = list(range(len(nodes1)))

dof1 = assign_dof(order)

K1 = assemble_pattern(len(nodes1)*2,elems1,dof1)

print("\nCASE1-A")
print("Total DOF:",len(nodes1)*2)
print("Bandwidth:",bandwidth(K1))

draw_truss(nodes1,elems1,dof1,order,"CASE1-A Truss")

print_matrix_pattern(K1,"CASE1-A MATRIX")

plot_matrix_pattern(K1,"CASE1-A MATRIX FIGURE")

# ---------- CASE1-B (TOP → BOTTOM) ----------

order = []

for i in range(6):
    order.append(i+6)  # top
    order.append(i)    # bottom


dof2 = assign_dof(order)

K2 = assemble_pattern(len(nodes1)*2,elems1,dof2)

print("\nCASE1-B")
print("Total DOF:",len(nodes1)*2)
print("Bandwidth:",bandwidth(K2))

draw_truss(nodes1,elems1,dof2,order,"CASE1-B Truss")

print_matrix_pattern(K2,"CASE1-B MATRIX")

plot_matrix_pattern(K2,"CASE1-B MATRIX FIGURE")

# ---------- CASE1-C (MIN BANDWIDTH) ----------

order = rcm_order(nodes1,elems1)

dofc = assign_dof(order)

Kc = assemble_pattern(len(nodes1)*2,elems1,dofc)

print("\nCASE1-C (MIN BANDWIDTH)")
print("Total DOF:",len(nodes1)*2)
print("Bandwidth:",bandwidth(Kc))

draw_truss(nodes1,elems1,dofc,order,"CASE1-C Truss")

print_matrix_pattern(Kc,"CASE1-C MATRIX")

plot_matrix_pattern(Kc,"CASE1-C MATRIX FIGURE")

# ======================================
# CASE 2
# ======================================

nodes2 = case2_nodes()
elems2 = case2_elements()

# ---------- CASE2-A ----------

order = list(range(len(nodes2)))

dof3 = assign_dof(order)

K3 = assemble_pattern(len(nodes2)*2,elems2,dof3)

print("\nCASE2-A")
print("Total DOF:",len(nodes2)*2)
print("Bandwidth:",bandwidth(K3))

draw_truss(nodes2,elems2,dof3,order,"CASE2-A Truss")

print_matrix_pattern(K3,"CASE2-A MATRIX")

plot_matrix_pattern(K3,"CASE2-A MATRIX FIGURE")

# ---------- CASE2-B (TOP → MIDDLE → BOTTOM) ----------

order = []

for i in range(6):
    order.append(i+12)  # top
    order.append(i+6)   # middle
    order.append(i)     # bottom


dof4 = assign_dof(order)

K4 = assemble_pattern(len(nodes2)*2,elems2,dof4)

print("\nCASE2-B")
print("Total DOF:",len(nodes2)*2)
print("Bandwidth:",bandwidth(K4))

draw_truss(nodes2,elems2,dof4,order,"CASE2-B Truss")

print_matrix_pattern(K4,"CASE2-B MATRIX")

plot_matrix_pattern(K4,"CASE2-B MATRIX FIGURE")

# ---------- CASE2-C (MIN BANDWIDTH) ----------

order = rcm_order(nodes2,elems2)

dofc2 = assign_dof(order)

Kc2 = assemble_pattern(len(nodes2)*2,elems2,dofc2)

print("\nCASE2-C (MIN BANDWIDTH)")
print("Total DOF:",len(nodes2)*2)
print("Bandwidth:",bandwidth(Kc2))

draw_truss(nodes2,elems2,dofc2,order,"CASE2-C Truss")

print_matrix_pattern(Kc2,"CASE2-C MATRIX")

plot_matrix_pattern(Kc2,"CASE2-C MATRIX FIGURE")
