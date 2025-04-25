import datetime
from zoneinfo import ZoneInfo
from google.adk.agents import LlmAgent, BaseAgent
from google.adk.tools import google_search  # Import the tool


def get_weather(city: str) -> dict:
    """Retrieves the current weather report for a specified city.

    Args:
        city (str): The name of the city for which to retrieve the weather report.

    Returns:
        dict: status and result or error msg.
    """
    if city.lower() == "new york":
        return {
            "status": "success",
            "report": (
                "The weather in New York is sunny with a temperature of 25 degrees"
                " Celsius (77 degrees Fahrenheit)."
            ),
        }
    else:
        return {
            "status": "error",
            "error_message": f"Weather information for '{city}' is not available.",
        }


def get_current_time(city: str) -> dict:
    """Returns the current time in a specified city.

    Args:
        city (str): The name of the city for which to retrieve the current time.

    Returns:
        dict: status and result or error msg.
    """

    if city.lower() == "new york":
        tz_identifier = "America/New_York"
    else:
        return {
            "status": "error",
            "error_message": (
                f"Sorry, I don't have timezone information for {city}."
            ),
        }

    tz = ZoneInfo(tz_identifier)
    now = datetime.datetime.now(tz)
    report = (
        f'The current time in {city} is {now.strftime("%Y-%m-%d %H:%M:%S %Z%z")}'
    )
    return {"status": "success", "report": report}


# google_search_function = Agent(
#    # A unique name for the agent.
#    name="basic_search_agent",
#    # The Large Language Model (LLM) that agent will use.
#    model="gemini-2.0-flash-exp", # Google AI Studio
#    #model="gemini-2.0-flash-live-preview-04-09" # Vertex AI Studio
#    # A short description of the agent's purpose.
#    description="Agent to answer questions using Google Search.",
#    # Instructions to set the agent's behavior.
#    instruction="You are an expert researcher. You always stick to the facts.",
#    # Add google_search tool to perform grounding with Google search.
#    tools=[google_search]
# )
task_doer = BaseAgent(
    name="TaskExecutor"
    # tool=[google_search]
)

function_agent = LlmAgent(
   name="weather_time_agent",
   model="gemini-2.0-flash",
   description=(
       "Agent to answer questions about the time and weather in a city."
   ),
   instruction=(
       "You are a helpful agent who can answer user questions about the time and weather in a city."
   ),
   tools=[get_weather, get_current_time],
)

# Create parent agent and assign children via sub_agents
root_agent = LlmAgent(
    name="Coordinator",
    model="gemini-2.0-flash",
    description="I coordinate greetings and tasks.",
    sub_agents=[ # Assign sub_agents here
        function_agent,
        task_doer
    ]
)
