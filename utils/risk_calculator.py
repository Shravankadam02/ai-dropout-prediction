"""
Risk Calculator for Student Dropout Prediction
Implements the heuristic-based risk scoring algorithm
"""

class RiskCalculator:
    def __init__(self):
        """Initialize risk calculator with weights and thresholds"""
        # Risk component weights
        self.weights = {
            'attendance': 0.50,
            'score_trend': 0.30,
            'fees': 0.15,
            'attempts': 0.05
        }
        
        # Risk level thresholds
        self.thresholds = {
            'high': 0.70,
            'medium': 0.40
        }
        
        # Color coding for UI
        self.colors = {
            'High': 'danger',    # Red
            'Medium': 'warning', # Yellow
            'Low': 'success'     # Green
        }

    def calculate_attendance_risk(self, attendance_percent):
        """
        Calculate attendance risk component
        Formula: max(0, (75 - attendance_percent) / 75)
        """
        if attendance_percent >= 75:
            return 0.0
        return max(0, (75 - attendance_percent) / 75)

    def calculate_score_trend_risk(self, previous_avg, current_avg):
        """
        Calculate score trend risk component
        Formula: min(max((previous_avg - current_avg)/100, 0), 1)
        """
        if previous_avg == 0 or current_avg == 0:
            return 0.0
        
        score_drop = previous_avg - current_avg
        if score_drop <= 0:
            return 0.0
        
        return min(max(score_drop / 100, 0), 1)

    def calculate_fee_risk(self, fees_due_days):
        """
        Calculate fee payment risk component
        Formula: min(fees_due_days / 90, 1)
        """
        return min(fees_due_days / 90, 1.0)

    def calculate_attempts_risk(self, attempts):
        """
        Calculate subject attempts risk component
        Formula: min((attempts - 1) / 4, 1)
        """
        if attempts <= 1:
            return 0.0
        return min((attempts - 1) / 4, 1.0)

    def calculate_risk(self, student_data):
        """
        Calculate overall risk score for a student
        Returns basic risk information
        """
        try:
            # Extract required fields with defaults
            attendance = float(student_data.get('attendance_percent', 0))
            fees_due = int(student_data.get('fees_due_days', 0))
            attempts = int(student_data.get('attempts_in_subject_X', 1))
            previous_avg = float(student_data.get('previous_3_tests_avg', 0))
            current_avg = float(student_data.get('last_3_tests_avg', 0))
            
            # Calculate individual risk components
            attendance_risk = self.calculate_attendance_risk(attendance)
            score_risk = self.calculate_score_trend_risk(previous_avg, current_avg)
            fee_risk = self.calculate_fee_risk(fees_due)
            attempts_risk = self.calculate_attempts_risk(attempts)
            
            # Calculate weighted overall risk score
            risk_score = (
                self.weights['attendance'] * attendance_risk +
                self.weights['score_trend'] * score_risk +
                self.weights['fees'] * fee_risk +
                self.weights['attempts'] * attempts_risk
            )
            
            # Determine risk level
            if risk_score >= self.thresholds['high']:
                risk_level = 'High'
            elif risk_score >= self.thresholds['medium']:
                risk_level = 'Medium'
            else:
                risk_level = 'Low'
            
            return {
                'risk_score': risk_score,
                'risk_level': risk_level,
                'risk_color': self.colors[risk_level]
            }
            
        except (ValueError, TypeError) as e:
            # Return safe defaults for malformed data
            return {
                'risk_score': 0.0,
                'risk_level': 'Low',
                'risk_color': self.colors['Low'],
                'error': f'Data processing error: {str(e)}'
            }

    def calculate_detailed_risk(self, student_data):
        """
        Calculate detailed risk analysis with explanations and recommendations
        Returns comprehensive risk breakdown
        """
        try:
            # Extract student data
            attendance = float(student_data.get('attendance_percent', 0))
            fees_due = int(student_data.get('fees_due_days', 0))
            attempts = int(student_data.get('attempts_in_subject_X', 1))
            previous_avg = float(student_data.get('previous_3_tests_avg', 0))
            current_avg = float(student_data.get('last_3_tests_avg', 0))
            
            # Calculate individual components
            attendance_risk = self.calculate_attendance_risk(attendance)
            score_risk = self.calculate_score_trend_risk(previous_avg, current_avg)
            fee_risk = self.calculate_fee_risk(fees_due)
            attempts_risk = self.calculate_attempts_risk(attempts)
            
            # Calculate overall risk
            risk_score = (
                self.weights['attendance'] * attendance_risk +
                self.weights['score_trend'] * score_risk +
                self.weights['fees'] * fee_risk +
                self.weights['attempts'] * attempts_risk
            )
            
            # Determine risk level
            if risk_score >= self.thresholds['high']:
                risk_level = 'High'
            elif risk_score >= self.thresholds['medium']:
                risk_level = 'Medium'
            else:
                risk_level = 'Low'
            
            # Generate explanations and reasons
            risk_factors = []
            
            # Attendance factor
            if attendance_risk > 0:
                risk_factors.append({
                    'factor': 'Attendance',
                    'value': f"{attendance}% (below 75%)",
                    'risk_contribution': attendance_risk * self.weights['attendance'],
                    'severity': 'High' if attendance < 50 else 'Medium' if attendance < 65 else 'Low'
                })
            
            # Score trend factor
            if score_risk > 0:
                score_drop = previous_avg - current_avg
                risk_factors.append({
                    'factor': 'Test Score Trend',
                    'value': f"Dropped by {score_drop:.1f} points",
                    'risk_contribution': score_risk * self.weights['score_trend'],
                    'severity': 'High' if score_drop > 15 else 'Medium' if score_drop > 8 else 'Low'
                })
            
            # Fee factor
            if fee_risk > 0:
                risk_factors.append({
                    'factor': 'Fee Payment',
                    'value': f"{fees_due} days overdue",
                    'risk_contribution': fee_risk * self.weights['fees'],
                    'severity': 'High' if fees_due > 90 else 'Medium' if fees_due > 30 else 'Low'
                })
            
            # Attempts factor
            if attempts_risk > 0:
                risk_factors.append({
                    'factor': 'Subject Attempts',
                    'value': f"{attempts} attempts",
                    'risk_contribution': attempts_risk * self.weights['attempts'],
                    'severity': 'High' if attempts >= 4 else 'Medium' if attempts >= 3 else 'Low'
                })
            
            # Sort risk factors by contribution (highest first)
            risk_factors.sort(key=lambda x: x['risk_contribution'], reverse=True)
            
            # Get top 2 reasons for explainability
            top_reasons = risk_factors[:2] if len(risk_factors) >= 2 else risk_factors
            
            # Generate recommendations
            recommendations = self.generate_recommendations(student_data, risk_factors)
            
            return {
                'risk_score': round(risk_score, 3),
                'risk_level': risk_level,
                'risk_color': self.colors[risk_level],
                'risk_components': {
                    'attendance_risk': round(attendance_risk, 3),
                    'score_trend_risk': round(score_risk, 3),
                    'fee_risk': round(fee_risk, 3),
                    'attempts_risk': round(attempts_risk, 3)
                },
                'weighted_components': {
                    'attendance_weighted': round(attendance_risk * self.weights['attendance'], 3),
                    'score_trend_weighted': round(score_risk * self.weights['score_trend'], 3),
                    'fee_weighted': round(fee_risk * self.weights['fees'], 3),
                    'attempts_weighted': round(attempts_risk * self.weights['attempts'], 3)
                },
                'risk_factors': risk_factors,
                'top_reasons': top_reasons,
                'recommendations': recommendations
            }
            
        except (ValueError, TypeError) as e:
            return {
                'risk_score': 0.0,
                'risk_level': 'Low',
                'risk_color': self.colors['Low'],
                'error': f'Detailed analysis error: {str(e)}',
                'risk_factors': [],
                'top_reasons': [],
                'recommendations': []
            }

    def generate_recommendations(self, student_data, risk_factors):
        """Generate intervention recommendations based on risk factors"""
        recommendations = []
        
        # Get primary risk factors
        primary_risks = [f['factor'] for f in risk_factors if f['severity'] in ['High', 'Medium']]
        
        if 'Attendance' in primary_risks:
            attendance = float(student_data.get('attendance_percent', 0))
            if attendance < 50:
                recommendations.append("URGENT: Schedule immediate parent-teacher meeting and attendance counseling")
            elif attendance < 65:
                recommendations.append("Schedule one-on-one attendance counseling session")
            else:
                recommendations.append("Monitor attendance closely and provide gentle reminders")
        
        if 'Test Score Trend' in primary_risks:
            score_drop = float(student_data.get('previous_3_tests_avg', 0)) - float(student_data.get('last_3_tests_avg', 0))
            if score_drop > 15:
                recommendations.append("Arrange remedial classes and peer tutoring support")
            elif score_drop > 8:
                recommendations.append("Provide additional study materials and practice sessions")
            else:
                recommendations.append("Regular check-ins on study habits and academic support")
        
        if 'Fee Payment' in primary_risks:
            fees_due = int(student_data.get('fees_due_days', 0))
            if fees_due > 90:
                recommendations.append("Connect with financial aid office for payment plan options")
            else:
                recommendations.append("Send fee payment reminder and discuss any financial difficulties")
        
        if 'Subject Attempts' in primary_risks:
            attempts = int(student_data.get('attempts_in_subject_X', 1))
            if attempts >= 4:
                recommendations.append("Consider alternative learning methods or course modification")
            else:
                recommendations.append("Provide focused support for challenging subject areas")
        
        # Add general recommendations based on risk level
        overall_risk = len([f for f in risk_factors if f['severity'] == 'High'])
        if overall_risk >= 2:
            recommendations.append("Schedule weekly mentor meetings and create comprehensive support plan")
        elif overall_risk >= 1:
            recommendations.append("Bi-weekly check-ins and targeted intervention strategy")
        
        return recommendations[:3]  # Return top 3 recommendations