from flask import Flask, request, render_template
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan():
    url = request.form['url']
    results = {
        'sql_injection': check_sql_injection(url),
        'xss': check_xss(url)
    }
    return render_template('results.html', results=results)

def check_sql_injection(url):
    sql_payloads = ["'", "1' OR '1' = '1", "'; --", "' OR '1'='1' --"]
    vulnerable = False
    for payload in sql_payloads:
        full_url = f"{url}{payload}"
        response = requests.get(full_url)
        if "SQL" in response.text or "syntax" in response.text:
            return True
    return False

def check_xss(url):
    xss_payloads = ["<script>alert('XSS')</script>", "\"<script>alert('XSS')</script>"]
    vulnerable = False
    for payload in xss_payloads:
        full_url = f"{url}?q={payload}"
        response = requests.get(full_url)
        if payload in response.text:
            return True
    return False

if __name__ == "__main__":
    app.run(debug=True)
