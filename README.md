# strike-ai

Python client for the [Strike](https://strike-ai.eu) API. You send content and typed questions. You get one answer per question, with probabilities.

```bash
pip install strike-ai
```

```python
import os
from strike_ai import Client

client = Client(api_key=os.environ["STRIKE_API_KEY"])
result = client.decide(
    "My card was charged twice for the same order. Please fix this today.",
    {
        "is_urgent": {
            "type": "noul",
            "instructions": "Does the customer express time pressure?",
        },
        "team": {
            "type": "choice",
            "instructions": "Which team should handle this message?",
            "criteria": {
                "billing": "Payments, refunds, invoices",
                "technical": "Bugs, outages, integrations",
                "other": None,
            },
        },
    },
)
```

`STRIKE_API_URL` overrides the default base URL, `https://strike-ai.eu`.

Strike is in beta. `strike-1` returns real model probabilities. They are not calibrated for production routing yet.

This repository is the public client. Model weights, training, and the API server are not in it.

## Endpoint

`POST https://strike-ai.eu/v1/systemone`

| Type | You ask | You get |
| --- | --- | --- |
| `noul` | A yes/no question | A value from 0 (no) to 1 (yes) |
| `choice` | One option from a set you define | The top option and a probability for every option |
| `score` | A rating on levels you define | A probability-weighted score and a probability per level |

The same call with curl:

```bash
curl https://strike-ai.eu/v1/systemone \
  -H "Authorization: Bearer $STRIKE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "strike-1",
    "state": "My card was charged twice for the same order. Please fix this today.",
    "questions": {
      "is_urgent": {
        "type": "noul",
        "instructions": "Does the customer express time pressure?"
      },
      "team": {
        "type": "choice",
        "instructions": "Which team should handle this message?",
        "criteria": {
          "billing": "Payments, refunds, invoices",
          "technical": "Bugs, outages, integrations",
          "other": null
        }
      }
    }
  }'
```

Docs: [strike-ai.eu/docs](https://strike-ai.eu/docs). Contact: [hello@strike-ai.eu](mailto:hello@strike-ai.eu).

Strike is not affiliated with TypeSafe. The hosted API speaks a System One-compatible wire format.
