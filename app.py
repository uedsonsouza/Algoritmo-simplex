import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from backend import gen_matrix, minz, minz_f1, maxz, constrain, obj, add_row, convert
from grafico import plotagraf, formatTable

def update_restricoes_entries():
    num_restricoes = int(restricoes_entry.get())

    # Verificar o número de campos existentes
    num_campos_atuais = len(restricoes_entries)

    if num_restricoes > num_campos_atuais:
        # Adicionar campos extras, se necessário
        for _ in range(num_campos_atuais, num_restricoes):
            restricao_label = tk.Label(restricoes_frame, text=f"Restrição {_ + 1}:")
            restricao_label.pack()
            restricao_entry = tk.Entry(restricoes_frame)
            restricao_entry.pack()
            restricoes_entries.append(restricao_entry)
            entry_labels.append(restricao_label)
    elif num_restricoes < num_campos_atuais:
        # Remover campos extras, se necessário
        for _ in range(num_campos_atuais - 1, num_restricoes - 1, -1):
            restricoes_entries[_].destroy()
            restricoes_entries.pop(_)
            entry_labels[_].destroy()
            entry_labels.pop(_)
    
    # Atualizar numeração das labels
    for i, entry in enumerate(restricoes_entries):
        entry_label = entry_labels[i]
        entry_label.config(text=f"Restrição {i+1}:")

def solve_problem():
    rows = int(variaveis_entry.get())
    cols = int(restricoes_entry.get())

    # Verificar se o número de restrições foi inserido corretamente
    if cols <= 0:
        tk.messagebox.showerror("Erro", "Número de restrições inválido")
        return

    m = gen_matrix(rows, cols)
    restr = []
    b = []

    for i in range(cols):
        constraint_str = restricoes_entries[i].get()
        type_const, const, b_temp = constrain(m, constraint_str)
        restr.append(const)
        b.append([b_temp])

    objective_str = objetivo_entry.get()
    z = obj(m, objective_str)
    type_problem = tipo_problema_entry.get()

    if add_W.get():
        tab = add_row(m)
        lc = len(tab[0, :])
        tab1 = minz_f1(tab)
        tab2 = np.delete(tab1, (-1), axis=0)
        j = rows + cols
        i = lc - 2
        while i > j:
            tab2 = np.delete(tab2, j, axis=1)
            i -= 1
        if type_problem == 'min':
            val, table, solution = minz(tab2)
        else:
            val, table, solution = maxz(tab2)
    else:
        if type_problem == 'min':
            val, table, solution = minz(m)
        else:
            val, table, solution = maxz(m)

    pp = [0.5, 0.5]
    xlim = (-1, 10)

    result_label.config(text=f"Resultado: {solution}")
    plotagraf(z, formatTable(restr, b), pp, xlim, xlim, solution)
    plt.show()

def reset_fields():
    variaveis_entry.delete(0, tk.END)
    restricoes_entry.delete(0, tk.END)
    objetivo_entry.delete(0, tk.END)
    tipo_problema_entry.delete(0, tk.END)

    for entry in restricoes_entries:
        entry.delete(0, tk.END)

    result_label.config(text="Resultado:")

# Criação da janela principal
janela = tk.Tk()
janela.title("Problema de Pesquisa Operacional")
janela.geometry("600x650")

# Criação dos elementos da interface
variaveis_label = tk.Label(janela, text="Número de Variáveis:")
variaveis_label.pack()
variaveis_entry = tk.Entry(janela)
variaveis_entry.pack()

restricoes_label = tk.Label(janela, text="Número de Restrições:")
restricoes_label.pack()
restricoes_entry = tk.Entry(janela)
restricoes_entry.pack()

restricoes_frame = tk.Frame(janela)
restricoes_frame.pack()

restricoes_entries = []
entry_labels = []

adicionar_restricoes_button = tk.Button(janela, text="Adicionar Restrições", command=update_restricoes_entries)
adicionar_restricoes_button.pack()

objetivo_label = tk.Label(janela, text="Função Objetivo:")
objetivo_label.pack()
objetivo_entry = tk.Entry(janela)
objetivo_entry.pack()

tipo_problema_label = tk.Label(janela, text="Tipo de Problema:")
tipo_problema_label.pack()
tipo_problema_entry = tk.Entry(janela)
tipo_problema_entry.pack()

add_W = tk.BooleanVar()
add_W_check = tk.Checkbutton(janela, text="Adicionar W", variable=add_W)
add_W_check.pack()

solve_button = tk.Button(janela, text="Resolver", command=solve_problem)
solve_button.pack()

result_label = tk.Label(janela, text="Resultado:")
result_label.pack()

reset_button = tk.Button(janela, text="Resetar Campos", command=reset_fields)
reset_button.pack()

# Executar a janela principal
janela.mainloop()
