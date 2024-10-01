import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import date

# -- Sidebar --
st.sidebar.image("Logo.jpg", width=175)
st.sidebar.title("Bike Sharing Dashboard")
st.sidebar.markdown("""
Dashboard ini memberikan informasi visual tentang tren penyewaan sepeda di Washington D.C. dari tahun 2011-2012. Data disajikan berdasarkan rata-rata penyewaaan per bulan, kondisi cuaca, kategori hari (weekday vs weekend), serta perbandingan pengguna kasual dengan pengguna terdaftar.
""")

# -- Filter Date --
start_date = st.sidebar.date_input("Start date", value=date(2011, 1, 1))
end_date = st.sidebar.date_input("End date", value=date(2012, 12, 31))

# Load dataset (Pastikan file csv tersedia)
@st.cache_data
def load_data():
    return pd.read_csv('main.csv')

hour_df = load_data()

# Filter data by selected date range
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])
filtered_data = hour_df[(hour_df['dteday'] >= pd.to_datetime(start_date)) & (hour_df['dteday'] <= pd.to_datetime(end_date))]

# -- Visualisasi Rata-rata Penyewaan Sepeda per Bulan --
st.title("Rata-rata Penyewaan Sepeda Per Bulan (2011 vs 2012)")
df_grouped = filtered_data.groupby(['yr', 'mnth'])['cnt'].mean().apply(np.floor).reset_index()
df_pivot = df_grouped.pivot(index='mnth', columns='yr', values='cnt').rename(columns={0: 2011, 1: 2012})

fig, ax = plt.subplots()
df_pivot.plot(kind='bar', color=['blue', 'orange'], ax=ax)
plt.xlabel('Bulan')
plt.ylabel('Rata-rata Jumlah')
plt.title('Rata-rata Jumlah per Bulan (2011 vs 2012)')
plt.legend(title='Tahun')
st.pyplot(fig)

# -- Visualisasi Rata-rata Penyewaan Sepeda Berdasarkan Cuaca --
st.title("Perbandingan Penyewaan Sepeda Berdasarkan Cuaca")
filtered_data['weather_category'] = filtered_data['weathersit'].apply(lambda x: 'Normal' if x in [1, 2] else 'Extreme')
average_rentals_per_weather = filtered_data.groupby('weather_category')['cnt'].mean().round()

fig2, ax2 = plt.subplots()
average_rentals_per_weather.plot(kind='bar', color=['skyblue', 'orange'], ax=ax2)
plt.title('Perbandingan Penyewaan Sepeda Berdasarkan Cuaca')
plt.xlabel('Kategori Cuaca')
plt.ylabel('Rata-rata Penyewaan Sepeda')
for index, value in enumerate(average_rentals_per_weather):
    ax2.text(index, value, f'{value:.0f}', ha='center', va='bottom')
st.pyplot(fig2)

# -- Visualisasi Rata-rata Penyewaan Berdasarkan Kategori Hari (Weekday vs Weekend) --
st.title("Perbandingan Penyewaan Sepeda: Weekday vs Weekend")
filtered_data['day_category'] = filtered_data['weekday'].apply(lambda x: 'Weekday' if x in [1, 2, 3, 4, 5] else 'Weekend')
average_rentals_per_day = filtered_data.groupby('day_category')['cnt'].mean().round()

fig3, ax3 = plt.subplots()
average_rentals_per_day.plot(kind='bar', color=['lightgreen', 'lightcoral'], ax=ax3)
plt.title('Perbandingan Penyewaan Sepeda: Weekday vs Weekend')
plt.xlabel('Kategori Hari')
plt.ylabel('Rata-rata Penyewaan Sepeda')
for index, value in enumerate(average_rentals_per_day):
    ax3.text(index, value, f'{value:.0f}', ha='center', va='bottom')
st.pyplot(fig3)

# -- Visualisasi Perbandingan Penggunaan Sepeda Kasual vs Registered --
st.title("Perbandingan Penggunaan Sepeda: Kasual vs Registered")

# Data untuk Weekday
weekday_data = filtered_data[filtered_data['day_category'] == 'Weekday']
weekday_rentals = [weekday_data['casual'].sum(), weekday_data['registered'].sum()]

# Data untuk Weekend
weekend_data = filtered_data[filtered_data['day_category'] == 'Weekend']
weekend_rentals = [weekend_data['casual'].sum(), weekend_data['registered'].sum()]

fig4, axs = plt.subplots(1, 2, figsize=(12, 6))

# Pie chart untuk Weekday
axs[0].pie(weekday_rentals, labels=['Casual', 'Registered'], autopct='%1.1f%%', startangle=90, colors=['skyblue', 'orange'])
axs[0].set_title('Penggunaan Sepeda di Weekday')

# Pie chart untuk Weekend
axs[1].pie(weekend_rentals, labels=['Casual', 'Registered'], autopct='%1.1f%%', startangle=90, colors=['lightgreen', 'coral'])
axs[1].set_title('Penggunaan Sepeda di Weekend')

plt.tight_layout()
st.pyplot(fig4)
