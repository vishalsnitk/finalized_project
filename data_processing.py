
import os
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import base64


def load_data(folder_path):
    all_data = []

    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r') as file:
                data = json.load(file)
                environment = data.get('Environment', {})
                environment_label = environment.get('Environment', {}).get(
                    'Group', 'Unknown')
                steps = data.get('StepDetails', [])
                for step in steps:
                    step_id = step.get('StepId', '')
                    memory_state = step.get('MemoryState', {})
                    assembly_state = step.get('AssemblyState', {}).get(
                        'Assembly Structure Details', {})
                    timer_state = step.get('TimerState',
                                           {}).get('Timer Stats', {})
                    network_state = step.get('NetworkState',
                                             {}).get('NetworkCount', {})

                    all_data.append({
                        'Baseline':
                        environment_label,
                        'StepId':
                        step_id,
                        'BytesPerObject':
                        memory_state.get('Bytes per Object', 0),
                        'BytesInUse':
                        memory_state.get('Bytes in use', 0),
                        'MaxBytesInUse':
                        memory_state.get('Max bytes in use', 0),
                        'BytesFromOS':
                        memory_state.get('Bytes from OS', 0),
                        'BytesForRollbackInUse':
                        memory_state.get('Bytes for Rollback in use', 0),
                        'OSBytesForRollback':
                        memory_state.get('OS Bytes for Rollback', 0),
                        'Number of Fully Loaded Parts':
                        assembly_state.get('Number of Fully Loaded Parts', 0),
                        'Number of Partially Loaded Parts':
                        assembly_state.get('Number of Partially Loaded Parts',
                                           0),
                        'Number of Minimally Loaded Parts':
                        assembly_state.get('Number of Minimally Loaded Parts',
                                           0),
                        'Time required to perform an operation':
                        timer_state.get(
                            'Time required to perform an operation', 0),
                        'NumSoaCalls':
                        network_state.get('NumSoaCalls', 0),
                        'NumPdiCalls':
                        network_state.get('NumPdiCalls', 0),
                        'NumFccCalls':
                        network_state.get('NumFccCalls', 0)
                    })

    df = pd.DataFrame(all_data)
    return df


def filter_data(df, baselines):
    if not baselines:
        return df
    return df[df['Baseline'].isin(baselines)]


def create_plot(df, columns, ylabel, title):
    baselines = df['Baseline'].unique()
    steps = df['StepId'].unique()

    fig, ax = plt.subplots(figsize=(18, 8))
    bar_width = 0.15
    bar_spacing = 0.05
    group_spacing = 0.5
    group_width = bar_width * len(steps) + bar_spacing * (len(steps) -
                                                          1) + group_spacing
    group_positions = np.arange(len(baselines)) * group_width
    colors = plt.cm.tab10(np.linspace(0, 1, len(columns)))

    for i, step in enumerate(steps):
        step_data = df[df['StepId'] == step]
        bar_positions = group_positions + i * (bar_width + bar_spacing)
        bottoms = np.zeros(len(baselines))

        for j, column in enumerate(columns):
            ax.bar(bar_positions,
                   step_data[column],
                   bar_width,
                   bottom=bottoms,
                   color=colors[j],
                   label=f'{column}' if i == 0 else "")
            bottoms += step_data[column]

    ax.set_xlabel('Baseline')
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.set_xticks(group_positions + (group_width - group_spacing) / 2 -
                  bar_width / 2)
    ax.set_xticklabels(baselines, rotation=45, ha='right')
    ax.legend(title=f'{ylabel} Metrics',
              bbox_to_anchor=(1.05, 1),
              loc='upper left')
    plt.tight_layout()

    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    return img_base64



def generate_stepwise_plots(df, selected_steps):
    memory_columns = ['BytesPerObject', 'BytesInUse', 'MaxBytesInUse', 'BytesFromOS', 'BytesForRollbackInUse', 'OSBytesForRollback']
    stepwise_plots = {}
    for step in selected_steps:
        step_data = df[df['StepId'] == step]
        fig, ax = plt.subplots(figsize=(10, 5))
        for column in memory_columns:
            ax.plot(step_data['Baseline'], step_data[column], marker='o', label=column)
        ax.set_title(f'Step: {step}')
        ax.set_xlabel('Baseline')
        ax.set_ylabel('Memory Usage (bytes)')
        ax.legend()
        ax.tick_params(axis='x', rotation=45)
        ax.grid(True)
        stepwise_plots[step] = plot_to_base64(fig)
        plt.close(fig)
    return stepwise_plots


def create_memory_usage_plot(df):
    columns = [
        'BytesPerObject', 'BytesInUse', 'MaxBytesInUse', 'BytesFromOS',
        'BytesForRollbackInUse', 'OSBytesForRollback'
    ]
    return create_plot(
        df, columns, 'Memory Usage (bytes)',
        'Clustered Stacked Bar Chart of Memory Usage by Baseline and Step')


def create_assembly_state_plot(df):
    columns = [
        'Number of Fully Loaded Parts', 'Number of Partially Loaded Parts',
        'Number of Minimally Loaded Parts'
    ]
    return create_plot(
        df, columns, 'Number of Parts',
        'Clustered Stacked Bar Chart of Assembly State by Baseline and Step')


def create_timer_state_plot(df):
    columns = ['Time required to perform an operation']
    return create_plot(
        df, columns, 'Time (seconds)',
        'Clustered Stacked Bar Chart of Timer State by Baseline and Step')


def create_network_state_plot(df):
    columns = ['NumSoaCalls', 'NumPdiCalls', 'NumFccCalls']
    return create_plot(
        df, columns, 'Number of Calls',
        'Clustered Stacked Bar Chart of Network State by Baseline and Step')

