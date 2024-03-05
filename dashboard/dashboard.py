import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import datetime

sns.set(style='dark')

# Helper function yang dibutuhkan untuk menyiapkan berbagai dataframe

def create_casual_register_df(df):
    casual_count_df = df.groupby("yr")["casual"].sum().reset_index()
    casual_count_df.columns = ["yr", "casual_count"]
    registered_count_df = df.groupby("yr")["registered"].sum().reset_index()
    registered_count_df.columns = ["yr", "registered_count"]  
    casual_register_df = casual_count_df.merge(registered_count_df, on="yr")
    return casual_register_df

def create_monthly_df(df):
    monthly_df = df.groupby(by=["mnth","yr"]).agg({
        "cnt": "sum"
    }).reset_index() 
    return monthly_df

def create_season_df(df):
    season_df = df.groupby(by=["season","yr"]).agg({
        "cnt": "sum"
    }).reset_index() 
    return season_df

def create_weathersit_df(df):
    weathersit_df = df.groupby(by=["weathersit","yr"]).agg({
        "cnt": "sum"
    }).reset_index() 
    return weathersit_df

def create_weekday_df(df):
    weekday_df = df.groupby(by=["weekday","yr"]).agg({
        "cnt": "sum"
    }).reset_index() 
    return weekday_df

def create_workingday_df(df):
    workingday_df = df.groupby(by=["workingday","yr"]).agg({
        "cnt": "sum"
    }).reset_index() 
    return workingday_df

def create_holiday_df(df):
    holiday_df = df.groupby(by=["holiday","yr"]).agg({
        "cnt": "sum"
    }).reset_index() 
    return holiday_df

# Load cleaned data
bike_day_df = pd.read_csv("main_data.csv")

# Filter data
bike_day_df["dteday"] = pd.to_datetime(bike_day_df["dteday"])
min_date = bike_day_df["dteday"].min()
max_date = bike_day_df["dteday"].max()

with st.sidebar:
    # Menambahkan logo 
    st.image("logo.jpg")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = bike_day_df[(bike_day_df["dteday"] >= str(start_date)) & 
                       (bike_day_df["dteday"] <= str(end_date))]


#Menyiapkan berbagai dataframe
casual_register_df = create_casual_register_df(main_df)
monthly_df = create_monthly_df(main_df)
season_df = create_season_df(main_df)
weathersit_df = create_weathersit_df(main_df)
weekday_df = create_weekday_df(main_df)
workingday_df = create_workingday_df(main_df)
holiday_df = create_holiday_df(main_df)

st.header('Bike Dashboard')

#Menampilkan Bagaimana pengaruh cuaca dan musim terhadap total jumlah penyewa sepeda dalam beberapa tahun terakhir
st.subheader('Pengaruh Cuaca dan Musim Terhadap Total Pengguna Penyewa Sepeda Per Tahun')
fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(15,10))

sns.barplot(
    data=season_df,
    x="season",
    y="cnt",
    hue="yr",
    palette="rocket",
    ax=axes[0]
)
axes[0].set_ylabel("Total Sewa")
axes[0].set_title("Total Jumlah Sewa Sepeda Berdasarkan Musim Tiap Tahun")
axes[0].legend(title="Tahun", loc="upper right")

sns.barplot(
    data=weathersit_df,
    x="weathersit",
    y="cnt",
    hue="yr",
    palette="rocket",
    ax=axes[1]
)
axes[1].set_ylabel("Total Sewa")
axes[1].set_title("Total Jumlah Sewa Sepeda Berdasarkan Cuaca Tiap Tahun")
axes[1].legend(title="Tahun", loc="upper right")

plt.tight_layout()
st.pyplot(plt.gcf())

# Menampilkan Apa tren yang terjadi terhadap Total jumlah casual dan Total jumlah pengguna baru dalam beberapa tahun terakhir
st.subheader('Tren Total Pengguna Casual dan Pengguna Registered By Year')
fig, ax = plt.subplots()
index = casual_register_df["yr"]
bar_width = 0.25
bar1 = ax.bar(index, casual_register_df["casual_count"], bar_width, label="Casual Count", color="grey")
bar2 = ax.bar(index + bar_width, casual_register_df["registered_count"], bar_width, label="Registered Count", color="blue")
ax.set_xlabel("Year")
ax.set_ylabel("Count")
ax.set_title("Tren Total Casual and Registered By")
ax.set_xticks(index + bar_width / 2)
ax.set_xticklabels(casual_register_df["yr"])
ax.legend()
for bar in bar1 + bar2:
    height = bar.get_height()
    ax.text(
        bar.get_x() + bar.get_width() / 2., 
        height + 1, 
        str(int(height)), 
        ha="center"
    )
plt.tight_layout()
st.pyplot(plt.gcf())

#Menampilkan Seberapa signifikan total dari jumlah pelanggan menyewa sepeda pada saat hari biasa, hari kerja, dan liburan
#Hari Biasa
st.subheader('Statistik Total Pengguna Menyewa Sepeda Saat Hari Biasa')
fig, ax = plt.subplots()

plt.figure(figsize=(10, 6))
sns.lineplot(
    data=weekday_df, 
    x="weekday", 
    y="cnt", 
    hue="yr", 
    palette="rocket", 
    marker="o"
)

plt.ylabel("Total")
plt.title("Total Pelanggan Menyewa Sepeda Saat Hari Biasa Tiap Tahun")
plt.legend(title="Tahun", loc="upper right")
plt.tight_layout()
st.pyplot(plt.gcf())

#Hari Kerja
st.subheader('Statistik Total Pengguna Menyewa Sepeda Saat Hari Kerja')
fig, ax = plt.subplots()
plt.figure(figsize=(10, 6))
sns.lineplot(
    data=workingday_df, 
    x="workingday", 
    y="cnt", 
    hue="yr", 
    palette="rocket", 
    marker="o"
)

plt.ylabel("Total")
plt.title("Total Pelanggan Menyewa Sepeda Saat Hari Kerja Tiap Tahun")
plt.legend(title="Tahun", loc="upper right")
plt.tight_layout()
st.pyplot(plt.gcf())

#Hari Libur
st.subheader('Statistik Total Pengguna Menyewa Sepeda Saat Hari Libur')
fig, ax = plt.subplots()

plt.figure(figsize=(10, 6))
sns.lineplot(
    data=holiday_df, 
    x="holiday", 
    y="cnt", 
    hue="yr", 
    palette="rocket", 
    marker="o"
)

plt.ylabel("Total")
plt.title("Total Pelanggan Menyewa Sepeda Saat Liburan Tiap Tahun")
plt.legend(title="Tahun", loc="upper right")
plt.tight_layout()
st.pyplot(plt.gcf())
st.caption('Copyright © Adesta Any Fitriani for ML-51')