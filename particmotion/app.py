import io
import base64
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
matplotlib.use('Agg') 

def generate_plot(force_func, t_final):
    t_steps = np.linspace(0, t_final, 100)
    f_values = [force_func(t) for t in t_steps]
    
    
    plt.figure(figsize=(5, 3))
    plt.plot(t_steps, f_values, color='#007bff', linewidth=2)
    plt.title('Force vs Time')
    plt.xlabel('Time (s)')
    plt.ylabel('Force (N)')
    plt.grid(True, linestyle='--')
    
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close() 
    buf.seek(0)
    
    
    plot_url = base64.b64encode(buf.getvalue()).decode('utf8')
    return plot_url



from flask import Flask, request, jsonify, render_template
from physics import classical_motion, relativistic_motion
import utils 

app=Flask(__name__)
@app.route("/")
def index():
    return render_template("visuals.html")
@app.route("/calculate", methods=["POST"])


def calculate():
    data = request.json
    try:
        m = float(data["mass"]) 
        v0 = float(data["v0"]) 
        t = float(data["t"]) 
        mode = data["mode"]
        force_type = data["force_type"]
        
        
        if force_type == "constant":
            force_func = utils.constant_force(float(data["F"])) 
        elif force_type == "sinusoidal":
            force_func = utils.sinusoidal_force(float(data["F0"]), float(data["omega"]))
        elif force_type == "linear":
            force_func = utils.linear_force(float(data["k"]))
        elif force_type == "exponential":
            force_func = utils.exponential_force(float(data["F0"]), float(data["tau"]))
        else:
            return jsonify({"error": "unknown force type"}), 400

        
        if mode == "classical":
            v, p = classical_motion(m, v0, force_func, t)
            graph_base64 = generate_plot(force_func, t)

            return jsonify({
                "v": round(v, 4), 
                "p": round(p, 4),
                "graph": graph_base64  
            })
        elif mode == "relativistic":
            v, p = relativistic_motion(m, v0, force_func, t)
            graph_base64 = generate_plot(force_func, t)

            return jsonify({
                "v": round(v, 4), 
                "p": round(p, 4),
                "graph": graph_base64  
            })
        


        
        
        return jsonify({"v": round(v, 4), "p": round(p, 4)})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__=="__main__":
    app.run(debug=True)
    