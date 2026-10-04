PRD notes: two-way SMS confirmations (Tidewell)

- problem: one-way reminders get ignored; front desk calls every unconfirmed patient (~2 hrs/day); no-shows avg $9k/month per clinic
- send SMS 48 hours before appt: "Reply C to confirm, R to reschedule"
- reply C -> appt marked confirmed in calendar
- reply R -> patient gets link to pick a new slot; old slot released to waitlist
- no reply by 24 hours before -> second SMS; still none -> appt flagged for front desk call list
- clinic can set a $25 no-show fee shown in the message (optional, off by default)
- patients who reply STOP are opted out, never texted again, flagged in record
- success: confirmed-appointment rate, front desk call time, no-show rate
- out of scope: email, voice calls, payments collection for the fee
