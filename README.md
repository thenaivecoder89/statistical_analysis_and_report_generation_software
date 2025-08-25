# statistical_analysis_and_report_generation_software
## Purpose: 
Run multiple statistical analysis on categorical and numerical data points and provide insights on the same.

## Architecture:
### Backend (Deployed on Railway)
- **Database**: PostgreSQL  
- **ORM / Connection**: SQLAlchemy (Python)  
- **Data Cleansing**: Pandas (Python)  
- **Statistical Analysis**: SciPy, Seaborn, Matplotlib, Pandas, NumPy  
- **Insights Generation**: OpenAI `chatgpt-4o-latest`  
- **API Layer**: FastAPI + Uvicorn  
### Frontend (Developed on Replit)
- **Framework**: React (with TypeScript)  
- **Build Tool / Dev Server**: Vite  
- **Styling**: TailwindCSS (via PostCSS)  
- **Data Fetching**: React Query (TanStack Query)  
- **State / Hooks**: Custom hooks (`use-toast`, `use-mobile`) and React Context  

## Workflow Overview:
1. **Data Ingestion**  
   SQLAlchemy pulls records from a PostgreSQL-based data lake.  
2. **Data Cleansing**  
   Pandas ensures completeness and consistency; cleansed data is written into data marts.  
3. **Statistical Analysis**  
   - *Categorical data*  
     - Cross-tab analysis  
     - Dendrogram clustering  
     - Chi-Square test  
   - *Numerical data*  
     - Histogram  
     - Kernel Density Estimation (KDE)  
     - Scatterplot  
     - Boxplot  
     - Correlation analysis  
4. **Insights Generation (LLM Layer)**  
   - Inputs: raw dataset (JSON), analyzed dataset (JSON), plots (JSON / Base64 encoded)  
   - Outputs:  
     - Overall summary  
     - Statistical significance insights (correlation, chi-square)  
     - Recommendations for decision-making  
5. **API Exposure**  
   FastAPI exposes the insights as cloud-ready endpoints returning JSON (including ASCII-encoded plots).  
6. **Frontend Integration**  
   The React/Vite frontend (hosted on Replit) fetches data from the API and provides an interactive UI with charts, analysis results, and AI-generated insights.

## Quick Start Guide:
```bash
# Inside /server
pip install -r requirements.txt
uvicorn index:app --reload
