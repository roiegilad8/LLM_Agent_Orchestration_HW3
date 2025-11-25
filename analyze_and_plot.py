import json
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Load data
with open('results/experiment.json', 'r') as f:
    data = json.load(f)

# Convert to DataFrame
df = pd.DataFrame(data)

# Group by error rate
grouped = df.groupby('error_rate').agg({
    'distance': ['mean', 'std', 'min', 'max']
}).reset_index()

error_rates = grouped['error_rate'].values
means = grouped['distance']['mean'].values
stds = grouped['distance']['std'].values

# Create figure with multiple subplots
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Translation Error Impact Analysis (54 Experiments)', fontsize=16, fontweight='bold')

# Plot 1: Line plot with error bars
ax1 = axes[0, 0]
ax1.errorbar(error_rates * 100, means, yerr=stds, 
             marker='o', markersize=8, capsize=5, linewidth=2, 
             color='#2E86AB', ecolor='#A23B72')
ax1.set_xlabel('Error Rate (%)', fontsize=12)
ax1.set_ylabel('Semantic Distance', fontsize=12)
ax1.set_title('Mean Distance vs Error Rate', fontsize=14, fontweight='bold')
ax1.grid(True, alpha=0.3)
ax1.set_ylim(0, max(means) * 1.2)

# Plot 2: Scatter plot with all points
ax2 = axes[0, 1]
colors = plt.cm.viridis(df['error_rate'] / df['error_rate'].max())
ax2.scatter(df['error_rate'] * 100, df['distance'], 
           c=colors, alpha=0.6, s=50, edgecolors='black', linewidth=0.5)
ax2.set_xlabel('Error Rate (%)', fontsize=12)
ax2.set_ylabel('Semantic Distance', fontsize=12)
ax2.set_title(f'All {len(df)} Individual Measurements', fontsize=14, fontweight='bold')
ax2.grid(True, alpha=0.3)

# Plot 3: Box plot
ax3 = axes[1, 0]
data_by_rate = [df[df['error_rate'] == rate]['distance'].values 
                for rate in sorted(df['error_rate'].unique())]
bp = ax3.boxplot(data_by_rate, labels=[f'{int(r*100)}%' for r in sorted(df['error_rate'].unique())],
                patch_artist=True)
for patch in bp['boxes']:
    patch.set_facecolor('#A8DADC')
    patch.set_alpha(0.7)
ax3.set_xlabel('Error Rate', fontsize=12)
ax3.set_ylabel('Semantic Distance', fontsize=12)
ax3.set_title('Distribution by Error Rate', fontsize=14, fontweight='bold')
ax3.grid(True, alpha=0.3, axis='y')

# Plot 4: Statistics table
ax4 = axes[1, 1]
ax4.axis('off')
table_data = []
for rate in sorted(df['error_rate'].unique()):
    subset = df[df['error_rate'] == rate]
    table_data.append([
        f"{int(rate*100)}%",
        f"{subset['distance'].mean():.3f}",
        f"{subset['distance'].std():.3f}",
        f"{len(subset)}"
    ])

table = ax4.table(cellText=table_data,
                 colLabels=['Error Rate', 'Mean', 'Std Dev', 'N'],
                 cellLoc='center',
                 loc='center',
                 colWidths=[0.25, 0.25, 0.25, 0.25])
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1, 2)
ax4.set_title('Summary Statistics', fontsize=14, fontweight='bold', pad=20)

# Style table
for i in range(len(table_data) + 1):
    if i == 0:
        for j in range(4):
            table[(i, j)].set_facecolor('#457B9D')
            table[(i, j)].set_text_props(weight='bold', color='white')
    else:
        for j in range(4):
            table[(i, j)].set_facecolor('#F1FAEE' if i % 2 == 0 else 'white')

plt.tight_layout()
plt.savefig('results/error_impact_detailed.png', dpi=300, bbox_inches='tight')
print("✅ Saved: results/error_impact_detailed.png")

plt.savefig('results/error_impact_graph.png', dpi=300, bbox_inches='tight')
print("✅ Saved: results/error_impact_graph.png")
