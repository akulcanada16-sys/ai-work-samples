# Data dictionary sample

This is an **AI-produced fictional demonstration**, not client work. It uses one fictional order-export table and the facts in the fictional brief below. No real records, customer meanings, tax conclusions, refund conclusions, or business guarantees are represented.

## Fictional brief

The export contains these fields: `order_id`, `ordered_on`, `customer_ref`, `currency`, `item_subtotal_minor`, `shipping_minor`, `total_minor`, `status`, and `source_ref`.

- IDs are opaque strings.
- `ordered_on` is the store’s local calendar date in ISO `YYYY-MM-DD` form; the store timezone is unknown and must be confirmed.
- Money values are nonnegative integer minor units. Currency is CAD. `total_minor = item_subtotal_minor + shipping_minor`.
- `status` is one of `new`, `processing`, `shipped`, or `cancelled`.
- The export schema includes eight required columns: `order_id`, `ordered_on`, `currency`, `item_subtotal_minor`, `shipping_minor`, `total_minor`, `status`, and `customer_ref`. All required fields are present; required non-null string fields are non-empty.
- `customer_ref` is present but may contain a non-empty string or JSON `null`; it cannot be an empty string.
- `source_ref` is optional: it may be absent, or present with an empty or non-empty string; it cannot be JSON `null`.

| Field | Type | Required | Nullable | Example | Meaning |
|---|---|---:|---:|---|---|
| `order_id` | string | yes | no | `ord_7K2mQ9` | Opaque order identifier |
| `ordered_on` | string (`YYYY-MM-DD`) | yes | no | `2026-09-16` | Store-local order date |
| `customer_ref` | string | yes | yes | `cust_A19x` | Opaque customer reference, or `null` |
| `currency` | string | yes | no | `CAD` | Currency code |
| `item_subtotal_minor` | integer | yes | no | `4599` | Item subtotal in minor units |
| `shipping_minor` | integer | yes | no | `800` | Shipping in minor units |
| `total_minor` | integer | yes | no | `5399` | Subtotal plus shipping in minor units |
| `status` | string | yes | no | `processing` | Order lifecycle status |
| `source_ref` | string | no | no | `src_20260916_0042` | Optional source reference; may be blank |

Example row: `{"order_id":"ord_7K2mQ9","ordered_on":"2026-09-16","customer_ref":"cust_A19x","currency":"CAD","item_subtotal_minor":4599,"shipping_minor":800,"total_minor":5399,"status":"processing","source_ref":"src_20260916_0042"}`

The structured dictionary is in [`dictionary.json`](./dictionary.json). “Required” describes whether the column must be present in the export schema; “nullable” describes whether its value may be JSON `null`; an empty string is a present string value and is separate from both a missing field and `null`.

## Draft offer

CAD100 for one table, up to 20 fields. The customer supplies the schema, field definitions, and sanitized examples. Deliverables are a Markdown summary and JSON dictionary, with one revision, within 2 business days after the brief is agreed. Produced and checked with AI tools; this demonstration is fictional. No past client work is claimed.

## Open questions

- What timezone defines the store’s local calendar date for `ordered_on`?
- Are cancelled orders included in any revenue reporting, or excluded by a separate business rule?
