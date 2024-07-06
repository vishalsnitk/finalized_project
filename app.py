from flask import Flask, render_template, request
import os
from data_processing import load_data, filter_data, create_memory_usage_plot, create_assembly_state_plot, create_timer_state_plot, create_network_state_plot

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    folder_path = os.path.join(app.root_path, 'static', 'all_json_files')
    df = load_data(folder_path)

    baselines = df['Baseline'].unique()
    selected_baselines = request.form.getlist('baselines')

    filtered_df = filter_data(df, selected_baselines)

    plot_memory_usage = create_memory_usage_plot(filtered_df)
    plot_assembly_state = create_assembly_state_plot(filtered_df)
    plot_timer_state = create_timer_state_plot(filtered_df)
    plot_network_state = create_network_state_plot(filtered_df)

    stepwise_plots = {}

    if request.method == 'POST':
        selected_steps = request.form.getlist('steps')
        stepwise_plots = generate_stepwise_plots(df, selected_steps)

    return render_template('home.html', 
                           baselines=baselines,
                           selected_baselines=selected_baselines,
                           plot_memory_usage=plot_memory_usage, 
                           plot_assembly_state=plot_assembly_state, 
                           plot_timer_state=plot_timer_state, 
                           plot_network_state=plot_network_state)

@app.route('/plot/<plot_type>')
def plot(plot_type):
    folder_path = os.path.join(app.root_path, 'static', 'all_json_files')
    df = load_data(folder_path)

    if plot_type == 'memory_usage':
        plot_img = create_memory_usage_plot(df)
        title = 'Memory Usage by Baseline and Step'
    elif plot_type == 'assembly_state':
        plot_img = create_assembly_state_plot(df)
        title = 'Assembly State by Baseline and Step'
    elif plot_type == 'timer_state':
        plot_img = create_timer_state_plot(df)
        title = 'Timer State by Baseline and Step'
    elif plot_type == 'network_state':
        plot_img = create_network_state_plot(df)
        title = 'Network State by Baseline and Step'
    else:
        return "Plot type not found", 404

    return render_template('plot.html', plot_img=plot_img, title=title)

if __name__ == '__main__':
    app.run(debug=True)




# from flask import Flask, render_template, request
# import os
# import json
# import pandas as pd
# import numpy as np
# import base64
# from io import BytesIO
# import matplotlib.pyplot as plt

# app = Flask(__name__)

# def load_data(folder_path):
#     all_data = []
#     for filename in os.listdir(folder_path):
#         if filename.endswith('.json'):
#             file_path = os.path.join(folder_path, filename)
#             with open(file_path, 'r') as file:
#                 data = json.load(file)
#                 environment = data.get('Environment', {})
#                 environment_label = environment.get('Environment', {}).get('Group', 'Unknown')
#                 steps = data.get('StepDetails', [])
#                 for step in steps:
#                     step_id = step.get('StepId', '')
#                     memory_state = step.get('MemoryState', {})
#                     all_data.append({
#                         'Baseline': environment_label,
#                         'StepId': step_id,
#                         'BytesPerObject': memory_state.get('Bytes per Object', 0),
#                         'BytesInUse': memory_state.get('Bytes in use', 0),
#                         'MaxBytesInUse': memory_state.get('Max bytes in use', 0),
#                         'BytesFromOS': memory_state.get('Bytes from OS', 0),
#                         'BytesForRollbackInUse': memory_state.get('Bytes for Rollback in use', 0),
#                         'OSBytesForRollback': memory_state.get('OS Bytes for Rollback', 0)
#                     })
#     df = pd.DataFrame(all_data)
#     return df

# def create_memory_usage_plot(df):
#     columns = ['BytesPerObject', 'BytesInUse', 'MaxBytesInUse', 'BytesFromOS', 'BytesForRollbackInUse', 'OSBytesForRollback']
#     plot_data = []
#     baselines = df['Baseline'].unique()
#     steps = df['StepId'].unique()
#     for baseline in baselines:
#         for step in steps:
#             step_data = df[(df['Baseline'] == baseline) & (df['StepId'] == step)]
#             for column in columns:
#                 plot_data.append({
#                     'Baseline': baseline,
#                     'StepId': step,
#                     'Metric': column,
#                     'Value': int(step_data[column].values[0]) if not step_data.empty else 0
#                 })
#     return plot_data

# def plot_to_base64(fig):
#     buf = BytesIO()
#     fig.savefig(buf, format='png')
#     buf.seek(0)
#     return base64.b64encode(buf.read()).decode('utf-8')

# def generate_stepwise_plots(df, selected_steps):
#     memory_columns = ['BytesPerObject', 'BytesInUse', 'MaxBytesInUse', 'BytesFromOS', 'BytesForRollbackInUse', 'OSBytesForRollback']
#     stepwise_plots = {}
#     for step in selected_steps:
#         step_data = df[df['StepId'] == step]
#         fig, ax = plt.subplots(figsize=(10, 5))
#         for column in memory_columns:
#             ax.plot(step_data['Baseline'], step_data[column], marker='o', label=column)
#         ax.set_title(f'Step: {step}')
#         ax.set_xlabel('Baseline')
#         ax.set_ylabel('Memory Usage (bytes)')
#         ax.legend()
#         ax.tick_params(axis='x', rotation=45)
#         ax.grid(True)
#         stepwise_plots[step] = plot_to_base64(fig)
#         plt.close(fig)
#     return stepwise_plots

# @app.route('/', methods=['GET', 'POST'])
# def home():
#     folder_path = os.path.join(app.root_path, 'static', 'all_json_files')
#     df = load_data(folder_path)

#     baselines = df['Baseline'].unique()
#     steps = df['StepId'].unique()

#     plot_memory_usage = create_memory_usage_plot(df)
#     plot_assembly_state = None  # Placeholder for your other plots
#     plot_timer_state = None     # Placeholder for your other plots
#     plot_network_state = None   # Placeholder for your other plots

#     stepwise_plots = {}

#     if request.method == 'POST':
#         selected_steps = request.form.getlist('steps')
#         stepwise_plots = generate_stepwise_plots(df, selected_steps)

#     return render_template('home.html', 
#                            baselines=baselines,
#                            steps=steps,
#                            plot_memory_usage=plot_memory_usage, 
#                            plot_assembly_state=plot_assembly_state, 
#                            plot_timer_state=plot_timer_state, 
#                            plot_network_state=plot_network_state,
#                            stepwise_plots=stepwise_plots)

# if __name__ == '__main__':
#     app.run(debug=True)



