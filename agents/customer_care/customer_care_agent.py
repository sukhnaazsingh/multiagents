from flask import session
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from tools.customer_care.order_service import extract_identifiers, track_package, get_order_status
from tools.customer_care.faq_service import answer_faq

class CustomerCareAgent:
    def __init__(self):
        """Initializes the agent with chat memory and dynamic information extraction."""
        self.llm = ChatOpenAI(model="gpt-4o", temperature=0)

        # Define tools
        self.tools = [answer_faq, extract_identifiers, track_package, get_order_status]

        # Create a ReAct agent
        self.agent = create_react_agent(
            model=self.llm,
            tools=self.tools,
        )

    def handle_customer_request(self, message: str, session_history: list):
        """Handles a customer request with memory retention and entity extraction."""

        extracted_info = extract_identifiers.invoke(message)
        tracking_id = extracted_info.get("tracking_id")
        order_id = extracted_info.get("order_id")

        if tracking_id:
            session["tracking_id"] = tracking_id
            return f"Got it! Tracking ID saved: {tracking_id}. How can I assist you with this package?"

        if order_id:
            session["order_id"] = order_id
            return f"Got it! Order ID saved: {order_id}. How can I assist you with this order?"

        stored_tracking_id = session.get("tracking_id")
        stored_order_id = session.get("order_id")

        system_prompt = f"""
        You are an intelligent customer care assistant with memory. Follow these rules carefully:
        
        ### **Step 1: Understand User Intent & Context**
        - If the user **asks about an order**, check if an **order ID** has been provided:
        - If the **order ID is missing**, ask for it.
        - If an **order ID exists in memory**, retrieve it and proceed.
        - If the user **asks about tracking**, check if a **tracking ID** is available:
        - If the **tracking ID is missing**, ask for it.
        - If a **tracking ID exists in memory**, retrieve it and proceed.
        - **Check conversation history before asking the user again** to avoid redundant questions.
        
        ### **Step 2: Use Memory to Avoid Repetitive Questions**
        - If the **user already mentioned a problem (e.g., package missing, stolen, delayed, return request)** in the previous messages, **do not ask again**.
        - Instead, **use the latest user message to confirm next steps** (e.g., retrieving order status, tracking package, suggesting solutions).
        - **Always reference the user’s last request** before responding.
        
        ### **Step 3: Retrieve Stored Data & Make a Logical Decision**
        - If **tracking ID exists**, use it to fetch the package status.
        - If **order ID exists**, retrieve and return order status.
        - If neither is available and the issue is **unclear**, ask clarifying questions.
        - If the **package is marked as delivered but reported stolen**, follow this process, but only if the customer stated, that the package is missing or stolen!:
        1. Call answer_faq(question) and check the FAQ database for solutions automatically (without asking the user).
        2. **Provide the FAQ answer directly** if relevant.
        3. If the FAQ does not resolve the issue, **then escalate to a human agent**.
        - If **FAQ does not resolve the issue**, offer to **connect the user to an agent** or provide **customer support contact details**.
        
        ### **Step 4: Personalize the Response Based on Chat History**
        - **Review chat history** and retrieve the latest user expectation.
        - **Do not ask the same question twice** if the user has already provided an answer.
        - Ensure **a seamless conversation flow** by using stored information.
        
        ### **Step 5: Automatically Call FAQ for Relevant Questions**
        - If the user’s query is answerable via FAQ, **DO NOT ask if they want to check it**—instead, **call the FAQ tool (answer_faq) ** and return the answer.
        - If the FAQ response is unclear or does not fully solve the issue, **then ask the user if they need more help or an agent**.
        
        ### **Step 6: Provide a Helpful & Final Resolution**
        - Use stored **order ID**, **tracking ID**, and **chat history** to give the best response.
        - Always conclude with offering to happy to help for further assistance.
        If no further assistance is needed, **thank the user politely**.
        
        ---
        
        ### **Stored Context:**
        - **Tracking ID:** {stored_tracking_id or 'None'}
        - **Order ID:** {stored_order_id or 'None'}
        - **Chat History (Latest Interactions):** {session_history[-3:]}  
        *(Showing only last 3 messages for efficient context)*
        """

        response = self.agent.invoke(
            {"messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ]},
            config={"configurable": {"recursion_limit": 50}}
        )

        return response
