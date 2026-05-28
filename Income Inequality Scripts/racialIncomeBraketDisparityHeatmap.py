import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import textwrap

# Load the dataset
#file_path = r"C:\Users\caden\OneDrive\Documents\Final Viz Project\Formatted\tableA2.csv"
file_path = "../Formatted/tableA2.csv"

data = pd.read_csv(file_path)

# Select necessary columns
columns = [
    "Year",
    "Race",
    "Under $15,000",
    "$15,000 \nto\n $24,999",
    "$25,000 \nto\n $34,999",
    "$35,000 \nto\n $49,999",
    "$50,000 \nto\n $74,999",
    "$75,000 \nto\n $99,999",
    "$100,000 \nto\n $149,999",
    "$150,000 \nto\n $199,999",
    "$200,000 and over",
    "Mean income\n(dollars) Estimate"  # Include Mean income column
]

# Filter and clean data
filtered_data = data[columns].dropna(subset=["Race", "Mean income\n(dollars) Estimate"])
filtered_data = filtered_data[filtered_data["Race"] != "All Races"]

# Clean the 'Mean income' column by removing commas and handling non-numeric values
filtered_data["Mean income\n(dollars) Estimate"] = (
    filtered_data["Mean income\n(dollars) Estimate"]
    .str.replace(",", "", regex=False)  # Remove commas
    .replace('N', np.nan)               # Replace 'N' with NaN
    .astype(float)                      # Convert to float
)

# Convert income brackets to float
income_brackets = columns[2:-1]  # Exclude 'Mean income' from income_brackets
filtered_data[income_brackets] = filtered_data[income_brackets].astype(float)

# Calculate the average percentage across all years for each racial group
average_data = filtered_data.groupby("Race")[income_brackets + ["Mean income\n(dollars) Estimate"]].mean().reset_index()

# Calculate the average mean income for each race
average_data["Average Mean Income"] = average_data["Mean income\n(dollars) Estimate"]

# Sort the races by highest to lowest average mean income
average_data = average_data.sort_values(by="Average Mean Income", ascending=False)

# Prepare the data for the heatmap
heatmap_data = average_data.set_index("Race")[income_brackets]

# Function to wrap y-axis labels
def wrap_labels(labels, width):
    return ['\n'.join(textwrap.wrap(label, width)) for label in labels]

# Wrap the y-axis labels
wrapped_labels = wrap_labels(heatmap_data.index.tolist(), width=30) 

# Generate the heatmap
plt.figure(figsize=(12, 8))
ax = sns.heatmap(
    heatmap_data,
    annot=False,  # Disable annotations
    cmap="coolwarm",
    cbar_kws={'label': 'Average Percentage Distribution (%)'},
    linewidths=0.5,
    linecolor="black",
    yticklabels=wrapped_labels ,
    xticklabels=True
)
plt.title("Average Income Distribution by Race Ordered by Mean Income", fontsize=16)
plt.xlabel("Income Brackets", fontsize=12)
plt.ylabel("Race (Ordered by Mean Income)", fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.yticks(rotation=0)

# Add tooltip functionality
annot = ax.annotate("", xy=(0, 0), xytext=(20, 20), textcoords="offset points",
                    bbox=dict(boxstyle="round", fc="w", alpha=0.8),
                    arrowprops=dict(arrowstyle="->"), visible=False)

def format_tooltip(row, col):
    """Format the tooltip text."""
    racial_group = heatmap_data.index[row]
    income_range = heatmap_data.columns[col]
    value = heatmap_data.iloc[row, col]
    return f"Race: {racial_group}\nIncome Range: {income_range}\nValue: {value:.2f}%"

def hover(event):
    """Update annotation based on hover."""
    if event.inaxes == ax:
        try:
            x, y = int(event.xdata), int(event.ydata)
            if 0 <= x < len(heatmap_data.columns) and 0 <= y < len(heatmap_data.index):
                annot.xy = (event.xdata, event.ydata)
                annot.set_text(format_tooltip(y, x))
                annot.set_visible(True)
                plt.draw()
            else:
                annot.set_visible(False)
                plt.draw()
        except (ValueError, IndexError):
            annot.set_visible(False)
            plt.draw()
    else:
        annot.set_visible(False)
        plt.draw()

plt.gcf().canvas.mpl_connect("motion_notify_event", hover)

plt.tight_layout()
plt.show()
