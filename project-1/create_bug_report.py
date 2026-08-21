import json
import os
import uuid
from datetime import datetime, timezone
import boto3

table = boto3.resource("dynamodb").Table(os.environ.get("TABLE_NAME", "BugReports-61d38090"))


def lambda_handler(event, context=None):
    print("EVENT:", json.dumps(event, indent=2, default=str))

    description = "General bug report"
    steps = "N/A"
    environment = "Web / Bedrock Flow"

    try:
        if isinstance(event, dict) and "fields" in event and isinstance(event["fields"], list):
            for f in event["fields"]:
                if isinstance(f, dict) and "content" in f:
                    c = f["content"]
                    description = c.get("document") if isinstance(c, dict) else (c.get("text") if isinstance(c, dict) else str(c))
        elif isinstance(event, dict) and "node" in event and "inputs" in event.get("node", {}):
            for inp in event["node"]["inputs"]:
                if isinstance(inp, dict) and inp.get("name") == "codeHookInput":
                    description = str(inp.get("value", description))
        elif isinstance(event, dict) and "parameters" in event:
            for p in event.get("parameters") or []:
                if isinstance(p, dict):
                    name = p.get("name")
                    if name == "description":
                        description = p.get("value", description)
                    elif name == "stepsToReproduce":
                        steps = p.get("value", steps)
                    elif name == "environment":
                        environment = p.get("value", environment)
        elif isinstance(event, str):
            description = event
    except Exception as e:
        description = str(event)[:500]

    ticket_id = str(uuid.uuid4())
    item = {
        "ticketId": ticket_id,
        "description": str(description)[:500],
        "stepsToReproduce": str(steps)[:500],
        "environment": str(environment)[:200],
        "priority": "HIGH",
        "source": "BedrockFlow",
        "status": "OPEN",
        "createdAt": datetime.now(timezone.utc).isoformat(),
    }

    try:
        table.put_item(Item=item)
    except Exception as e:
        print("DynamoDB error:", e)

    msg = f"Thank you for reporting this issue. A support ticket has been created with Ticket ID: {ticket_id}. Our engineering team is investigating with priority HIGH and status OPEN."

    # Check if caller was Bedrock Agent Action Group
    if isinstance(event, dict) and "actionGroup" in event:
        return {
            "messageVersion": "1.0",
            "response": {
                "actionGroup": event.get("actionGroup"),
                "function": event.get("function"),
                "functionResponse": {
                    "responseBody": {
                        "TEXT": {
                            "body": json.dumps({"ticketId": ticket_id, "status": "OPEN", "message": msg})
                        }
                    }
                },
            },
        }

    # Caller is Bedrock Flow Lambda Node
    return {
        "functionResponse": msg,
        "response": msg,
        "document": msg,
        "ticketId": ticket_id
    }
