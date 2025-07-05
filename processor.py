def analyze_trends(df):
    top_countries = df['origin_country'].value_counts().head(5)
    on_ground_ratio = df['on_ground'].value_counts(normalize=True)
    return {
        "top_countries": top_countries.to_dict(),
        "on_ground_ratio": on_ground_ratio.to_dict()
    }