"""
Quantitative Data Analyzer
Performs statistical analysis on quantitative datasets (surveys, questionnaires)
"""
import pandas as pd
import numpy as np
from scipy import stats
import os

class QuantitativeAnalyzer:
    def __init__(self, csv_file):
        """Initialize with path to CSV dataset"""
        self.csv_file = csv_file
        self.df = pd.read_csv(csv_file)
        print(f"📊 Loaded dataset: {len(self.df)} rows, {len(self.df.columns)} columns")
    
    def get_demographics_summary(self):
        """Generate demographic summary tables"""
        print("  📋 Analyzing demographics...")
        
        demographics = {}
        
        # Age distribution
        if 'Age' in self.df.columns:
            demographics['age'] = {
                'mean': self.df['Age'].mean(),
                'std': self.df['Age'].std(),
                'min': self.df['Age'].min(),
                'max': self.df['Age'].max(),
                'distribution': self.df['Age'].value_counts().to_dict()
            }
        
        # Gender distribution
        if 'Gender' in self.df.columns:
            demographics['gender'] = self.df['Gender'].value_counts().to_dict()
        
        # Education distribution
        if 'Education' in self.df.columns:
            demographics['education'] = self.df['Education'].value_counts().to_dict()
        
        # Occupation distribution
        if 'Occupation' in self.df.columns:
            demographics['occupation'] = self.df['Occupation'].value_counts().to_dict()
        
        return demographics
    
    def generate_frequency_tables(self, variables=None):
        """Generate frequency tables for categorical variables"""
        print("  📊 Generating frequency tables...")
        
        if variables is None:
            # Auto-detect categorical variables
            variables = [col for col in self.df.columns if col.startswith('Q') and not 'Likert' in col]
        
        tables = {}
        for var in variables:
            if var in self.df.columns:
                freq = self.df[var].value_counts()
                percent = (freq / len(self.df) * 100).round(2)
                tables[var] = pd.DataFrame({
                    'Frequency': freq,
                    'Percentage': percent
                })
        
        return tables
    
    def get_descriptive_statistics(self, likert_vars=None):
        """Calculate descriptive statistics for Likert scale variables"""
        print("  📈 Calculating descriptive statistics...")
        
        if likert_vars is None:
            # Auto-detect Likert variables
            likert_vars = [col for col in self.df.columns if 'Likert' in col or col.startswith('Q') and self.df[col].dtype in ['int64', 'float64']]
        
        stats_dict = {}
        for var in likert_vars:
            if var in self.df.columns and self.df[var].dtype in ['int64', 'float64']:
                stats_dict[var] = {
                    'mean': self.df[var].mean(),
                    'std': self.df[var].std(),
                    'min': self.df[var].min(),
                    'max': self.df[var].max(),
                    'median': self.df[var].median()
                }
        
        return stats_dict
    
    def perform_correlation_analysis(self, variables=None):
        """Perform correlation analysis between numeric variables"""
        print("  🔗 Performing correlation analysis...")
        
        if variables is None:
            # Auto-detect numeric variables
            numeric_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
            variables = [col for col in numeric_cols if col not in ['RespondentID', 'Age']]
        
        if len(variables) < 2:
            return None
        
        correlation_matrix = self.df[variables].corr()
        
        # Find significant correlations
        significant_corr = []
        for i in range(len(variables)):
            for j in range(i+1, len(variables)):
                corr_value = correlation_matrix.iloc[i, j]
                if abs(corr_value) > 0.3:  # Threshold for moderate correlation
                    significant_corr.append({
                        'var1': variables[i],
                        'var2': variables[j],
                        'correlation': corr_value,
                        'strength': self._interpret_correlation(corr_value)
                    })
        
        return {
            'matrix': correlation_matrix,
            'significant': significant_corr
        }
    
    def perform_regression_analysis(self, dependent_var, independent_vars):
        """Perform multiple regression analysis"""
        print(f"  📉 Performing regression: {dependent_var} ~ {independent_vars}")
        
        from sklearn.linear_model import LinearRegression
        from sklearn.metrics import r2_score
        
        # Prepare data
        X = self.df[independent_vars].dropna()
        y = self.df.loc[X.index, dependent_var]
        
        # Fit model
        model = LinearRegression()
        model.fit(X, y)
        
        # Predictions
        y_pred = model.predict(X)
        
        # Results
        results = {
            'coefficients': dict(zip(independent_vars, model.coef_)),
            'intercept': model.intercept_,
            'r_squared': r2_score(y, y_pred),
            'n': len(X)
        }
        
        return results
    
    def perform_chi_square_test(self, var1, var2):
        """Perform chi-square test for independence"""
        print(f"  ✖️  Chi-square test: {var1} vs {var2}")
        
        # Create contingency table
        contingency = pd.crosstab(self.df[var1], self.df[var2])
        
        # Perform test
        chi2, p_value, dof, expected = stats.chi2_contingency(contingency)
        
        return {
            'chi2': chi2,
            'p_value': p_value,
            'dof': dof,
            'significant': p_value < 0.05,
            'contingency_table': contingency
        }
    
    def perform_t_test(self, var, group_var):
        """Perform independent t-test"""
        print(f"  📊 T-test: {var} by {group_var}")
        
        groups = self.df[group_var].unique()
        if len(groups) != 2:
            return None
        
        group1 = self.df[self.df[group_var] == groups[0]][var]
        group2 = self.df[self.df[group_var] == groups[1]][var]
        
        t_stat, p_value = stats.ttest_ind(group1, group2)
        
        return {
            'groups': groups.tolist(),
            'group1_mean': group1.mean(),
            'group2_mean': group2.mean(),
            't_statistic': t_stat,
            'p_value': p_value,
            'significant': p_value < 0.05
        }
    
    def perform_anova(self, dependent_var, group_var):
        """Perform one-way ANOVA"""
        print(f"  📊 ANOVA: {dependent_var} by {group_var}")
        
        groups = self.df[group_var].unique()
        group_data = [self.df[self.df[group_var] == group][dependent_var].dropna() for group in groups]
        
        f_stat, p_value = stats.f_oneway(*group_data)
        
        # Calculate group means
        group_means = {group: self.df[self.df[group_var] == group][dependent_var].mean() 
                      for group in groups}
        
        return {
            'groups': groups.tolist(),
            'group_means': group_means,
            'f_statistic': f_stat,
            'p_value': p_value,
            'significant': p_value < 0.05,
            'effect_size': self._calculate_eta_squared(dependent_var, group_var)
        }
    
    def perform_ancova(self, dependent_var, group_var, covariate):
        """Perform ANCOVA (Analysis of Covariance)"""
        print(f"  📊 ANCOVA: {dependent_var} by {group_var}, controlling for {covariate}")
        
        from statsmodels.formula.api import ols
        from statsmodels.stats.anova import anova_lm
        
        # Create formula
        formula = f"{dependent_var} ~ C({group_var}) + {covariate}"
        
        # Fit model
        model = ols(formula, data=self.df).fit()
        anova_table = anova_lm(model, typ=2)
        
        return {
            'anova_table': anova_table,
            'r_squared': model.rsquared,
            'adjusted_r_squared': model.rsquared_adj
        }
    
    def perform_manova(self, dependent_vars, group_var):
        """Perform MANOVA (Multivariate Analysis of Variance)"""
        print(f"  📊 MANOVA: {dependent_vars} by {group_var}")
        
        from statsmodels.multivariate.manova import MANOVA
        
        # Create formula
        formula = f"{' + '.join(dependent_vars)} ~ C({group_var})"
        
        # Fit MANOVA
        manova = MANOVA.from_formula(formula, data=self.df)
        result = manova.mv_test()
        
        return {
            'result': result,
            'summary': str(result)
        }
    
    def perform_factor_analysis(self, variables, n_factors=None):
        """Perform Exploratory Factor Analysis"""
        print(f"  🔍 Factor Analysis on {len(variables)} variables")
        
        from sklearn.decomposition import FactorAnalysis
        from factor_analyzer import FactorAnalyzer
        
        # Prepare data
        data = self.df[variables].dropna()
        
        # Determine number of factors if not specified
        if n_factors is None:
            # Use Kaiser criterion (eigenvalues > 1)
            fa = FactorAnalyzer(rotation=None)
            fa.fit(data)
            ev, _ = fa.get_eigenvalues()
            n_factors = sum(ev > 1)
        
        # Perform factor analysis with rotation
        fa = FactorAnalyzer(n_factors=n_factors, rotation='varimax')
        fa.fit(data)
        
        loadings = fa.loadings_
        variance = fa.get_factor_variance()
        
        return {
            'n_factors': n_factors,
            'loadings': loadings,
            'variance_explained': variance[1],  # Proportional variance
            'cumulative_variance': variance[2],  # Cumulative variance
            'communalities': fa.get_communalities()
        }
    
    def calculate_cronbach_alpha(self, variables):
        """Calculate Cronbach's Alpha for reliability"""
        print(f"  ✅ Calculating Cronbach's Alpha for {len(variables)} items")
        
        from factor_analyzer.factor_analyzer import calculate_bartlett_sphericity, calculate_kmo
        
        data = self.df[variables].dropna()
        
        # Calculate Cronbach's Alpha
        item_variances = data.var(axis=0, ddof=1)
        total_variance = data.sum(axis=1).var(ddof=1)
        n_items = len(variables)
        
        alpha = (n_items / (n_items - 1)) * (1 - item_variances.sum() / total_variance)
        
        # KMO test
        kmo_all, kmo_model = calculate_kmo(data)
        
        # Bartlett's test
        chi_square, p_value = calculate_bartlett_sphericity(data)
        
        return {
            'cronbach_alpha': alpha,
            'n_items': n_items,
            'kmo': kmo_model,
            'bartlett_chi2': chi_square,
            'bartlett_p': p_value,
            'interpretation': self._interpret_alpha(alpha)
        }
    
    def perform_panel_analysis(self, dependent_var, independent_vars, entity_var, time_var):
        """Perform Panel Data Analysis (Fixed/Random Effects)"""
        print(f"  📊 Panel Analysis: {dependent_var}")
        
        from linearmodels import PanelOLS, RandomEffects
        
        # Set multi-index
        panel_data = self.df.set_index([entity_var, time_var])
        
        # Prepare formula
        formula = f"{dependent_var} ~ {' + '.join(independent_vars)}"
        
        # Fixed Effects Model
        fe_model = PanelOLS.from_formula(formula, data=panel_data)
        fe_result = fe_model.fit()
        
        # Random Effects Model
        re_model = RandomEffects.from_formula(formula, data=panel_data)
        re_result = re_model.fit()
        
        return {
            'fixed_effects': {
                'r_squared': fe_result.rsquared,
                'coefficients': fe_result.params.to_dict(),
                'p_values': fe_result.pvalues.to_dict()
            },
            'random_effects': {
                'r_squared': re_result.rsquared,
                'coefficients': re_result.params.to_dict(),
                'p_values': re_result.pvalues.to_dict()
            }
        }
    
    def perform_time_series_analysis(self, time_var, value_var):
        """Perform Time Series Analysis (Trend, Seasonality, ARIMA)"""
        print(f"  📈 Time Series Analysis: {value_var}")
        
        from statsmodels.tsa.seasonal import seasonal_decompose
        from statsmodels.tsa.arima.model import ARIMA
        from statsmodels.tsa.stattools import adfuller
        
        # Prepare time series data
        ts_data = self.df.set_index(time_var)[value_var].dropna()
        
        # Stationarity test (Augmented Dickey-Fuller)
        adf_result = adfuller(ts_data)
        
        # Decomposition
        decomposition = seasonal_decompose(ts_data, model='additive', period=12)
        
        # ARIMA model (auto-select parameters)
        model = ARIMA(ts_data, order=(1, 1, 1))
        arima_result = model.fit()
        
        # Forecast
        forecast = arima_result.forecast(steps=12)
        
        return {
            'adf_statistic': adf_result[0],
            'adf_p_value': adf_result[1],
            'is_stationary': adf_result[1] < 0.05,
            'trend': decomposition.trend.dropna().tolist(),
            'seasonal': decomposition.seasonal.dropna().tolist(),
            'arima_aic': arima_result.aic,
            'arima_bic': arima_result.bic,
            'forecast': forecast.tolist()
        }
    
    def perform_mediation_analysis(self, independent_var, mediator_var, dependent_var):
        """Perform Mediation Analysis (Baron & Kenny approach)"""
        print(f"  🔗 Mediation Analysis: {independent_var} → {mediator_var} → {dependent_var}")
        
        from sklearn.linear_model import LinearRegression
        
        # Step 1: X → Y (total effect)
        X = self.df[[independent_var]].dropna()
        Y = self.df.loc[X.index, dependent_var]
        model_total = LinearRegression().fit(X, Y)
        total_effect = model_total.coef_[0]
        
        # Step 2: X → M
        M = self.df.loc[X.index, mediator_var]
        model_xm = LinearRegression().fit(X, M)
        a_path = model_xm.coef_[0]
        
        # Step 3: X + M → Y (direct effect)
        XM = self.df[[independent_var, mediator_var]].dropna()
        Y_final = self.df.loc[XM.index, dependent_var]
        model_direct = LinearRegression().fit(XM, Y_final)
        direct_effect = model_direct.coef_[0]
        b_path = model_direct.coef_[1]
        
        # Indirect effect
        indirect_effect = a_path * b_path
        
        return {
            'total_effect': total_effect,
            'direct_effect': direct_effect,
            'indirect_effect': indirect_effect,
            'a_path': a_path,
            'b_path': b_path,
            'mediation_type': 'full' if abs(direct_effect) < 0.01 else 'partial'
        }
    
    def perform_moderation_analysis(self, independent_var, moderator_var, dependent_var):
        """Perform Moderation Analysis (Interaction Effects)"""
        print(f"  ⚡ Moderation Analysis: {independent_var} × {moderator_var} → {dependent_var}")
        
        from sklearn.linear_model import LinearRegression
        
        # Create interaction term
        self.df['interaction'] = self.df[independent_var] * self.df[moderator_var]
        
        # Model with interaction
        X = self.df[[independent_var, moderator_var, 'interaction']].dropna()
        Y = self.df.loc[X.index, dependent_var]
        
        model = LinearRegression().fit(X, Y)
        
        return {
            'main_effect_iv': model.coef_[0],
            'main_effect_moderator': model.coef_[1],
            'interaction_effect': model.coef_[2],
            'r_squared': model.score(X, Y),
            'significant_moderation': abs(model.coef_[2]) > 0.1
        }
    
    def _calculate_eta_squared(self, dependent_var, group_var):
        """Calculate effect size (eta squared) for ANOVA"""
        groups = self.df[group_var].unique()
        grand_mean = self.df[dependent_var].mean()
        
        ss_between = sum([len(self.df[self.df[group_var] == group]) * 
                         (self.df[self.df[group_var] == group][dependent_var].mean() - grand_mean)**2 
                         for group in groups])
        
        ss_total = sum((self.df[dependent_var] - grand_mean)**2)
        
        return ss_between / ss_total if ss_total > 0 else 0
    
    def _interpret_alpha(self, alpha):
        """Interpret Cronbach's Alpha"""
        if alpha >= 0.9:
            return "Excellent"
        elif alpha >= 0.8:
            return "Good"
        elif alpha >= 0.7:
            return "Acceptable"
        elif alpha >= 0.6:
            return "Questionable"
        else:
            return "Poor"
    
    def _interpret_correlation(self, r):
        """Interpret correlation strength"""
        abs_r = abs(r)
        if abs_r < 0.3:
            return "weak"
        elif abs_r < 0.7:
            return "moderate"
        else:
            return "strong"
    
    def generate_markdown_tables(self, demographics, freq_tables, descriptive_stats):
        """Generate markdown formatted tables for Chapter 4"""
        print("  📝 Generating markdown tables...")
        
        markdown = "# Chapter 4: Data Analysis Results\n\n"
        
        # Demographics
        markdown += "## 4.1 Demographic Characteristics\n\n"
        
        # Gender table
        if 'gender' in demographics:
            markdown += "### Table 4.1: Gender Distribution\n\n"
            markdown += "| Gender | Frequency | Percentage (%) |\n"
            markdown += "|--------|-----------|----------------|\n"
            total = sum(demographics['gender'].values())
            for gender, count in demographics['gender'].items():
                pct = (count / total * 100)
                markdown += f"| {gender} | {count} | {pct:.1f} |\n"
            markdown += f"| **Total** | **{total}** | **100.0** |\n\n"
        
        # Education table
        if 'education' in demographics:
            markdown += "### Table 4.2: Education Level Distribution\n\n"
            markdown += "| Education Level | Frequency | Percentage (%) |\n"
            markdown += "|----------------|-----------|----------------|\n"
            total = sum(demographics['education'].values())
            for edu, count in demographics['education'].items():
                pct = (count / total * 100)
                markdown += f"| {edu} | {count} | {pct:.1f} |\n"
            markdown += f"| **Total** | **{total}** | **100.0** |\n\n"
        
        # Descriptive statistics table
        if descriptive_stats:
            markdown += "## 4.2 Descriptive Statistics\n\n"
            markdown += "### Table 4.3: Descriptive Statistics for Key Variables\n\n"
            markdown += "| Variable | Mean | SD | Min | Max | Median |\n"
            markdown += "|----------|------|----|----|-----|--------|\n"
            for var, stats_val in list(descriptive_stats.items())[:10]:  # First 10 variables
                markdown += f"| {var} | {stats_val['mean']:.2f} | {stats_val['std']:.2f} | {stats_val['min']} | {stats_val['max']} | {stats_val['median']:.1f} |\n"
            markdown += "\n"
        
        return markdown
