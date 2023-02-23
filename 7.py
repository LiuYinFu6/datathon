import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd

# 加载数据
df_selected = pd.read_csv('C:/Users/yinfu/Desktop/FilesCSVFormat/Myselected.csv')
df_movement = pd.read_csv('C:/Users/yinfu/Desktop/FilesCSVFormat/Movement.csv')
df_generated = pd.read_csv('C:/Users/yinfu/Desktop/FilesCSVFormat/Generated.csv')
# 获取所有图像的URL
image_urls = df_selected['image_url'].tolist()

# 创建应用程序
app = dash.Dash(__name__)

# 创建布局
app.layout = html.Div([
    html.Div([
        html.H2('Select an image'),
        html.Div([
            html.Div([
                html.Img(src=url, style={'height': '300px'}),
                html.Button('Select', id={'type': 'select-button', 'url': url})
            ]) for url in image_urls
        ]),
        dcc.Store(id='selected-image-store'),
        html.Div(id='name-selection'),
        html.Button('Submit', id='submit-button'),
        html.Div([
            html.H2('Generated Image'),
            html.Img(id='generated-image')
        ])
    ]),
    html.Div([
        html.H2('Select a name'),
        dcc.Dropdown(
            id='name-dropdown',
            options=[{'label': name, 'value': name} for name in df_movement['name'].unique()]
        )
    ])
])

# 回调函数1：保存选择的图像
@app.callback(Output('selected-image-store', 'data'),
              [Input({'type': 'select-button', 'url': ALL}, 'n_clicks')],
              [State('selected-image-store', 'data')])
def save_image_selection(n_clicks_list, selected_image):
    # 获取被点击的按钮的URL
    clicked_url = [p['url'] for p in dash.callback_context.triggered][0]
    # 如果该URL的按钮被点击，则返回URL；否则返回None
    selected_url = clicked_url if any(n_clicks_list) else None
    return selected_url

# 回调函数2：显示所选图像的名称
@app.callback(Output('name-selection', 'children'),
              [Input('selected-image-store', 'data')],
              [State('selected-image-store', 'data_previous')])
def show_name(selected_image, previous_image):
    if selected_image and selected_image != previous_image:
        # 获取选择图像的名称
        selected_name = df_selected.loc[df_selected['image_url'] == selected_image, 'name'].iloc[0]
        return html.H3(f'Selected Name: {selected_name}')
    return ''

# 回调函数3：随机显示一个生成的图像
@app.callback(Output('generated-image', 'src'),
              [Input('submit-button', 'n_clicks')],
              [State('selected-image-store', 'data'),
               State('name-dropdown', 'value')])
def update_generated_image(n_clicks, selected_image, selected_name):
    if n_clicks and selected_image:
        # 获取所有与所选名称匹配的行
        df_matching_names = df_movement.loc[df_movement['name'] == selected_name]
        # 从匹配行中随机选择一行
        selected_row = df_matching_names.sample()
        # 获取选择行的图像URL
        generated_url = df_generated.loc[selected_row.index[0], 'image_url']
        return generated_url

if __name__ == '__main__':
    app.run_server(debug=True)