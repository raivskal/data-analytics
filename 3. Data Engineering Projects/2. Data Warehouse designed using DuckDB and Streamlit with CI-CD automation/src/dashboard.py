import os
import streamlit as st
import pandas as pd
import duckdb
import plotly.express as px

# 1. Page Configuration
st.set_page_config(
    page_title="E-Commerce Modern DWH Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Custom Styling & CSS (For premium design / wow factor)
st.markdown("""
<style>
    /* Global fonts and backgrounds */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    /* Elegant Title Styling with gradient */
    .dashboard-title {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #FF6B6B 0%, #4D96FF 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    .dashboard-subtitle {
        font-size: 1.1rem;
        color: #7d8c9b;
        margin-bottom: 2rem;
    }
    
    /* Card design with glassmorphism style */
    .metric-card {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(5px);
        -webkit-backdrop-filter: blur(5px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 1.5rem;
        text-align: center;
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 30px rgba(77, 150, 255, 0.2);
    }
    
    .metric-value {
        font-size: 2.2rem;
        font-weight: 800;
        color: #4D96FF;
    }
    
    .metric-label {
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #a0aec0;
        margin-top: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# 3. Data Loader Function
@st.cache_data
def load_data():
    db_path = "data/dev.duckdb"
    if not os.path.exists(db_path):
        return None, None
    
    conn = duckdb.connect(db_path)
    # Read our analytical marts
    df_orders = conn.execute("SELECT * FROM main.fct_orders").df()
    df_customers = conn.execute("SELECT * FROM main.dim_customers").df()
    conn.close()
    
    # Ensure timestamps
    df_orders['order_date'] = pd.to_datetime(df_orders['order_date'])
    df_customers['created_at'] = pd.to_datetime(df_customers['created_at'])
    
    return df_orders, df_customers

# Main App Logic
st.markdown('<div class="dashboard-title">E-Commerce Modern DWH Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="dashboard-subtitle">Powered by DuckDB & dbt-duckdb analytical models</div>', unsafe_allow_html=True)

df_orders, df_customers = load_data()

if df_orders is None or df_customers is None:
    st.warning("⚠️ Database file not found or analytical models have not been run yet.")
    st.info("Please run the ingestion script (`python src/ingestion.py`) and compile the dbt project (`dbt build`) to populate the warehouse.")
else:
    # Sidebar Filters
    st.sidebar.markdown("### 🔍 Filter Dimensions")
    
    # Country Filter
    countries = sorted(list(df_orders['customer_country'].unique()))
    selected_countries = st.sidebar.multiselect("Select Countries", countries, default=countries)
    
    # Order Status Filter
    statuses = list(df_orders['status'].unique())
    selected_statuses = st.sidebar.multiselect("Select Order Statuses", statuses, default=["completed", "pending"])
    
    # Date Range Filter
    min_date = df_orders['order_date'].min().date()
    max_date = df_orders['order_date'].max().date()
    start_date, end_date = st.sidebar.slider("Select Date Range", min_date, max_date, (min_date, max_date))
    
    # Filter Dataframes
    filtered_orders = df_orders[
        (df_orders['customer_country'].isin(selected_countries)) &
        (df_orders['status'].isin(selected_statuses)) &
        (df_orders['order_date'].dt.date >= start_date) &
        (df_orders['order_date'].dt.date <= end_date)
    ]
    
    filtered_customers = df_customers[
        df_customers['customer_id'].isin(filtered_orders['customer_id'])
    ]
    
    # Check if empty
    if filtered_orders.empty:
        st.error("No data matches the selected filters.")
    else:
        # Calculate KPIs
        total_revenue = filtered_orders[filtered_orders['status'] == 'completed']['amount'].sum()
        total_orders = filtered_orders.shape[0]
        avg_order_value = filtered_orders['amount'].mean() if total_orders > 0 else 0
        active_customers = filtered_orders['customer_id'].nunique()
        
        # Display KPIs with Custom Cards
        kpi_cols = st.columns(4)
        
        with kpi_cols[0]:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">${total_revenue:,.2f}</div>
                <div class="metric-label">Total Revenue (Completed)</div>
            </div>
            """, unsafe_allow_html=True)
            
        with kpi_cols[1]:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{total_orders:,}</div>
                <div class="metric-label">Total Orders</div>
            </div>
            """, unsafe_allow_html=True)
            
        with kpi_cols[2]:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">${avg_order_value:.2f}</div>
                <div class="metric-label">Avg Order Value (AOV)</div>
            </div>
            """, unsafe_allow_html=True)
            
        with kpi_cols[3]:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{active_customers:,}</div>
                <div class="metric-label">Active Customers</div>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Charts Row 1
        row1_cols = st.columns(2)
        
        with row1_cols[0]:
            # Line Chart: Revenue Trend over Time
            df_trend = filtered_orders.groupby(filtered_orders['order_date'].dt.to_period("M")).agg(
                revenue=('amount', lambda x: x[filtered_orders.loc[x.index, 'status'] == 'completed'].sum()),
                orders_count=('order_id', 'count')
            ).reset_index()
            df_trend['order_date'] = df_trend['order_date'].dt.to_timestamp()
            
            fig_trend = px.line(
                df_trend, 
                x='order_date', 
                y='revenue', 
                title='Monthly Revenue Trend ($)',
                template='plotly_dark',
                labels={'order_date': 'Month', 'revenue': 'Revenue ($)'}
            )
            fig_trend.update_traces(line_color='#FF6B6B', line_width=3)
            st.plotly_chart(fig_trend, use_container_width=True)
            
        with row1_cols[1]:
            # Bar Chart: Top Customers by Spend
            df_top_spend = filtered_customers.sort_values(by='total_spend', ascending=False).head(10)
            df_top_spend['customer_name'] = df_top_spend['first_name'] + ' ' + df_top_spend['last_name']
            
            fig_spend = px.bar(
                df_top_spend,
                y='customer_name',
                x='total_spend',
                title='Top 10 Customers by Spend ($)',
                orientation='h',
                template='plotly_dark',
                labels={'total_spend': 'Total Spend ($)', 'customer_name': 'Customer'}
            )
            fig_spend.update_traces(marker_color='#4D96FF')
            fig_spend.update_layout(yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig_spend, use_container_width=True)
            
        # Charts Row 2
        row2_cols = st.columns(2)
        
        with row2_cols[0]:
            # Pie/Donut Chart: Payment Method
            df_payment = filtered_orders.groupby('payment_method').size().reset_index(name='count')
            fig_payment = px.pie(
                df_payment,
                values='count',
                names='payment_method',
                title='Payment Method Distribution',
                hole=0.4,
                template='plotly_dark',
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            st.plotly_chart(fig_payment, use_container_width=True)
            
        with row2_cols[1]:
            # Bar Chart: Orders by Country
            df_country = filtered_orders.groupby('customer_country').size().reset_index(name='orders')
            fig_country = px.bar(
                df_country,
                x='customer_country',
                y='orders',
                title='Orders by Country',
                template='plotly_dark',
                labels={'orders': 'Number of Orders', 'customer_country': 'Country'}
            )
            fig_country.update_traces(marker_color='#6BCB77')
            st.plotly_chart(fig_country, use_container_width=True)
            
        # Data table details
        st.subheader("📋 Detailed Transactions Preview")
        st.dataframe(
            filtered_orders[['order_id', 'customer_email', 'order_date', 'status', 'amount', 'payment_method', 'customer_country']].head(100),
            use_container_width=True
        )
