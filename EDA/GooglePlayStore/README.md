#  Google Play Store EDA Project

Welcome to an exploratory data analysis (EDA) project based on real-world Google Play Store data.

The objective is to extract strategic, product, marketing, and technical insights from app metadata.

---

##  Section 1: Project Overview & Objectives

This project aims to demonstrate industrial-grade EDA practices using a mobile app dataset. The analysis is structured around **6 business-oriented objectives**:

###  Business Objectives:

1. **Product Strategy & Portfolio Insights**  
   → Understand app categories, genres, installs, and ratings.

2. **Market Insights & Monetization Strategy**  
   → Uncover trends in pricing, monetization, and potential revenue.

3. **User Engagement & Experience**  
   → Explore rating distributions, reviews, and app quality signals.

4. **App Maintenance & Lifecycle**  
   → Investigate how app updates affect performance and reputation.

5. **Platform Compatibility Analysis**  
   → Understand Android version targeting across the ecosystem.

6. **Anomaly & Opportunity Detection**  
   → Surface unusual patterns for product or business leverage.

---

##  Section 2: Dataset Overview

| Feature           | Description                             |
|------------------|-----------------------------------------|
| `app`            | App name                                |
| `category`       | Primary category                        |
| `rating`         | User rating (0.0 to 5.0)                |
| `reviews`        | Number of reviews                       |
| `size_mb`        | Size of app (in MBs)                    |
| `installs`       | Number of installs                      |
| `type`           | Free or Paid                            |
| `price_usd`      | Price in USD                            |
| `content_rating` | Age-appropriateness of the app          |
| `genres`         | Genre (extracted from multi-tag field)  |
| `last_updated`   | Last update date                        |
| `days_since_update` | Days since last update (feature added) |
| `android_ver`    | Minimum required Android version        |

###  Dataset Stats:

- **Total apps:** 9,656  
- **Features:** 16  
- **Missing values:** Mostly in `current_ver` and `android_ver` (minor)  
- **Duplicates:** Cleaned  
- **Nulls:** Handled via category-wise medians and drops

---

##  Section 3: Visual EDA Summaries

### Objective 1: Product Strategy & Portfolio Insights

- Top categories: Family, Game, Tools dominate app count
- Best-rated genres: Events, Books & Reference, Puzzle
- Most installed content: “Everyone” rated apps dominate installs
- Family & Game also lead in paid app volume
- Top genres by ratings ≠ Top genres by installs (Events rated high, Communication widely installed)

### Objective 2: Market Insights & Monetization Strategy

- 90%+ apps are free
- Paid apps have skewed price distribution; most under $10
- High-price outliers in Finance & Lifestyle
- Revenue proxy = price × installs shows Family, Lifestyle, and Game apps earning the most
- Correlation: Price has weak/no relationship with installs or ratings

### Objective 3: User Engagement & Experience

- Ratings skewed toward 4.0–4.5, peaking around 4.3
- Strong correlation between installs and number of reviews
- Top-rated apps have 5-star ratings and 1M+ installs (excellent UX)
- Low-rated apps with millions of installs hint at experience debt

### Objective 4: App Maintenance & Lifecycle

- Most apps haven’t been updated in 2+ years
- Slight decline in ratings with longer update gaps
- Categories like Dating and Shopping have longest update delays
- Frequent updates do not guarantee high ratings, but non-updated apps risk obsolescence

### Objective 5: Platform Compatibility Analysis

- Majority of apps target Android 4.0 - 5.0
- 68% of apps support Android ≤ 4.1 (legacy)
- Family, Game, and Tools categories are most affected by legacy burden
- No strong correlation between Android version and ratings or installs, but modern apps tend to perform better in installs

### Objective 6: Anomaly & Opportunity Detection

- Finance and Events: High average price, low installs → overpricing risk
- Underrated apps (4.5+ rating, low installs) → UX gems for promotion
- Legacy apps like Gmail, Facebook have 1B+ installs without updates → goldmines or technical risk
- Flagged segments for optimization: Pricing, promotion, update strategy

---

## Section 4: Key Strategic Insights

- **Category concentration:** A few categories dominate app creation
- **Rating vs installs gap:** High-rated apps often go unnoticed
- **Revenue ≠ Price:** Installs matter more than pricing in volume
- **Maintenance ≈ Trust:** Longer update delays subtly affect ratings
- **Backward compatibility:** Many apps support outdated Android versions
- **Hidden opportunities:** Legacy apps & niche UX performers are growth levers

---

## Section 5: Recommendations

### Product
- Promote underrated apps with proven UX
- Audit legacy apps with high installs for performance & UX improvements

### Marketing
- Adjust pricing strategies in overpriced low-volume categories
- Run freemium experiments in Finance, Business

### Engineering/QA
- Prioritize updates for apps not touched in 2+ years
- Decrease support for Android < 4.4 in low-install apps

---

## Final Note

This analysis demonstrates how real-world app metadata can uncover strategic insights across **product, marketing, engineering, and business operations**.

> Built with `Pandas`,  `Seaborn/Matplotlib`,  `EDA mindset`.

---
