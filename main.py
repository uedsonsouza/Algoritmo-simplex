from pickle import OBJ
from flask import Flask
from matplotlib.layout_engine import ConstrainedLayoutEngine

from backend import gen_matrix, minz, plot_solution
app = Flask(__name__)

@app.route("/")

def main():
    # Solicitar ao usuário os valores para a criação da matriz e as restrições
    rows = int(input("Informe o número de variaveis: "))
    cols = int(input("Informe o número de restrições: "))
    
    m = gen_matrix(rows, cols)
    
    num_constraints = cols
    for i in range(num_constraints):
        constraint_str = input(f"Informe a restrição {i+1} (na forma 'a,b,op,c'): ")
        ConstrainedLayoutEngine(m, constraint_str)
    
    objective_str = input("Informe a função objetivo (na forma 'a,b,c'): ")
    OBJ(m, objective_str)
    print(minz(m))
    plot_solution(m)
    
'''
   m = gen_matrix(2,3)
    constrain(m,'1,0,L,4')
    constrain(m,'0,2,L,12')
    constrain(m,'3,2,L,18')
    obj(m,'3,5,0')
    print(maxz(m))
    plot_func()

''' 