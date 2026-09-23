# RowProof demo script and storyboard

Target duration: 1 minute 45 seconds. Record the local browser window only; do not show private files, unrelated tabs, or personal information.

| Time | On screen | Presenter point |
| --- | --- | --- |
| 0:00–0:15 | RowProof landing screen | Introduce the problem: a CSV can appear fine but break an import or trigger a spreadsheet formula. State that RowProof audits entirely on the device. |
| 0:15–0:35 | Choose **Spreadsheet hazards** | Explain that the samples are deliberate test inputs. Select the `id` column as the unique key. |
| 0:35–0:58 | Findings and preview | Point to the blank/repeated keys, formula prefix, and control character with their row evidence. Show that the preview makes the evidence inspectable. |
| 0:58–1:20 | Choose **Broken import** | Show duplicate headers and the short row. Point out that normalized CSV download is disabled because RowProof will not invent a safe structure. |
| 1:20–1:35 | Choose **Quoted records** | Show that a quoted comma, quoted line break, and final empty quoted field remain a valid two-column file. |
| 1:35–1:45 | Download buttons and privacy note | Mention the JSON audit for a review trail and the safe-only normalized CSV. Close with: “Your CSV never leaves this browser.” |

## Recording checklist

- Start the app locally using the README command.
- Show the audit changing after each sample selection.
- Keep video under three minutes and upload it publicly to YouTube or Vimeo before submission.
- Do not claim that a sample is a customer file or that RowProof found results in a real external dataset.
