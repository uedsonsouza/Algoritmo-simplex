import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox
from backend import gen_matrix, minz, minz_f1, maxz, constrain, obj, add_row, convert
from grafico import plotagraf, formatTable

add_W = False

restricoes_entries = []

def criar_campos_restricoes():
    num_restricoes = int(restricoes_entry.get())
    restricoes_entries.clear()

    for widget in restricoes_frame.winfo_children():
        widget.destroy()

    for i in range(num_restricoes):
        restricao_label = tk.Label(restricoes_frame, text=f"Restrição {i+1} (na forma 'a,b,op,c'):")
        restricao_label.pack()
        restricao_entry = tk.Entry(restricoes_frame)
        restricao_entry.pack()
        restricoes_entries.append(restricao_entry)

def resolver():
    # Verificar se todos os campos foram preenchidos
    if not variaveis_entry.get() or not restricoes_entry.get() or not objetivo_entry.get() or not tipo_problema_entry.get():
        messagebox.showerror("Erro", "Preencha todos os campos antes de resolver o problema.")
        return

    rows = int(variaveis_entry.get())
    cols = int(restricoes_entry.get())
    
    m = gen_matrix(rows, cols)
    restr = []
    b = []
    
    num_constraints = cols
    for i in range(num_constraints):
        constraint_str = restricoes_entries[i].get()
        type_const, const, b_temp = constrain(m, constraint_str)
        restr.append(const)
        b.append([b_temp])

    objective_str = objetivo_entry.get()
    z = obj(m, objective_str)
    type_problem = tipo_problema_entry.get()

    if add_W:
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
            val, table, solution = minz(tab2)
    else:
        if type_problem == 'min':
            val, table, solution = minz(m)
        else:
            val, table, solution = maxz(m)

    # Resultados
    resultado_label.config(text=f"Resultado: {val}")

    table_str = "\n".join(["\t".join(map(str, row)) for row in table])
    table_label.config(text=f"Tabela Final:\n{table_str}")

    solution_label.config(text=f"Solução Ótima: {solution}")

    # Plotagem do gráfico
    pp = [0.5, 0.5]
    xlim = (-1, 10)

    plotagraf(z, formatTable(restr, b), pp, xlim, xlim, solution)
    plt.show()

# Criar a janela principal
janela = tk.Tk()
janela.title("Interface do Algoritmo Simplex")

# Estilos
label_style = {"font": ("Arial", 12)}
entry_style = {"font": ("Arial", 12), "width": 20}
button_style = {"font": ("Arial", 12), "width": 20, "pady": 5}

# Número de Variáveis
variaveis_label = tk.Label(janela, text="Número de Variáveis:", **label_style)
variaveis_label.pack()
variaveis_entry = tk.Entry(janela, **entry_style)
variaveis_entry.pack()

# Número de Restrições
restricoes_label = tk.Label(janela, text="Número de Restrições:", **label_style)
restricoes_label.pack()
restricoes_entry = tk.Entry(janela, **entry_style)
restricoes_entry.pack()

# Botão para criar os campos de restrições
criar_campos_button = tk.Button(janela, text="Criar Campos de Restrições", command=criar_campos_restricoes, **button_style)
criar_campos_button.pack()

# Frame para os campos de restrições
restricoes_frame = tk.Frame(janela)
restricoes_frame.pack()

# Entrada para a função objetivo
objetivo_label = tk.Label(janela, text="Função Objetivo (na forma 'a,b,c'):", **label_style)
objetivo_label.pack()
objetivo_entry = tk.Entry(janela, **entry_style)
objetivo_entry.pack()

# Entrada para o tipo de problema (minimização ou maximização)
tipo_problema_label = tk.Label(janela, text="Tipo de Problema (min ou max):", **label_style)
tipo_problema_label.pack()
tipo_problema_entry = tk.Entry(janela, **entry_style)
tipo_problema_entry.pack()

# Botão para resolver
resolver_button = tk.Button(janela, text="Resolver", command=resolver, **button_style)
resolver_button.pack()

# Resultados
resultado_label = tk.Label(janela, text="Resultado:", **label_style)
resultado_label.pack()
table_label = tk.Label(janela, text="Tabela Final:", **label_style)
table_label.pack()
solution_label = tk.Label(janela, text="Solução Ótima:", **label_style)
solution_label.pack()

# Executar a janela principal
janela.mainloop()
