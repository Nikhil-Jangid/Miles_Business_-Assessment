import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

df = pd.read_csv('temperature_data.csv')
df['date'] = pd.to_datetime(df['date'])

df.dropna(inplace=True)  

plt.figure(figsize=(10, 5))
plt.plot(df['date'], df['temperature'], marker='o', linestyle='-', color='b', label='Temp (°C)')

plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

max_temp = df['temperature'].max()
min_temp = df['temperature'].min()
max_date = df[df['temperature'] == max_temp]['date'].values[0]
min_date = df[df['temperature'] == min_temp]['date'].values[0]

max_date_str = pd.to_datetime(max_date).strftime('%Y-%m-%d')
min_date_str = pd.to_datetime(min_date).strftime('%Y-%m-%d')

plt.annotate(f'Highest: {max_temp}°C\non {max_date_str}', 
             xy=(max_date, max_temp), 
             xytext=(max_date, max_temp + 1),
             arrowprops=dict(facecolor='green', arrowstyle='->'),
             fontsize=10, ha='center')

plt.annotate(f'Lowest: {min_temp}°C\non {min_date_str}', 
             xy=(min_date, min_temp), 
             xytext=(min_date, min_temp - 2),
             arrowprops=dict(facecolor='red', arrowstyle='->'),
             fontsize=10, ha='center')

plt.title('Daily Temperature Variations')
plt.xlabel('Date')
plt.ylabel('Temp (°C)')
plt.xticks(rotation=45)
plt.grid()
plt.legend()
plt.tight_layout()

plt.show()

# Answer to Tricky Aspect of the task
# 1. I convert the date column to datetime format with pd.to_datetime() so matplotlib can properly display it on the x-axis.
# 2. I drop rows with missing temperature values using df.dropna(inplace=True) to prevent errors in plotting.