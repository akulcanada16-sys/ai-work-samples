# Branching learning storyboard: Read the chart, avoid the leap

**Format:** 8-screen microlearning storyboard · **Topic:** reading a fictional library-visits chart · **Audience:** beginning chart readers · **Source visual:** [fictional library-visits chart](../alt-text/library-visits-chart.svg) — April 120, May 180, June 150, July 240 visits.

> **Portfolio provenance:** This original, AI-created sample uses fictional data to demonstrate storyboard planning. It specifies a course for review and development; learner outcomes have not been tested.

## Learning objectives

By the end, a learner can:

1. Read and compare the displayed monthly visit totals.
2. Separate an observation supported by the chart from an unsupported claim about *why* visits changed.

## Branch map

```text
1 Start → 2 Read the chart → 3 Check 1
                              ├─ correct → 5 Check 2 → 6 Check 3 → 7 Check 4 → 8 Finish
                              └─ incorrect → 4 Compare again → 5 Check 2 → 6 Check 3 → 7 Check 4 → 8 Finish
```

Only Check 1 creates the short remedial branch. Checks 2–4 give answer-specific feedback in place, then continue to the next numbered screen.

## Global build conventions

- On every question screen, keep an expandable **Chart reference** control available. It contains the chart, its concise alternative, and the same HTML data table from Screen 2.
- Question screens share one layout: prompt, vertically stacked answer buttons, then a reserved feedback area. No answer is selected by default.
- Selecting a choice reveals its answer-specific feedback but **never** advances the learner. An explicit **Continue** or **Next** button follows the branch map.
- For each check, narration reads the prompt and options, then reads the selected feedback. The visual, interaction, and accessibility directions below inherit these conventions unless they add a specific requirement.
- Narration is optional, with labelled play/pause controls and matching on-screen text. Do not autoplay it over a screen reader.

---

## Screen 1 — Start with what the chart shows

**On-screen text**

> **Read the chart, avoid the leap**  
> A chart can show a pattern. It cannot automatically explain the reason for that pattern.

**Narration**  
“First, read the numbers. Then ask whether the chart actually supports the conclusion you want to draw.”

**Visual / layout direction**  
Clean title card: navy heading, teal rule, and four small bars rising left to right. Add a discreet “Short practice” label.

**Interaction / navigation**  
Continue button leads to Screen 2.

**Accessibility notes**  
Use a heading followed by a real button. The decorative mini-bars are hidden from assistive technology.

---

## Screen 2 — Read the evidence

**On-screen text**

> **Fictional library visits**  
> April 120 · May 180 · June 150 · July 240

Display the linked chart with a nearby data table:

| Month | Visits |
| --- | ---: |
| April | 120 |
| May | 180 |
| June | 150 |
| July | 240 |

**Narration**  
“The chart reports visit totals for four months. July has the largest displayed total.”

**Visual / layout direction**  
Two-column desktop layout: chart on the left, table on the right. On narrow screens, place the table immediately below the chart.

**Interaction / navigation**  
“Try a quick check” leads to Screen 3.

**Accessibility notes**  
Provide the table in HTML, not only inside the SVG. Give the chart a concise alternative: “Fictional library visits by month; data table follows.”

---

## Screen 3 — Check 1: find the highest total

**Prompt**  
Which month has the highest number of visits?

**Choices**  
A. April  
B. May  
C. June  
D. July

**Narration**  
“Which month has the highest number of visits? Choose April, May, June, or July.” After selection, read the feedback shown for that answer.

**Answer-specific feedback and branch**

| Learner choice | Feedback | Next |
| --- | --- | --- |
| **D. July** | **Correct.** July shows 240 visits, more than April (120), May (180), or June (150). | Screen 5 |
| A, B, or C | **Not yet.** Compare all four displayed totals; the highest bar and largest table value are 240. | Screen 4 |

**Visual / layout direction**  
One question per view, with four large keyboard-focusable answer buttons.

**Accessibility notes**  
Announce feedback in a polite live region after selection. Keep the selected answer visibly marked as well as described in text.

---

## Screen 4 — Remedial branch: compare every value

**On-screen text**

> **Compare before choosing**  
> 120, 180, 150, **240**  
> The largest displayed total is **240 in July**.

**Narration**  
“Reading the values in order makes the comparison clear: 240 is the largest number.”

**Visual / layout direction**  
A simple horizontal number line with 240 emphasized; no new data.

**Interaction / navigation**  
“Continue” leads to Screen 5. This is the single remedial branch; the learner does not need to repeat the earlier question.

**Accessibility notes**  
Use text and number emphasis, not colour alone. Preserve the same table values from Screen 2.

---

## Screen 5 — Check 2: calculate a comparison

**Prompt**  
How many more visits did July have than April?

**Choices**  
A. 60  
B. 90  
C. 120  
D. 240

**Narration**  
“How many more visits did July have than April? Choose 60, 90, 120, or 240.” After selection, read the feedback shown for that answer.

**Answer-specific feedback**

| Learner choice | Feedback |
| --- | --- |
| **C. 120** | **Correct.** 240 − 120 = 120 more visits. |
| A. 60 | **Not quite.** 60 is the difference between May (180) and April (120). For July versus April, subtract 120 from 240. |
| B. 90 | **Not quite.** 90 is the difference between July (240) and June (150). This question compares July with April: 240 − 120. |
| D. 240 | **Not quite.** 240 is July’s total. A comparison asks for the difference: 240 − 120. |

**Interaction / navigation**  
After feedback, “Next” leads to Screen 6.

**Accessibility notes**  
Present subtraction in text as well as visually. Do not require drag-and-drop or timed input.

---

## Screen 6 — Check 3: state only what the chart supports

**Prompt**  
Which statement is supported by the chart?

**Choices**  
A. July had more visits than June.  
B. A summer program caused July’s increase.  
C. People enjoyed July’s books more.  
D. Rain in June reduced visits.

**Narration**  
“Which statement is supported by the chart? Choose the one statement the displayed totals can establish.” Read choices A–D verbatim next. After selection, read the feedback shown for that answer.

**Answer-specific feedback**

| Learner choice | Feedback |
| --- | --- |
| **A. July had more visits than June.** | **Correct.** The chart displays 240 visits in July and 150 in June. |
| B | **Unsupported.** The chart shows that July is higher; it does not show what caused the change. |
| C | **Unsupported.** Enjoyment is not measured by these visit totals. |
| D | **Unsupported.** The chart includes no weather information. |

**Interaction / navigation**  
After feedback, “Next” leads to Screen 7.

**Accessibility notes**  
Write the complete statement in each choice so it can be understood without the chart image.

---

## Screen 7 — Check 4: spot the causal leap

**Prompt**  
Which sentence makes an unsupported causal claim?

**Choices**  
A. July’s total was 240 visits.  
B. July had 60 more visits than May.  
C. The library’s new display caused more people to visit in July.  
D. June’s total was lower than May’s.

**Narration**  
“Which sentence makes an unsupported causal claim? Choose the statement that gives a reason the chart does not establish.” Read choices A–D verbatim next. After selection, read the feedback shown for that answer.

**Answer-specific feedback**

| Learner choice | Feedback |
| --- | --- |
| **C. The library’s new display caused more people to visit in July.** | **Correct.** A cause needs evidence beyond the monthly visit totals. |
| A | **Supported, not causal.** The table gives July as 240. |
| B | **Supported, not causal.** 240 − 180 = 60. |
| D | **Supported, not causal.** June is 150 and May is 180. |

**Interaction / navigation**  
After feedback, “Finish” leads to Screen 8.

**Accessibility notes**  
Make the feedback programmatically associated with the selected answer and keep focus at the feedback heading.

---

## Screen 8 — Finish: read, compare, qualify

**On-screen text**

> **Take these habits with you:**  
> • read and compare the totals shown  
> • state a supported observation  
> • identify when a claim needs more evidence

> **Remember:** “July had the highest total” is supported. “A specific event caused July’s total” needs additional evidence.

**Narration**  
“Use the chart for what it shows, and look for more evidence before explaining why a pattern happened.”

**Visual / layout direction**  
Three short takeaway cards with a simple return-to-start option. No score or completion claim.

**Interaction / navigation**  
“Review chart” returns to Screen 2. “Restart” returns to Screen 1.

**Accessibility notes**  
Make both destination labels explicit. Do not trap keyboard focus or rely on automatic advancement.
