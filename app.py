
# from flask import Flask, render_template, request
# import os
# from data_processing import load_data, filter_data, create_memory_usage_plot, create_assembly_state_plot, create_timer_state_plot, create_network_state_plot, generate_stepwise_plots

# app = Flask(__name__)

# @app.route('/', methods=['GET', 'POST'])
# def home():
#     folder_path = os.path.join(app.root_path, 'static', 'all_json_files')
#     df = load_data(folder_path)

#     baselines = df['Baseline'].unique()
#     steps = df['StepId'].unique()
#     selected_baselines = request.form.getlist('baselines')

#     filtered_df = filter_data(df, selected_baselines)

#     plot_memory_usage = create_memory_usage_plot(filtered_df)
#     plot_assembly_state = create_assembly_state_plot(filtered_df)
#     plot_timer_state = create_timer_state_plot(filtered_df)
#     plot_network_state = create_network_state_plot(filtered_df)

#     stepwise_plots = {}

#     if request.method == 'POST':
#         selected_steps = request.form.getlist('steps')
#         stepwise_plots = generate_stepwise_plots(df, selected_steps)

#     return render_template('home.html', 
#                            baselines=baselines,
#                            steps=steps,
#                            selected_baselines=selected_baselines,
#                            plot_memory_usage=plot_memory_usage, 
#                            plot_assembly_state=plot_assembly_state, 
#                            plot_timer_state=plot_timer_state, 
#                            plot_network_state=plot_network_state,
#                            stepwise_plots=stepwise_plots)

# @app.route('/plot/<plot_type>')
# def plot(plot_type):
#     folder_path = os.path.join(app.root_path, 'static', 'all_json_files')
#     df = load_data(folder_path)

#     if plot_type == 'memory_usage':
#         plot_img = create_memory_usage_plot(df)
#         title = 'Memory Usage by Baseline and Step'
#     elif plot_type == 'assembly_state':
#         plot_img = create_assembly_state_plot(df)
#         title = 'Assembly State by Baseline and Step'
#     elif plot_type == 'timer_state':
#         plot_img = create_timer_state_plot(df)
#         title = 'Timer State by Baseline and Step'
#     elif plot_type == 'network_state':
#         plot_img = create_network_state_plot(df)
#         title = 'Network State by Baseline and Step'
#     else:
#         return "Plot type not found", 404

#     return render_template('plot.html', plot_img=plot_img, title=title)

# @app.route('/stepwise_analysis', methods=['POST'])
# def stepwise_analysis():
#     folder_path = os.path.join(app.root_path, 'static', 'all_json_files')
#     df = load_data(folder_path)
    
#     selected_steps = request.form.getlist('steps')
#     stepwise_plots = generate_stepwise_plots(df, selected_steps)

#     return render_template('plot.html', 
#                            stepwise_plots=stepwise_plots)
# if __name__ == '__main__':
#     app.run(debug=True)




from flask import Flask, render_template, request
import os
from data_processing import (
    load_data, filter_data, create_memory_usage_plot, create_assembly_state_plot, 
    create_timer_state_plot, create_network_state_plot, 
    generate_stepwise_memory_usage_plots, generate_stepwise_assembly_state_plots, 
    generate_stepwise_timer_state_plots, generate_stepwise_network_state_plots
)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    folder_path = os.path.join(app.root_path, 'static', 'all_json_files')
    df = load_data(folder_path)

    baselines = df['Baseline'].unique()
    steps = df['StepId'].unique()
    selected_baselines = request.form.getlist('baselines')

    filtered_df = filter_data(df, selected_baselines)

    plot_memory_usage = create_memory_usage_plot(filtered_df)
    plot_assembly_state = create_assembly_state_plot(filtered_df)
    plot_timer_state = create_timer_state_plot(filtered_df)
    plot_network_state = create_network_state_plot(filtered_df)

    return render_template('home.html', 
                           baselines=baselines,
                           steps=steps,
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

# @app.route('/stepwise_analysis/<step_type>', methods=['GET'])
# def stepwise_analysis(step_type):
#     folder_path = os.path.join(app.root_path, 'static', 'all_json_files')
#     df = load_data(folder_path)

#     selected_steps = [step_type]
#     if step_type == '0_LoadAssembly':
#         stepwise_plots = generate_stepwise_memory_usage_plots(df, selected_steps)
#     elif step_type == '1_OffsetRegionCommand':
#         stepwise_plots = generate_stepwise_assembly_state_plots(df, selected_steps)
#     elif step_type == '2_LoadS350BlockFully':
#         stepwise_plots = generate_stepwise_timer_state_plots(df, selected_steps)
#     elif step_type == '3_MakeS350BlockWorkPart':
#         stepwise_plots = generate_stepwise_network_state_plots(df, selected_steps)
#     else:
#         return "Step type not found", 404

#     return render_template('stepwise_analysis.html', 
#                            step_type=step_type,
#                            stepwise_plots=stepwise_plots)

@app.route('/stepwise_analysis/<step_type>', methods=['GET'])
def stepwise_analysis(step_type):
    folder_path = os.path.join(app.root_path, 'static', 'all_json_files')
    df = load_data(folder_path)

    selected_steps = [step_type]

    memory_plots = generate_stepwise_memory_usage_plots(df, selected_steps)
    assembly_plots = generate_stepwise_assembly_state_plots(df, selected_steps)
    timer_plots = generate_stepwise_timer_state_plots(df, selected_steps)
    network_plots = generate_stepwise_network_state_plots(df, selected_steps)

    # Combine all plots into a single dictionary
    stepwise_plots = {
        "Memory Usage": memory_plots,
        "Assembly State": assembly_plots,
        "Timer State": timer_plots,
        "Network State": network_plots
    }

    return render_template('stepwise_analysis.html', 
                           step_type=step_type,
                           stepwise_plots=stepwise_plots)




if __name__ == '__main__':
    app.run(debug=True)


