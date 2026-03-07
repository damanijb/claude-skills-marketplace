---
name: nano-banana
description: "Generate stunning, production-quality images, visualizations, infographics, and SVG-style graphics using Google's Nano Banana 2 (Gemini 3.1 Flash Image Preview) API. Use this skill whenever the user wants to create charts, data visualizations, diagrams, presentation graphics, slide backgrounds, icons, infographics, poster art, or any visual asset for documents, decks, or dashboards. Also trigger for requests like generate an image of, create a visual for, make a chart image, design a graphic, build an infographic, add visuals to my slides, create SVG-style art, generate slide backgrounds, or any request to produce AI-generated imagery for professional use."
---

# Nano Banana 2 — Visual Generation Skill

Nano Banana 2 is Google's Gemini 3.1 Flash Image Preview model — combining Pro-level intelligence with Flash speed. It supports resolutions up to 4K, follows instructions precisely, and excels at data visualizations, infographics, and presentation-ready graphics.

## Setup

**Install the SDK:**
```bash
pip install google-genai --break-system-packages --quiet
```

**Configure API key** (use the key provided by the user, or read from environment):
```python
import os
from google import genai
from google.genai import types

# Resolution order: env var → ~/.nano-banana/.env → ask user
API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    env_path = os.path.expanduser("~/.nano-banana/.env")
    if os.path.exists(env_path):
        for line in open(env_path):
            if line.startswith("GEMINI_API_KEY="):
                API_KEY = line.strip().split("=", 1)[1]

client = genai.Client(api_key=API_KEY)
MODEL = "gemini-3.1-flash-image-preview"
```

## Core Generation Script

Use this function for all image generation tasks.

```python
from google import genai
from google.genai import types
import base64, os

def generate_image(prompt: str, output_path: str, api_key: str,
                   aspect_ratio: str = "16:9", style_notes: str = "") -> str:
    """
    Generate an image using Nano Banana 2 and save to disk.

    Args:
        prompt: Detailed description of the image to create
        output_path: Where to save the PNG (absolute path)
        api_key: Gemini API key
        aspect_ratio: "16:9", "1:1", "4:3", "9:16", etc.
        style_notes: Optional style guidance appended to prompt

    Returns:
        Path to saved image
    """
    client = genai.Client(api_key=api_key)

    full_prompt = prompt
    if style_notes:
        full_prompt += f"\n\nStyle: {style_notes}"

    response = client.models.generate_content(
        model="gemini-3.1-flash-image-preview",
        contents=full_prompt,
        config=types.GenerateContentConfig(
            response_modalities=["IMAGE", "TEXT"],
            image_config=types.ImageConfig(
                aspect_ratio=aspect_ratio,
            )
        )
    )

    for part in response.candidates[0].content.parts:
        if part.inline_data is not None:
            image_data = part.inline_data.data
            if isinstance(image_data, str):
                image_bytes = base64.b64decode(image_data)
            else:
                image_bytes = image_data

            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, 'wb') as f:
                f.write(image_bytes)
            return output_path

    raise ValueError("No image in response. Check API key and model availability.")
```

## Prompt Engineering — General Principles

Nano Banana responds best to **narrative descriptions**, not keyword lists. Describe the scene as if you're briefing a professional graphic designer — explain the layout, hierarchy, and visual relationships.

**Effective approach:**
> "Create a professional infographic showing a tiered investment framework. At the top, a wide green band contains the three strongest banks. Below it, a narrower amber band shows two banks with monitoring flags. At the bottom, a narrow red band shows restricted access. Use clean sans-serif typography on a white background."

**Less effective:**
> "infographic, banks, green amber red, professional, 4K, high quality, masterpiece"

### Key principles:

1. **Start with "On a clean white background."** This is the single most impactful instruction for finance visuals. Gemini defaults to dark, colorful dashboards — you need to override this immediately. Put it at the very start of the prompt, before anything else.

2. **Lead with structure, not style.** Describe what goes where before describing how it looks. The model needs spatial clarity first.

3. **Be specific about text.** Don't say "add labels." Say: "Write 'ECB Avg: 9.88%' in bold text next to the dashed reference line." Gemini excels at text rendering when given exact strings.

4. **Use professional context.** Phrases like "as it would appear in a J.P. Morgan research PDF" or "suitable for a county treasurer board presentation" anchor the model's understanding of quality expectations. This is more effective than listing hex codes.

5. **Break complex layouts into sections.** Use spatial markers: "TOP SECTION:", "LEFT COLUMN:", "BOTTOM BAR:" to organize multi-element compositions.

6. **Explicitly exclude decoration.** Gemini will add gradients, shadows, icons, and colorful fills unless you tell it not to. End key sections with: "No icons, no fills, no gradients." It's better to explicitly say what you don't want than to hope the model infers restraint.

## Finance & Investment Research Defaults

When generating visuals for finance, economics, or investment research, apply these defaults unless the user specifies otherwise. The goal is output that looks like it came from a sell-side research desk — clean enough to paste into a Word document, print in a board packet, or embed in a PDF memo.

### The Enterprise Aesthetic

The single most important thing to get right: **restraint**. Professional research visuals use very few colors, generous white space, and let the data dominate. Think of the charts and infographics you'd see in a J.P. Morgan or Morgan Stanley research PDF — they're almost austere. That restraint is what signals credibility.

Common mistakes that make output look "AI-generated":
- Too many colors (rainbow palettes, gradients, decorative fills)
- Decorative elements (icons, borders, shadows, rounded corners everywhere)
- Dark or colored backgrounds
- Overly stylized typography
- Too much text crammed in — walls of text destroy the visual

### Typography Rules

Good typography is the difference between "looks AI-generated" and "looks like it came from a design team." Follow these rules strictly:

1. **Three sizes only.** Every infographic should use exactly three text sizes:
   - **Large**: Title only (one line)
   - **Medium**: Key metrics, entity names, data values
   - **Small**: Brief labels, footnotes, source lines

2. **Brevity is mandatory.** No descriptive line should exceed 8-10 words. Use fragments, not sentences. Instead of "Duration gains as front-end rallies. Curve steepening benefits barbell positions." write "Front-end rally → barbell benefits."

3. **Generous line spacing.** Explicitly request "generous vertical spacing between all text elements" and "at least 1.5x line height." Cramped text is the #1 clutter signal.

4. **One font weight contrast.** Use bold for labels/headers and regular weight for values. Don't mix italic, underline, or all-caps (except for short status badges like "RESOLVED").

### Anti-Clutter Rules

When constructing prompts, actively reduce content density:

- **Cap text elements.** No infographic should have more than 20-25 distinct text strings total. If you're exceeding this, split into two visuals or cut content.
- **No paragraph blocks.** Never include multi-sentence descriptions in an infographic prompt. Compress every description to a short fragment.
- **Prefer data over explanation.** Show "CET1: 14.2%" rather than "The CET1 ratio improved to 14.2% reflecting retained earnings."
- **Leave breathing room.** Explicitly say "leave 30% of the total area as empty white space" in the prompt.

### Prompt Construction for Finance Visuals

Build every finance prompt in this order:

1. **White background first.** Start every prompt with: "On a clean white background, create..."
   This is the most important single instruction. Gemini has a strong prior toward dark, colorful dashboards — you need to override it at the very beginning of the prompt.

2. **Structure and layout next.** Describe what goes where spatially.

3. **Data and text.** Specify exact strings, numbers, and labels.

4. **Style last, and keep it minimal.** Append this style block:

```
Style: Enterprise investment research. Clean white background with at
least 30% of the area as empty white space. Navy (#1a2332) for all text.
Use at most 2-3 accent colors: green (#16A34A), amber (#D97706),
muted red (#B91C1C). No decorative elements, no gradients, no shadows,
no colored backgrounds, no filled badges or boxes.
Typography: clean sans-serif, three sizes only — large title, medium
data values, small labels. Generous spacing between all text elements.
Bold for headers, regular weight for values. Keep all text fragments
short (under 10 words each). The visual should look like it belongs
in a printed J.P. Morgan or Morgan Stanley research PDF — restrained,
typographic, and spacious.
```

### Why this matters

Investment research gets printed, embedded in Word documents, inserted into PowerPoint decks, and shared as PDFs. Dark backgrounds waste toner, clash with document styling, and look out of place. Colorful, decorative visuals undermine credibility — they look like marketing material, not analysis. The target is clean, simple, and authoritative.

### Financial Infographic Templates

For finance-related requests, choose the template that best fits the content type. Each template describes the **layout** and **visual metaphor** that Nano Banana renders well.

Remember: every template starts with "On a clean white background" and uses at most 2-3 accent colors. The dominant color in every output should be white space. Keep all text fragments short — under 10 words. Never include multi-sentence descriptions in the prompt.

#### 1. Tiered Comparison (best for: bank rankings, credit tiers, risk categories)

```
On a clean white background, create a professional tiered comparison
infographic titled "[TITLE]".

Layout: Three horizontal bands stacked vertically, separated by thin
lines. Generous white space between sections. Navy (#1a2332) text throughout.

TIER 1 (top band — thin green #16A34A left accent bar, 4px wide):
[Entity names and key metrics in navy text]

TIER 2 (middle band — thin amber #D97706 left accent bar):
[Entity names and key metrics in navy text]

TIER 3 (bottom band — thin muted red #B91C1C left accent bar):
[Entity names and key metrics in navy text]

Each entity shows: name (bold) and primary metric (regular weight).
No descriptions or rationale text — just names and numbers.
Bottom: single-line summary in smaller text.
No icons, no fills, no gradients, no badges. Just text, thin accent bars,
and generous white space. Leave at least 30% of the image as empty space.
```

#### 2. Status Tracker (best for: risk monitoring, milestone tracking, project status)

```
On a clean white background, create a professional status tracker
titled "[TITLE]".

Layout: Simple vertical list with generous spacing between rows.
Navy (#1a2332) text for everything.

Each row is one line:
- Small filled circle (8px): green #16A34A, amber #D97706, or red #B91C1C
- Factor name in bold navy
- Status in regular weight
- Brief outcome description

Rows:
1. ● [Factor] — [Status] — [Outcome]
...

Bottom: "[X] of [Y] resolved" in smaller gray text.
No boxes, no cards, no backgrounds, no filled badges — just a clean list
with generous vertical spacing between rows. Each row should breathe.
```

#### 3. Flow / Migration Diagram (best for: rating changes, process flows, before/after)

```
On a clean white background, create a professional migration diagram
titled "[TITLE]".

Layout: Vertical axis on the left showing ordinal scale labels.
Navy (#1a2332) text and axis lines.

For each entity, a horizontal arrow shows direction of change:
- Green #16A34A arrows for improvements (pointing up/right)
- Red #B91C1C arrows for deteriorations (pointing down/right)
- Gray #9CA3AF lines for no change

Each arrow labeled with entity name in navy text.
Bottom: single-line summary. Minimal gridlines, maximum white space.
```

#### 4. Executive Summary Card (best for: report cover pages, key findings)

```
On a clean white background, create an executive summary infographic
titled "[TITLE]".

Layout: Navy (#1a2332) title text at top (no colored bar or banner).
Below: 3-4 key metrics displayed as large navy numbers with small
descriptive labels beneath each. Arrange in a single row or 2x2 grid.

Below the metrics: 2-3 bullet points summarizing key findings
in smaller navy text.

No icons, no colored boxes, no decorative elements.
The information hierarchy comes from font size alone:
title (large) → metrics (medium-large) → descriptions (small).
```

#### 5. Metric Comparison Table (best for: peer analysis, KPI dashboards)

```
On a clean white background, create a comparison table infographic
titled "[TITLE]".

Layout: Clean table with thin gray (#E5E7EB) gridlines.
Navy (#1a2332) text for all headers and values.

- Column headers: metric names, bold
- Row headers: entity names, bold
- Cell values: numbers in regular weight
- Cells that are above-average: green #16A34A text
- Cells that are below-average: red #B91C1C text
- Benchmark row highlighted with a light gray (#F3F4F6) background

No colored fills on headers. No thick borders. Just thin lines
and color-coded text values.
```

## Workflow for Creating Multiple Infographics

When generating a set of related visuals (e.g., for a research report):

1. **Plan the visual story** — Read the source document and identify 3-5 key messages that benefit from visual treatment. Not everything needs an infographic — focus on data that tells a story.

2. **Choose the right template** for each message from the templates above.

3. **Maintain visual consistency** — Use the same color palette, typography direction, and layout density across all pieces. This creates a cohesive visual identity.

4. **Generate with matching aspect ratios:**
   - `16:9` for presentation slides and widescreen displays
   - `3:4` or `4:5` for report inserts and portrait-oriented documents
   - `1:1` for social media or dashboard tiles

5. **Save organized by purpose:**
   ```
   infographics/
   ├── 01_executive_summary.png
   ├── 02_risk_tracker.png
   ├── 03_tier_comparison.png
   └── 04_metric_dashboard.png
   ```

6. **Verify and iterate** — View each generated image. If text is illegible or layout is off, refine the prompt with more spatial specificity and regenerate.

## Error Handling

- **401/403**: API key is invalid or lacks image generation permissions
- **Model not found**: Verify model is `gemini-3.1-flash-image-preview` (exact string)
- **No image in response**: The model may have filtered the request — rephrase the prompt
- **Rate limits**: Add `time.sleep(2)` between batch requests
- **Text illegibility**: Make the prompt more specific about text placement and size. Try a taller aspect ratio (3:4) to give more vertical space.

## CLI Alternative (nano-banana command)

If the nano-banana CLI is installed, you can also generate images via command line:

```bash
nano-banana "your prompt" -a 16:9 -s 2K -o output-name
```

See `references/cli-reference.md` for full CLI documentation including reference images, transparent backgrounds, and model selection.
