import numpy as np
import matplotlib.pyplot as plt
from matplotlib.layout_engine import ConstrainedLayoutEngine
from backend import gen_matrix, minz, minz_f1, maxz, constrain, obj, add_row,convert
from grafico import plotagraf, formatTable

def main():
    # Solicitar ao usuário os valores para a criação da matriz e as restrições
    global add_row, add_W
    rows = int(input("Informe o número de variaveis: "))
    cols = int(input("Informe o número de restrições: "))
    
    m = gen_matrix(rows, cols)
    restr=[]
    b=[]
    
    num_constraints = cols
    for i in range(num_constraints):
        constraint_str = input(f"Informe a restrição {i+1} (na forma 'a,b,op,c'): ")
        type_const, const, b_temp=constrain(m, constraint_str)
        print(const)
        restr.append(const)
        print(restr)
        print(b_temp)

        b.append([b_temp])
        print(b)
        add_W=False
        if type_const == 'G' or type_const=='E':
            add_W=True

    objective_str = input("Informe a função objetivo (na forma 'a,b,c'): ")
    z=obj(m, objective_str)
    type_problem = input("Maximização (max) ou Minimizaçao (min): ")

    if add_W:
        tab=add_row(m)
        print(tab)
        lc = len(tab[0,:])
        tab1=minz_f1(tab)
        print(tab1)
        tab2 = np.delete(tab1,(-1), axis = 0)
        j=rows+cols
        i=lc-2
        while i>j:
            tab2 = np.delete(tab2, j, axis=1)
            i-=1
        print(tab2)
        if type_problem=='min':
            val,table,solution=minz(tab2)
            print(val)
            print(table)
            print(solution)
        else:
            val,table,solution=minz(tab2)
    else:
        if type_problem=='min':
            val,table,solution=minz(m)
        else:
            val,table,solution=maxz(m)

    pp = [0.5, 0.5]
    xlim = (-1, 10)
    print(solution)
    plotagraf(z, formatTable(restr, b), pp, xlim, xlim,solution)
    plt.show()

main()