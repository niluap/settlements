from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from results import compute_settlements

app = Flask(__name__)
app.config['SECRET_KEY'] = 'kochampaulie'
app.config['CORS_HEADERS'] = 'Content-Type'

cors = CORS(app, resources={r"/tasks": {"origins": "http://localhost:80"}})


'''Compute settlemnets function--->Three elements tuple:
1 - The maximum depth at which loads affect settlement
2 - Settlements caused by secondary stresses
3 - settlements caused by primary stresses
'''
def isValidFormData(B, L, excavation_depth, evenly_distributed_load):
    if (not isinstance(B, (int, float))) or (B <= 0):
        return False
    if (not isinstance(L, (int, float))) or (L <= 0):
        return False
    if (not isinstance(excavation_depth, (int, float))) or (excavation_depth <= 0):
        return False
    if (not isinstance(evenly_distributed_load, (int, float))) or (evenly_distributed_load <= 0):
        return False

    return True

@app.before_request
def log_request_info():
    app.logger.info('Headers: %s', request.headers)
    app.logger.info('Body: %s', request.get_data())

@app.route('/', methods=['GET'])
def test():
    return jsonify({"message": "It works! but i do not know what i have done"})

@app.route('/tasks', methods=["POST"])
@cross_origin(origin='localhost', headers=['Content-Type', 'Authorization'])
def add_task():
    B = request.json['width']
    L = request.json['length']
    excavation_depth = request.json['excavation_depth']
    evenly_distributed_load = request.json['evenly_distributed_load']

    if not isValidFormData(B, L, excavation_depth, evenly_distributed_load):
        return jsonify({'error': True})
    else:
        get_results = compute_settlements(L, B, excavation_depth, evenly_distributed_load)
        total_settlement = get_results[1] + get_results[2]
        return jsonify({'error': False,\
                    'Maximum depth at which loads affect settlements [m]': get_results[0],\
                        'Total settlements [mm]': total_settlement})
'''
    {
        "error": False,
        "timestamp": 12341243,
        "data": {
            "maxDepth": {
                value: 10,
                unit: 'm',
                info: 'max depth at which loads affect settlements'
            }
        }
    }
'''
if __name__ == '__main__':
    # handler.setLevel(logging.INFO)
    app.run(debug=True, port=8080)

