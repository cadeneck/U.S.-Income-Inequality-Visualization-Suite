import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
#file_path = r"C:\Users\caden\OneDrive\Documents\Final Viz Project\Formatted\tableA2.csv"
file_path = "../Formatted/tableA2.csv"

data = pd.read_csv(file_path)

# Filter relevant columns and rename them for simplicity
filtered_data = data[['Year', 'Race', 'Under $15,000', '$200,000 and over']].copy()
filtered_data.rename(columns={'Under $15,000': 'Under 15k', '$200,000 and over': 'Over 200k'}, inplace=True)

filtered_data['Year'] = pd.to_numeric(filtered_data['Year'], errors='coerce')
filtered_data = filtered_data.dropna().sort_values(by='Year')

filtered_data = filtered_data.drop_duplicates(subset=['Year', 'Race'])

# Split the data into two subsets: before 2002 and 2002 onward
data_before_2002 = filtered_data[filtered_data['Year'] < 2002]
data_2002_onward = filtered_data[(filtered_data['Year'] >= 2002) & (~filtered_data['Race'].str.contains('combination', case=False)) & (~filtered_data['Race'].str.contains('two', case=False))]

# Pivot the data for grouping by race
pivot_before_2002 = data_before_2002.pivot(index='Year', columns='Race', values=['Under 15k', 'Over 200k'])
pivot_2002_onward = data_2002_onward.pivot(index='Year', columns='Race', values=['Under 15k', 'Over 200k'])

fig, axes = plt.subplots(2, 2, figsize=(14, 10), sharex=False, sharey=False)
lines = [] 
highlighted_colors = set() 
hovered_color = None  

# Tooltips for each subplot
annotations = {ax: ax.annotate(
    "",
    xy=(0.975, 0.96),  
    xycoords="axes fraction",
    ha="right", 
    va="top",  
    bbox=dict(boxstyle="round", fc="w", alpha=0.8),
    visible=False
) for ax in axes.flat}

# Helper function to update opacity based on color
def set_opacity_by_color(alpha=1.0, chosen_colors=None):
    """Update the opacity of all lines based on highlighted and hovered colors."""
    for line in lines:
        color = line.get_color()
        if chosen_colors and color in chosen_colors:
            line.set_alpha(1.0)  
        else:
            line.set_alpha(alpha) 
    fig.canvas.draw_idle()

# Update the tooltip annotation
def update_tooltip(ax, line, ind):
    """Update the tooltip to show the closest point's data."""
    x, y = line.get_data()
    index = ind["ind"][0]
    race = line.get_label()  # Get the label for the race
    text = f"Race: {race}\nYear: {x[index]}\nValue: {y[index]:.2f}"
    annotations[ax].set_text(text)
    annotations[ax].set_visible(True)
    fig.canvas.draw_idle()

# Event handler for mouse clicks
def on_click(event):
    """Handle line selection and reset behavior on click."""
    global highlighted_colors, hovered_color
    if event.inaxes:
        for line in event.inaxes.get_lines():
            if line.contains(event)[0]:  # Check if the click is on a line
                highlighted_colors.add(line.get_color())  # Add the color of the selected line
                set_opacity_by_color(alpha=0.2, chosen_colors=highlighted_colors)
                return
    # Reset all lines if clicking outside
    highlighted_colors.clear()
    hovered_color = None
    for annot in annotations.values():
        annot.set_visible(False)  # Hide all tooltips
    set_opacity_by_color(alpha=1.0)

# Event handler for mouse movement (hovering)
def on_hover(event):
    """Handle hover behavior."""
    global hovered_color
    if event.inaxes:
        for line in event.inaxes.get_lines():
            cont, ind = line.contains(event)
            if cont:  # Check if the mouse is over a line
                hovered_color = line.get_color()
                update_tooltip(event.inaxes, line, ind)  # Update the tooltip
                set_opacity_by_color(alpha=0.2, chosen_colors=highlighted_colors.union({hovered_color}))
                return
    # Reset hover if not over a line
    hovered_color = None
    for annot in annotations.values():
        annot.set_visible(False)  # Hide all tooltips
    set_opacity_by_color(alpha=0.2, chosen_colors=highlighted_colors)

# Plot for 'Under 15k' before 2002
for column in pivot_before_2002['Under 15k']:
    line, = axes[0, 0].plot(pivot_before_2002.index, pivot_before_2002['Under 15k'][column], label=column)
    lines.append(line)
axes[0, 0].set_title('Income Under $15,000 by Race (Before 2002)')
axes[0, 0].set_ylabel('Percent (%)')
axes[0, 0].set_ylim(0, 30)
axes[0, 0].grid(True)

# Plot for 'Over 200k' before 2002
for column in pivot_before_2002['Over 200k']:
    line, = axes[1, 0].plot(pivot_before_2002.index, pivot_before_2002['Over 200k'][column], label=column)
    lines.append(line)
axes[1, 0].set_title('Income $200,000 and Over by Race (Before 2002)')
axes[1, 0].set_xlabel('Year')
axes[1, 0].set_ylabel('Percent (%)')
axes[1, 0].set_ylim(0, 30)
axes[1, 0].grid(True)
axes[1, 0].legend(loc='upper left')

# Plot for 'Under 15k' 2002 onward
for column in pivot_2002_onward['Under 15k']:
    line, = axes[0, 1].plot(pivot_2002_onward.index, pivot_2002_onward['Under 15k'][column], label=column)
    lines.append(line)
axes[0, 1].set_title('Income Under $15,000 by Race (2002 Onward)')
axes[0, 1].set_ylabel('Percent (%)')
axes[0, 1].set_ylim(0, 30)
axes[0, 1].grid(True)

# Plot for 'Over 200k' 2002 onward
for column in pivot_2002_onward['Over 200k']:
    line, = axes[1, 1].plot(pivot_2002_onward.index, pivot_2002_onward['Over 200k'][column], label=column)
    lines.append(line)
axes[1, 1].set_title('Income $200,000 and Over by Race (2002 Onward)')
axes[1, 1].set_xlabel('Year')
axes[1, 1].set_ylabel('Percent (%)')
axes[1, 1].set_ylim(0, 30)
axes[1, 1].grid(True)

fig.canvas.mpl_connect('button_press_event', on_click)
fig.canvas.mpl_connect('motion_notify_event', on_hover)

# Adjust layout and show the plots
plt.tight_layout()
plt.subplots_adjust(hspace=0.3, wspace=0.15)
plt.show()
