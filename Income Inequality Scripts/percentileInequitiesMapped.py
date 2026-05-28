import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm

# Define unique colors and markers
quintile_colors = cm.tab10.colors[:3] 
inequality_colors = cm.tab10.colors[3:6]  
quintile_markers = ['o', 's', '^']  
inequality_markers = ['D', 'X', '*', 'v', 'P']  

# File path to the CSV
#file_path = r"C:\Users\caden\OneDrive\Documents\Final Viz Project\Formatted\tableA5(form)2.csv"
file_path = "../Formatted/tableA5(form)2.csv"

data = pd.read_csv(file_path)
data = data.apply(pd.to_numeric, errors='coerce').dropna()

quintile_columns = ['Year', 'Lowest quintile', 'Third quintile', 'Highest quintile']
quintile_data = data[quintile_columns]


# Prepare data for the inequality graph
inequality_columns = [
    'Year',
    '90th/10th',
    '90th/50th',
    '50th/10th'
]

inequality_data = data[inequality_columns]

# Create the subplots side by side
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))  # 1 row, 2 columns

# Quintile Graph
quintile_lines = []
quintile_labels = ['Lowest Quintile', 'Third Quintile', 'Highest Quintile']
for color, marker, label, column in zip(quintile_colors, quintile_markers, quintile_labels, quintile_columns[1:]):
    line = ax1.plot(quintile_data['Year'], quintile_data[column], label=label, color=color, marker=marker)[0]
    quintile_lines.append(line)

ax1.set_title('Income Quintiles Over Time', fontsize=16)
ax1.set_xlabel('Year', fontsize=12)
ax1.set_ylabel('Percentage Total Wealth (%)', fontsize=12)
ax1.legend()
ax1.grid(True)

# Inequality Graph
inequality_lines = []
inequality_labels = [
    '90th/10th',
    '90th/50th',
    '50th/10th'
]
for color, marker, label, column in zip(inequality_colors, inequality_markers, inequality_labels, inequality_columns[1:]):
    line = ax2.plot(inequality_data['Year'], inequality_data[column], label=label, color=color, marker=marker)[0]
    inequality_lines.append(line)

ax2.set_title('Percentile Income Inequality Over Time', fontsize=16)
ax2.set_xlabel('Year', fontsize=12)
ax2.set_ylabel('CPI Adjusted Income Ratios', fontsize=12)
ax2.legend(title='Measures', fontsize=10)
ax2.grid(True)

# Create subgraph-specific annotations
annot_ax1 = ax1.annotate(
    "", xy=(0, 0), xytext=(15, 15), textcoords="offset points",
    bbox=dict(boxstyle="round", fc="w", alpha=0.8),
    arrowprops=dict(arrowstyle="->"), visible=False
)

annot_ax2 = ax2.annotate(
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
    """Handle hover event for both subgraphs."""
    vis_ax1 = annot_ax1.get_visible()
    vis_ax2 = annot_ax2.get_visible()

    if event.inaxes == ax1:  
        for line in quintile_lines:
            cont, ind = line.contains(event)
            if cont:
                update_annot(line, ind, annot_ax1)
                fig.canvas.draw_idle()
                return
        if vis_ax1:
            annot_ax1.set_visible(False)
            fig.canvas.draw_idle()

    elif event.inaxes == ax2:  
        for line in inequality_lines:
            cont, ind = line.contains(event)
            if cont:
                update_annot(line, ind, annot_ax2)
                fig.canvas.draw_idle()
                return
        if vis_ax2:
            annot_ax2.set_visible(False)
            fig.canvas.draw_idle()

# Connect the hover event
fig.canvas.mpl_connect("motion_notify_event", hover)

# Adjust layout and show the plots
plt.tight_layout()
# Adjust layout to prevent overlapping and improve spacing
plt.subplots_adjust(wspace=0.15)  # Increase horizontal space between subplots


# Adjust layout and show the plots
plt.show()
