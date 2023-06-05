from pickle import OBJ
from flask import Flask
import numpy as np
#from matplotlib.layout_engine import ConstrainedLayoutEngine

from backend import gen_matrix, minz, minz_f1, maxz, constrain,obj, plot_solution, add_row
app = Flask(__name__)

@app.route("/")

def main():
    # Solicitar ao usuário os valores para a criação da matriz e as restrições
    global add_row, add_W
    rows = int(input("Informe o número de variaveis: "))
    cols = int(input("Informe o número de restrições: "))
    
    m = gen_matrix(rows, cols)
    
    num_constraints = cols
    for i in range(num_constraints):
        constraint_str = input(f"Informe a restrição {i+1} (na forma 'a,b,op,c'): ")
        type_const=constrain(m, constraint_str)
        add_W=False
        if type_const == 'G' or type_const=='E':
            add_W=True

    objective_str = input("Informe a função objetivo (na forma 'a,b,c'): ")
    obj(m, objective_str)
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
            print(minz(tab2))
        else:
            print(maxz(tab2))
    else:
        if type_problem=='min':
            print(minz(m))
        else:
            print(maxz(m))
    #plot_solution(m)

main()
'''
   m = gen_matrix(2,3)
    constrain(m,'1,0,L,4')
    constrain(m,'0,2,L,12')
    constrain(m,'3,2,L,18')
    obj(m,'3,5,0')
    print(maxz(m))
    plot_func()

''' 