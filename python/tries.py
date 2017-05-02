import bisect

soil_layers_database = [[3, 5, 9, 11], [20, 17, 19.5, 18], [36, 46, 42, 22], [40, 58, 80, 37]]
# reduce((lambda memo, current: memo + current), database.soil_layers_data[0], 0)
layers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]


def get_weight_at_depth(soil_base, depth):
    weight = bisect.bisect_left(soil_base[0], depth)
    return soil_base[1][weight]

weights = list(map(lambda x: get_weight_at_depth(soil_layers_database, x), layers))


def weight_of_layers(layers_ps, weights_ps):
    one_layer_weight = []
    for i in range(len(layers_ps)-1):
        stresses_1 = (layers_ps[i + 1] - layers_ps[i]) * weights_ps[i+1]
        one_layer_weight.append(round(stresses_1, 2))
    return one_layer_weight


def primary_stresses(layers_ps, one_layer_weight):
    stresses_11 = [0]
    for idx in range(1, len(layers_ps)):
        stresses_11.append(stresses_11[idx -1] + one_layer_weight[idx-1])
    return stresses_11


def get_modulus_at_depth(soil_base, depth):
    modulus = bisect.bisect_left(soil_base[0], depth)
    return soil_base[2][modulus], soil_base[3][modulus]

modules = list(map(lambda x: get_modulus_at_depth(soil_layers_database, x), layers))

print(modules)

