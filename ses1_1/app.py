from flask import *
from flask_bootstrap import Bootstrap
import pyotp

# configuring flask application
app = Flask(__name__)
app.config["SECRET_KEY"] = "APP_SECRET_KEY"
Bootstrap(app)

class OTPGen:
    def __init__(self):
        self.i = 0
        self.hotp = pyotp.HOTP(pyotp.random_base32())

    def generate(self):
        i = self.i
        otp = self.hotp.at(i)
        self.i += 1
        return [i,otp]

    def verify(self, i, otp):
        return self.hotp.verify(otp, i)

# login page route
@app.route("/")
def login():
    return render_template("login.html")

# login form route
@app.route("/", methods=["POST"])
def login_form():
    # demo creds
    creds = {"username": "gdsc", "password": "password"}

    # getting form data
    username = request.form.get("username")
    password = request.form.get("password")

    # authenticating submitted creds with demo creds
    if username == creds["username"] and password == creds["password"]:
        return redirect(url_for("login_2fa"))
    else:
       	# inform users if creds are invalid
       	flash("You have supplied invalid login credentials!", "danger")
        return redirect(url_for("login"))

# 2FA page route
@app.route("/login/2fa/")
def login_2fa():
    # generating random secret key for authentication
    i, otp = otp_gen.generate()
    print(otp)
    return render_template("login_2fa.html", i=i)

# 2FA form route
@app.route("/login/2fa/", methods=["POST"])
def login_2fa_form():
    # getting secret key used by user
    secret = int(request.form.get("i"))
    # getting OTP provided by user
    otp = request.form.get("otp")

    # verifying submitted OTP with PyOTP
    val = otp_gen.verify(secret,otp)
    if val:
        # inform users if OTP is valid
        flash("Valid", "success")
        return redirect(url_for("success"))
    else:
        # inform users if OTP is invalid
        flash("You have supplied an invalid 2FA token! Token Reset", "danger")
        return redirect(url_for("login_2fa"))

@app.route("/success/")
def success():
    return render_template("success.html")

# running flask server
if __name__ == "__main__":
    otp_gen = OTPGen()
    app.run(debug=True)

