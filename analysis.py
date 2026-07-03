def clean_price_column(df):
    df["price"] = df["price"].str.replace("Â£", "", regex=False)
    df["price"] = df["price"].str.replace("£", "", regex=False)
    df["price"] = df["price"].astype(float)
    return df


def get_most_expensive_book(df):
    index = df["price"].idxmax()
    return df.loc[index]


def get_cheapest_book(df):
    index = df["price"].idxmin()
    return df.loc[index]


def get_average_price(df):
    return df["price"].mean()