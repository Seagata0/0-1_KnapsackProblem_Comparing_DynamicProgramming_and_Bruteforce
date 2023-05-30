from flask import Flask, render_template, request

app = Flask(__name__)

weights = []
profits = []

weights_def = [2, 5, 7, 3, 1]
profits_def = [20, 30, 35, 12, 3]

@app.route('/')
def index():
    global x
    x = 0
    return render_template('index.html', x=x)

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
    capacity = int(request.form['capacity'])
    max_value, table = knapsackDP(weights, profits, capacity)
    return render_template('result.html', max_value=max_value, table=table, weights=weights, profits=profits, capacity=capacity, n=len(weights))


def knapsackDP(weights, profits, capacity):
    n = len(weights)

    table = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(n + 1):
        for w in range(capacity + 1):
            if i == 0 or w == 0:
                table[i][w] = 0
            elif weights[i - 1] <= w:
                table[i][w] = max(profits[i - 1] + table[i - 1][w - weights[i - 1]], table[i - 1][w])
            else:
                table[i][w] = table[i - 1][w]

    return table[n][capacity], table

def knapsackBF(weights, profits, capacity):
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(1, capacity + 1):
            if weights[i - 1] <= w:
                dp[i][w] = max(profits[i - 1] + dp[i - 1][w - weights[i - 1]], dp[i - 1][w])
            else:
                dp[i][w] = dp[i - 1][w]

    selected_items = []
    w = capacity
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            selected_items.append(i - 1)
            w -= weights[i - 1]

    return dp[n][capacity], selected_items[::-1]

def generate_table(weights, profits, capacity):
    n = len(weights)

    table = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(n + 1):
        for w in range(capacity + 1):
            if i == 0 or w == 0:
                table[i][w] = 0
            elif weights[i - 1] <= w:
                table[i][w] = max(profits[i - 1] + table[i - 1][w - weights[i - 1]], table[i - 1][w])
            else:
                table[i][w] = table[i - 1][w]

    table_html = "<table>"
    table_html += "<thead><tr><th>Weights</th><th>profits</th>"
    for w in range(capacity + 1):
        table_html += f"<th>{w}</th>"
    table_html += "</tr></thead>"
    
    table_html += "<tbody>"
    for i in range(n + 1):
        table_html += "<tr>"
        if i < n:
            table_html += f"<td>{weights[i]}</td><td>{profits[i]}</td>"
        else:
            table_html += "<td>-</td><td>-</td>"
        for w in range(capacity + 1):
            table_html += f"<td>{table[i][w]}</td>"
        table_html += "</tr>"
    table_html += "</tbody>"

    table_html += "</table>"

    return table_html


if __name__ == '__main__':
    app.run()
