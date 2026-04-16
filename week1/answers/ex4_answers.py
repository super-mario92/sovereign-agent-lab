"""
Exercise 4 — Answers
====================
Fill this in after running exercise4_mcp_client.py.
"""

# ── Basic results ──────────────────────────────────────────────────────────

# Tool names as shown in "Discovered N tools" output.
TOOLS_DISCOVERED = ["search_venues", "get_venue_details"]

QUERY_1_VENUE_NAME    = "The Haymarket Vaults"
QUERY_1_VENUE_ADDRESS = "1 Dalry Road, Edinburgh"
QUERY_2_FINAL_ANSWER  = "Okay, the user is looking for a venue in Edinburgh that can hold 300 people and has vegan options. I first tried using the search_venues function with min_capacity 300 and requires_vegan true, but got a validation error. Then I adjusted the tool call to include the parameters under the \"input\" object, which fixed the error. But the response came back with zero matches. Hmm, that means there are no venues available that meet both criteria. Maybe the capacity is too high, or there are no venues with vegan options at that size. I should check if there are any venues with a lower capacity or without the vegan requirement. Alternatively, maybe the user can consider multiple venues or adjust the capacity. Let me see if I can get more details on available venues without the vegan filter to see if there are options. If not, I'll have to inform the user that there are no available venues matching their request.\n</think>\n\nIt seems there are no Edinburgh venues currently available that can accommodate 300 people with vegan options. Would you like me to:\n1. Search for venues with a lower capacity (e.g., 200-299 guests)?\n2. Look for venues without the vegan requirement?\n3. Check if multiple smaller venues could work together?\n\nLet me know how you'd like to proceed!"



# ── The experiment ─────────────────────────────────────────────────────────
# Required: modify venue_server.py, rerun, revert.

EX4_EXPERIMENT_DONE = True   # True or False

# What changed, and which files did or didn't need updating? Min 30 words.
EX4_EXPERIMENT_RESULT = """
I had to update mcp_venue_server.py to set the availability status of The Albanachs to full.This cause the tool to only return one valid match instead of two. I didn't need to update exercise4_mcp_client.py at all, which shows that the client is decoupled from the server implementation. This is a key benefit of using MCP — I can change the server's internal logic and data without breaking the client, as long as the tool interfaces remain consistent.
"""

# ── MCP vs hardcoded ───────────────────────────────────────────────────────

LINES_OF_TOOL_CODE_EX2 = 150   # ~150 lines of tool definitions in venue_tools.py that exercise2 imports
LINES_OF_TOOL_CODE_EX4 = 0    # zero — tools are discovered at runtime from the MCP server

# What does MCP buy you beyond "the tools are in a separate file"? Min 30 words.
MCP_VALUE_PROPOSITION = """
MCP provides a standard protocol so that any compliant client — LangGraph, Rasa, or anything else — can discover and call tools at runtime without importing code or knowing the implementation. This means multiple agents share the same tool server, and you can add, remove, or change tools on the server without touching any client. In exercise 4, the client discovered search_venues and get_venue_details dynamically; if the server added a book_venue tool tomorrow, the client would see it automatically. That decoupling is what lets the two halves of PyNanoClaw (autonomous loop + structured agent) share a single tool layer.
"""

# ── PyNanoClaw architecture — SPECULATION QUESTION ─────────────────────────
#
# (The variable below is still called WEEK_5_ARCHITECTURE because the
# grader reads that exact name. Don't rename it — but read the updated
# prompt: the question is now about PyNanoClaw, the hybrid system the
# final assignment will have you build.)
#
# This is a forward-looking, speculative question. You have NOT yet seen
# the material that covers the planner/executor split, memory, or the
# handoff bridge in detail — that is what the final assignment (releases
# 2026-04-18) is for. The point of asking it here is to check that you
# have read PROGRESS.md and can imagine how the Week 1 pieces grow into
# PyNanoClaw.
#
# Read PROGRESS.md in the repo root. Then write at least 5 bullet points
# describing PyNanoClaw as you imagine it at final-assignment scale.
#
# Each bullet should:
#   - Name a component (e.g. "Planner", "Memory store", "Handoff bridge",
#     "Rasa MCP gateway")
#   - Say in one clause what that component does and which half of
#     PyNanoClaw it lives in (the autonomous loop, the structured agent,
#     or the shared layer between them)
#
# You are not being graded on getting the "right" architecture — there
# isn't one right answer. You are being graded on whether your description
# is coherent and whether you have thought about which Week 1 file becomes
# which PyNanoClaw component.
#
# Example of the level of detail we want:
#   - The Planner is a strong-reasoning model (e.g. Nemotron-3-Super or
#     Qwen3-Next-Thinking) that takes the raw task and produces an ordered
#     list of subgoals. It lives upstream of the ReAct loop in the
#     autonomous-loop half of PyNanoClaw, so the Executor never sees an
#     ambiguous task.

WEEK_5_ARCHITECTURE = """
- The Planner is a strong-reasoning model (e.g. Qwen3-32B) that takes Rod's raw request and breaks it into ordered subgoals (find venue, check weather, calculate cost, hand off to confirmation). It lives upstream of the ReAct loop in the autonomous-loop half, so the Executor never sees an ambiguous task.
- The Executor is the research_agent.py ReAct loop from Week 1, extended with web search and file tools. It lives inside the autonomous-loop half, calling tools from the shared MCP server to complete each subgoal the Planner sets.
- The Structured Agent is the Rasa CALM confirmation agent from Exercise 3, handling the pub manager phone call with deterministic flows and business-rule guards (deposit limit, cutoff time). It lives in the structured-agent half of PyNanoClaw, where every response is auditable and constrained to flows.yml.
- The Handoff Bridge sits in the shared layer between both halves. When the Executor reaches a step that requires a human conversation (e.g. confirming the deposit with the pub manager), it calls handoff_to_structured to delegate to Rasa. When Rasa finishes, it hands control back to the loop.
- The Shared MCP Tool Server (mcp_venue_server.py extended) is the shared layer that both halves connect to. It exposes venue search, web search, calendar, and booking tools via the MCP protocol. Neither half cares where a tool came from — they discover tools dynamically, which is what lets the hybrid system hang together.
- The Memory Store provides persistent filesystem-backed memory and a vector store for RAG. It lives in the shared layer so both the autonomous loop (to remember research results across steps) and the structured agent (to answer questions not covered by flows.yml) can access it.
"""

# ── The guiding question ───────────────────────────────────────────────────
# Which agent for the research? Which for the call? Why does swapping feel wrong?
# Must reference specific things you observed in your runs. Min 60 words.

GUIDING_QUESTION_ANSWER = """
The LangGraph agent belongs on the research side: in Exercise 2 it autonomously checked two venues, fetched weather, calculated catering, and generated a flyer — deciding the order itself based on what information it needed next. That open-ended reasoning is exactly what research requires. The Rasa CALM agent belongs on the confirmation call: in Exercise 3 it collected exactly three slots (guest count, vegan count, deposit), applied a deterministic deposit-limit rule, and either confirmed or escalated — never improvising. Swapping them feels wrong because LangGraph on the phone call could freestyle dangerous commitments (like it suggested train websites in the out-of-scope scenario), while Rasa on the research would be stuck — it cannot plan its own tool calls or reason across results, since it only follows flows explicitly defined in flows.yml. Each technology is shaped for one half of the problem, and using it for the other half would either lose guardrails or lose autonomy.
"""