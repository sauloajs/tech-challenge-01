import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import streamlit as st

st.title('Wine Market :wine_glass:')

tab1, tab2 = st.tabs(["Wine Evaluation", "Wine Harvest"])

with tab1:
    evaluations = pd.DataFrame({
        'Scores' : [
            '95~100',
            '90~94',
            '85~89',
            '80~84',
            '75~79',
            '50~74'
        ],
        'Explanation': [
            'Classic: a great wine',
            'Outstanding: a wine of superior character and style',
            'Very good: a wine with special qualities',
            'Good: a solid, well-made wine',
            'Mediocre: a drinkable wine that may have minor flaws',
            'Not recommended',
        ]
    })
    
    
    
    st.caption('Top wine producers countries wine evaluations and avg price')
    
    st.markdown('''
        ##### Wine Scores Methodology    
    ''')
    st.caption('A wine score is the quickest, simplest way for a wine critic to communicate their opinion about the quality of a wine. Often found alongside tasting notes, wine scores help consumers and collectors decide which wines to buy, and can be a powerful marketing tool.')
    
    st.markdown('''
        ##### 100-Point Scale
        <p>The 100-point wine-scoring scale was popularized by Wine Spectator magazine and by Robert Parker in his Wine Advocate newsletter. The effect of a high score from either publication is hard to understate, and can make or break a wine brand (see these lists of Wine Spectator Top 100 Wines and Robert Parker 100-Point Wines).</p>
        <p>There are many who question the value of the 100-point scale, typically because almost all wines evaluated fall within a narrow band between 85 and 100 points. The system is based on the American high-school marking system, so the scale starts at 50 (rather than 0), which has led to further criticism. Despite this the 100-point scale is used by more and more critics amateur and professional with each year that passes.</p>
    ''', unsafe_allow_html=True)
    
    st.table(evaluations)
    
    st.markdown('''
        #### Average Wine Prices
        <ol>
            <li>Auction prices are excluded.</li>
            <li>All units and prices are converted to a 1000ml equivalent.</li>
            <li>Average prices are calculated from a 'topped and tailed' data set. We remove the highest and lowest 20% to prevent the average being skewed by pricing errors. When only a small number of prices are available the median is used.</li>
        </ol>
    ''', unsafe_allow_html=True)