import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import streamlit as st
import requests
import plotly.express as px
from src.utils.grape_distribution import *

req = requests.get('https://economia.awesomeapi.com.br/last/USD-BRL')

COMMERCIALIZED_VALUE = float(req.json().get('USDBRL').get('bid'))

st.set_page_config(layout="wide", page_title='Wine Market', page_icon=':wine_glass:')

# CSS to remove first column of each table (dataframe index)
hide_table_row_index = """
        <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
        </style>
"""
st.markdown(hide_table_row_index, unsafe_allow_html=True)



st.title('Wine Market')

tab1, tab2, tab3 = st.tabs(["Wine Evaluation", "Wine grapes by country", "About"])

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
        ##### Average Wine Prices
        <ol>
            <li>Auction prices are excluded.</li>
            <li>All units and prices are converted to a 1000ml equivalent.</li>
            <li>Average prices are calculated from a 'topped and tailed' data set. We remove the highest and lowest 20% to prevent the average being skewed by pricing errors. When only a small number of prices are available the median is used.</li>
        </ol>
    ''', unsafe_allow_html=True)
    
    italian_quality = pd.read_csv('content/italian_wines_2_scores.csv')
    french_quality = pd.read_csv('content/french_wines_2_scores.csv')
    spanish_quality = pd.read_csv('content/spanish_wines_2_scores.csv')
    brazilian_quality = pd.read_csv('content/brazilian_wine_scores.csv')
    portuguese_quality = pd.read_csv('content/portuguese_wines_2_scores.csv')
    chilean_quality = pd.read_csv('content/chilean_wines_2_scores.csv')
    argentinean_quality = pd.read_csv('content/argentinean_wines_2_scores.csv')
    
    italian_quality['avg_price_liter'] = italian_quality['avg_price_liter'] / COMMERCIALIZED_VALUE
    french_quality['avg_price_liter'] = french_quality['avg_price_liter'] / COMMERCIALIZED_VALUE
    spanish_quality['avg_price_liter'] = spanish_quality['avg_price_liter'] / COMMERCIALIZED_VALUE
    brazilian_quality['avg_price_liter'] = brazilian_quality['avg_price_liter'] / COMMERCIALIZED_VALUE
    portuguese_quality['avg_price_liter'] = portuguese_quality['avg_price_liter'] / COMMERCIALIZED_VALUE
    chilean_quality['avg_price_liter'] = chilean_quality['avg_price_liter'] / COMMERCIALIZED_VALUE
    argentinean_quality['avg_price_liter'] = argentinean_quality['avg_price_liter'] / COMMERCIALIZED_VALUE
    
    italian_quality['score'] = italian_quality['score'].fillna(italian_quality['score'].mean())
    french_quality['score'] = french_quality['score'].fillna(french_quality['score'].mean())
    spanish_quality['score'] = spanish_quality['score'].fillna(spanish_quality['score'].mean())
    brazilian_quality['score'] = brazilian_quality['score'].fillna(brazilian_quality['score'].mean())
    portuguese_quality['score'] = portuguese_quality['score'].fillna(portuguese_quality['score'].mean())
    chilean_quality['score'] = chilean_quality['score'].fillna(chilean_quality['score'].mean())
    argentinean_quality['score'] = argentinean_quality['score'].fillna(argentinean_quality['score'].mean())
    
    median_wines = (
        [
            italian_quality['score'].mean(numeric_only=True).round(1),
            italian_quality['avg_price_liter'].mean(numeric_only=True).round(2),
        ],
        [
            french_quality['score'].mean(numeric_only=True).round(1),
            french_quality['avg_price_liter'].mean(numeric_only=True).round(2),
        ],
        [
            spanish_quality['score'].mean(numeric_only=True).round(1),
            spanish_quality['avg_price_liter'].mean(numeric_only=True).round(2)
        ],
        [
            brazilian_quality['score'].mean(numeric_only=True).round(1),
            brazilian_quality['avg_price_liter'].mean(numeric_only=True).round(2),
        ],
        [
            portuguese_quality['score'].mean(numeric_only=True).round(1),
            portuguese_quality['avg_price_liter'].mean(numeric_only=True).round(2)
        ],
        [
            chilean_quality['score'].mean(numeric_only=True).round(1),
            chilean_quality['avg_price_liter'].mean(numeric_only=True).round(2)
        ],
        [
            argentinean_quality['score'].mean(numeric_only=True).round(1),
            argentinean_quality['avg_price_liter'].mean(numeric_only=True).round(2)
        ]
    )

    median_wines = pd.DataFrame(median_wines, index=['Italy', 'France', 'Spain', 'Brazil', 'Portugal', 'Chile', 'Argentina'], columns=['score', 'avg_price_liter']).reset_index()
    median_wines.columns = ['country', 'score', 'avg_price_liter']
    
    fig = plt.figure(figsize=(8, 4))
    ax = sns.pointplot(data=median_wines, x='score', y='avg_price_liter', hue='country', scale=1.5, palette='cubehelix')
    ax.set_ylabel("AVG Price liter")
    ax.set_xlabel("Score")
    ax.set_title("Score x AVG Price liter")
    ax.yaxis.set_major_formatter(ticker.StrMethodFormatter("${x:,.2f}"))
    plt.legend(bbox_to_anchor=(1.05, 1.05), loc='upper left', borderaxespad=0, title="Country")
    plt.ylim(0, 150)
    plt.grid(color='gray', linestyle='--', linewidth=0.3)
    
    
    st.divider()
    
    st.pyplot(fig)
    
    
with tab2:
    # data
    italian_quality = pd.read_csv('content/italian_wines_2_scores.csv')
    french_quality = pd.read_csv('content/french_wines_2_scores.csv')
    spanish_quality = pd.read_csv('content/spanish_wines_2_scores.csv')
    brazilian_quality = pd.read_csv('content/brazilian_wine_scores.csv')
    portuguese_quality = pd.read_csv('content/portuguese_wines_2_scores.csv')
    chilean_quality = pd.read_csv('content/chilean_wines_2_scores.csv')
    argentinean_quality = pd.read_csv('content/argentinean_wines_2_scores.csv')
    
    italian_grape_distribution = getGrapeDistribution(italian_quality)
    french_grape_distribution = getGrapeDistribution(french_quality)
    spanish_grape_distribution = getGrapeDistribution(spanish_quality)
    brazilian_grape_distribution = getGrapeDistribution(brazilian_quality)
    portuguese_grape_distribution = getGrapeDistribution(portuguese_quality)
    chilean_grape_distribution = getGrapeDistribution(chilean_quality)
    argentinean_grape_distribution = getGrapeDistribution(argentinean_quality)
    
    
    # Displaying the data
    st.title("Italian Grapes")
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.pie(italian_grape_distribution, values='Used in how many wines?', names='Grape', title='')
        st.plotly_chart(fig)
    
    with col2:
        st.table(italian_grape_distribution)
        
    st.markdown('''
    <h5>Italy's geography and climate</h5>
    <p>
        Italy is unmistakable on the map, with its iconic, boot-like shape. 
        Effectively one vast peninsula jutting into the Mediterranean, the country runs NW–SE for 1,100 kilometers (700 miles) along a strong, steep spine formed by the Apennine Mountains. 
        On its western side, in the Tyrrhenian Sea, lie its two island regions, Sicily and Sardinia.
        It is hard to summarize in any useful way the climate of such a long and topographically varied country. 
        Vineyards here are planted anywhere from sea-level in eastern Emilia-Romagna to around 1,300 meters (4,200ft) in the alpine Aosta Valley. 
        Latitude is also a key factor here; at 46°N, the northern Alto Adige region lies a full 11 degrees north of Pantelleria, leaving it some 1,100km (680 miles) further from the warmth of the equator.
    </p>
    ''', unsafe_allow_html=True)
        
    st.divider()
    ##############################
    st.title("French Grapes")
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.pie(french_grape_distribution, values='Used in how many wines?', names='Grape', title='')
        st.plotly_chart(fig)
    
    with col2:
        st.table(french_grape_distribution)
        
    
    st.markdown('''
    ####
    <h5>France geography and climate</h5>
    <p>
        The diversity of French wine is due, in part, to the country's wide range of climates. 
        Champagne, its most northerly region, has one of the coolest climates anywhere in the wine-growing world – in stark contrast to the warm, dry Rhône Valley 560km (350 miles) away in the southeast.
        Bordeaux, in the southwest, has a maritime climate heavily influenced by the Atlantic ocean to its west and the various rivers that wind their way between its vineyards. 
        Far from any oceanic influence, eastern regions such as Burgundy and Alsace have a continental climate, with warm, dry summers and cold winters.
        In France's deep south, Provence and Languedoc-Roussillon enjoy a definitively Mediterranean climate, characterized by hot summers and relatively mild winters. 
        The South West, however, finds itself influenced by by the Mediterranean and Atlantic climates (it is a geographical inbetweener – often expressed in the style and makeup of its wines).
    </p>
    ''', unsafe_allow_html=True)
    
    st.divider()
    ##############################
    st.title("Spanish Grapes")
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.pie(spanish_grape_distribution, values='Used in how many wines?', names='Grape', title='')
        st.plotly_chart(fig)
    
    with col2:
        st.table(spanish_grape_distribution)
        
    st.markdown('''
    ####
    <h5>Spain geography and climate</h5>
    <p>
        The topography plays a fundamental role in defining Spain's many wine styles. From cool, green Galicia and the snow-capped Pyrenees in the north, via the parched central plateau, to sandy, sunny Andalucia in the south, the Spanish landscape is very diverse. The country spans seven degrees of latitude (36°N to 43°N), leaving 800 kilometers (500 miles) between its Atlantic and Mediterranean coasts.
        Between these two very different coastlines are various mountain ranges, each of which has its own particular effect on the local landscape and climate. The Cordillera Cantábrica range, for example, creates dramatic contrasts between the lush, green land on its northern, Atlantic side and dry, dusty Castilla y León on its southern, inland side.
        Among the mountain peaks and plateaux rise the rivers on which so many Spanish vineyards depend. These are significant not only as a source of much-needed water, but also because of their impact on local soils and mesoclimates.
        The most significant of the Spanish 'wine rivers' are the Miño, Duero, Tajo, Guadiana and Ebro. The first four of these flow westwards into Portugal, where they become the Minho, Douro, Tejo and Guadiana (see Portugal) respectively.
        The eastward-flowing Ebro, however, remains purely Spanish for its entire journey, and passes through some of the country's most important vineyard areas. On its descent from the mountains of Cantabria, the Ebro flows through Castilla y León, El Pais Vasco (or the Basque Country, as it is sometimes referred to), Navarra, Rioja and Aragon, before arriving at the Mediterranean coast in Catalonia.
        As climate, geology and topography vary around Spain, so do the wine styles. The cool vineyards of the far north and northwest create light, crisp, white wines, exemplified by Rías Baixas and particularly Txakoli.
        Those in warmer, drier regions further inland tend towards mid-bodied, fruit-driven reds such as Rioja, Ribera del Duero and Bierzo. Those close to the Mediterranean can produce heavier, more powerful reds (e.g. Jumilla), except in higher-altitude districts, wh
    </p>
    ''', unsafe_allow_html=True)
    
    
    st.divider()
    ##############################
    st.title("Brazilian Grapes")
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.pie(brazilian_grape_distribution, values='Used in how many wines?', names='Grape', title='')
        st.plotly_chart(fig)
    
    with col2:
        st.table(brazilian_grape_distribution)
        
        
    st.markdown('''
    ####
    <h5>Brazilian geography and climate</h5>
    <p>
        With roughly 83,000 hectares (205,000 acres) of vineyard, it ranks just behind its near-neighbors Argentina and Chile in terms of acreage under vine. Only a small proportion (about 10 percent) of these acres are planted with Vitis vinifera vines, however this large acreage does not translate into large volumes of quality wine.
        There are concerted efforts underway to improve this ratio. Although not yet recognized on an international scale, the quality of Brazilian wines is increasing year on year.
        Brazil's best-known wines are arguably its sparkling whites. There are some Champagne method wines made from Pinot Noir and Chardonnay. Many are made in a style similar to Italian spumante.
        Despite spanning a full 39 degrees of latitude (5°N to 34°S), this vast nation lies largely outside the 'wine belt' (the band of latitudes in which effective viniculture is traditionally thought possible). The southern hemisphere wine belt encircles the globe between 30°S and 45°S, leaving very little room for Brazil to develop its vineyard area.
    </p>
    ''', unsafe_allow_html=True)

    
    st.divider()
    ##############################
    st.title("Portuguese Grapes")
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.pie(portuguese_grape_distribution, values='Used in how many wines?', names='Grape', title='')
        st.plotly_chart(fig)
    
    with col2:
        st.table(portuguese_grape_distribution)    
    
    
    st.markdown('''
    ####
    <h5>Portugal geography and climate</h5>
    <p>
        Portugal's temperate, predominantly maritime climate has a great deal to offer winemakers. The country's portfolio of terroirs is not as broad as that of, say, France or Italy, but there is significant variation nonetheless between its mountains, river valleys, sandy littoral plains and limestone-rich coastal hills.
        The high levels of rainfall that blow in from the western Atlantic are a boon to those seeking high yields from their vineyards. However these showers bring a significantly increased risk of fungal problems in all but the best-ventilated sites.
    </p>
    ''', unsafe_allow_html=True)
    
    st.divider()
    ##############################
    st.title("Chilean Grapes")
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.pie(chilean_grape_distribution, values='Used in how many wines?', names='Grape', title='')
        st.plotly_chart(fig)
    
    with col2:
        st.table(chilean_grape_distribution)
        
    
    st.markdown('''
    ####
    <h5>Chile geography and climate</h5>
    <p>
        Chile spans 4300 kilometers (2700 miles) of land running north-south between the Pacific Ocean and the Andes Mountains. The topography is very favorable to viticulture, and despite the fact that Chile is only 160 kilometers (100 miles) wide, most climatic variation in the wine-growing regions happens from east to west, rather than from north to south.
        The Pacific, with its Antarctic Humboldt Current, brings cooling breezes to more coastal vineyards in regions such as the Casablanca and Limari valleys. Meanwhile the sheltering presence of the Coastal mountain range makes Chile's Central Valley relatively warm and dry.
        Along the eastern edge of the country, in the foothills of the Andes, high altitudes and abundant meltwater rivers make for a different terroir again. With the Pacific Ocean on one side and the forbidding barrier of the Andes on the other, Chile's vineyards have remained protected from the phylloxera aphid.
    </p>
    ''', unsafe_allow_html=True)
    
    st.divider()
    ##############################
    st.title("Argentinean Grapes")
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.pie(argentinean_grape_distribution, values='Used in how many wines?', names='Grape', title='')
        st.plotly_chart(fig)
    
    with col2:
        st.table(argentinean_grape_distribution)
        
    st.markdown('''
    ####
    <h5>Argentina geography and climate</h5>
    <p>
        Covering just over one million square miles (2.8 million sq km), Argentina is the second-largest country in South America. It stretches from the southern border of Bolivia in the north to the southern tip of the continent.
        It is home to a vast array of landscapes, from the rocky peaks of the Andes in the west to the fertile Pampas lowlands in the east. Most viticulture in Argentina takes place in the foothills of the Andes.
        Of its wine regions, Mendoza is, without doubt, the largest and best-known in the country, often producing great wines to ciritcal acclaim. Here, desert landscapes and high altitudes combine to make a terroir that gives rise to aromatic, intensely flavored reds.
        Vineyards in the Mendoza region reach as high as 1,500m (5,000ft) above sea level. Here, increased levels of solar radiation and a high diurnal temperature variation make for a long, slow ripening period, leading to balanced sugars and acidity in the grapes.
        Mendoza's position in the rain shadow of the Andes means that there is little rainfall, and irrigation is effectively supplied by Andean meltwater.
        Further north, the regions of Salta and Catamarca are even higher. A world-topping vineyard owned by Bodega Colomé in Molinos sits at 3000m (9,900ft) – higher than the peak of Mount St. Helens in the Pacific Northwest of America.
        Low latitudes in this corner of Argentina – which, at 22°N to 28°N, are considerably closer to the Equator than any European wine region – are tempered by the high altitude and cold mountain air. Here, Argentina's signature aromatic white grape, Torrontés, is grown, making an pungent, intensely floral, white wine.
    </p>
    ''', unsafe_allow_html=True)
    
    
with tab3:
    st.markdown('''
    <h5>Sources:</h5>
    <ul>
        <li>
            <a>https://www.wine-searcher.com/</a>
        </li>
        <li>
            <a>http://vitibrasil.cnpuv.embrapa.br/</a>
        </li>
    </ul>            
    ''', unsafe_allow_html=True)