from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    # 모든 데이터는 index.html에서 직접 관리합니다.
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port='4444')