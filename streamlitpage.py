def case_study_3():
    st.subheader("🛡️ Case Study 3: Insurance Penetration")
    st.write("Analyze insurance transaction penetration across states and quarters.")
    if agg_insurance is None:
        st.warning("Insurance data not available.")
        return
    col1, col2 = st.columns(2)
    with col1:
        year = st.selectbox("Select Year", sorted(agg_insurance['Years'].unique()), key='cs3_year')
    with col2:
        quarter = st.selectbox("Select Quarter", sorted(agg_insurance['Quarter'].unique()), key='cs3_quarter')
    state_summary = analyze_state_transactions(agg_insurance, year, quarter)
    fig = create_choropleth(state_summary, 'Transaction_amount', f"Insurance Amount by State (Q{quarter} {year})")
    st.plotly_chart(fig, use_container_width=True)
    st.write("Top 5 States by Insurance Amount:")
    st.dataframe(state_summary.nlargest(5, 'Transaction_amount'))

def case_study_4():
    st.subheader("🚀 Case Study 4: Market Expansion")
    st.write("Identify underserved and high-growth states for expansion.")
    if agg_transaction is None:
        st.warning("Transaction data not available.")
        return
    state_summary = agg_transaction.groupby('States')[['Transaction_count', 'Transaction_amount']].sum().reset_index()
    st.write("Top 10 States by Transaction Amount:")
    st.dataframe(state_summary.nlargest(10, 'Transaction_amount'))
    st.write("Bottom 10 States by Transaction Amount:")
    st.dataframe(state_summary.nsmallest(10, 'Transaction_amount'))

def case_study_5():
    st.subheader("👥 Case Study 5: User Engagement")
    st.write("Analyze user engagement patterns across states.")
    if map_user is None:
        st.warning("User map data not available.")
        return
    user_summary = map_user.groupby('States')[['RegisteredUser', 'AppOpens']].sum().reset_index()
    st.write("Top 10 States by Registered Users:")
    st.dataframe(user_summary.nlargest(10, 'RegisteredUser'))
    st.write("Top 10 States by App Opens:")
    st.dataframe(user_summary.nlargest(10, 'AppOpens'))

def case_study_6():
    st.subheader("📋 Case Study 6: Insurance Engagement")
    st.write("Analyze insurance engagement at state and district levels.")
    if map_insurance is None:
        st.warning("Insurance map data not available.")
        return
    state_summary = map_insurance.groupby('States')[['Transaction_count', 'Transaction_amount']].sum().reset_index()
    st.write("Top 10 States by Insurance Amount:")
    st.dataframe(state_summary.nlargest(10, 'Transaction_amount'))
    district_summary = map_insurance.groupby('Districts')[['Transaction_count', 'Transaction_amount']].sum().reset_index()
    st.write("Top 10 Districts by Insurance Amount:")
    st.dataframe(district_summary.nlargest(10, 'Transaction_amount'))

def case_study_7():
    st.subheader("🗺️ Case Study 7: Geographic Transaction Analysis")
    st.write("Identify top-performing states and districts for transactions.")
    if top_transaction is None:
        st.warning("Top transaction data not available.")
        return
    state_summary = top_transaction.groupby('States')[['Transaction_count', 'Transaction_amount']].sum().reset_index()
    st.write("Top 10 States by Transaction Amount:")
    st.dataframe(state_summary.nlargest(10, 'Transaction_amount'))
    pincode_summary = top_transaction.groupby('Pincodes')[['Transaction_count', 'Transaction_amount']].sum().reset_index()
    st.write("Top 10 Pincodes by Transaction Amount:")
    st.dataframe(pincode_summary.nlargest(10, 'Transaction_amount'))

def case_study_8():
    st.subheader("📝 Case Study 8: User Registration")
    st.write("Analyze user registration patterns across states and pincodes.")
    if top_user is None:
        st.warning("Top user data not available.")
        return
    state_summary = top_user.groupby('States')['RegisteredUser'].sum().reset_index()
    st.write("Top 10 States by Registered Users:")
    st.dataframe(state_summary.nlargest(10, 'RegisteredUser'))
    pincode_summary = top_user.groupby('Pincodes')['RegisteredUser'].sum().reset_index()
    st.write("Top 10 Pincodes by Registered Users:")
    st.dataframe(pincode_summary.nlargest(10, 'RegisteredUser'))

def case_study_9():
    st.subheader("🏥 Case Study 9: Insurance Transactions")
    st.write("Analyze insurance transactions by state and pincode.")
    if top_insurance is None:
        st.warning("Top insurance data not available.")
        return
    state_summary = top_insurance.groupby('States')[['Transaction_count', 'Transaction_amount']].sum().reset_index()
    st.write("Top 10 States by Insurance Amount:")
    st.dataframe(state_summary.nlargest(10, 'Transaction_amount'))
    pincode_summary = top_insurance.groupby('Pincodes')[['Transaction_count', 'Transaction_amount']].sum().reset_index()
    st.write("Top 10 Pincodes by Insurance Amount:")
    st.dataframe(pincode_summary.nlargest(10, 'Transaction_amount'))

def case_study_10_map():
    st.subheader("🌍 Case Study 10: State-wise Transaction Heatmap (Map)")
    st.write("Visualize transaction performance across Indian states using a choropleth map.")
    if map_transaction is None:
        st.warning("Map transaction data not available.")
        return
    col1, col2 = st.columns(2)
    with col1:
        year = st.selectbox("Select Year", sorted(map_transaction['Years'].unique()), key='cs10_year')
    with col2:
        quarter = st.selectbox("Select Quarter", sorted(map_transaction['Quarter'].unique()), key='cs10_quarter')
    df_filtered = map_transaction[(map_transaction['Years'] == year) & (map_transaction['Quarter'] == quarter)]
    state_summary = df_filtered.groupby('States')[['Transaction_count', 'Transaction_amount']].sum().reset_index()
    fig = create_choropleth(state_summary, 'Transaction_amount', f"Transaction Amount by State (Q{quarter} {year})")
    st.plotly_chart(fig, use_container_width=True)

# Remove duplicate code below this line
import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import pymysql
import plotly.express as px
import json
import requests

st.set_page_config(
    page_title="PhonePe Pulse Data Visualization",
    page_icon="📱",
    layout="wide"
)

# Configuration
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "123456789",
    "database": "phonepe_pulse_data",
    "port": 3306
}

GEOJSON_URL = ("https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/"
               "raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson")

@st.cache_data
def load_geojson():
    """Load India states GeoJSON data."""
    try:
        return json.loads(requests.get(GEOJSON_URL).content)
    except Exception as e:
        st.error(f"Failed to load GeoJSON data: {e}")
        return None

@st.cache_resource
def get_db_connection():
    """Create database connection."""
    try:
        return pymysql.connect(**DB_CONFIG)
    except Exception as e:
        st.error(f"Database connection failed: {e}")
        return None

@st.cache_data(ttl=3600)
def load_data():
    """Load all tables from database."""
    conn = get_db_connection()
    if not conn:
        return {}
    
    tables = {
        'aggregated_insurance': ['States', 'Years', 'Quarter', 'Transaction_type', 'Transaction_count', 'Transaction_amount'],
        'aggregated_transaction': ['States', 'Years', 'Quarter', 'Transaction_type', 'Transaction_count', 'Transaction_amount'],
        'aggregated_user': ['States', 'Years', 'Quarter', 'Brands', 'Transaction_count', 'Percentage'],
        'map_insurance': ['States', 'Years', 'Quarter', 'Districts', 'Transaction_type', 'Transaction_count', 'Transaction_amount'],
        'map_transaction': ['States', 'Years', 'Quarter', 'Districts', 'Transaction_count', 'Transaction_amount'],
        'map_user': ['States', 'Years', 'Quarter', 'Districts', 'RegisteredUser', 'AppOpens'],
        'top_insurance': ['States', 'Years', 'Quarter', 'Pincodes', 'Transaction_count', 'Transaction_amount'],
        'top_transaction': ['States', 'Years', 'Quarter', 'Pincodes', 'Transaction_count', 'Transaction_amount'],
        'top_user': ['States', 'Years', 'Quarter', 'Pincodes', 'RegisteredUser']
    }
    
    try:
        data = {}
        with conn.cursor() as cursor:
            for table, columns in tables.items():
                cursor.execute(f"SELECT * FROM {table}")
                result = cursor.fetchall()
                data[table] = pd.DataFrame(result, columns=columns)
        return data
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return {}
    finally:
        conn.close()

def format_indian(number):
    """Format a number in Indian currency style."""
    try:
        num = float(number)
        if num >= 10000000:  # Crores
            return f"₹{num/10000000:.2f} Cr"
        elif num >= 100000:  # Lakhs
            return f"₹{num/100000:.2f} L"
        return f"₹{num:,.2f}"
    except (ValueError, TypeError):
        return "N/A"

def create_choropleth(data, color_column, title, hover_data=None):
    """Create a choropleth map of India."""
    fig = px.choropleth(
        data,
        geojson=geojson_data,
        locations="States",
        featureidkey="properties.ST_NM",
        color=color_column,
        title=title,
        hover_data=hover_data,
        color_continuous_scale="Viridis",
    )
    fig.update_geos(fitbounds="locations", visible=False)
    return fig

# Load data
data = load_data()
geojson_data = load_geojson()

# Check for data load errors
if not data or not geojson_data:
    st.error("Failed to load required data. Please check your database connection.")
    st.stop()

# Get the DataFrames
agg_insurance = data['aggregated_insurance']
agg_transaction = data['aggregated_transaction']
agg_user = data['aggregated_user']
map_insurance = data['map_insurance']
map_transaction = data['map_transaction']
map_user = data['map_user']
top_insurance = data['top_insurance']
top_transaction = data['top_transaction']
top_user = data['top_user']

# Transaction specific analysis functions
def analyze_state_transactions(transactions_df, year=None, quarter=None):
    """Analyze transaction patterns by state."""
    filtered = transactions_df
    if year and quarter:
        filtered = transactions_df[
            (transactions_df['Years'] == year) &
            (transactions_df['Quarter'] == quarter)
        ]
    
    state_summary = filtered.groupby('States')[
        ['Transaction_count', 'Transaction_amount']
    ].sum().reset_index()
    
    return state_summary

def analyze_transaction_types(transactions_df, year=None, quarter=None):
    """Analyze transaction patterns by type."""
    filtered = transactions_df
    if year and quarter:
        filtered = transactions_df[
            (transactions_df['Years'] == year) &
            (transactions_df['Quarter'] == quarter)
        ]
    
    type_summary = filtered.groupby('Transaction_type')[
        ['Transaction_count', 'Transaction_amount']
    ].sum().reset_index()
    
    return type_summary

# User specific analysis functions
def analyze_brand_usage(user_df, year=None, quarter=None):
    """Analyze user patterns by mobile brand."""
    filtered = user_df
    if year and quarter:
        filtered = user_df[
            (user_df['Years'] == year) &
            (user_df['Quarter'] == quarter)
        ]
    
    brand_summary = filtered.groupby('Brands')[
        ['Transaction_count', 'Percentage']
    ].sum().reset_index()
    
    return brand_summary.sort_values('Transaction_count', ascending=False)

def analyze_user_distribution(user_df, year=None):
    """Analyze user distribution across states."""
    filtered = user_df
    if year:
        filtered = user_df[user_df['Years'] == year]
    
    state_summary = filtered.groupby('States')[
        ['RegisteredUser', 'AppOpens']
    ].sum().reset_index()
    
    return state_summary

def show_overview():
    """Show overview page with key metrics and national summary."""
    st.header("Overview")
    
    # Key metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        total_transactions = agg_transaction['Transaction_count'].sum()
        st.metric("Total Transactions", f"{total_transactions:,}")
    with col2:
        total_amount = agg_transaction['Transaction_amount'].sum()
        st.metric("Total Amount", format_indian(total_amount))
    with col3:
        total_users = agg_user['Transaction_count'].sum()
        st.metric("Total Users", f"{total_users:,}")
    
    # National summary map
    st.subheader("Transaction Distribution Across India")
    state_summary = agg_transaction.groupby('States')[
        ['Transaction_count', 'Transaction_amount']
    ].sum().reset_index()
    
    fig = create_choropleth(
        state_summary,
        'Transaction_amount',
        "Transaction Amount by State",
        hover_data={
            'Transaction_count': ':,.0f',
            'Transaction_amount': ':,.0f'
        }
    )
    st.plotly_chart(fig, use_container_width=True)

def show_transactions():
    """Show transaction analysis page."""
    st.header("Transaction Analysis")
    
    # Filters
    col1, col2 = st.columns(2)
    with col1:
        year = st.selectbox("Select Year", sorted(agg_transaction['Years'].unique()))
    with col2:
        quarter = st.selectbox("Select Quarter", sorted(agg_transaction['Quarter'].unique()))
    
    # Get transaction summaries
    state_summary = analyze_state_transactions(agg_transaction, year, quarter)
    type_summary = analyze_transaction_types(agg_transaction, year, quarter)
    
    # Map visualization
    st.subheader("State-wise Analysis")
    fig = create_choropleth(
        state_summary,
        'Transaction_amount',
        f"Transaction Amount by State (Q{quarter} {year})",
        hover_data={
            'Transaction_count': ':,.0f',
            'Transaction_amount': ':,.0f'
        }
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Transaction type analysis
    st.subheader("Transaction Type Analysis")
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.pie(
            type_summary,
            values='Transaction_amount',
            names='Transaction_type',
            title='Transaction Amount by Type'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.pie(
            type_summary,
            values='Transaction_count',
            names='Transaction_type',
            title='Transaction Count by Type'
        )
        st.plotly_chart(fig, use_container_width=True)

def show_users():
    """Show user analysis page."""
    st.header("User Analysis")
    
    # Brand analysis
    st.subheader("Mobile Brand Analysis")
    brand_summary = analyze_brand_usage(agg_user)
    
    fig = px.bar(
        brand_summary.head(10),
        x='Brands',
        y='Transaction_count',
        title='Top 10 Mobile Brands by Transaction Count'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # User distribution map
    st.subheader("User Distribution Across India")
    user_summary = analyze_user_distribution(map_user)
    
    fig = create_choropleth(
        user_summary,
        'RegisteredUser',
        "Registered Users by State",
        hover_data={
            'RegisteredUser': ':,.0f',
            'AppOpens': ':,.0f'
        }
    )
    st.plotly_chart(fig, use_container_width=True)

def show_insurance():
    """Show insurance analysis page."""
    st.header("Insurance Analysis")
    
    # Filters
    col1, col2 = st.columns(2)
    with col1:
        year = st.selectbox("Select Year", sorted(agg_insurance['Years'].unique()), key='ins_year')
    with col2:
        quarter = st.selectbox("Select Quarter", sorted(agg_insurance['Quarter'].unique()), key='ins_quarter')
    
    # Get insurance summary
    state_summary = analyze_state_transactions(agg_insurance, year, quarter)
    
    # Map visualization
    st.subheader("State-wise Analysis")
    fig = create_choropleth(
        state_summary,
        'Transaction_amount',
        f"Insurance Transaction Amount by State (Q{quarter} {year})",
        hover_data={
            'Transaction_count': ':,.0f',
            'Transaction_amount': ':,.0f'
        }
    )
    st.plotly_chart(fig, use_container_width=True)

def case_study_1():
    """Analyze transaction dynamics across states and transaction types."""
    st.subheader("📊 Case Study 1: Transaction Dynamics Analysis")
    st.write("**Objective:** Analyze transaction patterns across states to identify growth opportunities.")
    st.write("")
    
    if agg_transaction is None:
        st.warning("Data required for this case study is unavailable.")
        return

    col1, col2 = st.columns(2)
    with col1:
        year = st.selectbox("Select Year", sorted(agg_transaction["Years"].unique()), key="cs1_year")
    with col2:
        quarter = st.selectbox("Select Quarter", sorted(agg_transaction["Quarter"].unique()), key="cs1_quarter")
    
    # Get transaction summaries
    state_summary = analyze_state_transactions(agg_transaction, year, quarter)
    type_summary = analyze_transaction_types(agg_transaction, year, quarter)
    
    # State-wise transaction amount
    col1, col2 = st.columns(2)
    with col1:
        fig1 = px.bar(
            state_summary.nlargest(10, 'Transaction_amount'),
            x="States",
            y="Transaction_amount",
            title=f"Top 10 States by Amount (Q{quarter} {year})",
            color="Transaction_amount",
            color_continuous_scale="Viridis"
        )
        fig1.update_layout(xaxis={'categoryorder':'total descending', 'tickangle':45})
        st.plotly_chart(fig1, use_container_width=True)
    
    # State-wise transaction count
    with col2:
        fig2 = px.bar(
            state_summary.nlargest(10, 'Transaction_count'),
            x="States",
            y="Transaction_count",
            title=f"Top 10 States by Count (Q{quarter} {year})",
            color="Transaction_count",
            color_continuous_scale="Bluered"
        )
        fig2.update_layout(xaxis={'categoryorder':'total descending', 'tickangle':45})
        st.plotly_chart(fig2, use_container_width=True)
    
    # Transaction type analysis
    col1, col2 = st.columns(2)
    with col1:
        fig3 = px.pie(
            type_summary,
            values="Transaction_amount",
            names="Transaction_type",
            title="Amount Distribution by Type",
            hole=0.4
        )
        st.plotly_chart(fig3, use_container_width=True)
    
    with col2:
        fig4 = px.pie(
            type_summary,
            values="Transaction_count",
            names="Transaction_type",
            title="Count Distribution by Type",
            hole=0.4
        )
        st.plotly_chart(fig4, use_container_width=True)

def case_study_2():
    """Analyze device brand preferences and user engagement patterns."""
    st.subheader("📱 Case Study 2: Device Dominance and User Engagement Analysis")
    st.write("**Objective:** Understand user preferences across device brands to enhance engagement.")
    st.write("")
    
    if agg_user is None:
        st.warning("Data required for this case study is unavailable.")
        return

    col1, col2 = st.columns(2)
    with col1:
        year_cs2 = st.selectbox("Select Year", sorted(agg_user["Years"].unique()), key="cs2_year")
    with col2:
        quarter_cs2 = st.selectbox("Select Quarter", sorted(agg_user["Quarter"].unique()), key="cs2_quarter")
    
    # Get brand usage summary
    brand_summary = analyze_brand_usage(agg_user, year_cs2, quarter_cs2)
    
    # Top brands by transaction count
    col1, col2 = st.columns(2)
    with col1:
        fig1 = px.bar(
            brand_summary.head(15), 
            x="Brands", 
            y="Transaction_count",
            title=f"Top 15 Device Brands (Q{quarter_cs2} {year_cs2})",
            color="Transaction_count", 
            color_continuous_scale="Plasma"
        )
        fig1.update_layout(xaxis={'categoryorder':'total descending', 'tickangle':45})
        st.plotly_chart(fig1, use_container_width=True)
    
    # Market share visualization
    with col2:
        fig2 = px.pie(
            brand_summary.head(10),
            values="Transaction_count",
            names="Brands",
            title="Top 10 Brands Market Share",
            hole=0.4
        )
        st.plotly_chart(fig2, use_container_width=True)
    
    # Brand trend analysis
    yearly_trend = agg_user.groupby(
        ["Years", "Brands"]
    )["Transaction_count"].sum().reset_index()
    
    # Get top 5 brands for trend
    top_brands = brand_summary.head(5)["Brands"].tolist()
    trend_data = yearly_trend[yearly_trend["Brands"].isin(top_brands)]
    
    fig3 = px.line(
        trend_data,
        x="Years",
        y="Transaction_count",
        color="Brands",
        title="Top 5 Brands Trend Over Time",
        markers=True
    )
    st.plotly_chart(fig3, use_container_width=True)

def main():
    """Main application entry point."""
    st.title("PhonePe Pulse Data Visualization")
    
    # Navigation
    selected = option_menu(
        menu_title=None,
        options=["Overview", "Transactions", "Users", "Insurance"],
        icons=["house", "currency-exchange", "people", "shield-check"],
        orientation="horizontal"
    )
    
    try:
        if selected == "Overview":
            show_overview()
        elif selected == "Transactions":
            show_transactions()
        elif selected == "Users":
            show_users()
        elif selected == "Insurance":
            show_insurance()
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.exception(e)

if __name__ == "__main__":
    main()
    st.write("Drill down into specific business questions using interactive visualizations.")
    st.write("")
    
    case_study_choice = st.selectbox(
        "**Select a Case Study to Explore:**",
        [
            "Select a Case Study",
            "Case Study 1: Transaction Dynamics",
            "Case Study 2: Device Dominance",
            "Case Study 3: Insurance Penetration",
            "Case Study 4: Market Expansion",
            "Case Study 5: User Engagement",
            "Case Study 6: Insurance Engagement",
            "Case Study 7: Geographic Transaction Analysis",
            "Case Study 8: User Registration",
            "Case Study 9: Insurance Transactions",
            "Case Study 10: State-wise Transaction Heatmap (Map)" 
        ]
    )
    
    st.markdown("---")
    
    # Conditional checks added for data availability before calling case study functions
    if case_study_choice == "Case Study 1: Transaction Dynamics":
        case_study_1()
    elif case_study_choice == "Case Study 2: Device Dominance":
        case_study_2()
    elif case_study_choice == "Case Study 3: Insurance Penetration":
        case_study_3()
    elif case_study_choice == "Case Study 4: Market Expansion":
        case_study_4()
    elif case_study_choice == "Case Study 5: User Engagement":
        case_study_5()
    elif case_study_choice == "Case Study 6: Insurance Engagement":
        case_study_6()
    elif case_study_choice == "Case Study 7: Geographic Transaction Analysis":
        case_study_7()
    elif case_study_choice == "Case Study 8: User Registration":
        case_study_8()
    elif case_study_choice == "Case Study 9: Insurance Transactions":
        case_study_9()
    elif case_study_choice == "Case Study 10: State-wise Transaction Heatmap (Map)":
        case_study_10_map() 
    else:
        st.info("👆 Please select a case study from the dropdown above to begin your analysis")
        
        # Preview of case studies
        st.write("")
        st.subheader("📚 Case Study Descriptions")
        
        with st.expander("📊 Case Study 1: Transaction Dynamics"):
            st.write("Analyze transaction patterns across states and quarters to identify growth opportunities.")
        
        with st.expander("📱 Case Study 2: Device Dominance"):
            st.write("Understand device brand preferences and their correlation with user engagement.")
        
        with st.expander("🛡️ Case Study 3: Insurance Penetration"):
            st.write("Explore insurance adoption rates and identify high-potential markets.")
        
        with st.expander("🚀 Case Study 4: Market Expansion"):
            st.write("Identify underserved markets and high-growth regions for expansion.")
        
        with st.expander("👥 Case Study 5: User Engagement"):
            st.write("Analyze user engagement metrics to drive retention strategies.")
        
        with st.expander("📋 Case Study 6: Insurance Engagement"):
            st.write("Deep dive into insurance transaction patterns at state and district levels.")
        
        with st.expander("🗺️ Case Study 7: Geographic Analysis"):
            st.write("Identify top-performing states, districts, and pincodes for marketing.")
        
        with st.expander("📝 Case Study 8: User Registration"):
            st.write("Track user acquisition patterns across regions and time periods.")
        
        with st.expander("🏥 Case Study 9: Insurance Transactions"):
            st.write("Comprehensive analysis of insurance transaction hotspots.")
            
        with st.expander("🌍 **Case Study 10: State-wise Transaction Heatmap (Map)**"):
            st.write("Visually represent the distribution of total transaction count and amount across Indian states using a responsive choropleth map.")