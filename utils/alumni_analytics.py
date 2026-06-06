def placement_rate(df):

    placed = (
        df["placement_status"]
        .astype(str)
        .str.lower()
        .isin(["placed","yes","1","true"])
        .sum()
    )

    return round(
        (placed / len(df)) * 100,
        2
    )
def average_salary(df):
    return round(
        df["salary_package_lpa"].mean(),
        2
    )

def top_branch(df):
    return (
        df["branch"]
        .value_counts()
        .idxmax()
    )

def top_college_tier(df):
    return (
        df["college_tier"]
        .value_counts()
        .idxmax()
    )
