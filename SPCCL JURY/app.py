from flask import Flask, render_template, request
from main import MiniLangCompiler

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():

    result = None

    if request.method == 'POST':

        code = request.form['code']

        compiler = MiniLangCompiler()

        result = compiler.compile(code)

    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)