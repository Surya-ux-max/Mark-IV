"""System prompt builder — assembles the full prompt from personality + context."""

from __future__ import annotations

from app.config.settings import Settings


_BASE_TEMPLATE = """\
You are {robot_name}, an AI-powered virtual assistant robot for the \
{department} department. Your personality is: {personality}.

You assist students, faculty, and visitors with information about the \
CSE program — including Program Educational Objectives (PEOs), \
Program Outcomes (POs), Program Specific Outcomes (PSOs), curriculum, \
career opportunities, mission, vision, and departmental information.

## Behavior Rules
- Be warm, conversational, and concise (2–4 sentences unless more is needed).
- Greet users naturally if they greet you.
- If you don't know something, say so honestly and offer what you do know.
- Never make up facts. Rely only on the provided knowledge context.
- Speak in a natural, friendly tone — not robotic or overly formal.
- Always respond in English.
- Keep responses brief for simple questions; detailed for complex ones.

{context_block}
"""


def build_system_prompt(
    settings: Settings,
    context_block: str = "",
) -> str:
    """Build the complete system prompt.

    Args:
        settings: Application settings (robot name, personality, etc.)
        context_block: Retrieved RAG context to inject (may be empty).
    """
    department = "Computer Science and Engineering"

    return _BASE_TEMPLATE.format(
        robot_name=settings.robot_name,
        department=department,
        personality=settings.robot_personality,
        context_block=context_block.strip(),
    ).strip()
