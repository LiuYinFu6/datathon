import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd

# 加载数据
#df_selected = pd.read_csv('C:/Users/yinfu/Desktop/FilesCSVFormat/Myselected.csv')
#df_movement = pd.read_csv('C:/Users/yinfu/Desktop/FilesCSVFormat/Movement.csv')
#df_generated = pd.read_csv('C:/Users/yinfu/Desktop/FilesCSVFormat/Generated.csv')

df_selected = pd.read_csv('https://raw.githubusercontent.com/LiuYinFu6/datathon/main/Myselected.csv')
df_movement = pd.read_csv('https://raw.githubusercontent.com/LiuYinFu6/datathon/main/Movement.csv')
df_generated = pd.read_csv('https://raw.githubusercontent.com/LiuYinFu6/datathon/main/Generated.csv')
# 获取所有图像的URL
image_urls = df_selected['image_url'].tolist()

# 创建应用程序
app = dash.Dash(__name__)

# 创建布局
app.layout = html.Div([
    html.Div([
        html.H2('Select an image'),
        html.Div([
            html.Img(src=url, style={'height': '300px'}) for url in image_urls
        ]),
        dcc.RadioItems(
            id='image-radio',
            options=[{'label': url, 'value': url} for url in image_urls],
            labelStyle={'display': 'block'}
        )
    ]),
    html.Div([
        html.H2('Select a name'),
        dcc.Dropdown(
            id='name-dropdown',
            options=[{'label': name, 'value': name} for name in df_movement['name'].unique()]
        )
    ]),
    html.Button('Submit', id='submit-button'),
    html.Div([
        html.H2('Generated Image'),
        html.Img(id='generated-image')
    ])
])

# 回调函数1：更新图像
@app.callback(Output('selected-image', 'src'),
              [Input('image-radio', 'value')])
def update_image(image_url):
    return image_url

# 回调函数2：保存选择的名字
@app.callback(Output('name-selection', 'children'),
              [Input('name-dropdown', 'value')])
def save_name(name):
    return name

# 回调函数3：随机显示一个生成的图像
@app.callback(Output('generated-image', 'src'),
              [Input('submit-button', 'n_clicks')],
              [State('image-radio', 'value'),
               State('name-dropdown', 'value')])
def update_generated_image(n_clicks, selected_image, selected_name):
    if n_clicks:
        # 获取所有与所选名称匹配的行
        df_matching_names = df_movement.loc[df_movement['name'] == selected_name]
        # 从匹配行中随机选择一行
        selected_row = df_matching_names.sample()
        # 获取选择行的图像URL
        generated_url = df_generated.loc[selected_row.index[0], 'image_url']
        return generated_url
    return None

# 运行应用程序
if __name__ == '__main__':
    app.run_server(debug=True)
