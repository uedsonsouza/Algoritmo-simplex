import numpy as np

# gera uma matriz vazia com tamanho adequado para variáveis e restrições.
def gen_matrix(var, cons):
    tab = np.zeros((cons + 1, var + 2 * cons + 2))
    return tab


# verifica a coluna mais à direita para valores negativos ACIMA da última linha. Se existirem valores negativos, é necessário outro pivo.
def next_round_r(table):
    m = min(table[:-1, -1])
    if m >= 0:
        return False
    else:
        return True


# verifica se a linha inferior, excluindo a coluna final, tem valores negativos. Se existirem valores negativos, é necessário outro pivo.
def next_round(table):
    lr = len(table[:, 0])
    m = min(table[lr - 1, :-1])
    if m >= 0:
        return False
    else:
        return True


# Semelhante à função next_round_r, mas devolve o índice da linha do elemento negativo na coluna mais à direita.
def find_neg_r(table):
    # lc = number of columns, lr = number of rows
    lc = len(table[0, :])
    # Procurar em todas as linhas (excepto na última linha) da coluna final pelo valor mínimo
    m = min(table[:-1, lc - 1])
    if m <= 0:
        # n = índice de linha da localização m
        n = np.where(table[:-1, lc - 1] == m)[0][0]
    else:
        n = None
    return n


# Devolve o índice de coluna do elemento negativo na linha inferior
def find_neg(table):
    lr = len(table[:, 0])
    m = min(table[lr - 1, :-1])
    if m <= 0:
        # n = índice de linha para m
        n = np.where(table[lr - 1, :-1] == m)[0][0]
    else:
        n = None
    return n


# localiza o elemento pivot na tabelau para remover o elemento negativo da coluna mais à direita.
def loc_piv_r(table):
    total = []
    # r = índice de linha da entrada negativa
    r = find_neg_r(table)
    # encontra todos os elementos na linha, r, excluindo a coluna final
    row = table[r, :-1]
    # encontra o valor mínimo na linha (excluindo a última coluna)
    m = min(row)
    # c = índice de coluna para a entrada mínima na linha
    c = np.where(row == m)[0][0]
    # todos os elementos da coluna
    col = table[:-1, c]
    # é necessário percorrer esta coluna para encontrar o rácio positivo mais pequeno
    for i, b in zip(col, table[:-1, -1]):
        # i não pode ser igual a 0 e b/i tem de ser positivo.
        if i ** 2 > 0 and b / i > 0:
            total.append(b / i)
        else:
            # espaço reservado para os elementos que não satisfazem os requisitos acima referidos. Caso contrário, o nosso número de índice seria incorrecto.
            total.append(0)
    element = max(total)
    for t in total:
        if t > 0 and t < element:
            element = t
        else:
            continue

    index = total.index(element)
    return [index, c]


# processo semelhante, devolve um elemento específico da matriz para ser articulado.
def loc_piv(table):
    if next_round(table):
        total = []
        n = find_neg(table)
        for i, b in zip(table[:-1, n], table[:-1, -1]):
            if i ** 2 > 0 and b / i >= 0:
                total.append(b / i)
            else:
                # espaço reservado para os elementos que não satisfazem os requisitos acima referidos. Caso contrário, o nosso número de índice seria incorrecto.
                total.append(-1)
        element = max(total)
        for t in total:
            if t >= 0 and t < element:
                element = t
            else:
                continue

        index = total.index(element)
        return [index, n]

# processo semelhante, devolve um elemento específico da matriz para ser articulado.
def loc_pivf1(table):
    if next_round(table):
        total = []
        n = find_neg(table)
        for i, b in zip(table[:-1, n], table[:-1, -1]):
            if i ** 2 > 0 and b / i > 0:
                total.append(b / i)
            else:
                # espaço reservado para os elementos que não satisfazem os requisitos acima referidos. Caso contrário, o nosso número de índice seria incorrecto.
                total.append(0)
        element = max(total)
        for t in total:
            if t > 0 and t < element:
                element = t
            else:
                continue

        index = total.index(element)
        return [index, n]

# Recebe uma string de entrada e devolve uma lista de números a serem organizados numa tabela
def convert(eq):
    eq = eq.split(',')
    if '>=' in eq:
        g = eq.index('>=')
        del eq[g]
        eq = [float(i) for i in eq]
        type_const = "G"
        return eq, type_const
    if '<=' in eq:
        l = eq.index('<=')
        del eq[l]
        eq = [float(i) for i in eq]
        type_const = "L"
        return eq, type_const
    if '=' in eq:
        e = eq.index('=')
        del eq[e]
        eq = [float(i) for i in eq]
        type_const = "E"
        return eq, type_const


# A linha final da tabela num problema de mínimo é o oposto de um problema de maximização, pelo que os elementos são multiplicados por (-1)
def convert_min(table):
    table[-1, :-2] = [-1 * i for i in table[-1, :-2]]
    table[-1, -1] = -1 * table[-1, -1]
    return table


# gera x1,x2,...xn para o número variável de variáveis.
def gen_var(table):
    lc = len(table[0, :])
    lr = len(table[:, 0])
    #var = lc-2*lr+3
    var=lc-lr-1
    print(f'variaveis gen var {var}')
    v = []
    for i in range(var):
        v.append('x' + str(i + 1))
    return v

# dinamiza o quadro de modo a que os elementos negativos sejam eliminados da última linha e da última coluna
def pivot(row, col, table):
    # número de linhas
    lr = len(table[:, 0])
    # número de colunas
    lc = len(table[0, :])
    t = np.zeros((lr, lc))
    pr = table[row, :]
    if table[row, col] ** 2 > 0:  # new
        e = 1 / table[row, col]
        r = pr * e
        for i in range(len(table[:, col])):
            k = table[i, :]
            c = table[i, col]
            if list(k) == list(pr):
                continue
            else:
                t[i, :] = list(k - r * c)
        t[row, :] = list(r)
        return t
    else:
        print('Cannot pivot on this element.')


# Verifica se há espaço na matriz para adicionar outra restrição
def add_cons(table):
    lr = len(table[:, 0])
    # pretende saber SE existem pelo menos 2 linhas com todos os elementos nulos
    empty = []
    # iterar através de cada linha
    for i in range(lr):
        total = 0
        for j in table[i, :]:
            # utilizar o valor quadrático para que (-x) e (+x) não se anulem um ao outro
            total += j ** 2
        if total == 0:
            # acrescentar zero à lista APENAS se todos os elementos de uma linha forem zero
            empty.append(total)
    # Existem pelo menos 2 linhas com todos os elementos nulos se o seguinte for verdadeiro
    if len(empty) > 1:
        return True
    else:
        return False


# adiciona uma restrição à matriz
def constrain(table, eq):
    if add_cons(table) == True:
        lc = len(table[0, :])
        lr = len(table[:, 0])
        var = lc - 2 * lr
        const = lc - lr - var - 1
        # configurar o contador para iterar através do comprimento total das linhas
        j = 0
        while j < lr:
            # Iterar por linha
            row_check = table[j, :]
            # o total será a soma dos registos na linha
            total = 0
            # Encontrar a primeira linha com todas as entradas 0
            for i in row_check:
                total += float(i ** 2)
            if total == 0:
                # Encontrámos a primeira linha com todas as entradas zero
                row = row_check
                break
            j += 1

        eq, type_const = convert(eq)
        i = 0
        # itera através de todos os termos da função de restrição, excluindo o último
        while i < len(eq) - 1:
            # atribuir valores de linha de acordo com a equação
            row[i] = eq[i]
            i += 1
        # linha[len(eq)-1] = 1
        row[-1] = eq[-1]

        # adicionar variável de folga de acordo com a localização no quadro.
        if type_const == 'G':
            row[var + j] = -1
            row[var + const + j] = 1
        if type_const == 'L':
            row[var + j] = 1
        if type_const == 'E':
            row[var + const + j] = 1

    else:
        print('Cannot add another constraint.')
    const = eq[0:var]
    b = eq[-1]
    return type_const, const, b

def constrainbab(table, eq):
    if add_cons(table) == True:
        lc = len(table[0, :])
        lr = len(table[:, 0])
        var = lc - 2 * lr
        const = lc - lr - var - 1
        # configurar o contador para iterar através do comprimento total das linhas
        j = 0
        while j < lr:
            # Iterar por linha
            row_check = table[j, :]
            # o total será a soma dos registos na linha
            total = 0
            # Encontrar a primeira linha com todas as entradas 0
            for i in row_check:
                total += float(i ** 2)
            if total == 0:
                # Encontrámos a primeira linha com todas as entradas zero
                row = row_check
                break
            j += 1

        eq, type_const = convert(eq)
        i = 0
        # itera através de todos os termos da função de restrição, excluindo o último
        while i < len(eq) - 1:
            # atribuir valores de linha de acordo com a equação
            row[i] = eq[i]
            i += 1
        # linha[len(eq)-1] = 1
        row[-1] = eq[-1]

        # adicionar variável de folga de acordo com a localização no quadro.
        if type_const == 'G':
            row[var + j] = -1
            row[var + const + j] = 1
        if type_const == 'L':
            row[var + j] = 1
        if type_const == 'E':
            row[var + const + j] = 1

    else:
        print('Cannot add another constraint.')


# verifica se uma função objectivo pode ser adicionada à matriz
def add_obj(table):
    lr = len(table[:, 0])
    # pretende saber SE existe exactamente uma linha com todos os elementos nulos
    empty = []
    # iterar através de cada linha
    for i in range(lr):
        total = 0
        for j in table[i, :]:
            # utilizar o valor quadrático para que (-x) e (+x) não se anulem mutuamente
            total += j ** 2
        if total == 0:
            # acrescentar zero à lista APENAS se todos os elementos de uma linha forem zero
            empty.append(total)
    # Existe exactamente uma linha com todos os elementos nulos se o seguinte for verdadeiro
    if len(empty) == 1:
        return True
    else:
        return False


# adiciona a função objetivo à matriz.
def obj(table, eq):
    if add_obj(table) == True:
        eq = [float(i) for i in eq.split(',')]
        lr = len(table[:, 0])
        row = table[lr - 1, :]
        i = 0
        # itera através de todos os termos da função de restrição, excluindo o último
        while i < len(eq) - 1:
            # atribuir valores de linha de acordo com a equação
            row[i] = eq[i] * -1
            i += 1
        row[-2] = 1
        row[-1] = eq[-1]
    else:
        print('You must finish adding constraints before the objective function can be added.')
    #eq=eq.remove(-1)
    return eq


# resolve o problema de maximização para obter uma solução óptima, devolve um dicionário com as chaves x1,x2...xn e max.
def maxz(table, output='summary'):
    while next_round_r(table) == True:
        print(table)
        table = pivot(loc_piv_r(table)[0], loc_piv_r(table)[1], table)
    while next_round(table) == True:
        print(table)
        table = pivot(loc_piv(table)[0], loc_piv(table)[1], table)

    lc = len(table[0, :])
    lr = len(table[:, 0])
    var = lc - lr - 1
    print(var)
    const = lr - 1
    i = 0
    val = {}
    solution=np.zeros(var)
    print(table)

    for i in range(var):
        col = table[:var+const, i]
        s = sum(col)
        m = max(col)
        if float(s) == float(m):
            loc = np.where(col == m)[0][0]
            print(gen_var(table))
            val[gen_var(table)[i]] = table[loc, -1]
            solution[i]=table[loc, -1]
        else:
            val[gen_var(table)[i]] = 0
    val['max'] = table[-1, -1]
    z=table[-1, -1]
    for k, v in val.items():
        val[k] = round(v, 4)
    if output == 'table':
        return table
    else:
        return val, table, solution, z


# resolve problemas de minimização para obter uma solução óptima, devolve um dicionário com as chaves x1,x2...xn e min.
def minz(table, output='summary'):
    #global solution

    table = convert_min(table)

    while next_round_r(table) == True:
        table = pivot(loc_piv_r(table)[0], loc_piv_r(table)[1], table)
    while next_round(table) == True:
        table = pivot(loc_piv(table)[0], loc_piv(table)[1], table)

    lc = len(table[0, :])
    lr = len(table[:, 0])
    var = lc - lr - 1
    const = lr - 1
    i = 0
    val = {}
    solution=np.zeros(var)
    for i in range(var):
        col = table[:var+const, i]
        s = sum(col)
        m = max(col)
        if float(s) == float(m):
            loc = np.where(col == m)[0][0]
            val[gen_var(table)[i]] = table[loc, -1]
            solution[i]=table[loc, -1]
        else:
            val[gen_var(table)[i]] = 0
    val['min'] = table[-1, -1] * -1
    z=table[-1, -1] * -1
    for k, v in val.items():
        val[k] = round(v, 6)
    if output == 'table':
        return table
    else:
        return val, table, solution, z

def minz_f1(table, output='table'):
    #table = convert_min(table)

    while next_round_r(table) == True:
        table = pivot(loc_piv_r(table)[0], loc_piv_r(table)[1], table)
    while next_round(table) == True:
        table = pivot(loc_pivf1(table)[0], loc_pivf1(table)[1], table)

    lc = len(table[0, :])
    lr = len(table[:, 0])
    var = lc - 2 * lr
    const = lc - lr - var - 1
    i = 0
    val = {}
    for i in range(var):
        col = table[:, i]
        s = sum(col)
        m = max(col)
        if float(s) == float(m):
            loc = np.where(col == m)[0][0]
            val[gen_var(table)[i]] = table[loc, -1]
        else:
            val[gen_var(table)[i]] = 0
    val['min'] = table[-1, -1] * -1
    for k, v in val.items():
        val[k] = round(v, 6)
    if output == 'table':
        return table
    else:
        return val

# adicionar função artificial W
def add_row(table):
    lc = len(table[0, :])
    lr = len(table[:, 0])
    var = lc - 2 * lr
    const = lc - lr - var - 1
    w = np.zeros(lc)
    for i in range(0, const):
        if table[i, var + const + i] == 1:
            a = [-1 * j for j in table[i, 0:var + const]]
            a.extend([0*i for i in range(0,lc-(var + const)-1)])
            a.append(-1*table[i, -1])
            w = [e1 + e2 for e1, e2 in zip(w, a)]
    table_f1 = np.vstack((table,w))
    return table_f1

def otimizar(m,type_problem, add_W, rows, cols):
    if add_W==1:
        print(m)
        tab=add_row(m)
        print(tab)
        lc = len(tab[0,:])
        tab1=minz_f1(tab)
        print(tab1)
        tab2 = np.delete(tab1,(-1), axis = 0)
        print(tab2)
        j=rows+cols
        i=lc-2
        while i>j:
            tab2 = np.delete(tab2, j, axis=1)
            i-=1
        
        print(tab2)
        if type_problem=='min':
            val,table,solution,z=minz(tab2)
            return val, table, solution,z
            
        else:
            val,table,solution,z=maxz(tab2)
            return val,table,solution,z

    else:
        lc = len(m[0,:])
        j=rows+cols
        i=lc-2
        while i>j:
            m = np.delete(m, j, axis=1)
            i-=1

        if type_problem=='min':
            val,table,solution,z=minz(m)
            return val,table,solution,z

        else:
            val,table,solution,z=maxz(m)
            return val,table,solution,z


def branch_and_bound(solution, zotimo, rows, cols, type_problem, add_W, restricoes, funcao, liminferior):
    nvar = rows
    sol = [round(i,4) for i in solution]
    print(sol)
    for i in range(0,nvar):
        if sol[i] != round(sol[i]):
            pos = i
            break
    print(pos)
    pl1 = round(sol[pos]-0.5)
    pl2 = round(sol[pos]+0.5)
    
    tab1 = gen_matrix(rows, cols+1)
    tab2 = gen_matrix(rows, cols+1)
    #cols=cols+1

    print(pl1)
    print(pl2)

    for r in restricoes:
        constrainbab(tab1,r)

    if pos==0:      
        constrainbab(tab1, f'1,0,<=,{pl1}')
        rest1=f'1,0,<=,{pl1}'
    else:
        constrainbab(tab1, f'0,1,<=,{pl1}')
        rest1=f'0,1,<=,{pl1}'
    obj(tab1,funcao)
    print(tab1)
    cols=cols+1
    val1,table1,solution1,zpl1=otimizar(tab1, type_problem, add_W, rows, cols)
    print(table1)
    print(val1)
 

    for r in restricoes:
        constrainbab(tab2,r)

    if pos==0:      
        constrainbab(tab2, f'1,0,>=,{pl2}')
        rest2=f'1,0,>=,{pl2}'
        add_W=1
    else:
        constrainbab(tab2, f'0,1,>=,{pl2}')
        rest2=f'0,1,>=,{pl2}'
        add_W=1
    obj(tab2,funcao)
    val1,table1,solution2,zpl2=otimizar(tab2, type_problem, add_W, rows, cols)

    solinteira1 = False
    inte1=0
    for i in solution1:
        if i == round(i):
            inte1=inte1+1
        if inte1 == nvar:
            solinteira1 = True

    solinteira2 = False
    inte2=0
    for i in solution2:
        if i == round(i):
            inte2=inte2+1
        if inte2 == nvar:
            solinteira2 = True

    if solinteira1:
            solint = solution1
            zint = zpl1
            liminferior = zint
            return solint, zint
    
    if solinteira2:
            solint = solution2
            zint = zpl2
            liminferior = zint
            return solint, zint
    
    else:
        if zpl1>=zpl2:
            restricoes.append(rest1)
            solinteira, zinteira = branch_and_bound(solution1, zpl1, rows, cols, type_problem, add_W, restricoes, funcao, liminferior)
            for i in solinteira:
                if i == round(i):
                    inte1=inte1+1
                if inte1 == nvar:
                    inteira = True
            if  inteira:
                return solinteira, zinteira
        else:
            restricoes.append(rest2)
            solinteira, zinteira=branch_and_bound(solution2, zpl2, rows, cols, type_problem, add_W, restricoes, funcao, liminferior)
            for i in solinteira:
                if i == round(i):
                    inte1=inte1+1
                if inte1 == nvar:
                    inteira = True
            if  inteira:
                return solinteira, zinteira
