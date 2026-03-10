"""
RetailPulse 360 — Python Analytics & ML Pipeline
Covers: EDA, RFM Segmentation, Sales Forecasting, Churn Prediction, Anomaly Detection
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
from sklearn.cluster import KMeans
import warnings
warnings.filterwarnings('ignore')

DATA  = "/home/claude/retailpulse360/data"
FIGS  = "/home/claude/retailpulse360/outputs/figures"
import os
os.makedirs(FIGS, exist_ok=True)

# Colour palette
PALETTE = {"primary":"#00e5a0","secondary":"#5b8fff","danger":"#ff6b6b",
           "warning":"#ffd166","purple":"#c77dff","bg":"#0a0a0f","surface":"#111118"}

plt.rcParams.update({
    "figure.facecolor": PALETTE["surface"],
    "axes.facecolor":   PALETTE["surface"],
    "axes.edgecolor":   "#333",
    "text.color":       "#e8e8f0",
    "axes.labelcolor":  "#e8e8f0",
    "xtick.color":      "#888",
    "ytick.color":      "#888",
    "grid.color":       "#222",
    "font.family":      "DejaVu Sans",
})

print("="*55)
print("  RetailPulse 360 — Python Analytics Pipeline")
print("="*55)

# ─── LOAD DATA ──────────────────────────────────────────────
print("\n[1/7] Loading datasets...")
trans    = pd.read_csv(f"{DATA}/transactions.csv", parse_dates=["date"])
stores   = pd.read_csv(f"{DATA}/stores.csv")
products = pd.read_csv(f"{DATA}/products.csv")
customers= pd.read_csv(f"{DATA}/customers.csv", parse_dates=["registration_date"])
reviews  = pd.read_csv(f"{DATA}/reviews.csv")
inventory= pd.read_csv(f"{DATA}/inventory.csv")
print(f"   Transactions: {len(trans):,}  |  Customers: {len(customers):,}  |  Products: {len(products)}")

# ─── EDA: REVENUE TREND ─────────────────────────────────────
print("\n[2/7] EDA — Revenue trend analysis...")
monthly = trans.groupby(trans['date'].dt.to_period('M')).agg(
    revenue=('total_revenue','sum'),
    profit=('gross_profit','sum'),
    txns=('transaction_id','count')
).reset_index()
monthly['date_dt'] = monthly['date'].dt.to_timestamp()
monthly['margin'] = monthly['profit'] / monthly['revenue'] * 100

fig, axes = plt.subplots(2, 2, figsize=(16, 10))
fig.suptitle("NovaMart — Executive Revenue Overview (2022–2024)",
             fontsize=15, fontweight='bold', color=PALETTE["primary"], y=1.01)

# Revenue trend
ax = axes[0,0]
ax.fill_between(monthly['date_dt'], monthly['revenue']/1e6, alpha=0.2, color=PALETTE["primary"])
ax.plot(monthly['date_dt'], monthly['revenue']/1e6, color=PALETTE["primary"], linewidth=2)
ax.set_title("Monthly Revenue ($M)", color="#e8e8f0", fontweight='bold')
ax.set_ylabel("Revenue ($M)", color="#888")
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x,_: f'${x:.1f}M'))
ax.grid(True, alpha=0.2)

# GP Margin
ax = axes[0,1]
ax.fill_between(monthly['date_dt'], monthly['margin'], alpha=0.15, color=PALETTE["secondary"])
ax.plot(monthly['date_dt'], monthly['margin'], color=PALETTE["secondary"], linewidth=2)
ax.axhline(monthly['margin'].mean(), color=PALETTE["warning"], linestyle='--', linewidth=1.2, alpha=0.7)
ax.set_title("Gross Profit Margin %", color="#e8e8f0", fontweight='bold')
ax.set_ylabel("Margin %", color="#888")
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x,_: f'{x:.0f}%'))
ax.grid(True, alpha=0.2)

# Revenue by region
region_rev = trans.merge(stores[['store_id','region']], on='store_id')
rr = region_rev.groupby('region')['total_revenue'].sum().sort_values(ascending=True)
colors_reg = [PALETTE["primary"],PALETTE["secondary"],PALETTE["warning"],PALETTE["purple"],PALETTE["danger"]]
ax = axes[1,0]
bars = ax.barh(rr.index, rr.values/1e6, color=colors_reg, height=0.6)
ax.set_title("Revenue by Region ($M)", color="#e8e8f0", fontweight='bold')
ax.set_xlabel("Revenue ($M)", color="#888")
for bar, val in zip(bars, rr.values):
    ax.text(bar.get_width()+0.2, bar.get_y()+bar.get_height()/2,
            f'${val/1e6:.1f}M', va='center', color="#e8e8f0", fontsize=9)
ax.grid(True, alpha=0.2, axis='x')

# Revenue by Category
cat_rev = trans.merge(products[['product_id','category']], on='product_id')
cr = cat_rev.groupby('category')['total_revenue'].sum().sort_values(ascending=False)
ax = axes[1,1]
wedges, texts, autotexts = ax.pie(cr.values, labels=None, autopct='%1.1f%%',
    colors=colors_reg, startangle=140, pctdistance=0.75,
    wedgeprops={'edgecolor':'#111', 'linewidth':1.5})
for t in autotexts: t.set_color('white'); t.set_fontsize(8)
ax.legend(cr.index, loc='lower right', fontsize=8, framealpha=0.3,
          labelcolor="#e8e8f0", facecolor="#1a1a1a")
ax.set_title("Revenue by Category", color="#e8e8f0", fontweight='bold')

plt.tight_layout()
plt.savefig(f"{FIGS}/01_revenue_overview.png", dpi=150, bbox_inches='tight',
            facecolor=PALETTE["surface"])
plt.close()
print("   ✓ Revenue overview chart saved")

# ─── EDA: STORE PERFORMANCE ─────────────────────────────────
print("\n[3/7] EDA — Store & product deep-dive...")
store_perf = trans.merge(stores, on='store_id').groupby('store_name').agg(
    revenue=('total_revenue','sum'),
    profit=('gross_profit','sum'),
    transactions=('transaction_id','count'),
).reset_index()
store_perf['margin'] = store_perf['profit'] / store_perf['revenue'] * 100
store_perf = store_perf.sort_values('revenue', ascending=False)

fig, axes = plt.subplots(1, 2, figsize=(16, 7))
fig.suptitle("Store & Product Performance Analysis", fontsize=14, fontweight='bold',
             color=PALETTE["primary"])

ax = axes[0]
top10 = store_perf.head(10)
bar_colors = [PALETTE["primary"] if m >= store_perf['margin'].mean() else PALETTE["danger"]
              for m in top10['margin']]
bars = ax.barh(top10['store_name'], top10['revenue']/1e6, color=bar_colors, height=0.65)
ax.set_title("Top 10 Stores by Revenue", color="#e8e8f0", fontweight='bold')
ax.set_xlabel("Revenue ($M)", color="#888")
ax.invert_yaxis()
ax.grid(True, alpha=0.2, axis='x')
for bar in bars:
    ax.text(bar.get_width()+0.02, bar.get_y()+bar.get_height()/2,
            f'${bar.get_width():.1f}M', va='center', fontsize=8, color="#e8e8f0")

# Top products scatter: revenue vs margin
ax = axes[1]
prod_perf = trans.merge(products[['product_id','product_name','category','margin_pct']], on='product_id')
pp = prod_perf.groupby(['product_name','category']).agg(
    revenue=('total_revenue','sum'), qty=('quantity','sum')).reset_index()
pp = pp.sort_values('revenue', ascending=False).head(60)
cat_list = pp['category'].unique()
cat_colors = dict(zip(cat_list, [PALETTE["primary"],PALETTE["secondary"],
                                  PALETTE["warning"],PALETTE["purple"],PALETTE["danger"]]))
for cat in cat_list:
    sub = pp[pp['category']==cat]
    ax.scatter(sub['qty'], sub['revenue']/1000, s=60, label=cat,
               color=cat_colors[cat], alpha=0.75)
ax.set_title("Product Revenue vs Units Sold (Top 60)", color="#e8e8f0", fontweight='bold')
ax.set_xlabel("Units Sold", color="#888")
ax.set_ylabel("Revenue ($K)", color="#888")
ax.legend(fontsize=8, framealpha=0.3, labelcolor="#e8e8f0", facecolor="#1a1a1a")
ax.grid(True, alpha=0.2)

plt.tight_layout()
plt.savefig(f"{FIGS}/02_store_product_analysis.png", dpi=150, bbox_inches='tight',
            facecolor=PALETTE["surface"])
plt.close()
print("   ✓ Store & product analysis saved")

# ─── RFM SEGMENTATION ───────────────────────────────────────
print("\n[4/7] RFM Customer Segmentation...")
snapshot = trans['date'].max()
rfm = trans.groupby('customer_id').agg(
    recency  = ('date',          lambda x: (snapshot - x.max()).days),
    frequency= ('transaction_id','count'),
    monetary = ('total_revenue', 'sum')
).reset_index()

r_labels = [5,4,3,2,1]
f_labels = m_labels = [1,2,3,4,5]
rfm['R'] = pd.qcut(rfm['recency'],  5, labels=r_labels, duplicates='drop')
rfm['F'] = pd.qcut(rfm['frequency'].rank(method='first'), 5, labels=f_labels, duplicates='drop')
rfm['M'] = pd.qcut(rfm['monetary'], 5, labels=m_labels, duplicates='drop')
rfm['RFM'] = rfm['R'].astype(int) + rfm['F'].astype(int) + rfm['M'].astype(int)

def rfm_segment(score):
    if score >= 13:  return 'Champions'
    elif score >= 10: return 'Loyal Customers'
    elif score >= 7:  return 'Potential Loyalists'
    elif score >= 5:  return 'At Risk'
    else:             return 'Hibernating'

rfm['segment'] = rfm['RFM'].apply(rfm_segment)
seg_counts = rfm['segment'].value_counts()

fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle("RFM Customer Segmentation", fontsize=14, fontweight='bold',
             color=PALETTE["primary"])

seg_colors = {'Champions':PALETTE["primary"],'Loyal Customers':PALETTE["secondary"],
              'Potential Loyalists':PALETTE["warning"],'At Risk':PALETTE["danger"],'Hibernating':PALETTE["purple"]}

ax = axes[0]
bars = ax.bar(seg_counts.index, seg_counts.values,
              color=[seg_colors.get(s, '#888') for s in seg_counts.index], width=0.6)
ax.set_title("Customer Count by Segment", color="#e8e8f0", fontweight='bold')
ax.set_ylabel("Customers", color="#888")
ax.tick_params(axis='x', rotation=25)
ax.grid(True, alpha=0.2, axis='y')
for bar, val in zip(bars, seg_counts.values):
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+20,
            f'{val:,}', ha='center', fontsize=9, color="#e8e8f0")

ax = axes[1]
seg_value = rfm.groupby('segment')['monetary'].mean().sort_values(ascending=True)
bars = ax.barh(seg_value.index, seg_value.values,
               color=[seg_colors.get(s,'#888') for s in seg_value.index], height=0.5)
ax.set_title("Avg Monetary Value by Segment ($)", color="#e8e8f0", fontweight='bold')
ax.set_xlabel("Avg Revenue ($)", color="#888")
ax.grid(True, alpha=0.2, axis='x')
for bar, val in zip(bars, seg_value.values):
    ax.text(bar.get_width()+1, bar.get_y()+bar.get_height()/2,
            f'${val:,.0f}', va='center', fontsize=9, color="#e8e8f0")

plt.tight_layout()
plt.savefig(f"{FIGS}/03_rfm_segmentation.png", dpi=150, bbox_inches='tight',
            facecolor=PALETTE["surface"])
plt.close()
rfm.to_csv("/home/claude/retailpulse360/data/rfm_scores.csv", index=False)
print(f"   ✓ RFM segmentation complete: {seg_counts.to_dict()}")

# ─── CHURN PREDICTION ───────────────────────────────────────
print("\n[5/7] ML — Churn Prediction Model...")
churn_df = rfm.copy()
churn_df['churned'] = (churn_df['recency'] > 90).astype(int)

cust_feats = customers[['customer_id','age','loyalty_tier','email_opt_in']].copy()
cust_feats['age'] = cust_feats['age'].fillna(35)
cust_feats['tier_score'] = cust_feats['loyalty_tier'].map({'Gold':4,'Silver':3,'Bronze':2,'New':1}).fillna(1)
cust_feats['email_opt'] = cust_feats['email_opt_in'].astype(int)

ml_df = churn_df.merge(cust_feats, on='customer_id')
features = ['recency','frequency','monetary','R','F','M','RFM','age','tier_score','email_opt']
ml_df[features] = ml_df[features].apply(pd.to_numeric, errors='coerce').fillna(0)

X = ml_df[features]
y = ml_df['churned']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train)
X_test_s  = scaler.transform(X_test)

rf = RandomForestClassifier(n_estimators=100, max_depth=8, random_state=42, class_weight='balanced')
rf.fit(X_train_s, y_train)
y_pred = rf.predict(X_test_s)
y_proba = rf.predict_proba(X_test_s)[:,1]
auc = roc_auc_score(y_test, y_proba)
print(f"   ✓ Random Forest AUC: {auc:.4f}")

# Churn scores for all customers
ml_df['churn_probability'] = rf.predict_proba(scaler.transform(X))[:,1]
ml_df['churn_risk_label']  = pd.cut(ml_df['churn_probability'],
    bins=[0,0.3,0.6,1.0], labels=['Low Risk','Medium Risk','High Risk'])
ml_df[['customer_id','churn_probability','churn_risk_label','segment']].to_csv(
    "/home/claude/retailpulse360/data/churn_scores.csv", index=False)

# Feature importance plot
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle("Churn Prediction Model Results", fontsize=14, fontweight='bold',
             color=PALETTE["primary"])

ax = axes[0]
importances = pd.Series(rf.feature_importances_, index=features).sort_values(ascending=True)
bars = ax.barh(importances.index, importances.values, color=PALETTE["secondary"], height=0.6)
ax.set_title("Feature Importance", color="#e8e8f0", fontweight='bold')
ax.set_xlabel("Importance Score", color="#888")
ax.grid(True, alpha=0.2, axis='x')

ax = axes[1]
risk_dist = ml_df['churn_risk_label'].value_counts()
risk_colors = [PALETTE["primary"], PALETTE["warning"], PALETTE["danger"]]
wedges, texts, auts = ax.pie(risk_dist.values, autopct='%1.1f%%', colors=risk_colors,
    startangle=140, pctdistance=0.78, wedgeprops={'edgecolor':'#111','linewidth':1.5})
for t in auts: t.set_color('white'); t.set_fontsize(9)
ax.legend(risk_dist.index, loc='lower right', fontsize=9, framealpha=0.3,
          labelcolor="#e8e8f0", facecolor="#1a1a1a")
ax.set_title(f"Churn Risk Distribution\n(AUC = {auc:.3f})", color="#e8e8f0", fontweight='bold')

plt.tight_layout()
plt.savefig(f"{FIGS}/04_churn_model.png", dpi=150, bbox_inches='tight',
            facecolor=PALETTE["surface"])
plt.close()
print(f"   ✓ Churn scores saved")

# ─── SALES FORECASTING ──────────────────────────────────────
print("\n[6/7] ML — Sales Forecasting (Linear Trend Model)...")
daily = trans.groupby('date')['total_revenue'].sum().reset_index()
daily = daily.sort_values('date').reset_index(drop=True)
daily['t'] = np.arange(len(daily))
daily['month'] = daily['date'].dt.month
daily['dow']   = daily['date'].dt.dayofweek

# Seasonal encoding
from sklearn.linear_model import Ridge
month_dummies = pd.get_dummies(daily['month'], prefix='m', drop_first=True)
X_ts = pd.concat([daily[['t']], month_dummies], axis=1).astype(float)
y_ts = daily['total_revenue']

model_ts = Ridge(alpha=1.0)
model_ts.fit(X_ts, y_ts)
daily['fitted'] = model_ts.predict(X_ts)

# Forecast next 90 days
future_t = np.arange(len(daily), len(daily)+90)
future_dates = pd.date_range(daily['date'].max() + pd.Timedelta(days=1), periods=90)
future_months = future_dates.month
month_dum_f = pd.get_dummies(pd.Series(future_months), prefix='m', drop_first=True)
# Align columns
for col in month_dummies.columns:
    if col not in month_dum_f.columns:
        month_dum_f[col] = 0
month_dum_f = month_dum_f[month_dummies.columns]
X_fut = pd.concat([pd.DataFrame({'t': future_t}), month_dum_f.reset_index(drop=True)], axis=1).astype(float)
forecast = model_ts.predict(X_fut)

fig, ax = plt.subplots(figsize=(16, 6))
ax.fill_between(daily['date'], daily['total_revenue']/1000, alpha=0.15, color=PALETTE["primary"])
ax.plot(daily['date'], daily['total_revenue']/1000, color="#444", linewidth=0.8, alpha=0.7, label='Actual')
ax.plot(daily['date'], daily['fitted']/1000, color=PALETTE["primary"], linewidth=1.5, label='Trend Fit')
ax.plot(future_dates, forecast/1000, color=PALETTE["warning"], linewidth=2,
        linestyle='--', label='90-Day Forecast')
ax.fill_between(future_dates, (forecast*0.85)/1000, (forecast*1.15)/1000,
                alpha=0.15, color=PALETTE["warning"])
ax.axvline(daily['date'].max(), color=PALETTE["danger"], linestyle=':', linewidth=1.5, alpha=0.7)
ax.text(daily['date'].max(), ax.get_ylim()[1]*0.95, '  Forecast Start',
        color=PALETTE["danger"], fontsize=9)
ax.set_title("Daily Revenue — Actuals + 90-Day Forecast", color="#e8e8f0", fontweight='bold', fontsize=13)
ax.set_ylabel("Revenue ($K)", color="#888")
ax.set_xlabel("Date", color="#888")
ax.legend(facecolor="#1a1a1a", labelcolor="#e8e8f0", framealpha=0.5)
ax.grid(True, alpha=0.15)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x,_: f'${x:.0f}K'))
plt.tight_layout()
plt.savefig(f"{FIGS}/05_sales_forecast.png", dpi=150, bbox_inches='tight',
            facecolor=PALETTE["surface"])
plt.close()
print(f"   ✓ Forecast: avg next-90 daily revenue ${np.mean(forecast):,.0f}")

# ─── ANOMALY DETECTION ──────────────────────────────────────
print("\n[7/7] ML — Anomaly Detection...")
daily_feats = daily[['total_revenue','t']].copy()
daily_feats['rolling7'] = daily['total_revenue'].rolling(7, min_periods=1).mean()
daily_feats['pct_vs_roll'] = (daily['total_revenue'] - daily_feats['rolling7']) / daily_feats['rolling7']
daily_feats = daily_feats.fillna(0)

iso = IsolationForest(contamination=0.05, random_state=42)
daily['anomaly'] = iso.fit_predict(daily_feats[['total_revenue','pct_vs_roll']])
anomalies = daily[daily['anomaly']==-1]

fig, ax = plt.subplots(figsize=(16, 6))
ax.plot(daily['date'], daily['total_revenue']/1000, color=PALETTE["primary"],
        linewidth=0.9, alpha=0.8, label='Daily Revenue')
ax.scatter(anomalies['date'], anomalies['total_revenue']/1000, color=PALETTE["danger"],
           zorder=5, s=40, label=f'Anomalies ({len(anomalies)} detected)', alpha=0.9)
ax.set_title("Revenue Anomaly Detection (Isolation Forest)", color="#e8e8f0",
             fontweight='bold', fontsize=13)
ax.set_ylabel("Revenue ($K)", color="#888")
ax.set_xlabel("Date", color="#888")
ax.legend(facecolor="#1a1a1a", labelcolor="#e8e8f0", framealpha=0.5)
ax.grid(True, alpha=0.15)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x,_: f'${x:.0f}K'))
plt.tight_layout()
plt.savefig(f"{FIGS}/06_anomaly_detection.png", dpi=150, bbox_inches='tight',
            facecolor=PALETTE["surface"])
plt.close()
print(f"   ✓ Anomaly detection: {len(anomalies)} anomalies flagged")

# ─── SENTIMENT ANALYSIS ──────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle("Customer Sentiment Analysis by Store Region",
             fontsize=14, fontweight='bold', color=PALETTE["primary"])

rev_store = reviews.merge(stores[['store_id','region']], on='store_id')
sent_pivot = rev_store.groupby(['region','sentiment']).size().unstack(fill_value=0)
sent_pivot_pct = sent_pivot.div(sent_pivot.sum(axis=1), axis=0) * 100

ax = axes[0]
x = np.arange(len(sent_pivot_pct))
w = 0.25
colors_sent = [PALETTE["primary"], PALETTE["warning"], PALETTE["danger"]]
for i, (col, col_c) in enumerate(zip(sent_pivot_pct.columns, colors_sent)):
    ax.bar(x + i*w, sent_pivot_pct[col], w, label=col, color=col_c, alpha=0.85)
ax.set_xticks(x + w)
ax.set_xticklabels(sent_pivot_pct.index, rotation=20)
ax.set_title("Sentiment Distribution by Region (%)", color="#e8e8f0", fontweight='bold')
ax.set_ylabel("% of Reviews", color="#888")
ax.legend(facecolor="#1a1a1a", labelcolor="#e8e8f0", framealpha=0.5)
ax.grid(True, alpha=0.2, axis='y')

ax = axes[1]
avg_rating = rev_store.groupby('region')['rating'].mean().sort_values(ascending=True)
bars = ax.barh(avg_rating.index, avg_rating.values,
               color=[PALETTE["secondary"]]*len(avg_rating), height=0.5)
ax.set_xlim(0, 5)
ax.set_title("Average Rating by Region", color="#e8e8f0", fontweight='bold')
ax.set_xlabel("Avg Rating (out of 5)", color="#888")
ax.axvline(avg_rating.mean(), color=PALETTE["warning"], linestyle='--', alpha=0.7)
ax.grid(True, alpha=0.2, axis='x')
for bar, val in zip(bars, avg_rating.values):
    ax.text(bar.get_width()+0.02, bar.get_y()+bar.get_height()/2,
            f'{val:.2f} ★', va='center', fontsize=9, color="#e8e8f0")

plt.tight_layout()
plt.savefig(f"{FIGS}/07_sentiment_analysis.png", dpi=150, bbox_inches='tight',
            facecolor=PALETTE["surface"])
plt.close()

# ─── SUMMARY ────────────────────────────────────────────────
print("\n" + "="*55)
print("  ✅ Pipeline Complete!")
print("="*55)
print(f"  Total Revenue (3yr):  ${trans['total_revenue'].sum()/1e6:.1f}M")
print(f"  Total Gross Profit:   ${trans['gross_profit'].sum()/1e6:.1f}M")
print(f"  Avg GP Margin:        {trans['gross_profit'].sum()/trans['total_revenue'].sum()*100:.1f}%")
print(f"  Customer Segments:    {rfm['segment'].value_counts().to_dict()}")
print(f"  High-Risk Churners:   {(ml_df['churn_risk_label']=='High Risk').sum():,}")
print(f"  Anomalies Detected:   {len(anomalies)}")
print(f"  Charts saved to:      {FIGS}/")
