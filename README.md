# 🚀 cform-engine-nishant - Advanced Feedback Collection Platform

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Try%20Now-blue?style=for-the-badge&logo=streamlit)](https://cform-engine-nishant.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red?style=for-the-badge&logo=streamlit)](https://streamlit.io/)
[![Supabase](https://img.shields.io/badge/Supabase-Database-green?style=for-the-badge&logo=supabase)](https://supabase.com/)

## 🎯 Try the Live Application

**🔗 [Launch cform-engine-nishant - https://cform-engine-nishant.streamlit.app/](https://cform-engine-nishant.streamlit.app/)**

![Dashboard Preview](https://drive.google.com/file/d/1ZBkSzgeAxoU_YHeJUa3Xa1t_fV1tm8jH/view?usp=sharing)

https://drive.google.com/file/d/1ZBkSzgeAxoU_YHeJUa3Xa1t_fV1tm8jH/view?usp=sharing
## 📹 Video Demo

[![Watch Demo](https://img.shields.io/badge/Watch%20Demo-YouTube-red?style=for-the-badge&logo=youtube)](VIDEO_LINK_HERE)

*Click above to see a complete walkthrough of the application features*

---

## 🌟 Overview

**cform-engine-nishant** is a sophisticated, full-stack feedback collection platform that enables administrators to create, distribute, and analyze custom feedback forms with real-time response tracking. Built with modern technologies and featuring a clean, responsive interface, this platform streamlines the entire feedback collection process from creation to analysis.

### ✨ Key Highlights

- **Secure Authentication**: JWT-based user authentication with password hashing
- **Dynamic Form Builder**: Create custom forms with multiple question types
- **Public Form Sharing**: Generate shareable links for easy distribution
- **Real-time Analytics**: Interactive charts and response tracking
- **Live Notifications**: Get notified of new responses within minutes
- **Responsive Design**: Works seamlessly across all devices
- **Data Export**: Download responses as CSV files
- **Modern UI**: Clean, professional interface with STIX Two Text font

---

## 🛠️ Technology Stack

### Backend
- **Python 3.8+** - Core programming language
- **Streamlit** - Web application framework
- **Supabase** - PostgreSQL database and real-time subscriptions
- **JWT (PyJWT)** - Authentication tokens
- **Pandas** - Data manipulation and analysis
- **Requests** - HTTP client for API calls

### Frontend
- **Streamlit Components** - Interactive UI elements
- **Plotly** - Interactive charts and visualizations
- **Custom CSS** - Styling and responsive design
- **Google Fonts** - Typography (STIX Two Text)

### Database
- **PostgreSQL** (via Supabase) - Primary database
- **Real-time subscriptions** - Live data updates
- **RESTful API** - Database interactions

---

## 🚀 Features

### 🔐 User Management
- **Secure Registration**: Create admin accounts with email validation
- **JWT Authentication**: Secure session management
- **Password Hashing**: SHA-256 encryption for security
- **Session Persistence**: Stay logged in across browser sessions

### 📝 Form Creation
- **Dynamic Form Builder**: Create forms with 3-5 questions
- **Multiple Question Types**:
  - Text input for open-ended responses
  - Multiple choice with custom options
- **Real-time Preview**: See your form as you build it
- **Instant Sharing**: Generate public URLs immediately

### 🔗 Form Distribution
- **Public Form URLs**: Share forms via generated links
- **No Registration Required**: Users can submit without accounts
- **Mobile Responsive**: Forms work on all devices
- **Clean Interface**: User-friendly submission experience

### 📊 Analytics & Reporting
- **Real-time Dashboard**: Track responses as they come in
- **Response Metrics**: Total forms, responses, and averages
- **Interactive Charts**: 
  - Bar charts for response distribution
  - Timeline charts for submission patterns
- **Data Export**: Download responses as CSV files
- **Response History**: View all submissions with timestamps

### 🔔 Notifications
- **Live Updates**: Get notified of new responses within 5 minutes
- **Recent Activity**: See the latest form submissions
- **Refresh Tracking**: Know when data was last updated
- **Response Alerts**: Success notifications for new submissions

---

## 🏗️ Database Schema

### Users Table
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(64) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### Forms Table
```sql
CREATE TABLE forms (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    admin_id INTEGER REFERENCES users(id),
    title VARCHAR(200) NOT NULL,
    questions JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### Responses Table
```sql
CREATE TABLE responses (
    id SERIAL PRIMARY KEY,
    form_id UUID REFERENCES forms(id),
    responses JSONB NOT NULL,
    submitted_at TIMESTAMP DEFAULT NOW()
);
```

---

##  User Interface

### Login/Registration Page
- Clean, centered design with tabbed interface
- Input validation and error handling
- Professional styling with consistent branding

### Admin Dashboard
- **Header**: User info, refresh button, and logout
- **Notification Bar**: Real-time response alerts
- **Three Main Tabs**:
  1. **Create Form**: Dynamic form builder
  2. **My Forms**: View and manage created forms
  3. **Analytics**: Charts and metrics

### Public Form Page
- Minimal, distraction-free design
- Clear question presentation
- Instant submission feedback
- Thank you message with animations

---

## Responsive Design

The application is fully responsive and works seamlessly across:
- **Desktop**: Full-featured experience
- **Tablet**: Optimized layout for touch interaction
- **Mobile**: Streamlined interface for easy form submission

---

## 🔧 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Supabase account (free tier available)

### 1. Clone the Repository
```bash
git clone https://github.com/nishant0363/cform-engine-nishant.git
cd cform-engine-nishant
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Environment Setup
Create a `.env` file in the root directory:
```env
SECRET_KEY=your_jwt_secret_key_here
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
```

### 4. Database Setup
Run the following SQL commands in your Supabase SQL editor:

```sql
-- Create users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(64) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create forms table
CREATE TABLE forms (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    admin_id INTEGER REFERENCES users(id),
    title VARCHAR(200) NOT NULL,
    questions JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create responses table
CREATE TABLE responses (
    id SERIAL PRIMARY KEY,
    form_id UUID REFERENCES forms(id),
    responses JSONB NOT NULL,
    submitted_at TIMESTAMP DEFAULT NOW()
);
```

### 5. Run the Application
```bash
streamlit run app.py
```

---

## 📋 Usage Guide

### For Administrators

1. **Registration/Login**
   - Create an admin account or log in
   - Secure authentication with JWT tokens

2. **Creating Forms**
   - Navigate to "Create Form" tab
   - Enter form title and questions
   - Choose question types (text or multiple choice)
   - Click "Create Form" to generate

3. **Sharing Forms**
   - Copy the generated public URL
   - Share via email, social media, or any platform
   - No registration required for respondents

4. **Viewing Responses**
   - Check "My Forms" tab for all responses
   - Export data as CSV files
   - Monitor real-time analytics

### For Respondents

1. **Accessing Forms**
   - Click on the shared form URL
   - No account creation required

2. **Submitting Responses**
   - Fill out all required fields
   - Click "Submit Feedback"
   - See confirmation message

---

##  Use Cases

### Business Applications
- **Customer Feedback**: Collect product reviews and suggestions
- **Employee Surveys**: Gather internal feedback and insights
- **Event Feedback**: Post-event evaluation and improvements
- **Service Quality**: Monitor customer satisfaction levels

### Educational Applications
- **Course Evaluations**: Student feedback on courses and instructors
- **Workshop Assessments**: Training effectiveness measurement
- **Research Surveys**: Academic data collection
- **Student Satisfaction**: Campus services evaluation

### Personal Projects
- **Community Feedback**: Local organization input
- **Product Testing**: User experience research
- **Content Evaluation**: Blog or video feedback
- **Service Improvement**: Small business customer insights

---

##  Security Features

### Authentication Security
- **JWT Tokens**: Secure session management
- **Password Hashing**: SHA-256 encryption
- **Session Expiration**: 24-hour token validity
- **Input Validation**: Prevent SQL injection and XSS

### Data Protection
- **Secure Database**: Supabase with RLS policies
- **HTTPS Encryption**: All data transmission secured
- **Environment Variables**: Sensitive keys protected
- **Error Handling**: Graceful failure without data exposure

---

##  Analytics Features

### Response Metrics
- **Total Forms Created**: Track form creation activity
- **Total Responses**: Monitor submission volume
- **Average Responses**: Form performance indicators
- **Response Timeline**: Submission patterns over time

### Visual Analytics
- **Bar Charts**: Response distribution by form
- **Line Charts**: Daily submission trends
- **Real-time Updates**: Live data refresh
- **Interactive Visualizations**: Hover effects and details

---

##  Deployment

### Streamlit Cloud (Recommended)
1. Push code to GitHub repository
2. Connect to Streamlit Cloud
3. Set environment variables in Streamlit dashboard
4. Deploy with one click

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export SECRET_KEY="your_secret_key"
export SUPABASE_URL="your_supabase_url"
export SUPABASE_KEY="your_supabase_key"

# Run the application
streamlit run app.py
```

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Nishant**
- 📧 Email: [nishant0363@gmail.com](mailto:nishant0363@gmail.com)
- 📱 Phone: [+91-9306145426](tel:+919306145426)
- 💼 LinkedIn: [linkedin.com/in/nishant3603](https://www.linkedin.com/in/nishant3603/)
- 🐙 GitHub: [github.com/nishant0363](https://github.com/nishant0363)
- 📄 Resume: [View Resume](https://drive.google.com/file/d/1XPv4DTWq3_QCwWM4V0_m_SY6J0A1pY9e/view?usp=sharing)

---

## 🙏 Acknowledgments

- **Streamlit Team** for the amazing framework
- **Supabase Team** for the robust database platform
- **Plotly Team** for beautiful visualizations
- **Open Source Community** for inspiration and support

---


*Built with ❤️ by Nishant using Streamlit and Supabase*
