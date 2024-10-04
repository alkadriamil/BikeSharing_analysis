import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set page config
st.set_page_config(page_title="Bike Rental Dashboard", layout="wide")

# Load data
@st.cache_data
def load_data():
    hour_df = pd.read_csv("data_input/hour.csv")
    day_df = pd.read_csv("data_input/day.csv")
    
    # Convert date columns to datetime
    hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])
    day_df['dteday'] = pd.to_datetime(day_df['dteday'])
    
    # Preprocess data
    for df in [hour_df, day_df]:
        df['mnth'] = df['mnth'].map({1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
                                     7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'})
        df['season'] = df['season'].map({1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'})
        df['weekday'] = df['weekday'].map({0: 'Sun', 1: 'Mon', 2: 'Tue', 3: 'Wed', 4: 'Thu', 5: 'Fri', 6: 'Sat'})
        df['weathersit'] = df['weathersit'].map({1: 'Clear/Partly Cloudy', 2: 'Misty/Cloudy',
                                                 3: 'Light Snow/Rain', 4: 'Severe Weather'})
        df['yr'] = df['yr'].map({0: '2011', 1: '2012'})
        df['workingday'] = df['workingday'].map({0: 'Holiday', 1: 'Workingday'})
    
    return hour_df, day_df

hour_df, day_df = load_data()

# Title
st.title("🚲 Bike Rental Analysis Dashboard")

# Sidebar
st.sidebar.header("Filters")
year = st.sidebar.multiselect("Select Year", options=day_df['yr'].unique(), default=day_df['yr'].unique())
season = st.sidebar.multiselect("Select Season", options=day_df['season'].unique(), default=day_df['season'].unique())

# Filter data
filtered_df = day_df[(day_df['yr'].isin(year)) & (day_df['season'].isin(season))]

# KPIs
col1, col2, col3 = st.columns(3)
col1.metric("Total Rentals", f"{filtered_df['cnt'].sum():,}")
col2.metric("Average Daily Rentals", f"{filtered_df['cnt'].mean():.0f}")
col3.metric("Peak Day Rentals", f"{filtered_df['cnt'].max():,}")

# Yearly Trend
st.subheader("Monthly Rental Trend")
monthly_counts = filtered_df.groupby(by=["mnth","yr"]).agg({"cnt": "sum"}).reset_index()
monthly_counts['mnth'] = pd.Categorical(monthly_counts['mnth'], 
                                        categories=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],
                                        ordered=True)
fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(data=monthly_counts, x="mnth", y="cnt", hue="yr", palette="rocket", marker="o", ax=ax)
ax.set_title("Trend of Bike Rentals")
ax.set_xlabel(None)
ax.set_ylabel("Number of Rentals")
ax.legend(title="Year", loc="upper right")
st.pyplot(fig)

# Seasonal Pattern
st.subheader("Seasonal Rental Pattern")
season_pattern = filtered_df.groupby('season')[['registered', 'casual']].sum().reset_index()
season_pattern = season_pattern.melt(id_vars=['season'], var_name='type', value_name='count')
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=season_pattern, x='season', y='count', hue='type', palette=['tab:red', 'tab:blue'], ax=ax)
ax.set_title("Number of Bike Rentals by Season and User Type")
ax.set_xlabel(None)
ax.set_ylabel("Number of Rentals")
st.pyplot(fig)

# Weather Impact
st.subheader("Weather Impact on Rentals")
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=filtered_df, x='weathersit', y='cnt', ax=ax)
ax.set_title("Number of Bike Rentals by Weather Condition")
ax.set_xlabel("Weather Condition")
ax.set_ylabel("Number of Rentals")
st.pyplot(fig)

# Weekday vs Weekend
st.subheader("Weekday vs Weekend Rentals")
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=filtered_df, x='workingday', y='cnt', ax=ax)
ax.set_title("Comparison of Bike Rentals on Working Days and Holidays")
ax.set_xlabel(None)
ax.set_ylabel("Number of Rentals")
st.pyplot(fig)

# Hourly Rentals Trend
st.subheader("Hourly Rental Trend")
fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(data=day_df, x='hr', y='cnt', marker='o', ax=ax)
ax.set_title('Jumlah Penyewaan Sepeda Berdasarkan Jam')
ax.set_xlabel('Jam dalam Sehari')
ax.set_ylabel('Total Penyewaan')
ax.grid(True)
ax.set_xticks(range(24))
st.pyplot(fig)


# Additional Insights
st.subheader("Additional Insights")
st.write("""
1. **Seasonal Trends**: The data shows clear seasonal patterns in bike rentals. Summer and Fall seem to be the peak seasons, likely due to favorable weather conditions.

2. **Weather Impact**: Clear and partly cloudy days have the highest number of rentals. Severe weather conditions significantly reduce rental numbers.

3. **User Type Differences**: There's a noticeable difference between registered users and casual users. Registered users tend to be more consistent across seasons, while casual users show more variation.

4. **Yearly Growth**: There's an overall increase in rentals from 2011 to 2012, indicating growing popularity or expansion of the service.

5. **Day of Week Patterns**: Weekdays show different patterns compared to weekends. This could be due to commuting patterns on workdays.

6. **Temperature Correlation**: While not directly visualized here, the original data suggests a positive correlation between temperature and rental numbers.

7. **Holiday Effect**: The comparison between working days and holidays shows interesting patterns, possibly reflecting leisure vs. commute usage.

8. **Hourly Rentals Trend**: The hourly bike rental trend shows peaks during commuting hours (8 AM and 5-7 PM), a midday lull, and a decline after 8 PM, suggesting opportunities for targeted bike availability, maintenance during low periods, and promotional offers in off-peak hours.

These insights can be valuable for inventory management, marketing strategies, and service improvements. For instance, the bike rental company could:
- Adjust inventory based on seasonal demands
- Create targeted promotions for off-peak seasons or weather conditions
- Develop strategies to convert casual users to registered users
- Plan maintenance during off-peak times
""")

# Footer
st.markdown("---")
st.markdown("Dashboard created with Streamlit by Amil Al Kadri")
