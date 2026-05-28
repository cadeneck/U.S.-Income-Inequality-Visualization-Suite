import pandas as pd
import matplotlib.pyplot as plt

# Define unique colors and markers for the inequality graph
inequality_colors = [
    '#1f77b4',
    '#ff7f0e',  
    '#9b59b6',  
    '#6c3483',  
    '#512e5f'   
]
inequality_markers = ['o', 's', '^', 'v', 'P']  # Unique markers for inequality measures

# File path to the CSV
#file_path = r"C:\Users\caden\OneDrive\Documents\Final Viz Project\Formatted\tableA5(form)2.csv"
file_path = "../Formatted/tableA5(form)2.csv"

# Load the CSV file into a DataFrame
data = pd.read_csv(file_path)

data = data.apply(pd.to_numeric, errors='coerce').dropna()

inequality_columns = [
    'Year',
    'Gini index of income inequality',
    'Mean log deviation of income',
    'Atkinson e=0.25',
    'Atkinson e=0.50',
    'Atkinson e=0.75'
]
inequality_data = data[inequality_columns]

# Create the subplot for the inequality graph
fig, ax = plt.subplots(figsize=(12, 8))

# Inequality Graph
inequality_lines = []
inequality_labels = [
    'Gini Index', 'Mean Log Deviation', 'Atkinson (e=0.25)', 
    'Atkinson (e=0.50)', 'Atkinson (e=0.75)'
]
for color, marker, label, column in zip(inequality_colors, inequality_markers, inequality_labels, inequality_columns[1:]):
    line = ax.plot(inequality_data['Year'], inequality_data[column], label=label, color=color, marker=marker)[0]
    inequality_lines.append(line)

ax.set_title('Income Inequality Measures Over Time', fontsize=16)
ax.set_xlabel('Year', fontsize=12)
ax.set_ylabel('Index Value', fontsize=12)
ax.legend(title='Measures', fontsize=10)
ax.grid(True)

# Create an annotation for the inequality graph
annot = ax.annotate(
    "", xy=(0, 0), xytext=(15, 15), textcoords="offset points",
    bbox=dict(boxstyle="round", fc="w", alpha=0.8),
    arrowprops=dict(arrowstyle="->"), visible=False
)

def update_annot(line, ind, annot):
    """Update the annotation with the hovered data point."""
    x, y = line.get_data()
    annot.xy = (x[ind["ind"][0]], y[ind["ind"][0]])
    text = f"Year: {x[ind['ind'][0]]}\nValue: {y[ind['ind'][0]]:.2f}"
    annot.set_text(text)
    annot.set_visible(True)

def hover(event):
    """Handle hover event for the inequality graph."""
    vis = annot.get_visible()

    for line in inequality_lines:
        cont, ind = line.contains(event)
        if cont:
            update_annot(line, ind, annot)
            fig.canvas.draw_idle()
            return
    if vis:
        annot.set_visible(False)
        fig.canvas.draw_idle()

# Connect the hover event
fig.canvas.mpl_connect("motion_notify_event", hover)

# Adjust layout and show the plot
plt.tight_layout()
plt.show()
