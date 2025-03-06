import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style="dark")

# Load all_data
all_df = pd.read_csv("dashboard/all_data.csv")

def create_topCities_order_df(df):
    topCities_order_df = df.groupby(by="customer_city").order_id.nunique().sort_values(ascending=False).reset_index()
    topCities_order_df.rename(columns={
        "order_id": "order_count"
    }, inplace=True)

    return topCities_order_df

def create_topStates_order_df(df):
    topStates_order_df = df.groupby(by="customer_state").order_id.nunique().sort_values(ascending=False).reset_index()
    topStates_order_df.rename(columns={
        "order_id": "order_count"
    }, inplace=True)

    return topStates_order_df

def create_topCategory_order_df(df):
    topCategory_order_df = df.groupby("product_category_name_english").order_id.nunique().sort_values(ascending=False).reset_index()
    topCategory_order_df.rename(columns={
        "product_category_name_english": "product_category",
        "order_id": "order_count"
    }, inplace=True)

    return topCategory_order_df

def create_bottomCategory_order_df(df):
    bottomCategory_order_df = df.groupby("product_category_name_english").order_id.nunique().sort_values(ascending=False).reset_index()
    bottomCategory_order_df.rename(columns={
        "product_category_name_english": "product_category",
        "order_id": "order_count"
    }, inplace=True)

    return bottomCategory_order_df

datetime_columns = ["order_date", "delivery_date"]
all_df.sort_values(by="order_date", inplace=True)
all_df.reset_index(inplace=True)

for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

# Membuat komponen filter
min_date = all_df["order_date"].min()
max_date = all_df["order_date"].max()

with st.sidebar:
    # Memasukkan logo e-commerce
    st.image("https://www.pngmart.com/files/11/E-Commerce-PNG-Transparent.png")

    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label="Rentang waktu", min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_df[(all_df["order_date"] >= str(start_date)) & 
                 (all_df["order_date"] <= str(end_date))]

topCities_order_df = create_topCities_order_df(main_df)
topStates_order_df = create_topStates_order_df(main_df)
topCategory_order_df = create_topCategory_order_df(main_df)
bottomCategory_order_df = create_bottomCategory_order_df(main_df)

# Visualisasi dashboard

# Membuat header
st.header("E-Commerce Order Trend Dashboard")

# Membuat subheader
st.subheader("Geographic Based")

# Menghitung total dan membuat grafik order negara bagian
total_states_orders = topStates_order_df.order_count.sum()
st.metric("Total Orders", value=f"{total_states_orders:,}")

# Plot
fig, ax = plt.subplots(figsize=(10, 4))
sns.barplot(x="customer_state", y="order_count", data=topStates_order_df.head(10))

# Title & Label
plt.title("Top 10 States with the Most Orders", fontweight="bold", fontsize=12)
plt.xlabel("")
plt.ylabel("")
plt.xticks(fontsize=8, ha="right")
plt.yticks(fontsize=8)
plt.grid(axis="y", linestyle="--", alpha=0.8)

# Show
st.pyplot(fig)

# Plot
fig, ax = plt.subplots(figsize=(10, 4))
sns.barplot(x="customer_city", y="order_count", data=topCities_order_df.head(10))

# Title & Label
plt.title("Top 10 Cities with the Most Orders", fontweight="bold", fontsize=12)
plt.xlabel("")
plt.ylabel("")
plt.xticks(rotation=45, fontsize=8, ha="right")
plt.yticks(fontsize=8)
plt.grid(axis="y", linestyle="--", alpha=0.8)

# Show
st.pyplot(fig)

# Membuat subheader
st.subheader("Most & Least Category Product Order")

# Format
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))

colors_1 = ["#006400", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
colors_2 = ["#8B0000", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

# Plot 1
sns.barplot(y="product_category", x="order_count", data=topCategory_order_df.head(5), palette=colors_1, ax=ax[0])
ax[0].set_ylabel("")
ax[0].set_xlabel("Number of Order", fontsize=30)
ax[0].set_title("Most Order Product Category", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=35)
ax[0].tick_params(axis='x', labelsize=30)

# Plot 2
sns.barplot(y="product_category", x="order_count", data=bottomCategory_order_df.tail(5).sort_values(by="order_count", ascending=True), palette=colors_2, ax=ax[1])
ax[1].set_ylabel("")
ax[1].set_xlabel("Number of Order", fontsize=30)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Least Order Product Category", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)

# Show
st.pyplot(fig)