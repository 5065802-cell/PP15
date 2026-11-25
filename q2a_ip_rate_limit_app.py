from flask import Flask, request

app = Flask(__name__)
failed_attempts = {}

@app.route("/", methods=["GET", "POST"])
def login():
    ip = request.remote_addr
    if failed_attempts.get(ip, 0) >= 3:
        return "<h3>Too many failed attempts! Your IP is temporarily blocked.</h3>", 429

    msg = ""
    if request.method == "POST":
        u = request.form.get("username")
        p = request.form.get("password")
        if u == "admin" and p == "12345":
            failed_attempts[ip] = 0
            return "<h3>Login Successful!</h3>"
        else:
            failed_attempts[ip] = failed_attempts.get(ip, 0) + 1
            msg = f"Invalid credentials. Attempt {failed_attempts[ip]}/3"

    return f'''
    <h2>Rate-Limited Login</h2>
    <form method="POST">
      Username: <input name="username"><br><br>
      Password: <input name="password" type="password"><br><br>
      <button type="submit">Login</button>
    </form>
    <p style="color:red">{msg}</p>
    '''

if __name__ == "__main__":
    app.run(debug=True)
