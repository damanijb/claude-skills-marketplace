---
name: nano-banana
description: "Generate stunning, production-quality images, visualizations, infographics, and SVG-style graphics using Google's Nano Banana 2 (Gemini 3.1 Flash Image Preview) API. Supports two distinct aesthetics: (1) Enterprise/research style — clean white backgrounds, restrained typography for J.P. Morgan-grade board packets and research PDFs, and (2) Visual Capitalist editorial style — bold dark backgrounds, vibrant colors, proportional data shapes (treemaps, pyramids, Sankeys, hex grids, bubble charts, choropleths, bar rankings, stacked comparisons, scale visuals, and timeline arcs) for engaging, shareable data journalism. Use this skill whenever the user wants to create charts, data visualizations, diagrams, presentation graphics, slide backgrounds, icons, infographics, poster art, or any visual asset for documents, decks, or dashboards. Also trigger for requests like generate an image of, create a visual for, make a chart image, design a graphic, build an infographic, Visual Capitalist style, editorial infographic, data visualization, bold infographic, or any request to produce AI-generated imagery for professional use."
---

# Nano Banana 2 — Visual Generation Skill

Nano Banana 2 is Google's Gemini 3.1 Flash Image Preview model — combining Pro-level intelligence with Flash speed. It supports resolutions up to 4K, follows instructions precisely, and excels at data visualizations, infographics, and presentation-ready graphics.

This skill supports two distinct visual aesthetics:
- **Enterprise Research** (Templates 1-5): Clean white backgrounds, restrained palette, suitable for board packets, research PDFs, and formal presentations. Think J.P. Morgan / Morgan Stanley.
- **Visual Capitalist Editorial** (Templates 6-15): Bold dark backgrounds, vibrant saturated colors, proportional data shapes, oversized hero numbers. Think Visual Capitalist, Statista, or shareable data journalism. Includes treemaps, pyramids, Sankey flows, hex grids, bubble charts, choropleths, bar rankings, stacked comparisons, scale visuals, and timeline arcs.

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

## Visual Capitalist Style — Bold Editorial Infographics

When the user wants **engaging, shareable, visually striking** infographics — the kind you'd see on Visual Capitalist, Statista, or social media data visualizations — switch from the restrained enterprise aesthetic to this bold editorial style.

**When to use this style:**
- User says "infographic," "visual capitalist style," "make it bold," "editorial," "social media visual," "data art," or "engaging"
- Content is for public consumption, social sharing, newsletters, or blog posts
- The goal is to make data visually memorable, not just readable
- User wants something that looks like a professional data journalism piece

**When to keep enterprise style instead:**
- Board presentations, regulatory filings, internal memos
- User says "clean," "professional," "J.P. Morgan style," "restrained," "for print"
- Content goes into Word docs, PDFs, or formal PowerPoint decks

### The Visual Capitalist Aesthetic

The opposite of enterprise restraint — this style makes data **the spectacle**. Key DNA:

1. **Dark backgrounds dominate.** Deep navy (#0a0e27), near-black (#111827), or rich dark teal (#0c2340). This creates drama and makes colors pop. Alternatively, warm cream/beige (#f5f0e8) for a lighter editorial feel.

2. **Bold, oversized typography.** Titles in ALL CAPS, heavyweight sans-serif. Hero numbers displayed HUGE ($4.8T, 90.8%, 152). Typography IS the design — not decoration on top of design.

3. **Saturated accent colors.** Use 4-6 vibrant colors, not the 2-3 muted tones of enterprise. Teal (#00d4aa), electric blue (#3b82f6), warm amber (#f59e0b), vivid red (#ef4444), purple (#8b5cf6), lime green (#84cc16). Colors should be sector/category-coded.

4. **Data as physical metaphor.** Don't just chart the data — embody it. Values become proportional shapes (hexagons, rectangles, circles, pyramids). The visual shape itself communicates the story before you read any text.

5. **Logos, flags, and icons as visual anchors.** Instead of just text labels, reference real-world brand logos, country flags, or category icons to make the graphic immediately scannable.

6. **Source attribution and branding.** Always include a source line at the bottom ("Source: [name]") and a subtle creator/brand mark.

### Prompt Construction for Visual Capitalist Style

Build every editorial infographic prompt in this order:

1. **Background and mood first.** Start with: "On a deep dark navy background (#0a0e27), create a bold, visually striking infographic..."

2. **Title treatment.** "Title in large ALL CAPS white text: '[TITLE]'. Year or date badge in top-right corner."

3. **Layout metaphor.** Describe the specific visualization type (treemap, pyramid, flow diagram, bubble chart, etc.) and how data maps to visual properties (size, color, position).

4. **Data elements.** Specify exact values, labels, and categories with their assigned colors.

5. **Style anchor.** End with this block:

```
Style: Bold editorial data visualization in the style of Visual Capitalist
or Statista infographics. Dark background with vibrant, saturated colors.
Large bold sans-serif typography — title in ALL CAPS white. Hero numbers
displayed prominently. Data encoded as proportional shapes (not just charts).
Clean but dramatic — professional data journalism, not decorative clip art.
Include a thin source attribution line at the bottom.
```

### Editorial Infographic Templates

#### 6. Treemap / Proportional Grid (best for: market cap rankings, budget breakdowns, sector composition)

Visual Capitalist's signature — proportional rectangles sized by value, color-coded by category, with entity names and values inside each cell.

```
On a deep dark navy background (#0a0e27), create a bold proportional treemap
infographic titled "[TITLE]" in large ALL CAPS white text.

Layout: A grid of rectangles where each rectangle's area is proportional
to its value. Rectangles are packed tightly with thin dark borders between them.

Color-code by category:
- [Category 1]: teal (#00d4aa) — [Entity: $Value], [Entity: $Value]...
- [Category 2]: blue (#3b82f6) — [Entity: $Value], [Entity: $Value]...
- [Category 3]: amber (#f59e0b) — [Entity: $Value]...
- [Category 4]: purple (#8b5cf6) — [Entity: $Value]...

Inside each rectangle: entity name in bold white text, value below in
slightly smaller white text. Largest entities get the largest rectangles.

Category labels run vertically along the right edge of each color section.
Bottom: source line in small gray text.

Style: Bold editorial data visualization like Visual Capitalist. Dark background,
vibrant saturated sector colors, proportional rectangles, clean bold typography.
```

#### 7. Pyramid / Histogram Tower (best for: distribution of returns, frequency by range, historical data by bucket)

Color-gradient horizontal bars stacked in a pyramid shape — widest at the most common range, narrowing at extremes.

```
On a deep dark background (#111827), create a bold pyramid chart infographic
titled "[TITLE]" in large ALL CAPS white text at the top-left.

Layout: Horizontal bars stacked vertically, centered, forming a pyramid
shape. Each bar represents a range bucket. The widest bars are in the
middle (most common range), narrowing toward top (high extremes) and
bottom (low extremes). Each bar is divided into cells, one per data point.

Color gradient from top to bottom:
- Top rows (highest values): bright green (#22c55e)
- Upper-middle rows: teal (#14b8a6)
- Middle rows: cyan (#06b6d4)
- Lower-middle rows: amber (#f59e0b) to orange (#f97316)
- Bottom rows (lowest/negative values): red (#ef4444) to deep red (#991b1b)

Inside each cell: the year or label in bold text (white or dark depending
on background color for contrast).

X-axis at bottom showing the range scale (e.g., -50% to +50%).
Optional callout quote in the left margin area.

Style: Bold data visualization like Visual Capitalist's S&P 500 returns pyramid.
Dark background, vibrant color gradient, each cell clearly labeled.
```

#### 8. Sankey / Alluvial Flow (best for: trade flows, money flows, migration, supply chains)

Flow lines connecting origins to destinations, with width proportional to volume.

```
On a warm cream background (#f5f0e8), create a professional Sankey flow
diagram infographic titled "[TITLE]" in large dark text.

Layout: Left column shows origins with [flag/icon] and percentage labels.
Right column shows destinations with [flag/icon] and percentage labels.
Curved flow bands connect left to right, with bandwidth proportional to
flow volume. Flows pass through a central channel or bottleneck.

Origins (left side):
- [Entity 1]: [X]% — [color 1]
- [Entity 2]: [X]% — [color 2]
...

Destinations (right side):
- [Entity A]: [X]% — [color A]
- [Entity B]: [X]% — [color B]
...

Center: Total flow value displayed prominently (e.g., "Total: 14.2 mb/d").
Each flow band uses the origin's color with slight transparency.

Annotation boxes with brief context (1-2 sentences max).
Bottom: source attribution line.

Style: Warm editorial Sankey diagram like Visual Capitalist. Cream or light
tan background, proportional flow widths, small flag icons next to country names,
clean serif or sans-serif typography.
```

#### 9. Hexagonal Tile Grid (best for: brand rankings, entity comparisons with logos, top-N lists)

Honeycomb layout where each hexagon represents an entity, sized by value, with logo and metric inside.

```
On a deep dark navy background (#0a0e27), create a bold hexagonal tile
infographic titled "[TITLE]" in large ALL CAPS white text.

Layout: Honeycomb grid of hexagons. Each hexagon represents one entity.
Hexagon SIZE is proportional to value. Color-coded by region or category.

Hexagons (largest to smallest):
- [Entity 1]: $[Value] — large hex, [color 1] (#00d4aa)
- [Entity 2]: $[Value] — large hex, [color 1]
- [Entity 3]: $[Value] — medium hex, [color 2] (#3b82f6)
...

Inside each hexagon: rank number (small, top), entity name (bold, center),
value (below name).

Color legend:
- [Category 1]: teal
- [Category 2]: blue
- [Category 3]: red/coral for different region

Style: Bold hexagonal data visualization like Visual Capitalist's brand
rankings. Dark background, vibrant hex colors, clean white text inside each tile.
```

#### 10. Choropleth / Heat Map (best for: geographic data, state/country comparisons, regional metrics)

Map with gradient fill coloring by value, with labels on each region.

```
On a clean light background (#f8f9fa), create a choropleth map infographic
titled "[TITLE]" in large bold dark text.

Layout: [Map type — US states / World / Europe / etc.] with each region
colored on a gradient scale from [light color] (low values) to [dark color]
(high values).

Gradient scale:
- Low: light pink (#fce7f3) or light blue (#dbeafe)
- Medium: medium (#f472b6) or (#60a5fa)
- High: dark (#be185d) or (#1d4ed8)

Labels: Show the primary metric value on or next to each region.
A horizontal gradient legend bar at the top shows the scale range
(e.g., "$320K ←→ $485K").

Callout: "National Average: [value]" in a subtle badge.
Bottom: source line.

Style: Clean editorial choropleth like Visual Capitalist's mapped series.
Light background, clear gradient progression, readable value labels on
each region. Professional data journalism aesthetic.
```

#### 11. Bubble / Circle Pack (best for: proportional comparisons, entity sizes, market share)

Proportional circles arranged by size, with flag/logo icons and labels.

```
On a dark gradient background (deep purple #1e1b4b to navy #0f172a),
create a bold bubble chart infographic titled "[TITLE]" in large ALL CAPS
white text.

Layout: Circles arranged with largest in center/prominent position,
smaller circles surrounding it. Each circle's AREA is proportional to
its value.

Circles:
- [Entity 1]: [Value] — largest circle, [color 1]
- [Entity 2]: [Value] — second largest, [color 2]
- [Entity 3]: [Value] — medium, [color 3]
...

Inside each circle: [flag icon or emoji], entity name in bold white,
value below. Smallest circles may show just the name and value.

Style: Bold proportional bubble visualization like Visual Capitalist.
Dark gradient background, vibrant saturated circle colors, clean white
typography inside each bubble. Professional data journalism.
```

#### 12. Horizontal Bar Race / Ranking (best for: country rankings, metric comparisons with flags)

Horizontal bars with flag icons, sorted by value, with dual-metric columns.

```
On a deep dark background (#111827), create a bold horizontal bar ranking
infographic titled "[TITLE]" in large ALL CAPS white text. Subtitle or
date range below in smaller gray text.

Layout: Horizontal bars sorted from longest (top) to shortest (bottom).
Each bar has:
- [Flag icon/emoji] and entity name (left-aligned, white text)
- Colored bar extending rightward, length proportional to value
- Value label at the end of the bar

Optional: Two metric columns (left column: primary metric with bars,
right column: secondary metric as text values).

Bars colored by category or on a gradient:
- Top performers: green (#22c55e) or teal (#14b8a6)
- Middle: blue (#3b82f6) or amber (#f59e0b)
- Bottom: orange (#f97316) or gray (#6b7280)

Style: Bold editorial bar ranking like Visual Capitalist's "Ranked" series.
Dark background, vibrant bar colors, flag icons, clean bold white typography.
```

#### 13. Stacked Bar Comparison (best for: debt composition, revenue breakdown, portfolio allocation)

Horizontal stacked bars showing component breakdown for each entity.

```
On a deep dark background (#0a0e27), create a bold stacked bar comparison
infographic titled "[TITLE]" in large ALL CAPS white text.

Layout: Each row is one entity. The full bar represents 100% (or total value).
Segments within each bar are color-coded by component.

Components (color legend at top):
- [Component A]: red (#ef4444)
- [Component B]: orange (#f97316)
- [Component C]: amber (#f59e0b)

Entities (top to bottom):
- [Entity 1]: [A]% + [B]% + [C]% = [Total]%
- [Entity 2]: [A]% + [B]% + [C]% = [Total]%
...

Entity names and flags on the left. Total value on the right of each bar.
Percentage labels inside each segment if wide enough.

Style: Bold editorial stacked bar chart like Visual Capitalist's debt burden
visualizations. Dark background, warm red-to-amber color scheme, clean
white labels.
```

#### 14. Scale / "How Massive Is X" Comparison (best for: putting large numbers in context, entity vs. benchmark)

Shows one entity compared to others for dramatic scale context.

```
On a dark background (#111827) with subtle [green/blue/teal] accent color,
create a bold scale comparison infographic titled "How [Massive/Large] Is
[ENTITY]" in large ALL CAPS white text.

Layout: Central hero metric displayed HUGE: "$[X.X]T" or "[X]B" in the
entity's brand color. Entity name in bold below.

Surrounding the hero: comparison entities arranged in a descending arc or
column, each showing:
- [Flag/icon] [Name]: $[Value]

Callout text: "[Entity]'s valuation would rank it as the world's
[Nth]-largest [economy/company/etc.]"

Style: Bold dramatic scale comparison like Visual Capitalist. Dark background,
one dominant accent color for the hero entity, comparison values in white text.
The hero number should be the visual centerpiece — 3-5x larger than any
other text on the graphic.
```

#### 15. Timeline / Growth Arc (best for: historical growth, investment returns over time, milestone tracking)

Multi-colored lines or area fills showing growth trajectories with icon legends.

```
On a clean light background (#fafafa), create an editorial growth chart
infographic titled "[TITLE]" in large bold dark text. Subtitle: "[context]".

TOP ROW: Icon legend — small colored circles with labels for each series:
- [Series 1]: [color 1] (#ef4444)
- [Series 2]: [color 2] (#f59e0b)
- [Series 3]: [color 3] (#3b82f6)
...

MAIN AREA: Line chart or area chart showing growth of each series over
the time period. Lines should be thick (3-4px) and clearly distinguishable.
Key inflection points labeled with year and value.

Starting point anchored at left (e.g., "$100 invested in [YEAR]").
Ending values labeled at right terminus of each line.

X-axis: years. Y-axis: values (log scale if range is very large).

Style: Clean editorial growth visualization like Visual Capitalist's
asset class returns. Light background, vibrant distinct line colors,
icon legend row, clean axis labels. Professional data journalism.
```

### Combining Styles — Hybrid Approach

For maximum impact, you can combine enterprise clarity with editorial drama:

- **Dark bg + restrained data**: Use a dark background but keep the data presentation clean and uncluttered. Good for executive dashboards that need to look impressive on screens.
- **Light bg + bold typography**: Keep the white/cream background but use Visual Capitalist's bold ALL CAPS titles and hero numbers. Good for reports that need to feel modern but remain printable.
- **Data section + context section**: Use a bold editorial chart as the main visual, with a clean enterprise-style "Key Takeaways" bullet section below it.

### Aspect Ratio Guide for Editorial Infographics

- `9:16` or `3:4` — **Vertical / social-first**: Best for tall infographics (treemaps, rankings, timelines). Instagram stories, LinkedIn posts.
- `16:9` — **Widescreen / presentation**: Best for flow diagrams, comparison bars, scale visuals. Slides and blog headers.
- `1:1` — **Square / social tile**: Best for single-stat callouts, bubble charts, hex grids. Instagram posts, dashboard tiles.
- `4:5` — **Near-square portrait**: Best for choropleth maps and multi-section infographics. Facebook, presentation inserts.



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
