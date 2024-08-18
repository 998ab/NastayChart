import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from skimage import color
import numpy as np

# Определение словаря с данными о цветах
colors = [
    (84.8, 2.1, 16.8, 5),
    (84.3, 2.60, 17.40, 9),
    (75.1, 5.40, 23.1, 17),
    (61.1, 9.5, 30.4, 24),
    (54.40, 10.0, 30.5, 34),
    (49.9, 10.9, 30.8, 44),
    (48.0, 11.3, 30.6, 53),
    (49.5, 11.1, 31.0, 63),
    (51.5, 11.2, 32.1, 73),
    (55.6, 10.4, 32.1, 82),
    (58.1, 10.0, 31.4, 90),
    (61.9, 9.20, 31.7, 96),
]


# Функция для преобразования Lab в RGB
def lab_to_rgb(l, a, b):
    lab = np.array([[[l, a, b]]], dtype=np.float32)
    rgb = color.lab2rgb(lab)
    return rgb[0][0]


# Подготовка данных для графика
n_values = [color[3] for color in colors]
L_values = [color[0] for color in colors]
a_values = [color[1] for color in colors]
b_values = [color[2] for color in colors]

# Преобразование значений Lab в RGB для использования в графике
rgb_colors = ['rgb({},{},{})'.format(int(r * 255), int(g * 255), int(b * 255))
              for r, g, b in [lab_to_rgb(L, a, b) for L, a, b, _ in colors]]

# Создание Dash-приложения
app = dash.Dash(__name__)

# Определение макета приложения
app.layout = html.Div([
    dcc.Graph(id='lab-graph', config={'displayModeBar': False}),
    html.Div(id='color-square', style={
        'width': '100px',
        'height': '100px',
        'margin': '0 auto',
        'border': '1px solid black',
        'backgroundColor': 'rgb(255, 255, 255)'  # Белый цвет по умолчанию
    })
])


# Callback для обновления графика
@app.callback(
    Output('lab-graph', 'figure'),
    Input('lab-graph', 'hoverData'))
def update_graph(hoverData):
    fig = go.Figure()

    # Добавление линий для L, a и b
    fig.add_trace(go.Scatter(
        x=n_values,
        y=L_values,
        mode='markers+lines',
        name='L',
        marker=dict(
            color='blue',
            size=10,
        ),
        line=dict(color='blue'),
        textposition="top center",
        hoverinfo='text',
    ))

    fig.add_trace(go.Scatter(
        x=n_values,
        y=a_values,
        mode='markers+lines',
        name='a',
        marker=dict(
            color='green',
            size=10,
        ),
        line=dict(color='green'),
        textposition="top center",
        hoverinfo='text',
    ))

    fig.add_trace(go.Scatter(
        x=n_values,
        y=b_values,
        mode='markers+lines',
        name='b',
        marker=dict(
            color='red',
            size=10,
        ),
        line=dict(color='red'),
        textposition="top center",
        hoverinfo='text',
    ))

    # Настройка осей и макета
    fig.update_xaxes(title_text="n")
    fig.update_yaxes(title_text="Values")
    fig.update_layout(
        showlegend=True,
        height=600,
        width=600
    )

    return fig


# Callback для обновления цвета квадрата
@app.callback(
    Output('color-square', 'style'),
    Input('lab-graph', 'hoverData'))
def update_square_color(hoverData):
    if hoverData:
        point_index = hoverData['points'][0]['pointIndex']
        lab = colors[point_index]
        rgb_color = lab_to_rgb(*lab[:3])
        rgb_color_str = 'rgb({},{},{})'.format(int(rgb_color[0] * 255), int(rgb_color[1] * 255),
                                               int(rgb_color[2] * 255))
        return {
            'width': '100px',
            'height': '100px',
            'margin': '0 auto',
            'border': '1px solid black',
            'backgroundColor': rgb_color_str
        }
    else:
        return {
            'width': '100px',
            'height': '100px',
            'margin': '0 auto',
            'border': '1px solid black',
            'backgroundColor': 'rgb(255, 255, 255)'  # Белый цвет по умолчанию
        }


# Запуск приложения
if __name__ == '__main__':
    app.run_server(host="0.0.0.0", port=61100, debug=True)
