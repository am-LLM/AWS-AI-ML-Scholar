Project: Customer Support Chatbot with Amazon Bedrock Flows
Student: Ali Malik

1. Overview
In this project, I built a multi-path customer support workflow using Amazon Bedrock Flows. The application classifies incoming user messages and directs them to the right path:
- Bug Reports (Category A): Routes to an AWS Lambda function tool (create-bug-report) which saves the ticket description, reproduction steps, and user environment directly into the DynamoDB table (BugReports).
- Platform Questions (Category B): Answers user questions about shipping, returns, order cancellations, and payments using the provided online shop FAQ. If a question is not covered by the FAQ, it provides the phone support number (1-800-555-0199).
- Other Inquiries (Category C): Handles general inquiries or escalation requests by referring the customer to phone support (1-800-555-0199).

2. Flow Design and Prompts
- Classifier Node: Uses Amazon Nova Lite (amazon.nova-lite-v1:0). The prompt instructs the model to return only 'A', 'B', or 'C' so the condition node can reliably route the traffic.
- Condition Node: Uses Boolean expressions:
  - conditionInput == "A" -> routes to LambdaFunctionNode_1
  - conditionInput == "B" -> routes to FAQ_Prompt (Prompt_2)
  - Default fallback -> routes to Other_Prompt (Prompt_1)
- Prompt Nodes: The FAQ prompt embeds the store policies from online_shop_faq.md and gives clear instructions to only answer covered questions and escalate uncovered ones.

3. Testing and Evaluation
- I set up test cases in flow-tests.json covering all three paths (bug reports, covered FAQs, uncovered FAQs, and other general messages).
- Ran generate-eval-dataset.py to invoke the flow programmatically and generated the test output file eval-dataset.jsonl.
- Verified test prompts directly in the Bedrock Flow Test interface. The classifier correctly routed queries and returned accurate answers based on the store policies.

4. Screenshots Included
- flowdiagram.png: Complete Bedrock flow diagram showing all nodes, connections, and saved state.
- classifiercondition.png: Configuration panel showing the Condition node expressions and classifier prompt.
- lambdabinding.png: Lambda console showing create-bug-report function configuration.
- dynamodbrecord.png: DynamoDB table showing a bug report ticket created by the application.
- evalresults.png: Bedrock Flow test trace showing a live prompt execution and node completion steps.
