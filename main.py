import tkinter as tk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
from backend import *
from grafico import plotagraf, formatTable

input_entries = []
solve_problem = []
reset_fields = []

# Função para criar os campos de entrada para as restrições
def create_input_fields(num_constraints):
    # Limpar campos existentes
    clear_fields()

    # Criar campos de entrada para as restrições
    for i in range(num_constraints):
        entry_label = tk.Label(restricoes_frame, text=f"Restrição {i+1}:(a,b,op,c)")
        entry_label.pack()
        entry = tk.Entry(restricoes_frame)
        entry.pack()
        entry_labels.append(entry_label)
        input_entries.append(entry)

# Função para atualizar os campos de entrada com base no número de restrições fornecido
def update_restricoes_entries():
    num_constraints = int(restricoes_entry.get())
    create_input_fields(num_constraints)

# Função para limpar os campos de entrada
def clear_fields():
    for entry_label in entry_labels:
        entry_label.destroy()
    for entry in input_entries:
        entry.destroy()
    entry_labels.clear()
    input_entries.clear()

# Função para executar a otimização
def run_optimization():
    rows = int(variaveis_entry.get())
    cols = int(restricoes_entry.get())

    m = gen_matrix(rows, cols)
    restr = []
    b = []

    num_constraints = cols
    add_W = 0
    restricoes = []
    for i in range(num_constraints):
        constraint_str = input_entries[i].get()
        restricoes.append(constraint_str)
        type_const, const, b_temp = constrain(m, constraint_str)

        restr.append(const)
        b.append([b_temp])

        if type_const == 'G' or type_const == 'E':
            add_W = 1

    objective_str = objetivo_entry.get()
    funcao = (objective_str)
    z = obj(m, objective_str)
    type_problem = var_problem.get()

    val, table, solution, zotimo = otimizar(m, type_problem, add_W, rows, cols)
    solution_str = f"Solution: {solution}"
    zotimo_str = f"Optimal value: {zotimo}"

    tk.messagebox.showinfo("Optimization Result", f"{solution_str}\n{zotimo_str}")

    pp = [0.5, 0.5]
    xlim = (-1, 10)
    ylim = (-1, 10)

    solinteira, zinteira = branch_and_bound(solution, zotimo, rows, cols, type_problem, add_W, restricoes, funcao, 0)
    solinteira_str = f"Integer Solution: {solinteira}"
    zinteira_str = f"Integer Optimal value: {zinteira}"

    tk.messagebox.showinfo("Integer Optimization Result", f"{solinteira_str}\n{zinteira_str}")

    # Gerar e exibir o gráfico
    table = formatTable(restr, b)

    #magnus mexeu aqui, se der merda, excluir o ', solinteira'
    plotagraf(z, table, pp, xlim, ylim, solution, solinteira)

def show_plot():
    rows = int(variaveis_entry.get())
    cols = int(restricoes_entry.get())

    m = gen_matrix(rows, cols)
    restr = []
    b = []

    num_constraints = cols
    add_W= 0
    restricoes = []
    for i in range(num_constraints):
        constraint_str = input_entries[i].get()
        restricoes.append(constraint_str)
        type_const, const, b_temp = constrain(m, constraint_str)

        restr.append(const)
        b.append([b_temp])

        if type_const == 'G' or type_const == 'E':
            add_W = 1

    objective_str = objetivo_entry.get()
    funcao = (objective_str)
    z = obj(m, objective_str)
    type_problem = var_problem.get()

    pp = [0.5, 0.5]
    xlim = (-1, 10)
    ylim = (-1, 10)

    # Gerar e exibir o gráfico
    table = formatTable(restr, b)
    plotagraf(z, table, pp, xlim, ylim, [])

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

entry_labels = []

adicionar_restricoes_button = tk.Button(janela, text="Adicionar Restrições", command=update_restricoes_entries)
adicionar_restricoes_button.pack()

objetivo_label = tk.Label(janela, text="Função Objetivo (a,b,c):")
objetivo_label.pack()
objetivo_entry = tk.Entry(janela)
objetivo_entry.pack()

lbl_problem = tk.Label(janela, text="Tipo de problema:")
lbl_problem.pack()
var_problem = tk.StringVar()
option_menu = tk.OptionMenu(janela, var_problem, "max", "min")
option_menu.pack()

# Botão para executar a otimização
btn_optimize = tk.Button(janela, text="Executar Otimização", command=run_optimization)
btn_optimize.pack()

# Executar a janela principal
janela.mainloop()