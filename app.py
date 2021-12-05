from flask import *
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)


# @app.route('/')
# def hello():
#     return "Hello World"


# @app.route('/')
# def bootstrap():
#     return render_template('pages/bootstrap.html')

@app.route('/program/<name>')
def program(name):
    return render_template('bootstrap.html', name=name)
#왜 404 뜨지.. 근데 localhost:5000/program/어쩌구로 들어 간 거 맞지? 지금 다시 하면 어떰? 저거 templates 안에 넣어야 되네 이거 내가 실행해 볼 수 없으니 힘들구만 줌으로 화면 공유 부탁
# 아 이게 라이브러리 조 잇구나나
# 너는 실행 안됨??? 난 안 되는 것 같은데 애초에 지금 내 화면에 너가 실행하는 콘솔이 보임
# ttp://127.0.0.1:5000/program/Python 이렇게 들어감
# 너 화면에 실행버튼 떠? 어 너가 종료해서 보이긴 하는데 눌러 볼게 아 이거 지금 로컬호스트라 나도 저걸 가지고 있어야 되지 저거 좀 만어 볼게 아니 근데 그럼 공동 작업이 의미가 없네
# ㅋㅋㅋㅋㅋㅋ 그럼 일단 난 VSC로 받아 봄 ㄱㄷ 그 한 번 푸시 좀 해 줘 html 받게
# ㅋㅋ 제트브레인!! 일해@!! 오케 아마자 ㅋㅋ 잠만
if __name__ == '__main__':
    app.run()
