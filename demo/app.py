from flask import Flask, request, redirect, render_template

app = Flask(__name__)


@app.route('/list/<int:page>')
def list_items(page):
    return f'Listing items on page {page}'

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9191)
