import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import requests

BASE_URL = "https://api.coingecko.com/api/v3"
SUPPORTED_CURRENCIES = []
SUPPORTED_COINS = []

def clipDecimal(number, precision=1):
    return round(float(number), precision)

def format_price_change(percentage_change):
        if clipDecimal(percentage_change) > 0:
            return f"<span style='color:#32ca5b;'><span style='font-size: 10px;'>▲</span> {clipDecimal(percentage_change)}%</span>"
        else:
            return f"<span style='color:#ff3a33;'>🔻 {clipDecimal(percentage_change)}%</span>"

def showTrendingAssets():
    URL = f"{BASE_URL}/search/trending"

    try:
        response = requests.get(URL)
        data = response.json()
        if response.status_code == 200:
            st.markdown("## Trending Assets")

            cryptocurrency = st.selectbox("Select an asset:", options=[None, "Cryptocurrency", "NFTs", "Categories"])

            if cryptocurrency == "Cryptocurrency":
                
                table_html = """
                    <table style='width:100%;border-collapse: collapse;'>
                        <tr>
                            <th>#</th>
                            <th>Coin Name</th>
                            <th>Market Cap Rank</th>
                            <th>Price</th>
                            <th>24h</th>
                            <th>Market Cap</th>
                            <th>Total Volume</th>
                            <th>Sparkline</th>
                        </tr>
                """
                for i, coin in enumerate(data["coins"]):
                    coin=coin["item"]
                    table_html += "<tr>"
                    table_html += f"<td>{i+1}</td>"
                    table_html += f"<td><img src='{coin['thumb']}' width='24' /> &nbsp; {coin['name']} &nbsp; <span style='color:gray; font-size: small;'>{coin['symbol']}</span></td>"
                    table_html += f"<td>{coin['market_cap_rank']}</td>"
                    table_html += f"<td>${clipDecimal(coin['data']['price'], 3)}</td>"
                    table_html += f"<td>{format_price_change(coin['data']['price_change_percentage_24h']['usd'])}</td>"
                    table_html += f"<td>{coin['data']['market_cap']}</td>"
                    table_html += f"<td>{coin['data']['total_volume']}</td>"
                    table_html += f"<td><img src='{coin['data']['sparkline']}' width='100' /></td>"
                    table_html += "</tr>"
                table_html += "</table>"

                st.markdown(table_html, unsafe_allow_html=True)

            elif cryptocurrency == "NFTs":
                    
                table_html = """
                    <table style='width:100%;border-collapse: collapse;'>
                        <tr>
                            <th>#</th>
                            <th>Name</th>
                            <th>Floor Price</th>
                            <th>24h Price Change</th>
                            <th>24h Volume</th>
                            <th>Average Sale Price</th>
                            <th>Sparkline</th>
                        </tr>
                """
                for i, nft in enumerate(data['nfts']):
                    table_html += "<tr>"
                    table_html += f"<td>{i+1}</td>"
                    table_html += f"<td> <img src='{nft['thumb']}' width='50' /> &nbsp; {nft['name']} &nbsp; <span style='color:gray; font-size: small;'>{nft['symbol']}</span></td>"
                    table_html += f"<td>{nft['data']['floor_price']}</td>"
                    table_html += f"<td>{format_price_change(nft['data']['floor_price_in_usd_24h_percentage_change'])}</td>"
                    table_html += f"<td>{nft['data']['h24_volume']}</td>"
                    table_html += f"<td>{nft['data']['h24_average_sale_price']}</td>"
                    table_html += f"<td><img src='{nft['data']['sparkline']}' width='100' /></td>"
                    table_html += "</tr>"
                table_html += "</table>"

                st.markdown(table_html, unsafe_allow_html=True)

            elif cryptocurrency == "Categories":

                table_html = """
                    <table style='width:100%;border-collapse: collapse;'>
                        <tr>
                            <th>#</th>
                            <th>Name</th>
                            <th>Coins Count</th>
                            <th>24h Market Cap Change</th>
                            <th>Market Cap</th>
                            <th>Total Volume</th>
                            <th>Sparkline</th>
                        </tr>
                """
                for i, category in enumerate(data["categories"]):
                    table_html += "<tr>"
                    table_html += f"<td>{i+1}</td>"
                    table_html += f"<td>{category['name']}</td>"
                    table_html += f"<td>{category['coins_count']}</td>"
                    table_html += f"<td>{format_price_change(category['data']['market_cap_change_percentage_24h']['usd'])}</td>"
                    table_html += f"<td>${category['data']['market_cap']}</td>"
                    table_html += f"<td>${category['data']['total_volume']}</td>"
                    table_html += f"<td><img src='{category['data']['sparkline']}' width='100' /></td>"
                    table_html += "</tr>"
                
                table_html += "</table>"
                st.markdown(table_html, unsafe_allow_html=True)

        else:
            st.error("API call not successful. Please try again later.")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

@st.cache_data(ttl=86400)
def getSupportedCurrencies():
    global SUPPORTED_CURRENCIES

    URL = f"{BASE_URL}/simple/supported_vs_currencies"
    try:
        response = requests.get(URL)
        data = response.json()
        if response.status_code == 200:
            SUPPORTED_CURRENCIES = data
        else:
            st.error("API call not successful. Please try again later.")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
 
@st.cache_data(ttl=86400)
def getSupportedCoins():
    global SUPPORTED_COINS

    URL = f"{BASE_URL}/coins/list"
    try:
        response = requests.get(URL)
        data = response.json()
        if response.status_code == 200:
            SUPPORTED_COINS = [coin['id'] for coin in data]
        else:
            st.error("API call not successful. Please try again later.")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

def searchCryptocurrency(query):
    URL = f"{BASE_URL}/search?query={query}"
    try:
        response = requests.get(URL)
        data = response.json()
        if response.status_code == 200:
            results = data['coins']
            if results:
                st.title(f"Search Results for '{query}'")

                num_columns = 3
                for row in range(0, len(results), num_columns):
                    row_coins = results[row:row + num_columns]
                    cols = st.columns(len(row_coins))
                    for col, coin in zip(cols, row_coins):
                        with col:
                            st.markdown(
                                f"<div style='text-align: center;'><img src='{coin['large']}' style='width: 100px; height: auto;' /><br>"
                                f"<span style='font-size: large;'>{coin['name']}</span> &nbsp; <span style='color:gray; font-size: small;'>{coin['symbol']}</span> </br>"
                                f"<span style='color: gray; font-size: small;'>Market Cap Rank: {coin['market_cap_rank']}</span> </br></div>",
                                unsafe_allow_html=True
                            )
                            st.markdown("---")
            else:
                st.error("No results found.")
        else:
            st.error("API call not successful. Please try again later.")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

def cryptoConversion(from_coin, to_coin):
    URL = f"{BASE_URL}/simple/price?ids={from_coin}&vs_currencies={to_coin}"
    try:
        response = requests.get(URL)
        data = response.json()
        if response.status_code == 200:
            st.markdown("### Exchange Rates")
            price = data[from_coin][to_coin]
            st.markdown(f"**{from_coin.upper()} = {price:,.2f} {to_coin.upper()}**")
        else:
            st.error("API call not successful. Please try again later.")
    except Exception as e:
        st.error(f"The conversion from {from_coin.upper()} to {to_coin.upper()} is not valid. Please check your inputs.")

def showTopCryptocurrency():
    URL = f"{BASE_URL}/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=10"
    try:
        response = requests.get(URL)
        data = response.json()
        if response.status_code == 200:
            st.markdown("### Top 10 Cryptocurrency")
            st.markdown("On Market Cap")

            for coin in data:
                col1, col2 = st.columns([1, 3])

                with col1:
                    st.image(coin['image'], width=100)

                with col2:
                    st.subheader(f"{coin['name']} ({coin['symbol'].upper()})")
                    st.write(f"**Current Price**: ${coin['current_price']:,.2f}")
                    st.write(f"**Market Cap**: ${coin['market_cap']:,.0f}")
                    st.write(f"**24h Price Change**: {format_price_change(coin['price_change_percentage_24h'])}", unsafe_allow_html=True)
                    st.markdown("---")
        else:
            st.error("API call not successful. Please try again later.")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

def showCryptoMarketOverview():
    URL = f"{BASE_URL}/global"

    try:
        response = requests.get(URL)
        data = response.json()
        if response.status_code == 200:
            st.markdown("### Cryptocurrency Market Overview")
            
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric(label="Active Cryptocurrencies", value=data['data']['active_cryptocurrencies'])

            with col2:
                st.metric(label="Ongoing ICOs", value=data['data']['ongoing_icos'])

            with col3:
                st.metric(label="Ended ICOs", value=data['data']['ended_icos'])

            with col4:
                st.metric(label="Markets", value=data['data']['markets'])

            st.markdown(f"Market Capitalization Change (24h) {format_price_change(data['data']['market_cap_change_percentage_24h_usd'])}", unsafe_allow_html=True)


            coins = list(data['data']['total_volume'].keys())
            volume = list(data['data']['total_volume'].values())

            coin_volume_pairs = list(zip(coins, volume))
            top_10_coin_volume_pairs = sorted(coin_volume_pairs, key=lambda x: x[1], reverse=True)[:10]

            top_10_coins = [coin for coin, _ in top_10_coin_volume_pairs]
            top_10_volumes = [vol for _, vol in top_10_coin_volume_pairs]
            top_10_volume_percentages = [vol / sum(top_10_volumes) * 100 for vol in top_10_volumes]
            st.plotly_chart(px.pie(
                names=top_10_coins,
                values=top_10_volume_percentages,
                title="Cryptocurrency Volume Dominance",
                hole=0.3,
            ))


            st.plotly_chart(px.pie(
                names=[coin for coin in data['data']['market_cap_percentage']],
                values=[data['data']['market_cap_percentage'][coin] for coin in data['data']['market_cap_percentage']],
                title="Cryptocurrency Market Capitalization Dominance",
                hole=0.3,
            ))
        else:
            st.error("API call not successful. Please try again later.")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

def showCompanyHoldings():
    URL = f"{BASE_URL}/companies/public_treasury/bitcoin"

    try:
        response = requests.get(URL)
        data = response.json()
        if response.status_code == 200:
            st.markdown("### Cryptocurrency Market Overview")

            st.header("Bitcoin (BTC) Holdings")
            col1, col2, col3 = st.columns(3)
            col1.metric(label="Total Holdings", value=data["total_holdings"])
            col2.metric(label="Total Value (USD)", value=f"${data['total_value_usd']:.2f}")
            col3.metric(label="Market Cap Dominance", value=f"{data['market_cap_dominance']:.2f}%")
            st.subheader("Companies Holding Bitcoin")
            st.table(data["companies"])
        else:
            st.error("API call not successful. Please try again later.")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")


def cryptos():
    st.title("Cryptocurrency Dashboard")

    option = st.selectbox("Select an option:", options=[None, "Trending Assets", "Search Cryptocurrency", "Exchange Rates", "Top Cryptocurrency", "Crypto Global Market", "Companies Bitcoin Holdings"])

    if option == "Trending Assets":
        showTrendingAssets()
    
    elif option == "Search Cryptocurrency":
        query = st.text_input(f"Enter the coin name or symbol")
        if st.button("Search"):
            searchCryptocurrency(query)

    elif option == "Exchange Rates":
        if 'SUPPORTED_COINS' not in st.session_state:
            st.session_state.SUPPORTED_COINS = getSupportedCoins()

        if 'SUPPORTED_CURRENCIES' not in st.session_state:
            st.session_state.SUPPORTED_CURRENCIES = getSupportedCurrencies()

        from_currency = st.selectbox("From currency", options=SUPPORTED_COINS)
        to_currency = st.selectbox("To currency", options=SUPPORTED_CURRENCIES)

        if st.button("Convert"):
            cryptoConversion(from_currency, to_currency)

    elif option == "Top Cryptocurrency":
        showTopCryptocurrency()

    elif option == "Crypto Global Market":
        showCryptoMarketOverview()

    elif option == "Companies Bitcoin Holdings":
        showCompanyHoldings()
