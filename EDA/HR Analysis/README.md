# HR Analytics EDA Project

Welcome to a comprehensive Exploratory Data Analysis (EDA) project conducted on a real-world HR dataset. This project focuses on uncovering key insights related to workforce performance, engagement, diversity, attendance, and attrition, which are critical to data-driven HR decision-making.

---

## Section 1: Project Overview & Objectives

This project aims to simulate a real HR analytics scenario, where we act as a data analyst tasked with delivering business-oriented insights to help HR and leadership teams make smarter workforce decisions.

### Business Objectives:

1. **Understand Workforce Demographics & Diversity**
2. **Analyze Employee Engagement, Performance, and Productivity**
3. **Evaluate Attendance Risk Factors**
4. **Identify Attrition Patterns and Causes**
5. **Assess Custom HR Features for Strategic Impact**

---

## Section 2: Dataset Overview

| Feature | Description |
|--------|-------------|
| `Employee_Name` | Employee full name |
| `Salary` | Annual salary in USD |
| `Position` | Job title |
| `State`, `Zip` | Location info |
| `DOB`, `Age` | Date of birth and age |
| `Sex`, `RaceDesc`, `HispanicLatino` | Demographic info |
| `DateofHire`, `DateofTermination`, `TenureYears` | Employment lifecycle |
| `PerformanceScore`, `EmpSatisfaction`, `EngagementSurvey` | Performance & engagement measures |
| `Absences`, `DaysLateLast30` | Attendance info |
| `Department`, `ManagerName`, `RecruitmentSource` | Organizational details |
| `Is_Terminated`, `TerminationCategory`, `TermReason` | Attrition info |
| `ProjectParticipationLevel`, `EngagementLevel`, `SatisfactionLevel` | Custom engineered features |
| `SeniorityLevel`, `Is_Manager`, `ManagerTeamSize` | Hierarchy and role level |

---

## Section 3: Visual EDA Summary

### Demographic Representation
- Gender balance is skewed; majority male.
- Racial diversity shows underrepresentation in leadership roles.
- Hispanic/Latino representation is relatively low.

### Equity Analysis
- Minor pay gaps by gender and race detected.
- Leadership roles are disproportionately filled by majority demographic groups.

### Engagement, Performance & Productivity
- Positive correlation between engagement survey scores and performance.
- Higher satisfaction often co-occurs with fewer absences.
- Participation in special projects linked to stronger engagement.

### Attendance Risk Indicators
- Employees with high `AbsenceLevel` and `LatenessSeverity` scores tend to have lower performance and engagement.
- Violin plots show that performance dips at higher absence levels.

---

## Section 4: Custom Feature Evaluation

We engineered several custom features to enhance analysis:

- `SeniorityLevel`: Classified job titles into entry, mid, and senior levels.
- `EngagementLevel`, `SatisfactionLevel`: Binned continuous survey scores.
- `ProjectParticipationLevel`: Binned special projects count.
- `AbsenceLevel`, `LatenessSeverity`: Scaled attendance behavior.

### Key Insights:

- **EngagementLevel vs ProjectParticipation**: Higher participation is associated with higher engagement.
- **Seniority vs Salary & Performance**: Clear trend where higher seniority maps to better performance and higher salary.
- **Recruitment Channels**: Referrals and certain platforms bring in top-performing employees.

---

## Attrition & Retention Insights

- High termination rate in entry-level roles.
- Voluntary resignations are common among low-engagement employees.
- Leadership and senior professionals show lower attrition.

---

## Section 5: Key Strategic Takeaways

- **Diversity Gaps Exist**: Particularly in leadership and pay equity.
- **Engagement Drives Results**: Strong correlation with performance and retention.
- **Attendance Predicts Risk**: High absence or lateness scores correlate with poor performance.
- **Referral Strategy Works**: Referred employees show better engagement.
- **Custom Features Add Value**: Helped visualize patterns missed by raw data.

---

## Final Thoughts

This HR Analytics project demonstrates how a structured EDA process can extract critical insights that align with real business challenges. From diversity tracking to attrition prevention, this analysis bridges the gap between data and HR strategy.

>  Tools Used: `Pandas`, `Seaborn`, `Matplotlib`, `Numpy`, `Jupyter Notebook`

>  Real-World Focus: Performance optimization, retention, inclusion, and engagement strategy through data.

---

## Author

**Ubaid Khan**  
*Aspiring Data Analyst with focus on real-world business problems*

---

