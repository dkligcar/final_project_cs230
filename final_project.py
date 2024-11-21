"""
Daniel Kligerman Carvalho
CS230-6 Asynch
Data: Fast Food Restaurants in the USA

Description: This program contains data from the data set ‘Fast Food Restaurants in the United States’ to develop an web-based Python page that provides insight on one of the most established industries in America. In this app you are able to search the total amount of fast food chins per state, the breakdown of each chain's biggest presence,  with the cities with the most chains present. Lastly, you are also able to know the top 10 chains that increased the most each year from 2014 to 2018.
"""
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

def read_data():
    data = pd.read_csv('/Users/dk/Downloads/archive/Datafiniti_Fast_Food_Restaurants.csv')
    data['dateAdded'] = pd.to_datetime(data['dateAdded'])
    data['year'] = data['dateAdded'].dt.year  # dateAdded to year

    data['name'] = data['name'].apply(lambda x: x.strip().title()) #Lambda func to clean name column
    return data

def show_restaurants_by_state(data, state='CA'): #CA as default
    """ VIZ1: Number of restaurants per selected state with default state California."""
    if state not in data['province'].unique():
        st.error(f"Selected state {state} not found in the data.")
        return
    count = data[data['province'] == state].shape[0]
    st.subheader(f"Total Restaurants in {state}: {count}")

def chain_amount_analysis(data, chain_selection):
    """ VIZ2: Total locations and the state where the chain is most present."""
    chain_data = data[data['name'] == chain_selection]
    total_locations = chain_data.shape[0]
    if not chain_data.empty:
        most_present_state = chain_data['province'].value_counts().idxmax()
        most_present_state_count = chain_data['province'].value_counts().max()
    else:
        most_present_state = "N/A"
        most_present_state_count = 0
    st.subheader(f"**{chain_selection}** has **{total_locations}** total locations.")
    st.write(f"The state where **{chain_selection}** is most present is **{most_present_state}**, with **{most_present_state_count}** locations.")

def map_chain_locations(data, chain_selection):
    """VIZ3: Map locations of the selected chain across the country."""
    chain_data = data[data['name'] == chain_selection]
    location_data = chain_data[['latitude', 'longitude']].dropna()
    return location_data

def generate_bar_chart(city_counts, title):
    """VIZ5: Bar Chart indicating the cities with the most locations of the selected chain."""
    plt.figure(figsize=(10, 6))
    bars = city_counts.plot(kind='bar', color='orange')
    for index, value in enumerate(city_counts.values):
        plt.text(index, value, str(value), ha='center', va='bottom', fontsize=10, color='black')
    plt.title(title, fontsize=16)
    plt.xlabel("City", fontsize=12)
    plt.ylabel("Number of Locations", fontsize=12)
    plt.xticks(rotation=45, ha='right')
    st.pyplot(plt)

def generate_horizontal_bar_chart(data):
    """VIZ6: Top 10 chains opening the most locations in a selected year."""
    yearly_data = data.groupby(['year', 'name']).size().reset_index(name='count')
    selected_year = st.slider("Select Year:", int(yearly_data['year'].min()), int(yearly_data['year'].max()))
    top_chains = yearly_data[yearly_data['year'] == selected_year].nlargest(10, 'count')
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(top_chains['name'], top_chains['count'], color = ['red','blue','yellow', 'pink', 'brown', 'grey', 'purple','beige'])
    for index, value in enumerate(top_chains['count']):
        ax.text(value + 1, index, str(value), va='center', fontsize=10)
    ax.set_title(f"Top 10 Chains Opening the Most Locations in {selected_year}", fontsize=16)
    ax.set_xlabel("Number of Locations", fontsize=12)
    ax.set_ylabel("Chains", fontsize=12)
    st.pyplot(fig)


#ST Setup
st.markdown("<h1 style='text-align: center;'><u>Presence of Fast-Food Restaurants Across the United States</u></h1>", unsafe_allow_html=True)

data = read_data()

# Total restaurants by state
st.header("How many fast-food restaurants are there in each state?:")
state_options = sorted(data['province'].unique())
default_state_index = state_options.index('CA') if 'CA' in state_options else 0
state_selection = st.selectbox("Select a State:", state_options, index=default_state_index)
show_restaurants_by_state(data, state_selection)

st.markdown("<hr>", unsafe_allow_html=True)

# Presence analysis
st.header("Where is the largest presence of each fast-food chain?")
chain_selection = st.selectbox("Select a Chain:", data['name'].unique())
chain_amount_analysis(data, chain_selection)

#  Map
st.subheader(f"Map of {chain_selection} Locations Across the US")
location_data = map_chain_locations(data, chain_selection)
if location_data.empty:
    st.write(f"No location data available for {chain_selection}.")
else:
    st.map(location_data)


# Cities bar chart
city_counts = data[data['name'] == chain_selection]['city'].value_counts().head(10)
sort_option = st.radio("Sort cities by:", ('Alphabetical', 'Number of Locations'))
if sort_option == 'Alphabetical':
    city_counts = city_counts.sort_index()
else:
    city_counts = city_counts.sort_values(ascending=False)
generate_bar_chart(city_counts, f"Top Cities with the most {chain_selection} locations")

st.markdown("<hr>", unsafe_allow_html=True)

# Horizontal Bar Chart
st.subheader("Most stores opened by year (2014-2018)")
generate_horizontal_bar_chart(data)

st.markdown("<hr>", unsafe_allow_html=True)




#Summary
st.markdown("""
## What surprised me the most?:
  - Texas and California dominate with over 2,000 combined locations
  - Arizona and Colorado seem to have a less saturated market than expected
  - The discrepancy between McDonald's and Burger King's presence in the US is wider than expected
  - Great number of local dominant chains like Steak and Shake and Culver's
  - 7Eleven's data did not seem to match my perspective of their presence
""")
