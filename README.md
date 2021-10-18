# Python3.9 Flask SPA in Docker

Docker template

`Apache + Python3.9 + Flask (wsgi)`

## ref

- [Docker + Python + Flask で API サーバーを構築してみる](http://unalus.com/wp/2019/11/22/docker-python-flask%E3%81%A7api%E3%82%B5%E3%83%BC%E3%83%90%E3%83%BC%E3%82%92%E6%A7%8B%E7%AF%89%E3%81%97%E3%81%A6%E3%81%BF%E3%82%8B/)
- [Flask に SPA バックエンドを全て任せたい話 - Qiita](https://qiita.com/ytkj/items/ab67a1cee3cbfc42254d)

## TODO

- **pending** calender.get_schedule() で calendar_xxxx.json のファイルがない場合の挙動 (API 対応)
  - get_schedule() の戻りを empty dict にする
  - API で xxxx 別に取得するようにし、該当がない場合はエラーをレスポンスする

---

## pip install

コンテナ起動後に実行

```bash
pipenv install --dev
cd src
npm install
```

## auth database 初期化

```bash
pipenv run python
```

```python
from app import db, create_app
db.create_all(app=create_app())
```

## waitress serve

```bash
# with auto reload
hupper -m serve_waitress.py

#without auto reload
python serve_waitress.py
```

## port

- 8083:80   web http
- 8084:8080 npm run serve
- 8500:5000 flask-debug

## (hint) Python 3.9 + mod_wsgi のとき import エラー

`import numpy` が失敗する。エラーメッセージ内にあるように Python の version が 3.9 ではなく 3.7 になってしまっている。

```docker:logs
flask-web [wsgi:error] mod_wsgi (pid=9): Exception occurred processing WSGI script '/var/www/app.wsgi'.
flask-web [wsgi:error] Traceback (most recent call last):
flask-web [wsgi:error]   File "/var/www/.venv/lib/python3.9/site-packages/flask/app.py", line 2464, in __call__
flask-web [wsgi:error]     return self.wsgi_app(environ, start_response)
flask-web [wsgi:error]   File "/var/www/.venv/lib/python3.9/site-packages/flask/app.py", line 2450, in wsgi_app
flask-web [wsgi:error]     response = self.handle_exception(e)
flask-web [wsgi:error]   File "/var/www/.venv/lib/python3.9/site-packages/flask/app.py", line 1867, in handle_exception
flask-web [wsgi:error]     reraise(exc_type, exc_value, tb)
flask-web [wsgi:error]   File "/var/www/.venv/lib/python3.9/site-packages/flask/_compat.py", line 39, in reraise
flask-web [wsgi:error]     raise value
flask-web [wsgi:error]   File "/var/www/.venv/lib/python3.9/site-packages/flask/app.py", line 2447, in wsgi_app
flask-web [wsgi:error]     response = self.full_dispatch_request()
flask-web [wsgi:error]   File "/var/www/.venv/lib/python3.9/site-packages/flask/app.py", line 1952, in full_dispatch_request
flask-web [wsgi:error]     rv = self.handle_user_exception(e)
flask-web [wsgi:error]   File "/var/www/.venv/lib/python3.9/site-packages/flask/app.py", line 1821, in handle_user_exception
flask-web [wsgi:error]     reraise(exc_type, exc_value, tb)
flask-web [wsgi:error]   File "/var/www/.venv/lib/python3.9/site-packages/flask/_compat.py", line 39, in reraise
flask-web [wsgi:error]     raise value
flask-web [wsgi:error]   File "/var/www/.venv/lib/python3.9/site-packages/flask/app.py", line 1950, in full_dispatch_request
flask-web [wsgi:error]     rv = self.dispatch_request()
flask-web [wsgi:error]   File "/var/www/.venv/lib/python3.9/site-packages/flask/app.py", line 1936, in dispatch_request
flask-web [wsgi:error]     return self.view_functions[rule.endpoint](**req.view_args)
flask-web [wsgi:error]   File "/var/www/app/main.py", line 29, in sales
flask-web [wsgi:error]     import pandas as pd
flask-web [wsgi:error]   File "/var/www/.venv/lib/python3.9/site-packages/pandas/__init__.py", line 17, in <module>
flask-web [wsgi:error]     "Unable to import required dependencies:\\n" + "\\n".join(missing_dependencies)
flask-web [wsgi:error] ImportError: Unable to import required dependencies:
flask-web [wsgi:error] numpy:
flask-web [wsgi:error]
flask-web [wsgi:error] IMPORTANT: PLEASE READ THIS FOR ADVICE ON HOW TO SOLVE THIS ISSUE!
flask-web [wsgi:error]
flask-web [wsgi:error] Importing the numpy C-extensions failed. This error can happen for
flask-web [wsgi:error] many reasons, often due to issues with your setup or how NumPy was
flask-web [wsgi:error] installed.
flask-web [wsgi:error]
flask-web [wsgi:error] We have compiled some common reasons and troubleshooting tips at:
flask-web [wsgi:error]
flask-web [wsgi:error]     https://numpy.org/devdocs/user/troubleshooting-importerror.html
flask-web [wsgi:error]
flask-web [wsgi:error] Please note and check the following:
flask-web [wsgi:error]
flask-web [wsgi:error]   * The Python version is: Python3.7 from "/var/www/.venv/bin/python3"
flask-web [wsgi:error]   * The NumPy version is: "1.20.2"
flask-web [wsgi:error]
flask-web [wsgi:error] and make sure that they are the versions you expect.
flask-web [wsgi:error] Please carefully study the documentation linked above for further help.
flask-web [wsgi:error]
flask-web [wsgi:error] Original error was: No module named 'numpy.core._multiarray_umath'
flask-web [wsgi:error]
```

- `find / -name python3`

  - /usr/local/bin/python3 -> version 3.9
  - /usr/bin/python3 -> version 3.7
  - 使っているのが Debian10 ベースの Docker イメージで 標準のリポジトリは 3.7 のため 3.9 が別途追加されている状態と思われる

- cli で python インタプリタを動かして、import numpy してもエラーにならない
- flask ビルトインサーバーで動かすと Python 3.9 が使われエラーにはならない
- wsgi から呼び出すと sys.version_info が 3.7 になる（ただし Python のパス`sys.executable`は 3.9 の分が表示される）
- 環境変数が PATH が wsig から実行したとき(root?)とビルトインサーバー(www-data?)を使用したときで異なるので、dockerfile ENV PATH で 先頭に venv/bin パスを追加したがエラー直らず
- dockerfile で Python 3.7 のファイルを 3.9 のリンクにする `RUN ln -sf /usr/local/bin/python3 /usr/bin/python3` -> エラー直らず

### apt で モジュールをインストールせずに pip から mod_wsgi をインストールする

```dockerfile
(remove) apt-get install libapache2-mod-wsgi-py3
(add) pip install mod_wsgi
```

apt の場合は LoadModule が自動的に読み込まれるようになるが pip でインストールの場合は自分で apache config に追加する

```bash
mod_wsgi-express module-config # apache conf に追加する内容を確認する
# LoadModule wsgi_module "/usr/local/lib/python3.9/site-packages/mod_wsgi/server/mod_wsgi-py39.cpython-39-x86_64-linux-gnu.so"
# WSGIPythonHome "/usr/local"
```

wsgi から呼び出ししたときの import numpy エラーがでなくなった

## (hint) ファイル監視数の上限

npm watch, serve で`Error: ENOSPC: System limit for number of file watchers reached` となる場合、OS ファイル変更監視の上限を超過しているので、値を変更。docker は host 側の値を read-only で参照しているようなので、host 側で設定を変える。

```bash
# 確認
cat /proc/sys/fs/inotify/max_user_watches

# 設定（一時的）
sudo sysctl fs.inotify.max_user_watches=524288
```

恒久的に設定しておく場合は
/etc/sysctl.conf に fs.inotify.max_user_watches=
を追加する。（未確認）
