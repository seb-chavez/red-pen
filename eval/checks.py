"""Deterministic scoring. No model calls, so CI can run it for free."""
import re

TELLS = {
    "em_dash": r"—",
    "ai_vocabulary": r"\b(pivotal|crucial|robust|seamless(ly)?|leverag(e|es|ing)|enhanc(e|es|ing)|underscor(e|es|ing)|landscape|testament|foster(s|ing)?|delve|showcas(e|es|ing)|transformative|game-changing|empower(s|ing)?|unprecedented|cutting-edge)\b",
    "contrast_setup": r"\b(it'?s|this is|is) not (just |simply |only )?[^.;\n]{1,60}[;,.] ?(it'?s|but)\b",
    "vague_authority": r"\b(experts (say|agree)|studies show|industry research|it is widely recognized|it'?s no secret)\b",
    "summary_ending": r"(?m)^\W*(in conclusion|overall|in summary|to summarize)\b",
    "throat_clearing": r"(hope this helps|let me know if you have|don'?t hesitate to reach out|great question|i hope everyone)",
}


def words(text):
    return len(text.split())


def tells(text):
    counts = {name: len(re.findall(p, text, re.I)) for name, p in TELLS.items()}
    counts["total"] = sum(counts.values())
    return counts


def facts_kept(text, patterns):
    """Returns (kept, total, missing patterns)."""
    missing = [p for p in patterns if not re.search(p, text, re.I)]
    return len(patterns) - len(missing), len(patterns), missing
