import csv
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.legend_handler import HandlerBase

class TextHandler(HandlerBase):
    def create_artists(self, legend, text, xdescent, ydescent,
                      width, height, fontsize, trans):
        tx = plt.Text(width/2., height/2., text, fontsize=fontsize,
                     ha='center', va='center')
        return [tx]

try:
    # Read CSV file and calculate processing times
    processing_times = []
    with open('training_task_202503061143.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            created = datetime.strptime(row['created_at'], '%Y-%m-%d %H:%M:%S.%f')
            updated = datetime.strptime(row['updated_at'], '%Y-%m-%d %H:%M:%S.%f')
            time_diff = (updated - created).total_seconds() / 60
            processing_times.append(time_diff)
    
    # Convert to numpy array for easier manipulation
    times_array = np.array(processing_times)
    
    # Remove 2 highest and 2 lowest values
    sorted_times = np.sort(times_array)
    filtered_times = sorted_times[2:-2]  # Remove 2 from each end
    
    # Calculate average and median (excluding extremes)
    avg_time = np.mean(filtered_times)
    median_time = np.median(filtered_times)
    
    # Create figure
    plt.figure(figsize=(12, 6))
    
    # Plot bar chart
    bars = plt.bar(range(len(processing_times)), processing_times)
    
    # Add average line
    avg_line = plt.axhline(y=avg_time, color='r', linestyle='--')
    
    # Add median line
    median_line = plt.axhline(y=median_time, color='g', linestyle='--')
    
    # Set titles and labels
    plt.title('Task Processing Time Analysis', fontsize=14)
    plt.xlabel('Task Number', fontsize=12)
    plt.ylabel('Processing Time (minutes)', fontsize=12)
    
    # Add data labels
    for i, bar in enumerate(bars):
        height = bar.get_height()
        if height > 0:
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}',
                    ha='center', va='bottom', fontsize=8)
    
    # Add custom legend
    legend_elements = [
        (avg_line, f'Average: {avg_time:.1f} min'),
        (median_line, f'Median: {median_time:.1f} min'),
        ('', 'Excluding 2 highest and 2 lowest values')
    ]
    
    plt.legend(
        [item[0] for item in legend_elements],
        [item[1] for item in legend_elements],
        handler_map={str: TextHandler()},
        loc='upper right'
    )
    
    # Adjust layout
    plt.tight_layout()
    
    # Save chart
    plt.savefig('task_processing_time.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"""Chart generated successfully as 'task_processing_time.png'
Statistics:
- Average processing time (excluding extremes): {avg_time:.1f} minutes
- Median processing time (excluding extremes): {median_time:.1f} minutes
- Number of tasks analyzed: {len(processing_times)}
- Number of tasks used for average: {len(filtered_times)}""")
    
except Exception as e:
    print(f"Error generating chart: {str(e)}") 