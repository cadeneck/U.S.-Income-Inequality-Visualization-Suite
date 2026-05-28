import pandas as pd
import matplotlib.pyplot as plt

# File path to the CSV file
#file_path = r"c:\Users\caden\OneDrive\Documents\Final Viz Project\Formatted\tableA7.csv"
file_path = "../Formatted/tableA7.csv"

df = pd.read_csv(file_path)

df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
df['Male Median Earning Estimate'] = pd.to_numeric(df['Male Median Earning Estimate'], errors='coerce')
df['Female Median earnings (dollars) Estimate'] = pd.to_numeric(df['Female Median earnings (dollars) Estimate'], errors='coerce')
df['Male Number of Workers (thousands)'] = pd.to_numeric(df['Male Number of workers (thousands)'], errors='coerce')
df['Female Number of Workers (thousands)'] = pd.to_numeric(df['Female Number of workers (thousands)'], errors='coerce')

df = df.dropna(subset=[
    'Male Median Earning Estimate', 
    'Female Median earnings (dollars) Estimate', 
    'Male Number of Workers (thousands)', 
    'Female Number of Workers (thousands)'
])

df = df[(df['Year'] >= 1975) & (df['Year'] <= 2019)]

df['5-Year Group'] = ((df['Year'] - 1975) // 5) * 5 + 1975

grouped = df.groupby('5-Year Group').agg({
    'Male Median Earning Estimate': 'mean',
    'Female Median earnings (dollars) Estimate': 'mean',
    'Male Number of Workers (thousands)': 'sum',
    'Female Number of Workers (thousands)': 'sum'
}).reset_index()

grouped['Discrepancy'] = grouped['Male Median Earning Estimate'] - grouped['Female Median earnings (dollars) Estimate']
grouped['Discrepancy Bubble Size'] = grouped['Discrepancy'].abs() / grouped['Discrepancy'].abs().max() * 200  # Normalize discrepancy for bubble size

# Normalize bubble sizes for workers
scale_factor = 40  
grouped['Male Bubble Size'] = grouped['Male Number of Workers (thousands)'] / scale_factor
grouped['Female Bubble Size'] = grouped['Female Number of Workers (thousands)'] / scale_factor

fig, ax = plt.subplots(figsize=(16, 10))

# Male data
male_scatter = ax.scatter(
    grouped['5-Year Group'],
    grouped['Male Median Earning Estimate'],
    s=grouped['Male Bubble Size'],  # Scaled bubble size for male workers
    color='blue',
    alpha=0.5,
    label='Male Earnings'
)

# Female data
female_scatter = ax.scatter(
    grouped['5-Year Group'],
    grouped['Female Median earnings (dollars) Estimate'],
    s=grouped['Female Bubble Size'],  # Scaled bubble size for female workers
    color='pink',
    alpha=0.5,
    label='Female Earnings'
)

# Discrepancy data
discrepancy_scatter = ax.scatter(
    grouped['5-Year Group'],
    grouped['Discrepancy'],
    s=grouped['Discrepancy Bubble Size'],  # Bubble size based on normalized discrepancy
    color='grey',
    alpha=0.6,
    label='Discrepancy (M - F)'
)

# Title and labels
ax.set_title('Earnings, Workers, and Discrepancy by Gender (1975-2020)', fontsize=18)
ax.set_xlabel('5-Year Group', fontsize=14)
ax.set_ylabel('Median Earnings / Discrepancy ($)', fontsize=14)

# Set x-axis and y-axis limits
plt.xlim([1970, 2020])  
plt.ylim([0, 100000]) 

# Add legend with smaller circles
legend_handles = [
    plt.Line2D([0], [0], marker='o', color='w', label='Male Earnings', markersize=10, markerfacecolor='blue', alpha=0.5),
    plt.Line2D([0], [0], marker='o', color='w', label='Female Earnings', markersize=10, markerfacecolor='pink', alpha=0.5),
    plt.Line2D([0], [0], marker='o', color='w', label='Discrepancy (M - F)', markersize=10, markerfacecolor='grey', alpha=0.6)
]
ax.legend(handles=legend_handles, fontsize=12)

ax.grid(axis='y', linestyle='--', alpha=0.7)

# Add tooltip annotation
annot = ax.annotate(
    "", xy=(0, 0), xytext=(15, 15), textcoords="offset points",
    bbox=dict(boxstyle="round", fc="w", alpha=0.8),
    arrowprops=dict(arrowstyle="->"), visible=False
)

def update_tooltip(event):
    """Update the annotation based on mouse hover."""
    visible = annot.get_visible()

    # Iterate through all scatter plots and handle each separately
    for scatter, label, y_column in zip(
        [male_scatter, female_scatter, discrepancy_scatter],
        ['Male', 'Female', 'Discrepancy'],
        [
            'Male Median Earning Estimate',
            'Female Median earnings (dollars) Estimate',
            'Discrepancy'
        ]
    ):
        contains, ind = scatter.contains(event)
        if contains:
            idx = ind["ind"][0]  

            # Format tooltip text dynamically
            if label == 'Discrepancy':
                text = (
                    f"{label}\n5-Year Group: {grouped['5-Year Group'][idx]}\n"
                    f"Value: {grouped['Discrepancy'][idx]:.2f}"
                )
                annot.xy = (
                    grouped['5-Year Group'][idx],
                    grouped['Discrepancy'][idx]
                )
            else:
                text = (
                    f"{label} Earnings\n5-Year Group: {grouped['5-Year Group'][idx]}\n"
                    f"Value: {grouped[y_column][idx]:.2f}"
                )
                annot.xy = (
                    grouped['5-Year Group'][idx],
                    grouped[y_column][idx]
                )

            annot.set_text(text)
            annot.set_visible(True)
            fig.canvas.draw_idle()
            return

    # Hide annotation if no point is hovered
    if visible:
        annot.set_visible(False)
        fig.canvas.draw_idle()

# Connect the hover event
fig.canvas.mpl_connect("motion_notify_event", update_tooltip)


# Adjust layout and display the plot
plt.tight_layout()
plt.show()
