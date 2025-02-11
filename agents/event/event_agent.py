from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from tools.event.event_service import get_current_month, check_special_occasions, get_preparation_tips

class EventAgent:
    def __init__(self):
        """Initializes all agents to automatically fetch event stock insights."""
        self.llm_date = ChatOpenAI(model="gpt-4o", temperature=0)
        self.llm_occasion = ChatOpenAI(model="gpt-4o", temperature=0)
        self.llm_preparation = ChatOpenAI(model="gpt-4o", temperature=0)

        # Create Agents
        self.date_agent = create_react_agent(model=self.llm_date, tools=[get_current_month])
        self.occasion_agent = create_react_agent(model=self.llm_occasion, tools=[check_special_occasions])
        self.preparation_agent = create_react_agent(model=self.llm_preparation, tools=[get_preparation_tips])

    def run_ambient_check(self):
        """Automatically runs all agents and returns event stock insights."""

        # Step 1: Get the current month
        month_result = self.date_agent.invoke(
            {"messages": [
                {"role": "system", "content": "You are the DateAgent. Call get_current_month() and return the output."},
                {"role": "user", "content": "Check the current month and give only two digits number of month."}
            ]},
            config={"configurable": {"recursion_limit": 50}}
        )
        current_month = month_result["messages"][-1].content #TODO Change for Demo
        #current_month = "05"

        # Step 2: Check for special occasions
        occasion_result = self.occasion_agent.invoke(
            {"messages": [
                {"role": "system",
                 "content": "You are the OccasionAgent. Call check_special_occasions(month) and return the output."},
                {"role": "user", "content": f"Check for special occasions in month {current_month}"}
            ]},
            config={"configurable": {"recursion_limit": 50}}
        )
        occasions = occasion_result["messages"][-1].content

        # Step 3: Get preparation tips
        preparation_result = self.preparation_agent.invoke(
            {"messages": [
                {"role": "system",
                 "content": "You are the PreparationAgent. Call get_preparation_tips(month) and suggest what the product seller like Amazon has to do to prepare in full detail containing the month and what upcoming events are coming for better sales."},
                {"role": "user", "content": f"Give preparation tips for month {current_month} containing occasions {occasions}."},
            ]},
            config={"configurable": {"recursion_limit": 50}}
        )
        preparations = preparation_result["messages"][-1].content

        # Combine results
        return {
            "preparation_tips": preparations
        }
