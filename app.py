

# from flask import Flask, render_template, jsonify
# import os
# from data_processing import load_data, create_memory_usage_plot, create_assembly_state_plot, create_timer_state_plot, create_network_state_plot

# app = Flask(__name__)

# @app.route('/')
# def home():
#     folder_path = os.path.join(app.root_path, 'static', 'all_json_files')
#     df = load_data(folder_path)

#     plot_memory_usage = create_memory_usage_plot(df)
#     plot_assembly_state = create_assembly_state_plot(df)
#     plot_timer_state = create_timer_state_plot(df)
#     plot_network_state = create_network_state_plot(df)

#     return render_template('home.html', 
#                            plot_memory_usage=plot_memory_usage, 
#                            plot_assembly_state=plot_assembly_state, 
#                            plot_timer_state=plot_timer_state, 
#                            plot_network_state=plot_network_state)

# if __name__ == '__main__':
#     app.run(debug=True)


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

    return render_template('home.html', 
                           baselines=baselines,
                           selected_baselines=selected_baselines,
                           plot_memory_usage=plot_memory_usage, 
                           plot_assembly_state=plot_assembly_state, 
                           plot_timer_state=plot_timer_state, 
                           plot_network_state=plot_network_state)

if __name__ == '__main__':
    app.run(debug=True)
