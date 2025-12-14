from flask import Flask, render_template
from data import portfolio_data

app = Flask(__name__)

@app.route('/')
def index():
    # data.py에서 정의한 데이터를 템플릿으로 넘겨줍니다.
    return render_template('index.html', data=portfolio_data)

if __name__ == '__main__':
    app.run(debug=True, port='4444')