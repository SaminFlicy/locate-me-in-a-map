from flask import Flask, render_template, request
import requests
import urllib.parse
import urllib.request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def details():
    if request.method == "GEt":
        return render_template("index.html")
    location = request.form.get("location", "".strip())
    if not location:
        return render_template("index.html", error="Give the correct location")
    try:
        url = "https://nominatim.openstreetmap.org/search"

        params = {
            "q": location, 
            "format": "json",
            "limit": 1
        }
        headers = {
            "User-Agent": "Mozilla/5.0 (locationApp)"

        }
        response = requests.get(url, params=params, headers=headers, timeout=10)
        data = response.json()

        print(data)

        if not data:
            return render_template("index.html", error="Location not found")
        return render_template("index.html", data={
            "latitude": data[0]["lat"],
            "longitude": data[0]["lon"],
            "name": data[0].get("display_name", location)

        })
    except Exception as e:
        print("ERROR:", e)
        return render_template("index.html", error=str(e))
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
