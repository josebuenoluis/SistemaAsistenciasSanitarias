from flask import Flask,jsonify,request
import time
app = Flask(__name__)

@app.route("/relay/0")
def accion_led():
    turn = request.args.get("turn","")
    if turn == "on":
        print("Encendido")
    else:
        print("Apagado")

    return jsonify({"success":True})


if __name__ == '__main__':
    
    app.run(debug=True,host="0.0.0.0",port=8000)