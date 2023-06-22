from flask import Flask, request, jsonify, render_template
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField
from wtforms.validators import DataRequired, NumberRange
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.layout_engine import ConstrainedLayoutEngine
from backend import gen_matrix, minz, minz_f1, maxz, constrain, obj, add_row, convert
from grafico import plotagraf, formatTable

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

# Classe do formulário
class OptimizationForm(FlaskForm):
    rows = IntegerField('Número de Variáveis', validators=[DataRequired(), NumberRange(min=1)])
    cols = IntegerField('Número de Restrições', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Enviar')

# Rota para renderizar o formulário
@app.route('/', methods=['GET', 'POST'])
def index():
    form = OptimizationForm()

    if form.validate_on_submit():
        rows = form.rows.data
        cols = form.cols.data

        # Redirecionar para a rota de entrada de valores das restrições
        return jsonify({'redirect': '/constraints', 'rows': rows, 'cols': cols})

    return render_template('index.html', form=form)

# Rota para entrada de valores das restrições
@app.route('/constraints', methods=['GET', 'POST'])
def enter_constraints():
    rows = int(request.args.get('rows'))
    cols = int(request.args.get('cols'))

    # Cria um novo formulário dinamicamente para cada restrição
    class ConstraintForm(FlaskForm):
        constraint = StringField('Restrição', validators=[DataRequired()])
        submit = SubmitField('Enviar')

    forms = [ConstraintForm(prefix=f'constraint_{i+1}') for i in range(cols)]

    if request.method == 'POST':
        # Obter os valores das restrições fornecidos pelo usuário
        constraints = [form.constraint.data for form in forms]

        # Redirecionar para a rota de otimização com os dados fornecidos
        return jsonify({'redirect': '/optimize', 'rows': rows, 'cols': cols, 'constraints': constraints})

    return render_template('constraints.html', forms=forms)

# Rota para realizar a otimização
@app.route('/optimize', methods=['POST'])
def optimize():
    data = request.get_json()
    rows = int(data['rows'])
    cols = int(data['cols'])
    constraints = data['constraints']

    m = gen_matrix(rows, cols)
    restr = []
    b = []

    num_constraints = cols
    for i in range(num_constraints):
        constraint_str = constraints[i]
        type_const, const, b_temp = constrain(m, constraint_str)
        restr.append(const)
        b.append([b_temp])
        if type_const == '>=' or type_const == '=':
            add_W = True

    objective_str = data['objective']
    z = obj(m, objective_str)
    type_problem = data['problem_type']

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

    pp = [0.5, 0.5]
    xlim = (-1, 10)

    result = {
        'value': val,
        'table': table.tolist(),
        'solution': solution.tolist()
    }

    return jsonify(result)

if __name__ == '__main__':
    app.run(port=5001)
