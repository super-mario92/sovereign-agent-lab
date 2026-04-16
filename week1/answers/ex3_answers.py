"""
Exercise 3 — Answers
====================
Fill this in after completing the three Rasa conversations.

CALM vs Old Rasa — what changed
---------------------------------
The old open-source Rasa approach used:
  - nlu.yml: intent training examples
  - rules.yml: explicit dialogue rules
  - FormValidationAction: Python class to parse slot values

Rasa Pro CALM uses:
  - flows.yml: natural language descriptions of what each flow does
  - from_llm slots: the LLM extracts values from conversation
  - ONE custom action: ActionValidateBooking for the business rules

The conversation is the same from the manager's perspective.
The machinery underneath is completely different.

CONVERSATION SCRIPTS
---------------------
Conversation 1 (happy path):
  You:    calling to confirm a booking
  Agent:  [asks guest count]
  You:    160 guests
  Agent:  [asks vegan count]
  You:    about 50 need vegan
  Agent:  [asks deposit]
  You:    £200 deposit
  Agent:  [confirms or escalates?]

Conversation 2 (deposit too high):
  Same as above but use a deposit above £300 (e.g. "£500 deposit").

Conversation 3 (out of scope):
  Start normally, then when asked for vegan count say something like
  "can you arrange parking for the speakers?" and observe what happens.
  Does CALM handle this differently than the old rules approach?
"""

# ── Conversation 1: Happy path ─────────────────────────────────────────────

CONVERSATION_1_TRACE = """
Bot loaded. Type a message and press enter (use '/stop' to exit): 
Your input ->  calling to confirm a booking                                                                                                                                                                      
How many guests are you confirming for tonight's event?
Your input ->  160 guests                                                                                                                                                                                        
And how many of those guests will need vegan meals?
Your input ->  about 50 need vegan                                                                                                                                                                               
2026-04-16 17:11:46 WARNING  rasa.utils.log_utils  - [warning  ] CompactLLMCommandGenerator.parse_commands actions='<think>
Okay, let\'s see. The user said, "about 50 need vegan." The current flow is confirm_booking, and the current step is asking for vegan_count. The guest_count is already set to 160. So the user is providing the number of vegan guests here.                                                                                                                                                                                     
                                                                                                                                                                                                                 
First, I need to set the vegan_count slot. The user mentioned "about 50," so I should take that as the value. The slot expects a float, so even though it\'s "about 50," the value should be 50.0. But the user might have said "about," but the instruction says to extract the exact value as provided. Wait, the user said "about 50," but the slot is a float. Should I take 50 as the value? The example in the slot extraction shows that when the user says "send money to John," they set the recipient. So here, even if it\'s approximate, the value is 50.0.                                                                            
                                                                                                                                                                                                                 
So the action would be set slot vegan_count 50.0. Then, since the current flow is confirm_booking, and the next step would be to ask for the deposit amount. But the user hasn\'t provided that yet. However, the task is to respond to the last message. The user\'s last message is providing the vegan count, so the AI should set that slot and then proceed. Since the current step was requesting vegan_count, after setting it, the flow would move to the next requested slot, which is deposit_amount_gbp. But according to the instructions, do I need to start another flow or just set the slot? The example shows that when a slot is provided, you set it and then the flow continues. So the next step would be to prompt for the deposit amount. But the user hasn\'t mentioned it yet, so the AI\'s next action would be to ask for the deposit. However, the task here is to output the actions based on the user\'s last message. So the only action needed here is to set the vegan_count slot. The next step would be handled in the next user message. Wait, but the current state\'s active_flow is confirm_booking, and the current_step is requesting vegan_count. Once that\'s set, the flow would proceed to the next step, which is deposit_amount_gbp. But the user hasn\'t provided that yet, so the AI\'s next message would be to ask for the deposit. However, in the action list, do I need' message='No commands were parsed from the LLM actions.'                                 
2026-04-16 17:11:46 WARNING  rasa.utils.log_utils  - [warning  ] llm_command_generator.predict_commands message='No commands were predicted as the LLM response could not be parsed or the LLM responded with an invalid command. Returning a CannotHandleCommand instead.'                                                                                                                                                       
I’m sorry I am unable to understand you, could you please rephrase?
And how many of those guests will need vegan meals?
Your input ->  50                                                                                                                                                                                                
What deposit amount in GBP are you proposing to secure the booking?
Your input ->  200                                                                                                                                                                                               
Thank you — booking confirmed. 160 guests, 50 requiring vegan meals, £200 deposit accepted. I'll send written confirmation to the organiser shortly.
Is there anything else I can help you with?
"""

CONVERSATION_1_OUTCOME = "confirmed"   # "confirmed" or "escalated"

# ── Conversation 2: Deposit too high ───────────────────────────────────────

CONVERSATION_2_TRACE = """
Your input ->  calling to confirm a booking                                                                                                                                                                      
How many guests are you confirming for tonight's event?
Your input ->  160                                                                                                                                                                                               
And how many of those guests will need vegan meals?
Your input ->  50                                                                                                                                                                                                
What deposit amount in GBP are you proposing to secure the booking?
Your input ->  500                                                                                                                                                                                               
I need to check one thing with the organiser before I can confirm. The issue is: a deposit of £500 exceeds the organiser's authorised limit of £300. Can I call you back within 15 minutes?
Is there anything else I can help you with?
Your input ->  yes """

CONVERSATION_2_OUTCOME = "escalated"   # "confirmed" or "escalated"
CONVERSATION_2_REASON  = "deposit exceeds limit"   # the reason the agent gave for escalating

# ── Conversation 3: Out of scope ───────────────────────────────────────────

CONVERSATION_3_TRACE = """
And how many of those guests will need vegan meals?
Your input ->  can you arrange parking for the speakers?                                                                                                                                                         
I can only help with confirming tonight's venue booking. For anything else, please contact the event organiser directly.
Would you like to continue with confirm booking?
"""

# Describe what CALM did after the out-of-scope message. Min 20 words.
CONVERSATION_3_WHAT_HAPPENED = """
it said it can only help with the booking and I should contact the event organiser directly. It then asked if I wanted to continue with confirming the booking.
"""

# Compare Rasa CALM's handling of the out-of-scope request to what
# LangGraph did in Exercise 2 Scenario 3. Min 40 words.
OUT_OF_SCOPE_COMPARISON = """
Rasa CALM strictly refused the out-of-scope request and redirected me back to the active booking flow, asking if I wanted to continue. It never attempted to answer the parking question at all. LangGraph, by contrast, acknowledged it lacked the right tools but still improvised a helpful-sounding response, suggesting external resources like National Rail and Trainline. CALM is constrained to its defined flows and cannot go off-script, while LangGraph can say anything the LLM generates — helpful in some cases, but a guardrail risk in a production booking assistant.
"""

# ── Task B: Cutoff guard ───────────────────────────────────────────────────

TASK_B_DONE = True   # True or False

# List every file you changed.
TASK_B_FILES_CHANGED = ["actions/actions.py"]

# How did you test that it works? Min 20 words.
TASK_B_HOW_YOU_TESTED = """
Set the condiction in actions.py to true as i cannot influence the time in testing, then I ran the agent and tried to confirm a booking. The agent immediately escalated the booking instead of asking for details, which is the expected behaviour when the cutoff guard is triggered.
"""

# ── CALM vs Old Rasa ───────────────────────────────────────────────────────

# In the old open-source Rasa (3.6.x), you needed:
#   ValidateBookingConfirmationForm with regex to parse "about 160" → 160.0
#   nlu.yml intent examples to classify "I'm calling to confirm"
#   rules.yml to define every dialogue path
#
# In Rasa Pro CALM, you need:
#   flow descriptions so the LLM knows when to trigger confirm_booking
#   from_llm slot mappings so the LLM extracts values from natural speech
#   ONE action class (ActionValidateBooking) for the business rules
#
# What does this simplification cost? What does it gain?
# Min 30 words.

CALM_VS_OLD_RASA = """
The LLM now handles intent classification and slot extraction — tasks that previously required hand-written NLU training examples and regex parsing in Python. This means you no longer need to anticipate every phrasing a user might use; the LLM generalises from natural language descriptions in flows.yml instead. Python still handles the business rules (e.g. deposit limit validation in ActionValidateBooking), and rightly so — those are deterministic checks that must never be left to an LLM's judgement. The trade-off: the old regex approach was fully predictable and testable, while LLM-based extraction can occasionally misparse ambiguous input (as seen when "about 50" initially failed). You gain flexibility and far less boilerplate, but you lose the certainty that every input maps to an exact, reproducible output.
"""

# ── The setup cost ─────────────────────────────────────────────────────────

# CALM still required: config.yml, domain.yml, flows.yml, endpoints.yml,
# rasa train, two terminals, and a Rasa Pro licence.
# The old Rasa ALSO needed nlu.yml, rules.yml, and a FormValidationAction.
#
# CALM is simpler. But it's still significantly more setup than LangGraph.
# That setup bought you something specific.
# Min 40 words.

SETUP_COST_VALUE = """
All that setup — config files, training, two terminals, a licence — buys you constrained behaviour. The CALM agent cannot improvise a response it wasn't trained on and cannot call a tool that wasn't defined in flows.yml. For a booking confirmation use case, that is a feature, not a limitation: you want the agent to collect exactly three slots, apply the deposit rule, and either confirm or escalate — nothing more. LangGraph could freestyle (e.g. suggesting train websites when asked about schedules), which is creative but dangerous in a production workflow where every response should be predictable and auditable. The setup cost is the price you pay for guardrails: the agent does only what you explicitly designed it to do.
"""
