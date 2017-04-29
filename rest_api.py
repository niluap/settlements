from flask import Flask, jsonify, request
from results import compute_settlements
app = Flask(__name__)

'''Compute settlemnets function--->Three elements tuple:
1 - The maximum depth at which loads affect settlement
2 - Settlements caused by secondary stresses
3 - settlements caused by primary stresses
'''

@app.route('/', methods=['GET'])
def test():
    return jsonify({"message": "it works! but i do not know what i have done"})


@app.route('/tasks', methods=["POST"])
def add_task():
    B = request.json['width']
    L = request.json['length']
    excavation_depth = request.json['excavation_depth']
    evenly_distributed_load = request.json['evenly_distributed_load']
    status = "OK"
    if B <= 0 or L<= 0:
        status = "NOT OK"
    else:
        get_results = compute_settlements(L, B, excavation_depth, evenly_distributed_load)
        total_settlement = get_results[1] + get_results[2]
        return jsonify({'Status': status,\
                    'The maximum depth at which loads affect settlement [m]': get_results[0],\
                        'Total settlements [mm]': total_settlement})


'''
#Dane wyjściowe - wpisywane przez użytkowanika
L = L_from_api #10 float(input("L:"))
B = B_from_api #2 float(input("B:"))

z = round(database.soil_layers_data[0][-1], 2)

excavation_depth = excavation_depth_from_api #1.1 float(input("excavation depth:"))
evenly_distributed_load = evenly_distributed_load_from_api #100 float(input("q:"))
'''

if __name__ == '__main__':
    app.run(debug=True, port=8080)

