from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():

    return """
    <html>

    <head>

        <title>AeroFlowAI</title>

        <meta http-equiv="refresh" content="2">

        <style>

            body{
                background:#0b0f19;
                color:white;
                font-family:Arial;
                text-align:center;
                padding-top:100px;
            }

            h1{
                color:#00d4ff;
                font-size:50px;
            }

            .card{
                background:#111827;
                width:500px;
                margin:auto;
                padding:30px;
                border-radius:20px;
                box-shadow:0px 0px 20px rgba(0,212,255,0.3);
            }

        </style>

    </head>

    <body>

        <h1>🚀 AeroFlowAI</h1>

        <div class="card">

            <h2>AI Aerospace Monitoring System</h2>

            <p>Hydraulic Network Simulation Running...</p>

            <p>Status: 🟢 ACTIVE</p>

            <p>Machine Learning Prediction Engine Online</p>

        </div>

    </body>

    </html>
    """

if __name__ == "__main__":

    import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)