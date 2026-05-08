import pandas as pd
from thefuzz import process
import json
import os
import re

# --- CONFIGURATION ---
QS_FILE = 'QS.xlsx'
ARWU_FILE = 'ARWU.xlsx'
CWUR_FILE = 'CWUR.xlsx'
MAPPING_FILE = 'Mapping.xlsx' 
OUTPUT_FOLDER = 'Subject_JSONs'

if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

# Load Excel Objects
print("📂 Loading Files...")
qs_excel = pd.ExcelFile(QS_FILE)
arwu_excel = pd.ExcelFile(ARWU_FILE)
mapping_df = pd.read_excel(MAPPING_FILE)
cwur_raw = pd.read_excel(CWUR_FILE, header=None)

def deep_clean_name(name):
    name = str(name).strip()
    prefixes = ['United Kingdom ', 'USA ', 'Canada ', 'Switzerland ', 'Singapore ', 
                'Australia ', 'Germany ', 'Japan ', 'China ', 'France ', 'Italy ', 
                'Netherlands ', 'South Korea ', 'Republic of Korea ', 'India ']
    for p in prefixes:
        if name.startswith(p):
            name = name.replace(p, "", 1)
    return name.strip()

def safe_int(value):
    try: return int(float(value))
    except: return None

def get_cwur_subject_block(subject_name):
    try:
        mask = cwur_raw[0].astype(str).str.contains(re.escape(str(subject_name)), case=False, na=False)
        row_idx = cwur_raw[mask].index
        if not row_idx.empty:
            start_row = row_idx[0] + 3 
            block = cwur_raw.iloc[start_row : start_row + 10, [0, 1, 2]].copy()
            block.columns = ['RANK', 'NAME', 'LOCATION']
            block['NAME'] = block['NAME'].apply(deep_clean_name)
            return block
    except: return pd.DataFrame()
    return pd.DataFrame()

# --- START THE ENGINE ---
for index, row in mapping_df.iterrows():
    cwur_target = row['CWUR_Subject']
    qs_target = row['QS_Subject']
    arwu_target = row['ARWU_Subject']
    
    print(f"🔄 Processing: {cwur_target}...")

    df_qs = pd.read_excel(qs_excel, sheet_name=qs_target) if qs_target in qs_excel.sheet_names else pd.DataFrame()
    df_arwu = pd.read_excel(arwu_excel, sheet_name=arwu_target) if arwu_target in arwu_excel.sheet_names else pd.DataFrame()
    df_cwur = get_cwur_subject_block(cwur_target) 

    if not df_qs.empty: df_qs['NAME'] = df_qs['NAME'].apply(deep_clean_name)
    if not df_arwu.empty: df_arwu['NAME'] = df_arwu['NAME'].apply(deep_clean_name)

    all_names = []
    if not df_qs.empty: all_names.extend(df_qs['NAME'].tolist())
    if not df_arwu.empty: all_names.extend(df_arwu['NAME'].tolist())
    if not df_cwur.empty: all_names.extend(df_cwur['NAME'].tolist())
    
    unique_names = list(dict.fromkeys([n for n in all_names if str(n) != 'nan']))
    temp_results = []

    for name in unique_names:
        scores_dict = {}
        if not df_qs.empty:
            match = process.extractOne(name, df_qs['NAME'].astype(str).tolist(), score_cutoff=95)
            if match:
                rank = safe_int(df_qs.loc[df_qs['NAME'].astype(str) == match[0], 'RANK'].values[0])
                if rank and rank <= 50: scores_dict['QS'] = 101 - rank
        if not df_arwu.empty:
            match = process.extractOne(name, df_arwu['NAME'].astype(str).tolist(), score_cutoff=95)
            if match:
                rank = safe_int(df_arwu.loc[df_arwu['NAME'].astype(str) == match[0], 'RANK'].values[0])
                if rank and rank <= 50: scores_dict['ARWU'] = 101 - rank
        if not df_cwur.empty:
            match = process.extractOne(name, df_cwur['NAME'].astype(str).tolist(), score_cutoff=95)
            if match:
                rank = safe_int(df_cwur.loc[df_cwur['NAME'].astype(str) == match[0], 'RANK'].values[0])
                if rank and rank <= 10: scores_dict['CWUR'] = 101 - rank

        if scores_dict:
            weighted_pts = (scores_dict.get('QS',0)*0.5 + scores_dict.get('ARWU',0)*0.3 + scores_dict.get('CWUR',0)*0.2)
            total_w = (0.5 if 'QS' in scores_dict else 0) + (0.3 if 'ARWU' in scores_dict else 0) + (0.2 if 'CWUR' in scores_dict else 0)
            avg_score = weighted_pts / total_w
            bonus = (len(scores_dict) - 1) * 2
            final_score = avg_score + bonus
            
            loc = "Check Site"
            if not df_qs.empty:
                m = process.extractOne(name, df_qs['NAME'].tolist(), score_cutoff=95)
                if m: loc = df_qs.loc[df_qs['NAME'] == m[0], 'LOCATION'].values[0]

            temp_results.append({"University": name, "Location": loc, "Total_Score": round(final_score, 2)})

    # --- CONSOLIDATION STEP (KILL THE DUPLICATES) ---
    final_results = []
    if temp_results:
        temp_df = pd.DataFrame(temp_results).sort_values(by='Total_Score', ascending=False)
        seen_names = []
        for _, r in temp_df.iterrows():
            # Check if this university was already added under a similar name
            match = process.extractOne(r['University'], seen_names, score_cutoff=90)
            if not match:
                final_results.append(r.to_dict())
                seen_names.append(r['University'])

    if final_results:
        final_df = pd.DataFrame(final_results)
        final_df['Meta_Rank'] = final_df['Total_Score'].rank(ascending=False, method='min').astype(int)
        filename = re.sub(r'[\\/*?:"<>|]', "", str(cwur_target)).replace(" ", "_")
        final_df.to_json(os.path.join(OUTPUT_FOLDER, f"{filename}.json"), orient='records', indent=4)

print(f"\n🚀 ALL {len(mapping_df)} SUBJECTS PROCESSED AND DUPLICATES MERGED!")