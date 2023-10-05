import streamlit as st
import plotly.express as px

st.set_page_config(layout="wide")
try:
    conn = st.experimental_connection('data', type='sql')
except:
    st.error('Database Connection Error')

try:
    st.subheader("Filters")

    cols_10 = st.columns([1, 1])
    with cols_10[0]:
        price = st.slider('Price', 0, 1000, (0, 500))
    with cols_10[1]:
        nights = st.slider('Nights', 1, 100, (1, 100))

    cols_20 = st.columns([1, 1, 1])
    with cols_20[0]:
        all_room_types = conn.query('SELECT room_type FROM listings_summary_dec18 GROUP BY room_type')['room_type'].unique()
        room_type = st.selectbox('Room Type', ['Any'] + list(all_room_types)).replace('Any', '%')
    with cols_20[1]:
        all_neighbourhoods = conn.query('SELECT neighbourhood FROM listings_summary_dec18 GROUP BY neighbourhood')['neighbourhood'].unique()
        neighbourhood = st.selectbox('Neighbourhood', ['Any'] + list(all_neighbourhoods)).replace('Any', '%')
    with cols_20[2]:
        filter_name = st.selectbox('Filter', ['room_type', 'neighbourhood', 'minimum_nights'])
        


    st.subheader("Results")
    df = conn.query(f'SELECT name, price_2 as price, neighbourhood, room_type, minimum_nights_2 as minimum_nights, number_of_reviews, availability_365 FROM listings_summary_dec18 WHERE (price_2 >= {price[0]} AND price_2 <= {price[1]}) AND (minimum_nights_2 >= {nights[0]} AND minimum_nights_2 <= {nights[1]}) AND room_type LIKE \'{room_type}\' AND neighbourhood LIKE \'{neighbourhood}\'')
    cols_30 = st.columns([1,1,1,1])
    with cols_30[0]:
        st.text("Average Price")
        st.text(str(df['price'].mean()))

    with cols_30[1]:
        st.text("Average Nights")
        st.text((df['minimum_nights'].mean()))

    cols_40 = st.columns([1, 1])
    with cols_40[0]:
        #filter_name = st.selectbox('Filter', ['room_type', 'neighbourhood', 'minimum_nights'])
        
        fig = px.pie(df, names=filter_name, height=300, width=200)
        fig.update_layout(margin=dict(l=20, r=20, t=30, b=0),)
        st.plotly_chart(fig, use_container_width=True)

    with cols_40[1]:
        st.dataframe(df)
except:
    st.error('Something Went Wrong')