def getGrapeDistribution(df):
    data = df.groupby('grape').count().reset_index().iloc[:, 0:2].sort_values(by='product', ascending=False).iloc[:8, :]
    data.columns = ['Grape', 'Used in how many wines?']
    return data