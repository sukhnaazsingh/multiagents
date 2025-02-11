from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from tools.route.route_service import get_weather, get_events_near_route, generate_recommendation

class RouteAgent:
    def __init__(self):
        """Initializes agents to fetch weather, events, and provide recommendations."""
        self.llm_weather = ChatOpenAI(model="gpt-4o", temperature=0)
        self.llm_events = ChatOpenAI(model="gpt-4o", temperature=0)
        self.llm_recommendation = ChatOpenAI(model="gpt-4o", temperature=0)

        # Create Agents
        self.weather_agent = create_react_agent(
            model=self.llm_weather,
            tools=[get_weather]
        )

        self.events_agent = create_react_agent(
            model=self.llm_events,
            tools=[get_events_near_route]
        )

        self.recommendation_agent = create_react_agent(
            model=self.llm_recommendation,
            tools=[generate_recommendation]
        )

    def get_route_analysis(self, start: str, end: str):
        """Fetches weather, events, and gives a travel recommendation."""

        # Step 1: Get Weather Conditions
        weather_start = self.weather_agent.invoke(
            {"messages": [
                {"role": "system", "content": "Fetch weather data for the location."},
                {"role": "user", "content": f"Get weather for {start}"}
            ]},
            config={"configurable": {"recursion_limit": 50}}
        )

        weather_end = self.weather_agent.invoke(
            {"messages": [
                {"role": "system", "content": "Fetch weather data for the location."},
                {"role": "user", "content": f"Get weather for {end}"}
            ]},
            config={"configurable": {"recursion_limit": 50}}
        )

        # Step 2: Check Events on Route
        events = self.events_agent.invoke(
            {"messages": [
                {"role": "system", "content": "Fetch events near the route."},
                {"role": "user", "content": f"Get events between {start} and {end}"}
            ]},
            config={"configurable": {"recursion_limit": 50}}
        )

        # Step 3: Generate Route Recommendation
        prompt = f"""
        Given the following conditions:
        - Weather at {start}: {weather_start["messages"][-1].content}
        - Weather at {end}: {weather_end["messages"][-1].content}
        - Events near the route: {events["messages"][-1].content}

        Provide a travel recommendation, including:
        1. Check the path the driver would be suggested by a Maps Software.
        2. If on the way there might be interruptions, then suggest an alternate route with exact details, like which highway, route etc.
        3. Whether the route is good or if delays are expected.
        4. If congestion is likely, suggest alternatives.
        5. If weather is bad, recommend extra precautions.
        """

        recommendation = self.recommendation_agent.invoke(
            {"messages": [
                {"role": "system", "content": "Analyze the data and generate a travel recommendation."},
                {"role": "user", "content": prompt}
            ]},
            config={"configurable": {"recursion_limit": 50}}
        )

        # Step 4: Return Results
        return {
            "start_location": start,
            "end_location": end,
            "weather_start": weather_start["messages"][-1].content,
            "weather_end": weather_end["messages"][-1].content,
            "events": events["messages"][-1].content,
            "recommendation": recommendation["messages"][-1].content
        }
