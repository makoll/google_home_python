import yaml
from copy import deepcopy
from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup

url = 'https://www.library.city.kita.tokyo.jp/'

f = open('config/library_private.yaml', 'r+')
library_private_conf = yaml.load(f)

# セッションを開始
session = requests.session()

# 自身の名称を app という名前でインスタンス化する
app = Flask(__name__)


@app.route('/borrowed_books')
def get_borrowed_books():
    user = request.args.get('user', '')
    _login_info = deepcopy(library_private_conf.get(user))
    _login_info['LOGIN'] = 'ログイン'

    url_login = 'https://www.library.city.kita.tokyo.jp/opac/OPP1000?MENUNO=4'
    res = session.post(url_login, data=_login_info)
    res.raise_for_status()  # エラーならここで例外を発生させる

    soup = BeautifulSoup(res.text, 'lxml')
    trs = soup.select('form[name="EXTEND"] a')
    returns = []
    for tr in trs:
        returns.append(tr.text)
    return jsonify(returns)


if __name__ == '__main__':
    app.debug = True  # デバッグモード有効化
    app.run(host='0.0.0.0')  # どこからでもアクセス可能に
