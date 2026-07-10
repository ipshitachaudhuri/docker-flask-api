from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return {"message": "Hello from Docker Project!"}

@app.route("/health")
def health():
    return {"status": "healthy"}

# ADD THIS HERE
@app.route("/version")
def version():
    return {
        "application": "flask-api",
        "version": "1.0.0",
        "environment": "production"
    }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
