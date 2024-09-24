import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px
from PIL import Image
from streamlit_option_menu import option_menu

#Setting page icon
icon = Image.open("icon.png")
st.set_page_config(page_title= "Zomato Data Analysis and Visualization",
                   page_icon= icon,
                   layout= "wide",
                   initial_sidebar_state= "expanded",
                   )

col1, col2, col3 = st.columns([1,1,1])
col2.image("icon2.png", width=100,use_column_width='always')

selected = option_menu(None, ["Home","Visualization"],
                       icons=["house",""],
                       default_index=0,
                       orientation="horizontal",
                       styles={"nav-link": {"font-size": "15px", "text-align": "centre", "margin": "-2px", "--hover-color": "Red"},
                               "icon": {"font-size": "35px"},
                               "container" : {"max-width": "5000px"},
                               "nav-link-selected": {"background-color": "Red"}})


# Reading the Cleaned DataFrame
df = pd.read_excel("zomato_updated.xlsx")
country = df['Country'].unique()

if selected == "Visualization":
        tab1, tab2, tab3 = st.tabs(["***Restaurant & Ratings - Country Wise(Global)***", "***Restaurant & Ratings - City Wise(Global)***", "***Restaurant & Ratings - City Wise(India)***"])
        with tab1:
                subtab1, subtab2,subtab3 = st.tabs(["Restaurant Data", "Rating","Dine-in vs Online-delivery"])

                with subtab1:
                        selected_country = st.selectbox("Select a Country", df['Country'].unique())

                        # Filter data based on the selected country
                        country_data = df[df['Country'] == selected_country]
                        total_restaurants = country_data['Restaurant Name'].nunique()
                        st.write(f"Total number of restaurants in {selected_country}: {total_restaurants}")

                        # Second: Display restaurant names along with their cuisines
                        restaurant_info = country_data[['Restaurant Name', 'Cuisines']].drop_duplicates().reset_index(drop=True)

                        # Display the DataFrame with restaurant names and cuisines
                        st.write(f"Restaurants and their cuisines:")
                        st.dataframe(restaurant_info)

                with subtab2:
                        # Dropdown to select a country
                        selected_country = st.selectbox("Select a Country", df['Country'].unique(), key="country_select")

                        # Filter data based on the selected country
                        country_data = df[df['Country'] == selected_country]

                        # Sort by rating in descending order to get the top-rated restaurants
                        top_rated_data = country_data.sort_values(by='Aggregate rating', ascending=False)

                        # You can limit to top N restaurants if you want (e.g., top 10)
                        top_rated_data = top_rated_data.head(20)

                        # Bar chart based on restaurant ratings
                        rating_chart = top_rated_data.groupby('Restaurant Name')['Aggregate rating'].mean().reset_index()
                        fig1 = px.bar(rating_chart, x='Restaurant Name', y='Aggregate rating',
                                title=f"Top Rated Restaurants in {selected_country}",
                                labels={'Aggregate rating': 'Average Rating'})
                        st.plotly_chart(fig1)

                        # Filter for restaurants with ratings >= 4 for the DataFrame
                        high_rating_data = country_data[country_data['Aggregate rating'] >= 4]

                        # Display the DataFrame of top-rated restaurants with rating >= 4
                        st.write(f"Top rated restaurants in {selected_country} (Rating greater than 4):")
                        st.dataframe(high_rating_data[['Restaurant Name', 'Cuisines', 'Aggregate rating']])
                
                with subtab3:
                        # Country selection
                        country = st.selectbox("Select a Country:", df['Country'].unique(), key="unique_country_select_3")

                        # Filter data based on selected country and city
                        filtered_data = df[(df['Country'] == country)]

                        # Display pie chart for online delivery vs dine-in
                        st.subheader(f"Online Delivery vs Dine-in in {country}")
                       
                        # Check if both columns exist
                        if 'Has Table booking' in filtered_data.columns and 'Has Online delivery' in filtered_data.columns:
                        
                                # Count occurrences of each type
                                booking_counts = {'Has Table Booking': (filtered_data['Has Table booking'] == 'Yes').sum(),
                                                   'Has Online Delivery': (filtered_data['Has Online delivery'] == 'Yes').sum()}

                                # Check if there are any counts to display
                                if booking_counts['Has Table Booking'] > 0 or booking_counts['Has Online Delivery'] > 0:
                                        # Create a pie chart
                                        fig = px.pie(
                                        names=booking_counts.keys(),  # Booking types
                                        values=booking_counts.values(),  # Counts of each type
                                        labels={'Has Table Booking': 'Table Booking', 'Has Online Delivery': 'Online Delivery'},
                                        )
                                        # Display the pie chart
                                        st.plotly_chart(fig)
                                else:
                                        st.write("No data available for table booking or online delivery in this city.")
        

        with tab2:
                subtab1, subtab2, subtab3 = st.tabs(["Famous Cuisine", "Costlier Cuisine","Ratings"])

                with subtab1:
                        # Country selection
                        country = st.selectbox("Select a Country:", df['Country'].unique())

                        # City selection based on selected country
                        city = st.selectbox("Select a City:", df[df['Country'] == country]['City'].unique())

                        # Filter data based on selected country and city
                        filtered_data = df[(df['Country'] == country) & (df['City'] == city)]

                        # Display famous cuisines in a bar chart
                        st.subheader(f"Famous Cuisines in {city}, {country} (Based on Popularity and Ratings)")

                        # Check if there are any cuisines in the filtered data
                        if not filtered_data['Cuisines'].isnull().all():
                                # Group the data by Cuisines and calculate the mean rating and count for each cuisine
                                cuisine_stats = filtered_data.groupby('Cuisines').agg(
                                        average_rating=('Aggregate rating', 'mean'),
                                        count=('Cuisines', 'size')
                                ).sort_values(by=['average_rating', 'count'], ascending=[False, False])
                                
                                # Display all cuisines ranked by average rating and count in the city
                                st.write(f"All cuisines in {city} ranked by average rating and popularity:")
                                st.dataframe(cuisine_stats)

                                # Display the most famous cuisine based on both rating and count
                                most_famous_cuisine = cuisine_stats.index[0]
                                st.write(f"The most famous cuisine in {city} based on ratings and popularity is {most_famous_cuisine}.")
                
                with subtab2:
                        # Country selection with unique key
                        country = st.selectbox("Select a Country:", df['Country'].unique(), key="unique_country_select_1")

                        # City selection with unique key based on selected country
                        city = st.selectbox("Select a City:", df[df['Country'] == country]['City'].unique(), key="unique_city_select_1")

                        # Filter data based on selected country and city
                        filtered_data = df[(df['Country'] == country) & (df['City'] == city)]
                        # Display costlier cuisines in a pie chart
                        st.subheader(f"Costly Cuisines in {city}, {country} in INR")

                        # Check if there are any cuisines in the filtered data
                        if not filtered_data['Cuisines'].isnull().all():
                                # Group the data by Cuisines and calculate the average cost for each cuisine
                                cuisine_cost = filtered_data.groupby('Cuisines')['Price_INR'].mean().sort_values(ascending=False)
                                # Create a bar chart
                                fig = px.bar(
                                        x=cuisine_cost.index,  # Cuisine names
                                        y=cuisine_cost,  # Average cost
                                        title=f"Costlier Cuisines in {city}",
                                        labels={'x': 'Cuisine', 'y': 'Average Cost in INR'},  # Axis labels
                                        height=500  # Set height for better readability
                                )
                                st.plotly_chart(fig)
                                # Highlight the most costly cuisine
                                most_costly_cuisine = cuisine_cost.idxmax()
                                st.write(f"The costliest cuisine in {city} is **{most_costly_cuisine}**, with an average cost of  ₹ {cuisine_cost.max()}")

                with subtab3:
                        # Country selection
                        country = st.selectbox("Select a Country:", df['Country'].unique(), key="unique_country_select_2")

                        # Filter data based on selected country
                        filtered_data = df[df['Country'] == country]

                        # Display average ratings for cities in the country
                        st.subheader(f"Average Ratings for Cities in {country}")

                        # Check if there are any ratings in the filtered data
                        if 'City' in filtered_data.columns and 'Aggregate rating' in filtered_data.columns and not filtered_data['Aggregate rating'].isnull().all():
    
                                # Group the data by City and calculate the average rating for each city
                                average_ratings = filtered_data.groupby('City')['Aggregate rating'].mean().sort_values(ascending=False)

                                # Create a bar chart for average city ratings
                                fig = px.bar(
                                        x=average_ratings.index,  # City names
                                        y=average_ratings,  # Average ratings
                                        labels={'x': 'City', 'y': 'Average Rating'},  # Axis labels
                                        height=500  # Set height for better readability
                                )
                                
                                # Display the bar chart
                                st.plotly_chart(fig)

                                # Highlight the city with the highest average rating
                                highest_rated_city = average_ratings.idxmax()
                                st.write(f"The highest rated city in {country} is **{highest_rated_city}** with an average rating of {average_ratings.max():.2f}.")

                                
        with tab3:
                subtab5, subtab6, subtab7, subtab8 = st.tabs(["Dine-in vs Online","Average Cost","Costlier Cuisine","Ratings for city"])

                with subtab5:
                        # Filter for India
                        india_data = df[df['Country'] == 'India']

                        # Count occurrences of online delivery and dine-in options by city
                        online_delivery_counts = india_data[india_data['Has Online delivery'] == 'Yes'].groupby('City').size()
                        dine_in_counts = india_data[india_data['Has Table booking'] == 'Yes'].groupby('City').size()
                        # Calculate average cost for each city
                        average_costs = india_data.groupby('City')['Price_INR'].mean()
                        # Ensure both series have the same index by using reindex
                        combined_index = online_delivery_counts.index.union(dine_in_counts.index)
                        online_delivery_counts = online_delivery_counts.reindex(combined_index, fill_value=0)
                        dine_in_counts = dine_in_counts.reindex(combined_index, fill_value=0)

                        # Create a DataFrame from the aligned counts
                        data = pd.DataFrame({
                        'City': combined_index,
                        'Online Delivery': online_delivery_counts.values,
                        'Dine-In': dine_in_counts.values
                        })

                        # Melt the data to have a long-form DataFrame for plotly express
                        melted_data = data.melt(id_vars='City', value_vars=['Online Delivery', 'Dine-In'], 
                                                var_name='Delivery Type', value_name='Count')

                        # Create the bar chart using plotly express
                        fig = px.bar(melted_data, 
                                x='City', 
                                y='Count', 
                                color='Delivery Type', 
                                title='Online Delivery vs Dine-In in Cities of India',
                                labels={'Count': 'Count', 'City': 'City', 'Delivery Type': 'Type of Service'},
                                barmode='group')

                        # Display the chart
                        st.plotly_chart(fig)

                        dine_in_costs = india_data[india_data['Has Table booking'] == 'Yes'].groupby('City')['Price_INR'].mean()
                        online_delivery_costs = india_data[india_data['Has Online delivery'] == 'Yes'].groupby('City')['Price_INR'].mean()

                        # Sort the costs in descending order and select the top 5 cities for each type
                        top_dine_in_cities = dine_in_costs.sort_values(ascending=False).head(5)
                        top_online_delivery_cities = online_delivery_costs.sort_values(ascending=False).head(5)

                        # Create a combined DataFrame for visualization
                        top_cities_data = pd.DataFrame({
                        'City': top_dine_in_cities.index.tolist() + top_online_delivery_cities.index.tolist(),
                        'Cost': top_dine_in_cities.tolist() + top_online_delivery_cities.tolist(),
                        'Service Type': ['Dine-In'] * len(top_dine_in_cities) + ['Online Delivery'] * len(top_online_delivery_cities)
                        })

                        # Create a bar chart using Plotly Express
                        fig = px.bar(top_cities_data, 
                                x='City', 
                                y='Cost', 
                                color='Service Type', 
                                title='Top 5 Cities with Highest Costs for Dine-In and Online Delivery',
                                labels={'Cost': 'Average Cost (INR)', 'City': 'City', 'Service Type': 'Type of Service'},
                                barmode='group')

                        # Display the bar chart
                        st.plotly_chart(fig)

                        # Find the city with the highest cost for each type
                        city_highest_dine_in = dine_in_costs.idxmax()
                        city_highest_online_delivery = online_delivery_costs.idxmax()

                        # Get the corresponding maximum costs
                        highest_dine_in_cost = dine_in_costs.max()
                        highest_online_delivery_cost = online_delivery_costs.max()

                        # Display the results
                        st.write(f"The city with the highest dine-in cost is **{city_highest_dine_in}** with an average cost of **{highest_dine_in_cost:.2f}**.")
                        st.write(f"The city with the highest online delivery cost is **{city_highest_online_delivery}** with an average cost of **{highest_online_delivery_cost:.2f}**.")
                
                with subtab6:
                        # Filter for India
                        india_data = df[df['Country'] == 'India']
                        average_costs = india_data.groupby('City')['Price_INR'].mean()
                        average_costs_df = pd.DataFrame({
                        'City': average_costs.index,
                        'Average Cost': average_costs.values
                        })

                        # Create the bar chart using plotly express
                        fig = px.bar(average_costs_df, 
                                x='City', 
                                y='Average Cost', 
                                title='Average Spending per City in India',
                                labels={'Average Cost': 'Average Cost', 'City': 'City'})

                        # Display the chart
                        st.plotly_chart(fig)


                        # Sort and select the top five cities by average cost
                        top_5_cities = average_costs_df.sort_values(by='Average Cost', ascending=False).head(5)

                        # Create the bar chart using plotly express
                        fig = px.bar(top_5_cities, 
                                x='City', 
                                y='Average Cost', 
                                title='Top 5 Cities Spending the Most in India',
                                labels={'Average Cost': 'Average Cost', 'City': 'City'})

                        # Display the chart
                        st.plotly_chart(fig)

                with subtab8:
                        # Filter the data where Country is India
                        india_data = df[df['Country'] == 'India']

                        # City selection
                        city = st.selectbox("Select a City:", india_data['City'].unique(), key="unique_city_select_2")

                        # Filter data based on the selected city
                        filtered_data = india_data[india_data['City'] == city]

                        # Group the filtered data by rating text and count occurrences
                        rating_counts = filtered_data['Rating text'].value_counts()

                        # Create a pie chart
                        fig = px.pie(
                        names=rating_counts.index,
                        values=rating_counts.values,
                        title=f"Restaurant Ratings Distribution in {city}",
                        labels={'Rating Text': 'Rating', 'value': 'Count'}
                        )

                        # Display the pie chart
                        st.plotly_chart(fig)

                        # Get unique rating texts
                        rating_counts = filtered_data['Rating text'].unique()

                        # Capture the click event
                        selected_rating = st.selectbox("Select a Rating to view Restaurants:", rating_counts)

                        # Filter restaurants based on the selected rating
                        restaurants_with_selected_rating = filtered_data[filtered_data['Rating text'] == selected_rating]

                        # Display the list of restaurants with the selected rating
                        if not restaurants_with_selected_rating.empty:
                                st.write(f"Restaurants in {city} with a rating of **{selected_rating}**:")
                        
                                # Create a DataFrame with selected columns
                                result_df = restaurants_with_selected_rating[['Restaurant Name', 'Cuisines', 'Aggregate rating', 'Price_INR']]
                        
                                # Display the DataFrame
                                st.dataframe(result_df)

                with subtab7:
                        # Filter the data where Country is India
                        india_data = df[df['Country'] == 'India']

                        # City selection
                        city = st.selectbox("Select a City:", india_data['City'].unique(), key="unique_city_select_3")

                        # Filter data based on the selected city
                        filtered_data = india_data[india_data['City'] == city]

                        # Check if there are any cuisines in the filtered data
                        if not filtered_data['Cuisines'].isnull().all():
                                # Group the data by Cuisines and calculate the average cost for each cuisine
                                cuisine_cost = filtered_data.groupby('Cuisines')['Price_INR'].mean().sort_values(ascending=False)
                                # Create a bar chart
                                fig = px.bar(
                                        x=cuisine_cost.index,  # Cuisine names
                                        y=cuisine_cost,  # Average cost
                                        title=f"Costlier Cuisines in {city}",
                                        labels={'x': 'Cuisine', 'y': 'Average Cost in INR'},  # Axis labels
                                        height=500  # Set height for better readability
                                )
                                st.plotly_chart(fig)
                                # Highlight the most costly cuisine
                                most_costly_cuisine = cuisine_cost.idxmax()
                                st.write(f"The costliest cuisine in {city} is **{most_costly_cuisine}**, with an average cost of  ₹ {cuisine_cost.max()}")

if selected == "Home":
        st.subheader(':red[Domain :]')
        st.markdown('<h5>Food Industry',unsafe_allow_html=True)

        st.subheader(':red[Skills & Technologies :]')
        st.markdown('<h5> Python scripting, Data Preprocessing,  Streamlit, Plotly, Streamlit ',unsafe_allow_html=True)

        st.subheader(':red[Overview :]')
        st.markdown('''  <h5>Data Engineering  <br>     
                        <li> Currency Conversion: Add a new column to convert currencies into Indian Rupees (INR).
                        <li> Comparison Plot: Create a visual comparison of the Indian Rupee with other countries' currencies.''',unsafe_allow_html=True)
        
        st.markdown('''  <h5>Dashboard Development <br>     
                        <li> The dashboard offers insights through various interactive features such as
                        visualize metrics through two customizable charts such as customer count, total sales, and popular cuisines and many more.''',unsafe_allow_html=True)
        
        st.markdown('''  <h5>Expected Outcomes <br>     
                        <li> A comprehensive analysis of Zomato’s business performance across different regions and cuisines.
                        <li> Insights that enable better decision-making for restaurants, investors, and Zomato itself.
                        <li> A user-friendly dashboard accessible via a web app for easy interaction with the analysis..''',unsafe_allow_html=True)
