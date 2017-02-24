import plotly
import plotly.graph_objs as go

trace1 = go.Scatter(
    x=[1, 2, 3, 4],
    y=[0, 2, 3, 5],
    fill='tozeroy')

trace2 = go.Scatter(
    x=[1, 2, 3, 4],
    y=[3, 5, 1, 7],
    fill='tonexty')

data = [trace1, trace2]
plotly.offline.plot(data, filename='basic-area.html')







#########################################

minus_one = -1

depth = []
for i in layers:
    C = float(i * float(minus_one))
    depth.append(C)

dodatkowe_stresses = []
for i in zd_stresses:
    D = float(i * float(minus_one))
    dodatkowe_stresses.append(D)

excavation_line = go.Scatter(
    x=[dodatkowe_stresses[0], zd_stresses[0]],
    y=[depth[0], depth[0]],
    fill='None',
    line=dict(color='rgb(0, 0, 0)'))

naprezenia_pionowe = go.Scatter(
    x=z_stresses,
    y=depth,
    fill='tozerox',
    line=dict(color='rgb(143, 19, 131)'))

odprezenie = go.Scatter(
    x=excavation_stresses,
    y=depth,
    fill='tozerox',
    line=dict(color='rgb(0, 164, 0)'))

obciazenie = go.Scatter(
    x=dodatkowe_stresses,
    y=depth,
    fill='tozerox',
    line=dict(color='rgb(255, 204, 0)'))

data = [naprezenia_pionowe, excavation_line, odprezenie, obciazenie]
plotly.offline.plot(data, filename='napr_1.html')




