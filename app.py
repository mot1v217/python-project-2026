from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)


@app.route("/")
def index():
    reports = pd.read_csv("data/reports.csv")
    return render_template("index.html", reports=reports.to_dict("records"))


if __name__ == "__main__":
    app.run(debug=True)