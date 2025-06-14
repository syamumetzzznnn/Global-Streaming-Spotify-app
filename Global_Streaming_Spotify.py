import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

# Load data dengan cache
@st.cache_data
def load_data():
    df = pd.read_csv("Spotify_2024_Global_Streaming_Data.csv")
    return df

df = load_data()

# Judul Aplikasi
st.title("🎧 Dashboard Global Streaming Spotify 2024")

# Sidebar Filter
with st.sidebar:
    st.header("🔍 Filter Data")
    selected_country = st.selectbox("Pilih Negara", options=["All"] + sorted(df["Country"].unique()))
    selected_genre = st.multiselect("Pilih Genre", options=df["Genre"].unique(), default=df["Genre"].unique())

# Filter berdasarkan input pengguna
filtered_df = df.copy()
if selected_country != "All":
    filtered_df = filtered_df[filtered_df["Country"] == selected_country]
filtered_df = filtered_df[filtered_df["Genre"].isin(selected_genre)]

# Statistik Data Stream
st.subheader("📊 Statistik Data Stream")
col1, col2, col3 = st.columns(3)
col1.metric("Jumlah Artis", filtered_df["Artist"].nunique())
col2.metric("Total Stream (Juta)", f"{filtered_df['Total Streams (Millions)'].sum():,.0f}")
col3.metric("Rata-rata Skip Rate (%)", f"{filtered_df['Skip Rate (%)'].mean():.2f}")

# Visualisasi Stream
st.subheader("📈 Jumlah Streaming Artis")
fig, ax = plt.subplots(figsize=(10, 5))
top_artists = filtered_df.groupby("Artist")["Total Streams (Millions)"].sum().nlargest(10)
sns.barplot(x=top_artists.values, y=top_artists.index, ax=ax, palette="viridis")
ax.set_xlabel("Total Streams (Juta)")
ax.set_ylabel("Artis")
st.pyplot(fig)

# Editor Data Interaktif
st.subheader("📝 Data Spotify")
editable_cols = ["Artist", "Album", "Genre", "Monthly Listeners (Millions)", "Total Streams (Millions)", "Skip Rate (%)"]
editable_df = st.data_editor(filtered_df[editable_cols], num_rows="dynamic", use_container_width=True)


