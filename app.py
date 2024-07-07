from flask import Flask, render_template, request
import os
from data_processing import (
    load_data, filter_data, create_memory_usage_plot, create_assembly_state_plot, 
    create_timer_state_plot, create_network_state_plot, 
    generate_stepwise_memory_usage_plots, generate_stepwise_assembly_state_plots, 
    generate_stepwise_timer_state_plots, generate_stepwise_network_state_plots,
generate_memory_usage_line_plot, generate_assembly_state_line_plot,
generate_timer_state_line_plot,generate_network_state_line_plot,
convert_bytes_to_mb
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

    # Debug print statements
    print(f"Step type: {step_type}")
    for category, plots in stepwise_plots.items():
        for step, plot in plots.items():
            print(f"Category: {category}, Step: {step}, Plot: {plot[:30]}...")

    return render_template('stepwise_analysis.html', 
                           step_type=step_type,
                           stepwise_plots=stepwise_plots)

@app.route('/baseline_analysis/<baseline>', methods=['GET'])
def baseline_analysis(baseline):
    folder_path = os.path.join(app.root_path, 'static', 'all_json_files')
    df = load_data(folder_path)

    baseline_df = df[df['Baseline'] == baseline]

    # Convert memory-related columns to MB
    memory_columns = [
        'BytesPerObject', 'BytesInUse', 'MaxBytesInUse', 'BytesFromOS',
        'BytesForRollbackInUse', 'OSBytesForRollback'
    ]
    baseline_df = convert_bytes_to_mb(baseline_df, memory_columns)

    # Create memory usage plot
    memory_plot = generate_memory_usage_line_plot(baseline_df)

    # Similarly create assembly state, timer state, and network state plots
    assembly_plot = generate_assembly_state_line_plot(baseline_df)
    timer_plot = generate_timer_state_line_plot(baseline_df)
    network_plot = generate_network_state_line_plot(baseline_df)

    return render_template('baseline_analysis.html',
                           baseline=baseline,
                           memory_plot=memory_plot,
                           assembly_plot=assembly_plot,
                           timer_plot=timer_plot,
                           network_plot=network_plot)


if __name__ == '__main__':
    app.run(debug=True)


