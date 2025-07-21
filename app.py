from flask import Flask, render_template
app=Flask(__name__)
@app.route("/")
def main():
    return render_template("home.html")
@app.route("/market")
def market():
    return render_template("market.html")