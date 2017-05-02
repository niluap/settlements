import funkcje
import plotly.plotly as py
import plotly.graph_objs as go
import database
import copy


'''
#Dane wyjściowe - wpisywane przez użytkowanika
L = rest_api.L_from_api #10 float(input("L:"))
B = rest_api.B_from_api #2 float(input("B:"))
excavation_depth = excavation_depth_from_api #1.1 float(input("excavation depth:"))
evenly_distributed_load = evenly_distributed_load_from_api #100 float(input("q:"))'''


def compute_settlements(L, B, excavation_depth, evenly_distributed_load):
    z = round(database.soil_layers_data[0][-1], 2)
    # Prawdopodobnie depth_step bedzie na stałe ustalone na 0.01. Ułatwi to podziął na warstwy + dokłądnosc wyników
    depth_step = 0.01 #float(input("depth step:"))

    soil_layers_database = database.soil_layers_data
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


    #ZASIĘG ZLICZANIA OSIADAŃ
    z_max = layers[funkcje.settlement_scope(z_stresses, zd_stresses, layers)]
    z_max_index = funkcje.settlement_scope(z_stresses, zd_stresses, layers)
    #print("Głębokość sumowania osiadań poszczególnych warstewek:{0}m".format(z_max))


    #POMOCNICZNA LISTA GLEBOKOSCI DO OSIADAN
    layers_for_settelments = layers[0:z_max_index+1]


    #OSIADANIA W ZAKRESI NAPREZEN WTORNYCH
    secondary_modules = list(map(lambda x: funkcje.get_secondary_modulus_at_depth(soil_layers_database, x),
                                 layers_for_settelments))

    secondary_settlements = 0
    for i in range(len(layers_for_settelments)):
        S_secondary = zs_stresses[i]*depth_step/secondary_modules[i]
        secondary_settlements += S_secondary
    #print("Osiadania w zakresie naprężeń wtórnych:{0}mm".format(round(secondary_settlements, 2)))

    #OSIADANIA W ZAKRESIE NAPREZEN PIEROWTNYCH
    primary_modules = list(map(lambda x: funkcje.get_primary_modulus_at_depth(soil_layers_database, x),
                               layers_for_settelments))
    primary_settlements = 0
    for i in range(len(layers_for_settelments)):
        S_primary = zd_stresses[i]*0.01/primary_modules[i]
        primary_settlements += S_primary
    #print("Osiadania w zakresie naprężeń pierowntych:{0}mm".format(round(primary_settlements, 2)))

    return z_max, round(secondary_settlements, 2), round(primary_settlements, 2)


'''
print("Całkowite osiadanie na głebokości {0}m wynosi {1}mm".format(z_max, \
                                                                   round(secondary_settlements + primary_settlements,
                                                                         2)))
'''
'''
#!!!!WYKRESY!!!!
minus_one = -1
depth = []
for i in layers:
    C = float(i * float(minus_one))
    depth.append(C)

napr_pion_0_3 = []
for i in z_stresses:
   item= 0.3*i*minus_one
   napr_pion_0_3.append(item)


dodatkowe_stresses = []
for i in zd_stresses:
    D = float(i * float(minus_one))
    dodatkowe_stresses.append(D)

excavation_line = go.Scatter(
    name='Excavation depth',
    x=[-100, 100],
    y=[depth[0], depth[0]],
    fill='None',
    line=dict(color='rgb(255, 87, 51)'))

settelments_line = go.Scatter(
    name='Maximum settelment depth',
    x=[-100, 100],
    y=[z_max*-1, z_max*-1],
    fill='None',
    line=dict(color='rgb(144, 12, 63)'))

naprezenia_pionowe = go.Scatter(
    name='Vertical Stresses',
    x=z_stresses,
    y=depth,
    fill='tozerox',
    line=dict(color='rgb(143, 19, 131)'))

naprezenia_pionowe_0_3 = go.Scatter(
    name='1/3 of Vertical Stresses',
    x=napr_pion_0_3,
    y=depth,
    fill='tozerox',
    line=dict(color='rgb(215, 48, 66)'))

odprezenie = go.Scatter(
    name='Stresses caused by excavation',
    x=excavation_stresses,
    y=depth,
    fill='tozerox',
    line=dict(color='rgb(0, 164, 0)'))

obciazenie = go.Scatter(
    name='Stresses from external loads',
    x=dodatkowe_stresses,
    y=depth,
    fill='tozerox',
    line=dict(color='rgb(255, 204, 0)'))

layout = dict(title='STRESSES UNDER FOUNDATION',
              xaxis=dict(title = 'Stresses (kPa)'),
              yaxis=dict(title = 'Depth (m)'),
              )
data = [naprezenia_pionowe, odprezenie, obciazenie, excavation_line, naprezenia_pionowe_0_3, settelments_line]
py.plot(data, filename='napr_1.html')
'''
