import funkcje
import plotly.plotly as py
#import plotly.graph_objs as go
import copy


'''
soil_layers_data - layout:
[[soil layer depth], [soil unit weight], [primary modulus of compressibility], [secondary modulus of compressibility]]
'''


def compute_settlements(L, B, excavation_depth, evenly_distributed_load, soil_layers_data):
    z = round(soil_layers_data[0][-1], 2)
    depth_step = 0.01 
    soil_layers_database = soil_layers_data
    layers = funkcje.division_into_layers(soil_layers_database, depth_step, excavation_depth)
    layers_with_zero = copy.copy(layers)
    layers_with_zero.insert(0, 0)
    layers_after_leveling = funkcje.ground_levelling(excavation_depth, layers)
    weights = list(map(lambda x: funkcje.get_weight_at_depth(soil_layers_database, x), layers_with_zero))
    weight_of_one_layer = funkcje.weight_of_layers(layers_with_zero, weights)


    z_stresses = funkcje.primary_stresses(layers_with_zero, weight_of_one_layer)
    wspolczynnik_o = funkcje.center_point_method(L, B, layers_after_leveling)
    wspolczynnik_n = funkcje.corner_point_method(L, B, layers_after_leveling)
    excavation_stresses = funkcje.relief_stresses(excavation_depth, wspolczynnik_o, weights, layers_with_zero)
    load_stresses = funkcje.q_stresses(evenly_distributed_load, wspolczynnik_o)
    zs_stresses = funkcje.zsecondary_stresses(evenly_distributed_load, excavation_stresses, load_stresses)
    zd_stresses = funkcje.zadditional_stresses(evenly_distributed_load, load_stresses, zs_stresses, excavation_stresses)


    #RANGE OF COMPUTING SETTLEMENTS
    z_max = layers[funkcje.settlement_scope(z_stresses, zd_stresses, layers)]
    z_max_index = funkcje.settlement_scope(z_stresses, zd_stresses, layers)
    #print("Głębokość sumowania osiadań poszczególnych warstewek:{0}m".format(z_max))


    #AUXILIARY ARRAY FOR COMPUTING SETTLEMENTS
    layers_for_settelments = layers[0:z_max_index+1]


    #SETTLEMENTS CAUSED BY SECONDARY STRESSES
    secondary_modules = list(map(lambda x: funkcje.get_secondary_modulus_at_depth(soil_layers_database, x),
                                 layers_for_settelments))

    secondary_settlements = 0
    for i in range(len(layers_for_settelments)):
        S_secondary = zs_stresses[i]*depth_step/secondary_modules[i]
        secondary_settlements += S_secondary

    #SETTLEMENTS CAUSED BY PRIMARY STRESSES
    primary_modules = list(map(lambda x: funkcje.get_primary_modulus_at_depth(soil_layers_database, x),
                               layers_for_settelments))
    primary_settlements = 0
    for i in range(len(layers_for_settelments)):
        S_primary = zd_stresses[i]*0.01/primary_modules[i]
        primary_settlements += S_primary

    #DATA FOR PLOTS
    depth = []
    for i in layers:
        C = float(i * float(-1))
        depth.append(C)
    vertical_stresses = z_stresses[1:]

    return z_max, round(secondary_settlements, 2), round(primary_settlements, 2), depth, vertical_stresses, excavation_stresses, zd_stresses