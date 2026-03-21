---
description: Generate the monthly Investment Pool Report
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Task, TodoWrite, AskUserQuestion, WebSearch, WebFetch
argument-hint: [YYYYMMDD or "latest"]
---

Generate a monthly Investment Pool Report for San Bernardino County's treasury portfolio.

## Instructions

1. Read the pool-report-generator skill at `${CLAUDE_PLUGIN_ROOT}/skills/pool-report-generator/SKILL.md`.
2. Read the PPTX skill for PptxGenJS syntax and best practices.
3. Read ALL reference files in `${CLAUDE_PLUGIN_ROOT}/skills/pool-report-generator/references/` — design system, data dictionary, policy limits, chart specs, tone guide, AND economic research guide.
4. Follow the **Parallel Phase Pipeline** in the skill:

   **Phase 0 (Setup):** Read refs, determine report date from `$1` (YYYYMMDD) or query DB for latest.

   **Phase 1 (3 Parallel Agents):** Launch simultaneously via Task tool:
   - Agent A: SQL data pull (holdings + cashflow)
   - Agent B: FRED data pull (latest values + 12-month history for all series)
   - Agent C: Economic research (WebSearch for Fed policy, inflation, employment, credit conditions, market themes)

   **Phase 2 (2 Parallel Agents):** After Phase 1 completes:
   - Agent D: Data transformation + chart generation (portfolio + economic trend charts)
   - Agent E: Economic commentary writing (plain-English narratives for Board audience)

   **Phase 3 (Sequential):** Build the PPTX with all data, charts, and commentary.

   **Phase 4 (Sequential):** QA — convert to images, inspect, fix, deliver.

5. Save the final .pptx to the user's workspace folder.
6. Use the TodoWrite tool to track progress through each phase.

## Key Reminders

- **Parallel execution**: Use the Task tool to launch agents simultaneously. This cuts generation time significantly.
- **Economic storytelling**: The report now includes 8-9 economic slides with trend charts and plain-English narratives. Follow the economic-research.md guide.
- **Content safe zone**: All content between y=0.9" and y=4.9". Nothing below 4.9" or it hits the footer.
- **Portfolio Impact callout**: Every economic slide ends with a gold-highlighted "PORTFOLIO IMPACT" box.
- **Typography**: Arial Black for slide titles, Calibri for everything else. See design-system.md for exact sizes.
- **Charts**: Match the aspect ratio exactly when embedding. Never stretch. Economic charts are 4.5" × 3.0".
- **Voice**: Fiduciary stewardship, not active management. Plain English for economic slides. See tone-guide.md.
- **QA is mandatory**: Convert to images and visually inspect before delivering.
