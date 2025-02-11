import pandas as pd
from langchain_core.tools import tool


@tool
def extract_trending_products(csv_path: str) -> list:
    """
    Extracts potential sellable products from a Google Trends CSV file.

    :param csv_path: Path to the uploaded CSV file.
    :return: A list of trending products.
    """
    try:
        df = pd.read_csv(csv_path)

        # Assuming Google Trends CSV has a column that contains search terms
        possible_columns = ["Trends", "Search volume", "Started", "Ended", "Trend breakdown"]
        column_name = next((col for col in possible_columns if col in df.columns), None)

        if not column_name:
            return ["Error: No valid column for trending search terms found."]

        trending_products = df[column_name].dropna().unique().tolist()
        return trending_products

    except Exception as e:
        return [f"Error processing CSV: {str(e)}"]


@tool
def generate_trend_analysis_report(trending_products: list) -> str:
    """
    Generates a trend analysis report based on trending products.

    :param trending_products: List of trending product keywords.
    :return: A detailed analysis report.
    """
    if not trending_products:
        return "No trending products identified."

    report = f"**Trending Product Analysis Report**\n\n"
    report += "**Identified Trending Products:**\n"
    for product in trending_products:
        report += f"- {product}\n"

    report += "\n**Stock Recommendations:**\n"
    report += "1. Ensure availability of trending products in your inventory.\n"
    report += "2. Check supplier availability for new trending items.\n"
    report += "3. Optimize marketing campaigns around these trends.\n"

    report += "\n**Potential Next Steps:**\n"
    report += "✔️ Analyze competitors offering these products.\n"
    report += "✔️ Consider bundles or promotions around high-demand items.\n"
    report += "✔️ Monitor these trends daily to adjust stock levels accordingly.\n"

    return report
