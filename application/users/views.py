from flask import Flask
#インスタンスを生成
app = Flask(__name__)
 
#ルーティング
@app.route('/')
def hello_world ():
    return '<html><body><h1>hello world</h1><h2>これはサンプルページです</h2></html></body>'


#実行プログラム
if __name__ == '__main__':
    app.run()