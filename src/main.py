from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/update", methods=["GET", "POST"])

def update():
    if request.method == "POST":
        major = request.form.get("major")
        graduation = request.form.get("graduation")
        # TODO: Save to database
        print("Major:", major)
        print("Graduation Date:", graduation)
        return redirect(url_for("requirements"))

    return render_template("update.html")

@app.route("/requirements")
def requirements():
    return render_template("requirements.html")

@app.route("/optimal-path")
def optimal_path():
    return render_template("optimal_path.html")

@app.route("/patriotai")
def patriotai():
    return render_template("patriotai.html")

if __name__ == "__main__":
    app.run(debug=True)
