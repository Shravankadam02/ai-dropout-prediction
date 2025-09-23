# AI-based Dropout Prediction & Counseling System
## Smart India Hackathon 2025 - MVP Prototype

### Overview
This prototype demonstrates an AI-powered system to predict student dropout risk and facilitate mentor interventions. The system analyzes student data including attendance, test scores, fee status, and subject attempts to generate risk scores with explainability.

### Features (MVP)
- **Login System**: Hardcoded credentials for demo (mentor/admin)
- **Data Upload**: CSV upload or sample data loading
- **Risk Assessment**: Rule-based heuristic scoring system
- **Mentor Dashboard**: Color-coded student risk table
- **Student Profiles**: Detailed view with charts and intervention notes
- **Admin Dashboard**: Summary statistics and charts
- **Explainability**: Clear reasons for risk flags with suggestions

### Tech Stack
- **Backend**: Python Flask
- **Frontend**: HTML5, Bootstrap 5, Chart.js
- **Data**: CSV files, JSON persistence
- **ML**: Rule-based heuristics (production-ready for scikit-learn integration)

## Setup Instructions

### Prerequisites
- Python 3.8+ installed
- Git (optional)

### Installation Steps

1. **Clone/Download Project**
```bash
# If using git
git clone <your-repo-url>
cd dropout-prediction-system

# Or download and extract ZIP file
```

2. **Create Virtual Environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Create Data Directory Structure**
```bash
mkdir -p data static/uploads
```

5. **Add Sample Data**
Place `students_sample.csv` in the `data/` directory.

6. **Run the Application**
```bash
python app.py
# Or
python -m flask run
```

7. **Access the Application**
Open browser and navigate to: `http://localhost:5000`

### Demo Credentials
- **Username**: `mentor`
- **Password**: `admin`

## Quick Demo Flow

1. **Login** → Use mentor/admin credentials
2. **Load Data** → Upload CSV or use sample data
3. **View Dashboard** → See color-coded risk students
4. **Check Profile** → Click on high-risk student
5. **Add Note** → Log intervention in student modal
6. **Admin View** → Check summary statistics

## Risk Scoring Algorithm

The system uses a weighted heuristic approach:

### Components (0-1 scale each):
1. **Attendance Risk** (50% weight): `max(0, (75 - attendance_percent) / 75)`
2. **Score Drop Risk** (30% weight): `min(max((previous_avg - current_avg)/100, 0), 1)`
3. **Fee Due Risk** (15% weight): `min(fees_due_days / 90, 1)`
4. **Attempts Risk** (5% weight): `min((attempts - 1) / 4, 1)`

### Risk Thresholds:
- **High Risk**: ≥ 0.70 (Red)
- **Medium Risk**: 0.40-0.69 (Yellow) 
- **Low Risk**: < 0.40 (Green)

## File Structure
```
dropout-prediction-system/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── README.md          # This file
├── data/
│   ├── students_sample.csv    # Sample student data
│   └── student_notes.json     # Intervention notes storage
├── templates/         # HTML templates
├── static/           # CSS, JS, uploads
└── utils/            # Risk calculation utilities
```

## Expected Sample Outputs

Based on the provided sample data, expected risk classifications:
- **High Risk**: S1003 (Amit Singh), S1008 (Pooja Joshi)
- **Medium Risk**: S1001 (Ramesh Kumar), S1005 (Rohit Gupta), S1007 (Arjun Mehta), S1011 (Karan Yadav)
- **Low Risk**: S1002, S1004, S1006, S1009, S1010, S1012

## What's Implemented vs Simulated

### ✅ Implemented:
- Complete risk scoring algorithm
- CSV data processing
- Interactive dashboard
- Student profile modals
- Note-taking functionality
- Bootstrap responsive design
- Chart.js visualizations

### 🔄 Simulated (for demo):
- Authentication (hardcoded)
- SMS/Email notifications (UI only)
- Real-time data updates
- Production database

## Security Considerations (Production Checklist)
- [ ] Implement JWT tokens for authentication
- [ ] Use bcrypt for password hashing
- [ ] Enable HTTPS in production
- [ ] Encrypt sensitive data in database
- [ ] Add input validation and sanitization
- [ ] Implement rate limiting
- [ ] Add CSRF protection

## Deployment Options

### Local Development
```bash
python app.py
```

### Heroku Deployment
```bash
# Add Procfile: web: python app.py
heroku create your-app-name
git push heroku main
```

### Render Deployment
```bash
# Add render.yaml configuration
# Deploy via Render dashboard
```

## Future Roadmap
1. **Advanced ML**: Replace heuristics with trained models (Random Forest, Neural Networks)
2. **Real-time Data**: Connect to Student Information System APIs
3. **Mobile App**: React Native companion app
4. **Advanced Analytics**: Predictive modeling with time-series analysis
5. **Integration**: SMS/Email notifications, calendar integration
6. **Scalability**: Database optimization, caching layer

## Support
For demo purposes, this prototype includes sample data and hardcoded configurations. Contact the development team for production deployment guidance.

---
**Smart India Hackathon 2025** | **Team**: [Your Team Name] | **Problem Statement**: Student Dropout Prediction