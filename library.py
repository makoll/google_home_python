import yaml
from copy import deepcopy
from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup, NavigableString

url = 'https://www.library.city.kita.tokyo.jp/'

f = open('config/library_private.yaml', 'r+')
library_private_conf = yaml.load(f)

# セッションを開始
session = requests.session()
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3)' 'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'Accept': '*/*'
}

# 自身の名称を app という名前でインスタンス化する
app = Flask(__name__)


@app.route('/borrowed_books')
def get_borrowed_books():
    user = request.args.get('user', '')
    _login_info = deepcopy(library_private_conf.get(user))
    _login_info['LOGIN'] = 'ログイン'

    # url_login = 'https://www.library.city.kita.tokyo.jp/opac/OPP1000?MENUNO=4'
    # session.post(url_login, data=_login_info)
    # res = session.get(url_login, headers=headers)
    # res.raise_for_status()  # エラーならここで例外を発生させる
    # text = res.text

    # f = open('/tmp/text.txt', 'w') # 書き込みモードで開く
    # f.write(text) # 引数の文字列をファイルに書き込む
    # f.close() # ファイルを閉じる

    f = open('/tmp/text.txt', 'r')
    text = f.read()
    f.close()

    soup = BeautifulSoup(text, 'lxml')
    aa = soup.find('form', attrs={'name': 'EXTEND_F'})
    trs = aa.find_all('td')
    returns = []
    for hr in trs:
        next_elm = hr.next_sibling
        ci = 1
        while next_elm:
            print('No: ', ci)
            tgt_elm = next_elm
            next_elm = tgt_elm.next_sibling
            if type(tgt_elm) is not NavigableString:
                continue
            print(tgt_elm)
            returns.append(tgt_elm)

    return jsonify(returns)


if __name__ == '__main__':
    app.debug = True  # デバッグモード有効化
    app.run(host='0.0.0.0')  # どこからでもアクセス可能に
