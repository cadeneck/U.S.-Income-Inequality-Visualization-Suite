import pandas as pd
import matplotlib.pyplot as plt

# File path to the CSV file
#file_path = r"c:\Users\caden\OneDrive\Documents\Final Viz Project\Formatted\tableA7.csv"
file_path = "../Formatted/tableA7.csv"

# Read the CSV file into a DataFrame
df = pd.read_csv(file_path)

# Ensure relevant columns are numeric
df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
df['Female-to-male earnings ratio'] = pd.to_numeric(df['Female-to-male earnings ratio'], errors='coerce')

# Sort data by Year in ascending order
df = df.sort_values(by='Year')

fig, ax = plt.subplots(figsize=(14, 8))

# Plot the earnings ratio as a bar chart
bars = ax.bar(df['Year'], df['Female-to-male earnings ratio'], color='purple', alpha=0.7)

# Add labels, title, and grid
ax.set_xlabel('Year', fontsize=12)
ax.set_ylabel('Female-to-Male Earnings Ratio', fontsize=12)
ax.set_title('Female-to-Male Earnings Ratio Over Time', fontsize=16)
ax.set_xticks(df['Year'])
ax.set_xticklabels(df['Year'], rotation=45)
ax.grid(axis='y', linestyle='--', alpha=0.7)

# Add a line to indicate equality (ratio = 1)
ax.axhline(y=1, color='red', linestyle='--', linewidth=1, label='Equal Earnings (1:1)')

ax.legend()

annot = ax.annotate(
    "", xy=(0, 0), xytext=(15, 15), textcoords="offset points",
    bbox=dict(boxstyle="round", fc="w", alpha=0.8),
    arrowprops=dict(arrowstyle="->"), visible=False
)

def update_tooltip(event):
    """Update the annotation based on mouse hover."""
    visible = annot.get_visible()
    if event.inaxes == ax:
        for bar, year, ratio in zip(bars, df['Year'], df['Female-to-male earnings ratio']):
            if bar.contains(event)[0]:
                # Update the annotation
                annot.xy = (event.xdata, event.ydata)
                annot.set_text(f"Year: {year}\nRatio: {ratio:.2f}")
                annot.set_visible(True)
                fig.canvas.draw_idle()
                return
    if visible:
        annot.set_visible(False)
        fig.canvas.draw_idle()

# Connect hover event
fig.canvas.mpl_connect("motion_notify_event", update_tooltip)

# Adjust layout and show the plot
plt.tight_layout()
plt.show()
