import funkcje
import plotly
import plotly.graph_objs as go
import database
import copy
from functools import reduce

L = 10 #float(input("L:"))
B = 2 #float(input("B:"))
z = round(database.soil_layers_data[0][-1], 2)
excavation_depth = 1.1 #float(input("excavation depth:"))
depth_step = 0.1 #float(input("depth step:"))
evenly_distributed_load = 31 #float(input("q:"))
soil_layers_database = database.soil_layers_data
layers = funkcje.division_into_layers(soil_layers_database, depth_step, excavation_depth)
layers_with_zero = copy.copy(layers)
layers_with_zero.insert(0, 0)

layers_after_leveling = funkcje.ground_levelling(excavation_depth, layers)
weights = list(map(lambda x: funkcje.get_weight_at_depth(soil_layers_database, x), layers_with_zero))
weight_of_one_layer = funkcje.weight_of_layers(layers_with_zero, weights)

print(len(layers_with_zero))
print(len(weights))
print(len(weight_of_one_layer))

z_stresses = funkcje.primary_stresses(layers_with_zero, weight_of_one_layer)
print(len(z_stresses))



'''
wspolczynnik_o = funkcje.center_point_method(L, B, layers_after_leveling )
wspolczynnik_n = funkcje.corner_point_method(L, B, layers_after_leveling )
)
excavation_stresses = funkcje.relief_stresses(excavation_depth, wspolczynnik_o)
load_stresses = funkcje.q_stresses(evenly_distributed_load, wspolczynnik_o)
zs_stresses = funkcje.zsecondary_stresses(evenly_distributed_load, excavation_depth, excavation_stresses, load_stresses)
zd_stresses = funkcje.zadditional_stresses(evenly_distributed_load, excavation_depth, load_stresses, zs_stresses)'''

#print("depth:", layers)
#print("levelled depth:",layers_after_leveling)
#print("weights of layers:", weights)
#print("z_stresses:", z_stresses)
#print("excavation_stresses:", excavation_stresses)
#print("load_stresses:", load_stresses)
#print("zs_stresses:", zs_stresses)
#print("zd_stresses", zd_stresses)


minus_one = -1

depth = []
for i in layers_with_zero:
    C = float(i * float(minus_one))
    depth.append(C)

naprezenia_pionowe = go.Scatter(
    x=z_stresses,
    y=depth,
    fill='tozerox',
    line=dict(color='rgb(143, 19, 131)'))


data = [naprezenia_pionowe]
plotly.offline.plot(data, filename='napr_1.html')

