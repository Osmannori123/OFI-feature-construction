# ofi_features.py

import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.linear_model import LassoCV
from sklearn.preprocessing import StandardScaler

df = pd.read_csv("first_25000_rows.csv")
# best-level 
def computeOFI(df):
    def _ofi(row):
        direction = 1 if row['action'] == 'A' else -1 if row['action'] == 'C' else 0
        multiplier = 1 if row['side'] == 'B' else -1
        return direction * multiplier * row['size']

    df = df.copy()
    df['ofi_contrib'] = df.apply(_ofi, axis=1)
    return df


# multi-level (normalized)
def multiLevel(df):
    df = df.copy()
    df['minute'] = pd.to_datetime(df['ts_event']).dt.floor('min')

    df = computeOFI(df)

    ofiByLevel = (df.groupby(['minute', 'depth'])['ofi_contrib'].sum().unstack().reindex(columns=range(10), fill_value=0).rename(columns=lambda x: f'OFI_{x}').reset_index())

    df['size_contrib'] = df['size']
    avgSize= (df.groupby(['minute', 'depth'])['size_contrib'].mean().unstack().reindex(columns=range(10), fill_value=0).rename(columns=lambda x: f'DEPTH_{x}').reset_index())

    merged = pd.merge(ofiByLevel, avgSize, on='minute')
    merged['QM'] = merged[[f'DEPTH_{i}' for i in range(10)]].mean(axis=1)

    for i in range(10):
        merged[f'nOFI_{i}'] = merged[f'OFI_{i}'] / merged['QM']

    return merged[['minute'] + [f'nOFI_{i}' for i in range(10)]]

# integrated 
def integrated(normDF):
    ofiMatrix = normDF.drop(columns=['minute']).fillna(0)
    pca = PCA(n_components=1)
    pca.fit(ofi_matrix)
    w1 = pca.components_[0]
    w1Norm = w1 / np.sum(np.abs(w1))
    integrated = ofi_matrix.dot(w1Norm)

    return pd.DataFrame({'minute': normDF['minute'],'Integrated_OFI': integrated})

# cross-asset (only appl stock information is in the file)
def crossAsset(integratedOFI):
    returns = integratedOFI['Integrated_OFI'].diff().shift(-1).dropna()
    X = integratedOFI.loc[returns.index, ['Integrated_OFI']]
    scaler = StandardScaler()
    xScaled = scaler.fit_transform(X)
    lasso = LassoCV(cv=5)
    lasso.fit(xScaled, returns)

    return pd.DataFrame({'Feature': ['Integrated_OFI'],'Coefficient': lasso.coef_})
  
bestlevelOFI = computeOFI(df)
multilevelOFI = multiLevel(bestlevelOFI)
IntegratedOFI = integrated(multilevelOFI)
CrossAssetOFI = crossAsset(IntegratedOFI)



