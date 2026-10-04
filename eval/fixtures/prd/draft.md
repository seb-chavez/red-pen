# PRD: Two-Way SMS Confirmations

## Overview

In an increasingly mobile-first world, patients expect seamless, convenient communication with their healthcare providers. Two-way SMS confirmations represent a pivotal step forward in Tidewell's mission to transform the patient experience and empower dental practices with cutting-edge engagement tools. This document describes the vision, goals, and requirements for this transformative feature.

## Background and Problem Statement

It's no secret that missed appointments are a persistent challenge for dental practices. Industry research consistently shows that no-shows erode revenue and disrupt clinical workflows. Our current one-way reminders, while helpful, are frequently ignored by patients. As a result, front-desk staff must call every unconfirmed patient, a process that consumes roughly two hours per day. Meanwhile, the average clinic loses approximately $9,000 per month to no-shows. This is not just an operational inefficiency; it's a fundamental barrier to practice growth.

## Vision

We envision a world where confirming a dental appointment is as easy as sending a text to a friend. By enabling patients to respond directly to reminders, we can foster a more engaged, responsive patient base while freeing front-desk teams to focus on high-value interactions.

## Goals

- Enhance patient engagement
- Reduce the burden on front-desk staff
- Decrease no-show rates
- Deliver a delightful, intuitive experience

## Requirements

- The system will send an SMS 48 hours before the appointment asking the patient to reply C to confirm or R to reschedule.
- Patients can confirm or reschedule by replying.
- If a patient does not reply, the system will follow up appropriately, at 24 hours before.
- Clinics can optionally display a $25 no-show fee.
- Rescheduled slots go to the waitlist.
- Patients can opt out by replying STOP.

## Success Metrics

We will measure success through a variety of key indicators, including confirmed-appointment rate, front-desk call time, and no-show rate. These metrics will help us understand the impact of the feature and guide future iterations.

## Out of Scope

Email, voice calls, and collecting payment for the no-show fee are out of scope for this release.

## Conclusion

Two-way SMS confirmations are a game-changing addition to the Tidewell platform. By meeting patients where they are, we will strengthen relationships, streamline operations, and deliver measurable value to the practices we serve.
