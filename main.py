from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

# /home - テキストボックスを表示
@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        url = request.form['url']
        mode = request.form['mode']
        if mode == '1':
            return f'<a href="/proxy?1={url}">コードを表示する</a>'
        elif mode == '2':
            return f'<a href="/proxy?2={url}">HTMLを実行する</a>'
        else:
            return "無効な選択です。"
    return '''
    <form method="post">
        <label for="url">リンクを入力:</label>
        <input type="text" id="url" name="url" required>
        <br>
        <label for="mode">モード選択:</label>
        <select id="mode" name="mode">
            <option value="1">コード表示</option>
            <option value="2">コード実行 (HTMLのみ)</option>
        </select>
        <br>
        <button type="submit">送信</button>
    </form>
    '''

# /proxy?1=${url} - コードを表示
@app.route('/proxy', methods=['GET'])
def proxy():
    url = request.args.get('1') or request.args.get('2')
    if not url:
        return "URLが提供されていません。"

    try:
        response = requests.get(url)
        response.raise_for_status()
        if '1' in request.args:
            # コードを表示
            return f"<pre>{response.text}</pre>"
        elif '2' in request.args:
            # HTMLを実行
            return response.text
    except requests.RequestException as e:
        return f"エラーが発生しました: {e}"

if __name__ == '__main__':
    app.run(debug=True)
