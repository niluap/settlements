import math
import bisect
import copy


def division_into_layers(soil_layers_database, depth_step, excavation_depth):
    layers_depth = copy.copy(soil_layers_database[0])
    layers_depth.insert(0, excavation_depth)
    #print(layers_depth)
    layer_range = int(float(layers_depth[-1])/float(depth_step) + 1.0)
    steps = []
    for j in range(len(layers_depth)-1):
        for i in range(layer_range):
            if float(layers_depth[j]) <= float(depth_step*i) <= float(layers_depth[j+1]):
                steps.append(round(depth_step*i, 2))
    return steps


def ground_levelling(excavation_depth, layers_after_leveling):
    layers_for_center_and_point_method = []
    for i in layers_after_leveling:
        levelling = float(i) - float(excavation_depth)
        layers_for_center_and_point_method.append(round(levelling, 2))
    return layers_for_center_and_point_method


def center_point_method(L, B, layers_after_leveling):
    etta_center_point = []
    for i in layers_after_leveling:
        if float(i) == float(0.0):
            #global etta_o
            etta_o = float(1.0)
            etta_center_point.append(etta_o)
        else:
            m_cpm = float(L/B)
            n_cpm = float(float(i)/B)
            cpm_part_1 = float(math.atan(m_cpm/(2*n_cpm*math.sqrt(1 + m_cpm**2 + 4*n_cpm**2))))
            cpm_part_2 = float(2*m_cpm*n_cpm/math.sqrt(1 + m_cpm**2 + 4*n_cpm**2))
            cpm_part_3 = float(1/(1+4*n_cpm**2) + (1/(m_cpm**2 + 4*n_cpm**2)))
            etta_o = float((2/math.pi) * (cpm_part_1 + cpm_part_2*cpm_part_3))
            #print("for {0} m depth, etta_o is equal to: {1}".format(i, etta_o))
            etta_center_point.append(etta_o)
    return etta_center_point


def corner_point_method(L, B, layers_after_leveling):
    etta_corner_point = []
    for i in layers_after_leveling:
        if float(i) == float(0.0):
            etta_n = float(1.0)
            etta_corner_point.append(etta_n)
        else:
            m_copm = float(L/B)
            n_copm = float(float(i)/B)
            copm_part_1 = float(math.atan(m_copm/(n_copm*math.sqrt(1 + m_copm**2 + n_copm**2))))
            copm_part_2 = float(m_copm*n_copm/math.sqrt(1 + m_copm**2 + n_copm**2))
            copm_part_3 = float(1/(1 + n_copm**2) + (1/(m_copm**2 + n_copm**2)))
            etta_n = float((1/(2*math.pi)) * (copm_part_1 + copm_part_2*copm_part_3))
            #print("for {0} m depth, etta_n is equal to: {1}".format(i, etta_n))
            etta_corner_point.append(etta_n)
    return etta_corner_point


def get_weight_at_depth(soil_base, depth):
    weight_index = bisect.bisect_left(soil_base[0], depth)
    return soil_base[1][weight_index]


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

'''
def relief_stresses(excavation_depth, wspolczynnik_o):
    stresses_22 = []
    for k in range(len(wspolczynnik_o)):
        stresses_2 = float(wspolczynnik_o[k]) * float(excavation_depth) * float(database.first_layer['unit weight'])
        stresses_22.append(stresses_2)
    #print(stresses_22)
    return stresses_22


def q_stresses(evenly_distributed_load, wspolczynnik_o):
    stresses_33 = []
    for k in range(len(wspolczynnik_o)):
        stresses_3 = float(wspolczynnik_o[k]) * float(evenly_distributed_load)
        stresses_33.append(stresses_3)
    #print(stresses_33)
    return stresses_33


def zsecondary_stresses(evenly_distributed_load, excavation_depth, excavation_stresses, load_stresses):
    secondary_stresses = []
    for i in range(len(excavation_stresses)):
        if float(evenly_distributed_load) > float(excavation_depth) * float(database.first_layer['unit weight']):
            secondary_stress = float(excavation_stresses[i])
        else:
            secondary_stress = float(load_stresses[i])
        secondary_stresses.append(secondary_stress)
    #print(secondary_stresses)
    return secondary_stresses


def zadditional_stresses(evenly_distributed_load, excavation_depth, load_stresses, zs_stresses):
    additional_stresses = []
    for i in range(len(zs_stresses)):
        if float(evenly_distributed_load) > float(excavation_depth) * float(database.first_layer['unit weight']):
            additional_stress = float(load_stresses[i]) - float(zs_stresses[i])
        else:
            additional_stress = i*0
        additional_stresses.append(additional_stress)
    return additional_stresses
'''





