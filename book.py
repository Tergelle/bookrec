import streamlit as st
import pandas as pd

# Loading the data
df = pd.read_csv('Books_df.csv')

# Dropping missing values from the Author column
df = df.dropna(subset=['Author'])

# Filtering the book types 
book_types = ['Paperback', 'Kindle Edition', 'Audible Audiobook', 'Hardcover']
df = df[df['Type'].isin(book_types)]

# Converting the Indian Amazon domain to US Amazon 
df['URLs'] = df['URLs'].str.replace('.in', '.com')

# Cleaning 'Price' column by removing non-numeric characters and converting to numeric
df['Price'] = df['Price'].replace('[₹,]', '', regex=True)
df['Price'] = pd.to_numeric(df['Price'], errors='coerce')

# Drop missing values from the Price column
df = df.dropna(subset=['Price'])

# Convert INR prices to approximate USD prices
exchange_rate = 84.0
df['price_usd_approx'] = df['Price'] / exchange_rate

st.title("Book Recommendation App")

# Sidebar for user input
with st.sidebar:
    st.header("Filter Options")
    genre = st.selectbox("Select Genre", df['Main Genre'].unique())
    book_type = st.selectbox("Select Book Type", df['Type'].unique())
    min_rating, max_rating = st.slider("Select Rating Range", 0.0, 5.0, (3.0, 4.0))
    min_price, max_price = st.slider("Select Price Range (USD)", 0.0, df['price_usd_approx'].max(), (5.0, 50.0))
    get_result = st.button("Get Result")

if get_result:
    filtered_data = df[(df['Main Genre'] == genre) & 
                       (df['Type'] == book_type) & 
                       (df['Rating'] >= min_rating) & 
                       (df['Rating'] <= max_rating) &
                       (df['price_usd_approx'] >= min_price) &
                       (df['price_usd_approx'] <= max_price)]

    filtered_data = filtered_data.sort_values(by=['No. of People rated'], ascending=False)

    #Bar chart for recommended books by price
    if not filtered_data.empty:
        st.write("Top Recommended Books by Price (USD Approx.)")
        st.bar_chart(data=filtered_data.set_index('Title')['price_usd_approx'])

        # Display detailed information for each book below the bar chart
        for index, row in filtered_data.iterrows():
            st.write(f"**Title**: {row['Title']}")
            st.write(f"**Author**: {row['Author']}")
            st.write(f"**Rating**: {row['Rating']} / 5")
            st.write(f"**Price (USD Approx.)**: ${row['price_usd_approx']:.2f}")
            st.write(f"**Number of People Rated**: {row['No. of People rated']}")
            st.markdown(f"[View on Amazon]({row['URLs']})")
            st.write("---")
    else:
        st.write("No books found with the selected criteria.")
