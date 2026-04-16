"""
Exercise 2 — Answers
====================
Fill this in after running exercise2_langgraph.py.
Run `python grade.py ex2` to check for obvious issues.
"""

# ── Task A ─────────────────────────────────────────────────────────────────

# List of tool names called during Task A, in order of first appearance.
# Look at [TOOL_CALL] lines in your terminal output.
# Example: ["check_pub_availability", "get_edinburgh_weather"]

TASK_A_TOOLS_CALLED = ["check_pub_availability", "calculate_catering_cost", "get_edinburgh_weather", "generate_event_flyer"]

# Which venue did the agent confirm? Must be one of:
# "The Albanach", "The Haymarket Vaults", or "none"
TASK_A_CONFIRMED_VENUE = "The Albanach"

# Total catering cost the agent calculated. Float, e.g. 5600.0
# Write 0.0 if the agent didn't calculate it.
TASK_A_CATERING_COST_GBP = 5600.0

# Did the weather tool return outdoor_ok = True or False?
TASK_A_OUTDOOR_OK = False

# Optional — anything unexpected.
# If you used a non-default model via RESEARCH_MODEL env var, note it here.
# Example: "Used nvidia/nemotron-3-super-120b-a12b for the agent loop."
TASK_A_NOTES = ""

# ── Task B ─────────────────────────────────────────────────────────────────
#
# The scaffold ships with a working generate_event_flyer that has two paths:
#
#   - Live mode: if FLYER_IMAGE_MODEL is set in .env, the tool calls that
#     model and returns a real image URL.
#   - Placeholder mode: otherwise (the default) the tool returns a
#     deterministic placehold.co URL with mode="placeholder".
#
# Both paths return success=True. Both count as "implemented" for grading.
# This is not the original Task B — the original asked you to write a direct
# FLUX image call, but Nebius removed FLUX on 2026-04-13. See CHANGELOG.md
# §Changed for why we pivoted the task.

# Did your run of the flyer tool produce a success=True result?
# (This will be True for both live and placeholder mode — both are valid.)
TASK_B_IMPLEMENTED = True   # True or False

# Which path did your run take? "live" or "placeholder"
# Look for the "mode" field in the TOOL_RESULT output of Task B.
# If you didn't set FLYER_IMAGE_MODEL in .env, you will get "placeholder".
TASK_B_MODE = "placeholder"

# The image URL returned by the tool. Copy exactly from your terminal output.
# In placeholder mode this will be a placehold.co URL.
# In live mode it will be a provider CDN URL.
TASK_B_IMAGE_URL = "https://placehold.co/1200x628/1a1a2e/eaeaea?text=The+Haymarket+Vaults+%7C+160+guests&id=2ef939fbbaf6"

# The prompt sent to the image model. Copy from terminal output.
TASK_B_PROMPT_USED = "Professional event flyer for Edinburgh AI Meetup, tech professionals, modern venue at The Haymarket Vaults, Edinburgh. 160 guests tonight. Warm lighting, Scottish architecture background, clean modern typography."

# Why did the agent's behaviour NOT change when Nebius removed FLUX?
# One sentence. This is the point of the lesson.
TASK_B_WHY_AGENT_SURVIVED = """
Because its gracefully handled: _attempt_real_image_generation returns none if no model is set and then the answer is some placeholder.
"""

# ── Task C ─────────────────────────────────────────────────────────────────

# Scenario 1: first choice unavailable
# Quote the specific message where the agent changed course. Min 20 words.
SCENARIO_1_PIVOT_MOMENT = """
The user wanted to check The Bow Bar first for 160 vegan guests. The first tool call showed that The Bow Bar's capacity is 80, which is too small. So, they didn't meet the requirements. Then, the assistant checked The Haymarket Vaults next.
"""

SCENARIO_1_FALLBACK_VENUE = "The Haymarket Vaults"

# Scenario 2: impossible constraint (300 guests)
# Did the agent recommend a pub name not in the known venues list?
SCENARIO_2_HALLUCINATED = False   # True or False

# Paste the final [AI] message.
SCENARIO_2_FINAL_ANSWER = """
Okay, let's see. The user wanted to check The Bow Bar first for 160 vegan guests. The first tool call showed that The Bow Bar's capacity is 80, which is too small. So, they didn't meet the requirements. Then, the assistant checked The Haymarket Vaults next. The response says The Haymarket Vaults has a capacity of 160 and vegan options available, with status \"available\" and meets all constraints.\n\nSo, the user's main goal is to find a pub that can accommodate 160 vegan guests. Since The Haymarket Vaults meets all the requirements, the next step is to confirm this venue. The assistant should inform the user that this pub is suitable. Also, maybe check if the user wants to proceed with this one or if they need more info. But according to the tools provided, after confirming the venue, they might need to use other functions like calculate_catering_cost or generate_event_flyer. However, the user hasn't asked for those yet. The current task was just to check availability. So the answer should state that The Haymarket Vaults is available and meets all the requirements, providing the address and maybe asking if they want to proceed with that venue.\n</think>\n\nThe Haymarket Vaults meets all your requirements:\n- Capacity: 160 (exactly matches your needs)\n- Vegan options: Available\n- Status: Available\n- Address: 1 Dalry Road, Edinburgh\n\nWould you like me to proceed with this venue or check any other details?"
"""

# Scenario 3: out of scope (train times)
# Did the agent try to call a tool?
SCENARIO_3_TRIED_A_TOOL = False   # True or False

SCENARIO_3_RESPONSE = "Okay, the user is asking about the last train time from Edinburgh Waverley to London tonight. Let me check the tools provided.\n\nLooking at the available functions: check_pub_availability, get_edinburgh_weather, calculate_catering_cost, generate_event_flyer. None of these are related to train schedules. The functions are for checking pub availability, weather, catering costs, and generating flyers. \n\nSince there's no tool for train times, I can't use any of the provided functions to answer this. I need to inform the user that I don't have access to that information and suggest they check a train service website or app.\n</think>\n\nI don't have access to real-time train schedules or transportation data. For the most accurate information about the last train from Edinburgh Waverley to London, I recommend checking:\n1. The National Rail website (https://www.nationalrail.co.uk)\n2. Train service apps like Citymapper or Trainline\n3. The specific train operator's website (e.g., LNER)\n\nWould you like help with anything related to Edinburgh pubs, weather, or event planning instead?"


# Would this behaviour be acceptable in a real booking assistant? Min 30 words.
SCENARIO_3_ACCEPTABLE = """
Yes, I think it's acceptable for the assistant to recognize when a request is out of scope and to respond by informing the user that it cannot provide that information, while also suggesting alternative resources where the user can find the information they need. This shows that the assistant understands its limitations and can guide the user appropriately without providing incorrect or misleading information.
"""

# ── Task D ─────────────────────────────────────────────────────────────────

# Paste the Mermaid output from `python exercise2_langgraph.py task_d` here.
TASK_D_MERMAID_OUTPUT = """
graph TD;
        __start__([<p>__start__</p>]):::first
        agent(agent)
        tools(tools)
        __end__([<p>__end__</p>]):::last
        __start__ --> agent;
        agent -.-> __end__;
        agent -.-> tools;
        tools --> agent;
        classDef default fill:#f2f0ff,line-height:1.2
        classDef first fill-opacity:0
        classDef last fill:#bfb6fc
"""

# Compare the LangGraph graph to exercise3_rasa/data/flows.yml. Min 30 words.
TASK_D_COMPARISON = """
Langgraph consists of a single loop between the agent and the tools, we have no control over the flow of the conversation, while in Rasa we can define a specific flow for the conversation, which allows us to have more control over the user experience and to handle different scenarios more effectively. In Rasa, we can also define different actions and responses based on the user's input, which allows for a more personalized and dynamic interaction. Overall, Rasa provides more flexibility and control over the conversation flow compared to LangGraph's single loop structure.
"""

# ── Reflection ─────────────────────────────────────────────────────────────

# The most unexpected thing the agent did. Min 40 words.
# Must reference a specific behaviour from your run.

MOST_SURPRISING = """
The agent did not hallucinate any venues or information, even when faced with impossible constraints (300 guests). It correctly identified that The Haymarket Vaults was the only venue that met the requirements and did not try to invent any other options. This shows that the agent was able to handle the task effectively without resorting to fabrication, which is impressive given the complexity of the scenario.
"""