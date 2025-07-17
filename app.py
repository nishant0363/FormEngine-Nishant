import streamlit as st
import pandas as pd
import hashlib
import jwt
import datetime
from typing import Dict, List, Optional
import json
import uuid
import plotly.express as px
import plotly.graph_objects as go
import os
import requests

# Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "CK+mOFOUq/uEAlbQ77D1c9iKn5xZYCaAb+OZ6fcRAM5sYK0DSgVvPiFIyb88Nuem2cOryU2QYdxnkL3CAtAGRg==")
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://fxeccascddxuyscnpsax.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZ4ZWNjYXNjZGR4dXlzY25wc2F4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTI3MjU1NDcsImV4cCI6MjA2ODMwMTU0N30.KIfqbe4x__DhYibIS_9StwFeJreJgevKRy5Olw8xdSY")

# Supabase client setup with improved error handling
class SupabaseClient:
    def __init__(self, url: str, key: str):
        self.url = url
        self.key = key
        self.headers = {
            "apikey": key,
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json"
        }
    
    def insert(self, table: str, data: dict):
        """Insert data into table with improved error handling"""
        try:
            response = requests.post(
                f"{self.url}/rest/v1/{table}",
                headers=self.headers,
                json=data
            )
            
            # Debug information
            print(f"Insert response status: {response.status_code}")
            print(f"Insert response text: {response.text}")
            
            if response.status_code == 201:
                # Check if response has content before trying to parse JSON
                if response.text and response.text.strip():
                    try:
                        return response.json()
                    except json.JSONDecodeError:
                        print("Warning: Could not parse JSON response, but insert was successful")
                        return {"success": True}  # Return success indicator
                else:
                    # Empty response but successful status code
                    return {"success": True}
            else:
                print(f"Insert failed with status {response.status_code}: {response.text}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error in insert: {e}")
            return None
    
    def select(self, table: str, query: str = ""):
        """Select data from table with improved error handling"""
        try:
            url = f"{self.url}/rest/v1/{table}"
            if query:
                url += f"?{query}"
            
            response = requests.get(url, headers=self.headers)
            
            # Debug information
            print(f"Select response status: {response.status_code}")
            
            if response.status_code == 200:
                if response.text and response.text.strip():
                    try:
                        return response.json()
                    except json.JSONDecodeError:
                        print("Warning: Could not parse JSON response from select")
                        return []
                else:
                    return []
            else:
                print(f"Select failed with status {response.status_code}: {response.text}")
                return []
                
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            return []
        except Exception as e:
            print(f"Unexpected error in select: {e}")
            return []
    
    def update(self, table: str, query: str, data: dict):
        """Update data in table with improved error handling"""
        try:
            response = requests.patch(
                f"{self.url}/rest/v1/{table}?{query}",
                headers=self.headers,
                json=data
            )
            
            # Debug information
            print(f"Update response status: {response.status_code}")
            
            return response.status_code == 204
            
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            return False
        except Exception as e:
            print(f"Unexpected error in update: {e}")
            return False

# Initialize Supabase client
supabase = SupabaseClient(SUPABASE_URL, SUPABASE_KEY)

def hash_password(password: str) -> str:
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password: str, hashed: str) -> bool:
    """Verify password against hash"""
    return hashlib.sha256(password.encode()).hexdigest() == hashed

def create_jwt_token(user_id: int, username: str) -> str:
    """Create JWT token for user authentication"""
    payload = {
        'user_id': user_id,
        'username': username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def verify_jwt_token(token: str) -> Optional[Dict]:
    """Verify JWT token and return user info"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

# Database operations using Supabase with improved error handling
def register_user(username: str, email: str, password: str) -> bool:
    """Register a new admin user"""
    try:
        # Check if user already exists
        existing = supabase.select("users", f"username=eq.{username}")
        if existing and len(existing) > 0:
            return False
        
        existing_email = supabase.select("users", f"email=eq.{email}")
        if existing_email and len(existing_email) > 0:
            return False
        
        # Create new user
        password_hash = hash_password(password)
        
        user_data = {
            'username': username,
            'email': email,
            'password_hash': password_hash,
            'created_at': datetime.datetime.now().isoformat()
        }
        
        result = supabase.insert("users", user_data)
        return result is not None
        
    except Exception as e:
        print(f"Error in register_user: {e}")
        return False

def authenticate_user(username: str, password: str) -> Optional[Dict]:
    """Authenticate user and return user info"""
    try:
        users = supabase.select("users", f"username=eq.{username}")
        
        if users and len(users) > 0:
            user = users[0]
            if verify_password(password, user['password_hash']):
                return {
                    'id': user['id'],
                    'username': user['username'],
                    'email': user['email']
                }
        return None
        
    except Exception as e:
        print(f"Error in authenticate_user: {e}")
        return None

def create_form(admin_id: int, title: str, questions: List[Dict]) -> str:
    """Create a new feedback form"""
    try:
        form_id = str(uuid.uuid4())
        
        form_data = {
            'id': form_id,
            'admin_id': admin_id,
            'title': title,
            'questions': json.dumps(questions),
            'created_at': datetime.datetime.now().isoformat()
        }
        
        result = supabase.insert("forms", form_data)
        return form_id if result else None
        
    except Exception as e:
        print(f"Error in create_form: {e}")
        return None

def get_form(form_id: str) -> Optional[Dict]:
    """Get form by ID"""
    try:
        forms = supabase.select("forms", f"id=eq.{form_id}")
        
        if forms and len(forms) > 0:
            form = forms[0]
            return {
                'id': form['id'],
                'title': form['title'],
                'questions': json.loads(form['questions'])
            }
        return None
        
    except Exception as e:
        print(f"Error in get_form: {e}")
        return None

def get_admin_forms(admin_id: int) -> List[Dict]:
    """Get all forms created by an admin"""
    try:
        forms = supabase.select("forms", f"admin_id=eq.{admin_id}&order=created_at.desc")
        
        return [{
            'id': form['id'],
            'title': form['title'],
            'created_at': form['created_at']
        } for form in forms]
        
    except Exception as e:
        print(f"Error in get_admin_forms: {e}")
        return []

def submit_response(form_id: str, responses: Dict) -> bool:
    """Submit a response to a form"""
    try:
        response_data = {
            'form_id': form_id,
            'responses': json.dumps(responses),
            'submitted_at': datetime.datetime.now().isoformat()
        }
        
        result = supabase.insert("responses", response_data)
        return result is not None
        
    except Exception as e:
        print(f"Error in submit_response: {e}")
        return False

def get_form_responses(form_id: str) -> List[Dict]:
    """Get all responses for a form"""
    try:
        responses = supabase.select("responses", f"form_id=eq.{form_id}&order=submitted_at.desc")
        
        return [{
            'responses': json.loads(response['responses']),
            'submitted_at': response['submitted_at']
        } for response in responses]
        
    except Exception as e:
        print(f"Error in get_form_responses: {e}")
        return []

def get_recent_responses(admin_id: int, minutes: int = 5) -> List[Dict]:
    """Get recent responses for admin's forms within specified minutes"""
    try:
        # Get admin's forms
        admin_forms = supabase.select("forms", f"admin_id=eq.{admin_id}")
        admin_form_ids = [form['id'] for form in admin_forms]
        
        if not admin_form_ids:
            return []
        
        # Get recent responses
        cutoff_time = (datetime.datetime.now() - datetime.timedelta(minutes=minutes)).isoformat()
        
        recent_responses = []
        for form_id in admin_form_ids:
            responses = supabase.select("responses", 
                                      f"form_id=eq.{form_id}&submitted_at=gte.{cutoff_time}&order=submitted_at.desc")
            
            for response in responses:
                # Get form title
                form_title = next((form['title'] for form in admin_forms if form['id'] == form_id), 'Unknown Form')
                recent_responses.append({
                    'form_title': form_title,
                    'submitted_at': response['submitted_at'],
                    'responses': json.loads(response['responses'])
                })
        
        return sorted(recent_responses, key=lambda x: x['submitted_at'], reverse=True)
        
    except Exception as e:
        print(f"Error in get_recent_responses: {e}")
        return []

def get_app_url() -> str:
    """Get the current app URL for Streamlit Cloud"""
    # Replace with your actual Streamlit Cloud URL
    return "https://cform-engine-nishant.streamlit.app/"

# Rest of your code remains the same...
def main():
    st.set_page_config(
        page_title="cform-engine-nishant",
        page_icon="",
        layout="wide"
    )
    
    # Apply global style: Segoe UI + larger base font
    st.markdown("""
    <style>
    html, body, [class*="css"] {
        font-family: 'Segoe UI', sans-serif;
        font-size: 22px;
    }
    </style>
    """, unsafe_allow_html=True)

    # Hide Streamlit's default header, footer, and menu
    # Inject custom CSS: remove header/footer, top padding, set font
    st.markdown("""
        <style>
        /* Import custom font */
        @import url('https://fonts.googleapis.com/css2?family=STIX+Two+Text&display=swap');

        /* Apply font globally */
        html, body, [class*="css"]  {
            font-family: 'STIX Two Text', serif !important;
        }

        /* Apply font to Streamlit widgets */
        h1, h2, h3, h4, h5, h6,
        .stMarkdown, .stText, .stHeader, .stSubheader,
        .stButton > button, .stDownloadButton > button,
        .stDataFrame, .stAlert, .stSelectbox label,
        .stTextInput, .stFileUploader label, .stForm, .stFormLabel {
            font-family: 'STIX Two Text', serif !important;
        }

        /* Remove default Streamlit padding & space */
        .block-container {
            padding-top: 0rem !important;
            padding-bottom: 0rem !important;
        }

        /* Hide default Streamlit header and footer */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>
    """, unsafe_allow_html=True)

    # Display your custom image as the header (only if file exists)
    try:
        st.image("header.png", use_container_width=True)
    except:
        st.title("Feedback Collection Platform")
    
    # Initialize session state
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'user_info' not in st.session_state:
        st.session_state.user_info = None
    if 'last_refresh' not in st.session_state:
        st.session_state.last_refresh = datetime.datetime.now()
    
    # Check for form submission URL parameter
    query_params = st.query_params
    if 'form_id' in query_params:
        show_public_form(query_params['form_id'])
        return
    
    # Main application logic
    if not st.session_state.authenticated:
        show_auth_page()
    else:
        show_dashboard()

def show_auth_page():
    """Show authentication page (login/register)"""
    
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login")
            
            if submitted:
                if username and password:
                    user_info = authenticate_user(username, password)
                    if user_info:
                        st.session_state.authenticated = True
                        st.session_state.user_info = user_info
                        st.success("Login successful!")
                        st.rerun()
                    else:
                        st.error("Invalid username or password")
                else:
                    st.error("Please fill in all fields")
    
    with tab2:
        st.subheader("Create New Account")
        with st.form("register_form"):
            new_username = st.text_input("Username", key="reg_username")
            new_email = st.text_input("Email", key="reg_email")
            new_password = st.text_input("Password", type="password", key="reg_password")
            confirm_password = st.text_input("Confirm Password", type="password", key="reg_confirm")
            submitted = st.form_submit_button("Register")
            
            if submitted:
                if new_username and new_email and new_password and confirm_password:
                    if new_password == confirm_password:
                        if register_user(new_username, new_email, new_password):
                            st.success("Registration successful! Please login.")
                        else:
                            st.error("Username or email already exists")
                    else:
                        st.error("Passwords do not match")
                else:
                    st.error("Please fill in all fields")

    st.markdown("""
    <div style="text-align:center; font-size:23px; padding:0.5rem 1rem;">
        <strong>Nishant</strong> &nbsp; | &nbsp;
        📧 <a href="mailto:nishant0363@gmail.com" target="_blank">nishant0363@gmail.com</a> &nbsp; | &nbsp;
        📱 <a href="tel:+919306145426" target="_blank">+91-9306145426</a> &nbsp; | &nbsp;
        🌐 <a href="https://nishant0363.github.io/projects.com" target="_blank">Portfolio</a> &nbsp; | &nbsp;
        💼 <a href="https://www.linkedin.com/in/nishant3603/" target="_blank">LinkedIn</a> &nbsp; | &nbsp;
        🐙 <a href="https://github.com/nishant0363" target="_blank">GitHub</a> &nbsp; | &nbsp;
        📄 <a href="https://drive.google.com/file/d/1hOJqhdY38XSEGrRRrjJsipSg2taqWYu-/view?usp=drive_link" target="_blank">Resume</a>
    </div>
    """, unsafe_allow_html=True)

def show_dashboard():
    """Show admin dashboard"""
    st.title("Admin Dashboard")
    
    # Header with user info, refresh button, and logout
    col1, col2, col3 = st.columns([7, 1, 1])
    with col1:
        st.write(f"Welcome, **{st.session_state.user_info['username']}**!")
    with col2:
        if st.button("Refresh", help="Check for new responses"):
            st.session_state.last_refresh = datetime.datetime.now()
            st.rerun()
    with col3:
        if st.button("Logout"):
            st.session_state.authenticated = False
            st.session_state.user_info = None
            st.rerun()
    
    # Show last refresh time
    st.caption(f"Last refreshed: {st.session_state.last_refresh.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Check for recent responses and show notification
    recent_responses = get_recent_responses(st.session_state.user_info['id'], minutes=5)
    if recent_responses:
        st.success(f"{len(recent_responses)} new response(s) in the last 5 minutes!")
        with st.expander("View Recent Responses"):
            for response in recent_responses:
                st.write(f"**{response['form_title']}** - {response['submitted_at']}")
                st.json(response['responses'])
                st.divider()
    
    # Dashboard tabs
    tab1, tab2, tab3 = st.tabs(["Create Form", "My Forms and Responses", "Analytics"])
    
    with tab1:
        show_create_form()
    
    with tab2:
        show_my_forms()
    
    with tab3:
        show_analytics()

    st.markdown("""
    <div style="text-align:center; font-size:23px; padding:0.5rem 1rem;">
        <strong>Nishant</strong> &nbsp; | &nbsp;
        📧 <a href="mailto:nishant0363@gmail.com" target="_blank">nishant0363@gmail.com</a> &nbsp; | &nbsp;
        📱 <a href="tel:+919306145426" target="_blank">+91-9306145426</a> &nbsp; | &nbsp;
        🌐 <a href="https://nishant0363.github.io/projects.com" target="_blank">Portfolio</a> &nbsp; | &nbsp;
        💼 <a href="https://www.linkedin.com/in/nishant3603/" target="_blank">LinkedIn</a> &nbsp; | &nbsp;
        🐙 <a href="https://github.com/nishant0363" target="_blank">GitHub</a> &nbsp; | &nbsp;
        📄 <a href="https://drive.google.com/file/d/1hOJqhdY38XSEGrRRrjJsipSg2taqWYu-/view?usp=drive_link" target="_blank">Resume</a>
    </div>
    """, unsafe_allow_html=True)

def show_create_form():
    """Show form creation interface"""
    st.subheader("Create New Feedback Form")
    
    # Move dynamic parts outside the form
    title = st.text_input("Form Title", placeholder="e.g., Customer Satisfaction Survey")
    
    st.write("**Questions:**")
    num_questions = st.number_input("Number of Questions", min_value=3, max_value=5, value=3)
    
    questions = []
    
    # Create questions dynamically outside the form
    for i in range(num_questions):
        st.write(f"**Question {i+1}:**")
        col1, col2 = st.columns([3, 1])
        
        with col1:
            question_text = st.text_input(f"Question Text", key=f"q{i}_text", placeholder="Enter your question here...")
        
        with col2:
            question_type = st.selectbox(
                "Type",
                ["text", "multiple_choice"],
                key=f"q{i}_type"
            )
        
        question_data = {
            'text': question_text,
            'type': question_type
        }
        
        # Show options input immediately when multiple_choice is selected
        if question_type == "multiple_choice":
            options = st.text_area(
                f"Options (one per line)",
                key=f"q{i}_options",
                placeholder="Option 1\nOption 2\nOption 3"
            )
            if options:
                question_data['options'] = [opt.strip() for opt in options.split('\n') if opt.strip()]
        
        questions.append(question_data)
    
    # Simple submit button outside of form
    if st.button("Create Form", type="primary"):
        if title and all(q['text'] for q in questions):
            form_id = create_form(st.session_state.user_info['id'], title, questions)
            
            if form_id:
                st.success("Form created successfully!")
                
                # Show shareable link using the proper URL
                base_url = get_app_url()
                form_url = f"{base_url}?form_id={form_id}"
                
                st.info(f"**Shareable Link:** {form_url}")
                st.code(form_url, language="text")
            else:
                st.error("Failed to create form. Please try again.")
        else:
            st.error("Please fill in the form title and all questions")

def show_my_forms():
    """Show list of admin's forms with responses"""
    st.subheader("My Forms")
    st.text("Click on a form to view responses")
    
    forms = get_admin_forms(st.session_state.user_info['id'])
    
    if not forms:
        st.info("No forms created yet. Create your first form in the 'Create Form' tab!")
        return
    
    for form in forms:
        with st.expander(f"{form['title']} (Created: {form['created_at']})"):
            col1, col2 = st.columns([5, 1])
            
            with col1:
                # Show form link
                base_url = get_app_url()
                form_url = f"{base_url}?form_id={form['id']}"
                st.write(f"**Public Link:** {form_url}")
                st.code(form_url, language="text")
            
            with col2:
                responses = get_form_responses(form['id'])
                st.metric("Total Responses", len(responses))
            
            if responses:
                st.subheader("Responses")
                
                # Show the most recent response time
                if responses:
                    latest_response = responses[0]['submitted_at']
                    st.info(f"Latest response: {latest_response}")
                
                # Create DataFrame for tabular view
                df_data = []
                for idx, response in enumerate(responses):
                    row = {'Response #': idx + 1, 'Submitted At': response['submitted_at']}
                    for question, answer in response['responses'].items():
                        row[question] = answer
                    df_data.append(row)
                
                df = pd.DataFrame(df_data)
                st.dataframe(df, use_container_width=True)
                
                # Download responses as CSV
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download as CSV",
                    data=csv,
                    file_name=f"{form['title']}_responses.csv",
                    mime="text/csv"
                )
            else:
                st.info("No responses yet. Share the form link to start collecting feedback!")

def show_analytics():
    """Show analytics dashboard"""
    st.subheader("Analytics Overview")
    
    forms = get_admin_forms(st.session_state.user_info['id'])
    
    if not forms:
        st.info("No forms available for analytics.")
        return
    
    # Overall metrics
    total_forms = len(forms)
    total_responses = sum(len(get_form_responses(form['id'])) for form in forms)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Forms", total_forms)
    with col2:
        st.metric("Total Responses", total_responses)
    with col3:
        if total_forms > 0:
            avg_responses = total_responses / total_forms
            st.metric("Avg Responses per Form", f"{avg_responses:.1f}")
    
    # Responses per form chart
    if total_responses > 0:
        form_response_data = []
        for form in forms:
            responses = get_form_responses(form['id'])
            form_response_data.append({
                'Form': form['title'],
                'Responses': len(responses)
            })
        
        df_chart = pd.DataFrame(form_response_data)
        fig = px.bar(df_chart, x='Form', y='Responses', title='Responses per Form')
        st.plotly_chart(fig, use_container_width=True)
        
        # Response timeline
        timeline_data = []
        for form in forms:
            responses = get_form_responses(form['id'])
            for response in responses:
                timeline_data.append({
                    'Date': response['submitted_at'][:10],  # Extract date only
                    'Form': form['title']
                })
        
        if timeline_data:
            df_timeline = pd.DataFrame(timeline_data)
            daily_counts = df_timeline.groupby('Date').size().reset_index(name='Count')
            fig_timeline = px.line(daily_counts, x='Date', y='Count', title='Daily Response Submissions')
            st.plotly_chart(fig_timeline, use_container_width=True)

def show_public_form(form_id: str):
    """Show public form for submission"""
    form = get_form(form_id)
    
    if not form:
        st.error("Form not found!")
        return
    
    st.title(f"{form['title']}")
    st.write("Please fill out the form below:")
    
    with st.form("feedback_form"):
        responses = {}
        
        for question in form['questions']:
            if question['type'] == 'text':
                response = st.text_area(question['text'], key=f"q_{question['text']}")
            elif question['type'] == 'multiple_choice':
                response = st.selectbox(
                    question['text'],
                    options=[''] + question.get('options', []),
                    key=f"q_{question['text']}"
                )
            
            responses[question['text']] = response
        
        submitted = st.form_submit_button("Submit Feedback")
        
        if submitted:
            if all(responses.values()):
                if submit_response(form_id, responses):
                    st.success("Thank you for your feedback!")
                    st.balloons()
                else:
                    st.error("Failed to submit feedback. Please try again.")
            else:
                st.error("Please answer all questions before submitting.")

    st.markdown("""
    <div style="text-align:center; font-size:23px; padding:0.5rem 1rem;">
        <strong>Nishant</strong> &nbsp; | &nbsp;
        📧 <a href="mailto:nishant0363@gmail.com" target="_blank">nishant0363@gmail.com</a> &nbsp; | &nbsp;
        📱 <a href="tel:+919306145426" target="_blank">+91-9306145426</a> &nbsp; | &nbsp;
        🌐 <a href="https://nishant0363.github.io/projects.com" target="_blank">Portfolio</a> &nbsp; | &nbsp;
        💼 <a href="https://www.linkedin.com/in/nishant3603/" target="_blank">LinkedIn</a> &nbsp; | &nbsp;
        🐙 <a href="https://github.com/nishant0363" target="_blank">GitHub</a> &nbsp; | &nbsp;
        📄 <a href="https://drive.google.com/file/d/1hOJqhdY38XSEGrRRrjJsipSg2taqWYu-/view?usp=drive_link" target="_blank">Resume</a>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()