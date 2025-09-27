from agents import Agent

from .tools import get_leads, lookup_lead, score_lead_industry, write_lead_update


instructions = (
    "You are a sales assistant. Use tools to find leads, apply a simple industry score, "
    "update status/notes, then confirm by listing relevant leads with `get_leads`. "
    "Keep responses short and businesslike."
)


agent = Agent(
    name="Mini CRM Lead Qualifier",
    instructions=instructions,
    tools=[lookup_lead, score_lead_industry, write_lead_update, get_leads],
)


