from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from tools.trends.trends_service import extract_trending_products, generate_trend_analysis_report

class TrendsAgent:
    def __init__(self):
        """Initializes the agent for processing Google Trends CSV data and generating insights."""
        self.llm_trends = ChatOpenAI(model="gpt-4o", temperature=0)

        # Create Agents
        self.trend_extraction_agent = create_react_agent(
            model=self.llm_trends,
            tools=[extract_trending_products]
        )

        self.trend_analysis_agent = create_react_agent(
            model=self.llm_trends,
            tools=[generate_trend_analysis_report]
        )

    def analyze_trends_from_csv(self, csv_path: str):
        """Processes the uploaded CSV and provides insights on trending products."""

        # Step 1: Extract Trending Products
        extracted_products = self.trend_extraction_agent.invoke(
            {"messages": [
                {"role": "system", "content": "Extract trending products from a Google Trends CSV file."},
                {"role": "user", "content": f"Extract products from {csv_path}"}
            ]}
        )

        trending_products = extracted_products["messages"][-1].content

        # Step 2: Generate a Trend Analysis Report
        trend_report = self.trend_analysis_agent.invoke(
            {"messages": [
                {"role": "system", "content": "You are the retail and trend expert. The user relies on your analysis and expects a detailed Report. Generate a report on trending products and stock recommendations. Be precise and give as many information as possible. Give also smart strategic decision suggestions."},
                {"role": "user", "content": f"Trending products: {', '.join(trending_products)}"}
            ]}
        )

        return {
            "trending_products": trending_products,
            "trend_report": trend_report["messages"][-1].content
        }
