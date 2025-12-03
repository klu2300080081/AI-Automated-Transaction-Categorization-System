def load_css():
    return """
    <style>
    /* Dark Theme Colors */
    :root {
        --primary-bg: #0e1117;
        --secondary-bg: #1a1d29;
        --card-bg: #262730;
        --accent-color: #00d4ff;
        --text-primary: #ffffff;
        --text-secondary: #b0b0b0;
        --success-color: #00c853;
        --error-color: #ff5252;
        --warning-color: #ffa726;
    }
    
    /* Main App Styling */
    .stApp {
        background-color: var(--primary-bg);
    }
    
    /* Custom Card Styling */
    .custom-card {
        background-color: var(--card-bg);
        border-radius: 12px;
        padding: 25px;
        margin: 15px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Header Styling */
    .custom-header {
        color: var(--accent-color);
        font-size: 2.5em;
        font-weight: bold;
        text-align: center;
        margin-bottom: 30px;
        text-shadow: 0 0 10px rgba(0, 212, 255, 0.3);
    }
    
    .custom-subheader {
        color: var(--text-primary);
        font-size: 1.8em;
        font-weight: 600;
        margin-bottom: 20px;
        border-bottom: 2px solid var(--accent-color);
        padding-bottom: 10px;
    }
    
    /* Button Styling */
    .stButton > button {
        background-color: var(--accent-color);
        color: var(--primary-bg);
        border: none;
        border-radius: 8px;
        padding: 12px 30px;
        font-weight: bold;
        font-size: 16px;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        background-color: #00b8e6;
        box-shadow: 0 0 20px rgba(0, 212, 255, 0.5);
        transform: translateY(-2px);
    }
    
    /* Input Fields */
    .stTextInput > div > div > input,
    .stDateInput > div > div > input,
    .stTimeInput > div > div > input {
        background-color: var(--secondary-bg);
        color: var(--text-primary);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 8px;
        padding: 12px;
    }
    
    .stTextInput > div > div > input:focus,
    .stDateInput > div > div > input:focus,
    .stTimeInput > div > div > input:focus {
        border-color: var(--accent-color);
        box-shadow: 0 0 10px rgba(0, 212, 255, 0.3);
    }
    
    /* Success/Error Messages */
    .success-message {
        background-color: rgba(0, 200, 83, 0.1);
        border-left: 4px solid var(--success-color);
        padding: 15px;
        border-radius: 8px;
        color: var(--success-color);
        margin: 15px 0;
    }
    
    .error-message {
        background-color: rgba(255, 82, 82, 0.1);
        border-left: 4px solid var(--error-color);
        padding: 15px;
        border-radius: 8px;
        color: var(--error-color);
        margin: 15px 0;
    }
    
    /* Transaction Card */
    .transaction-card {
        background: linear-gradient(135deg, var(--card-bg) 0%, rgba(38, 39, 48, 0.8) 100%);
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
        border: 1px solid rgba(0, 212, 255, 0.2);
        transition: all 0.3s ease;
    }
    
    .transaction-card:hover {
        border-color: var(--accent-color);
        box-shadow: 0 0 20px rgba(0, 212, 255, 0.2);
        transform: translateX(5px);
    }
    
    /* Stats Card */
    .stats-card {
        background: linear-gradient(135deg, #1a1d29 0%, #262730 100%);
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        border: 2px solid var(--accent-color);
        box-shadow: 0 0 20px rgba(0, 212, 255, 0.2);
    }
    
    .stats-number {
        font-size: 2.5em;
        font-weight: bold;
        color: var(--accent-color);
        margin: 10px 0;
    }
    
    .stats-label {
        color: var(--text-secondary);
        font-size: 1em;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Confidence Badge */
    .confidence-high {
        background-color: rgba(0, 200, 83, 0.2);
        color: var(--success-color);
        padding: 5px 15px;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
    }
    
    .confidence-medium {
        background-color: rgba(255, 167, 38, 0.2);
        color: var(--warning-color);
        padding: 5px 15px;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
    }
    
    .confidence-low {
        background-color: rgba(255, 82, 82, 0.2);
        color: var(--error-color);
        padding: 5px 15px;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: var(--secondary-bg);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
        color: var(--text-primary);
    }
    
    /* Remove sidebar highlight/border on navigation items */
    [data-testid="stSidebar"] nav {
        background-color: transparent;
    }
    
    section[data-testid="stSidebar"] > div:first-child {
        background-color: var(--secondary-bg);
    }
    
    /* Remove blue border/highlight around sidebar sections */
    [data-testid="stSidebar"] > div > div {
        border: none !important;
        outline: none !important;
        box-shadow: none !important;
    }
    
    /* Remove focus/active state borders */
    [data-testid="stSidebar"] button:focus,
    [data-testid="stSidebar"] button:active,
    [data-testid="stSidebar"] a:focus,
    [data-testid="stSidebar"] a:active {
        outline: none !important;
        border: none !important;
        box-shadow: none !important;
    }
    
    /* Table Styling */
    .dataframe {
        background-color: var(--card-bg) !important;
        color: var(--text-primary) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    .dataframe thead tr th {
        background-color: var(--secondary-bg) !important;
        color: var(--accent-color) !important;
        font-weight: bold !important;
    }
    
    .dataframe tbody tr:hover {
        background-color: rgba(0, 212, 255, 0.1) !important;
    }
    
    /* Metric Styling */
    [data-testid="stMetricValue"] {
        color: var(--accent-color);
        font-size: 2em;
    }
    
    /* Expander Styling */
    .streamlit-expanderHeader {
        background-color: var(--card-bg);
        border-radius: 8px;
        color: var(--text-primary);
    }
    
    .streamlit-expanderHeader:hover {
        background-color: rgba(0, 212, 255, 0.1);
    }
    
    /* Hide Sidebar Completely */
    [data-testid="stSidebar"] {
        display: none !important;
    }
    
    [data-testid="collapsedControl"] {
        display: none !important;
    }
    
    /* Expand main content to full width */
    .main .block-container {
        max-width: 100% !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Remove any blue borders or outlines globally */
    * {
        outline: none !important;
    }
    
    *:focus {
        outline: none !important;
        box-shadow: none !important;
    }
    
    /* Remove Streamlit's default blue focus borders */
    div[data-testid="stSidebar"] div,
    div[data-testid="stSidebar"] section {
        border: none !important;
        box-shadow: none !important;
    }
    </style>
    """