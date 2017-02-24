import funkcje
import plotly
import plotly.graph_objs as go
import database
from functools import reduce

L = float(input("L:"))
B = float(input("B:"))
z = reduce((lambda memo, current: memo + current), database.soil_layers_database[0], 0)
print(z)
excavation_depth = float(input("excavation depth:"))
depth_step = float(input("depth step:"))
evenly_distributed_load = float(input("q:"))


layers = funkcje.division_into_layers(excavation_depth, z, depth_step)
layers_after_leveling = funkcje.ground_levelling(excavation_depth, layers)
wspolczynnik_o = funkcje.center_point_method(L, B, layers_after_leveling )
wspolczynnik_n = funkcje.corner_point_method(L, B, layers_after_leveling )
z_stresses = funkcje.primary_stresses(layers)
excavation_stresses = funkcje.relief_stresses(excavation_depth, wspolczynnik_o)
load_stresses = funkcje.q_stresses(evenly_distributed_load, wspolczynnik_o)
zs_stresses = funkcje.zsecondary_stresses(evenly_distributed_load, excavation_depth, excavation_stresses, load_stresses)
zd_stresses = funkcje.zadditional_stresses(evenly_distributed_load, excavation_depth, load_stresses, zs_stresses)

#print("depth:", layers)
#print("levelled depth:",layers_after_leveling)
#print("z_stresses:", z_stresses)
#print("excavation_stresses:", excavation_stresses)
#print("load_stresses:", load_stresses)
#print("zs_stresses:", zs_stresses)
#print("zd_stresses", zd_stresses)



