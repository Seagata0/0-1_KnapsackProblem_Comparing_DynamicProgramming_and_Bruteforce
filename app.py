from flask import Flask, render_template, request
import itertools

app = Flask(__name__)

weights = [
1120,
800,
3050,
1850,
1740,
6650,
1700,
4600,
1590,
1970,
1120,
1840,
2000,
1380,
950,
540,
710,
1470,
2350,
3010,
500,
1740,
680,
140,
140,
300,
270,


]
profits = [40,
39
,38
,37
,36
,35
,34
,33
,32
,31
,30
,29
,28
,27
,26
,25
,24
,23
,22
,21
,20
,19
,18
,17
,13
,11
,8]

weights_def = [2, 5, 7, 3, 1]
profits_def = [20, 30, 35, 12, 3]

@app.route('/')
def index():
    global x
    x = len(weights)
    return render_template('index.html', x=x, weights=weights, profits=profits)

@app.route('/item', methods=['POST'])
def inputitem():
    itemw = int(request.form['weight'])
    itemp = int(request.form['profit'])
    weights.append(itemw)
    profits.append(itemp)
    x = len(weights)
    return render_template('index.html', weights=weights, profits=profits, x=x)


@app.route('/knapsack', methods=['POST'])
def knapsack():
    action = request.form.get('action')
    global capacity
    capacity = int(request.form['capacity'])
    if action == 'dynamic':
        profit, weight, items ,table = knapsackDP(weights, profits, capacity)
        return render_template('resultDP.html', profit=profit, weight=weight, items=items, table=table, weights=weights, profits=profits, capacity=capacity, n=len(weights))
    elif action == 'brute':
        profit, items, iteration = knapsackBF(weights, profits, capacity)
        return render_template('resultBF.html',profit=profit, items=items, iteration=iteration, weights=weights, profits=profits, capacity=capacity, n=len(weights), m=len(iteration))
    elif action == 'home':
        return render_template('index.html', x=x, weights=weights, profits=profits)
    elif action == 'kelompok':
        return render_template('kelompok.html', x=x, weights=weights, profits=profits)


@app.route('/knapsack2', methods=['POST'])
def knapsack2():
    action = request.form.get('action')
    if action == 'dynamic':
        profit, weight, items ,table = knapsackDP(weights, profits, capacity)
        return render_template('resultDP.html', profit=profit, weight=weight, items=items, table=table, weights=weights, profits=profits, capacity=capacity, n=len(weights))
    elif action == 'brute':
        profit, items, iteration = knapsackBF(weights, profits, capacity)
        return render_template('resultBF.html',profit=profit, items=items, iteration=iteration, weights=weights, profits=profits, capacity=capacity, n=len(weights), m=len(iteration))
    elif action == 'home':
        return render_template('index.html', x=x, weights=weights, profits=profits)
    elif action == 'kelompok':
        return render_template('kelompok.html', x=x, weights=weights, profits=profits)

def knapsackDP(weight, profit, capacity):
    n = len(weight)
    table = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for w in range(1, capacity + 1):
            if weight[i - 1] > w:
                table[i][w] = table[i - 1][w]
            else:
                table[i][w] = max(table[i - 1][w], profit[i - 1] + table[i - 1][w - weight[i - 1]])
    item_dipilih = []
    total_weight = capacity
    for i in range(n, 0, -1):
        if table[i][total_weight] != table[i - 1][total_weight]:
            item_dipilih.append(i - 1)
            total_weight -= weight[i - 1]
    item_dipilih.reverse()
    item_dipilih = [x+1 for x in item_dipilih]
    return table[n][capacity], total_weight, item_dipilih, table


def knapsackBF(weight, profit, capacity):
    n = len(weight)
    max_value = float("-inf")
    item_dipilih = []
    iterations = []
    x=1
    def recursive_knapsack(i, w, cur_value, cur_items):
        nonlocal max_value, item_dipilih
        if i == 0 or w == 0:
            if cur_value > max_value:
                max_value = cur_value
                item_dipilih = [0] * n
                for x in cur_items:
                  item_dipilih[x] = 1 
            return
        if weight[i - 1] > w:
            recursive_knapsack(i - 1, w, cur_value, cur_items)
        else:
            recursive_knapsack(i - 1, w, cur_value, cur_items)
            recursive_knapsack(i - 1, w - weight[i - 1], cur_value + profit[i - 1], cur_items + [i - 1])
    recursive_knapsack(n, capacity, 0, [])
    for i in range(1, len(weight) + 1):
        combinations = itertools.combinations(range(len(weight)), i)
        for combination in combinations:
            total_value = sum(profit[i] for i in combination)
            total_weight = sum(weight[i] for i in combination)
            combination = [x+1 for x in combination]
            iterations.append((x,total_value,total_weight,combination))
            x+=1
    return max_value, item_dipilih, iterations


if __name__ == '__main__':
    app.run()
