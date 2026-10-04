#!/usr/bin/env node
// Loads rules/red-pen.md into the session (SessionStart) and into every sub-agent (SubagentStart).
const fs = require("fs");
const path = require("path");

let event = "SessionStart";
try {
  event = JSON.parse(fs.readFileSync(0, "utf8")).hook_event_name || event;
} catch {}

const rules = fs.readFileSync(path.join(__dirname, "..", "rules", "red-pen.md"), "utf8");
process.stdout.write(JSON.stringify({
  hookSpecificOutput: { hookEventName: event, additionalContext: rules },
}));
