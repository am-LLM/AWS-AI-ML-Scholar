Project: Customer Support Chatbot with Amazon Bedrock Flows
Student: Ali Malik

1. Overview
In this project, I built a multi-path customer support workflow using Amazon Bedrock Flows. The application classifies incoming user messages and directs them to the right path:
- Bug Reports (Category A): Routes to an AWS Lambda function tool (create-bug-report) which saves the ticket description, reproduction steps, and user environment directly into the DynamoDB table (BugReports).
- Platform Questions (Category B): Answers user questions about shipping, returns, order cancellations, and payments using the provided online shop FAQ. If a question is not covered by the FAQ, it provides the phone support number (1-800-555-0199).
- Other Inquiries (Category C): Handles general inquiries or escalation requests by referring the customer to phone support (1-800-555-0199).

2. Flow Design and Prompts
- Classifier Node (Classifier_Prompt): Uses Amazon Nova Lite (amazon.nova-lite-v1:0). The prompt instructs the model to return strictly single-character labels ('A', 'B', or 'C') so the condition node can reliably route the traffic without parse errors.
- Condition Node (ConditionNode_1): Evaluates Boolean routing expressions:
  - conditionInput == "A" -> routes to LambdaFunctionNode_1
  - conditionInput == "B" -> routes to FAQ_Prompt
  - Default fallback -> routes to Other_Request_Prompt
- FAQ Prompt Node (FAQ_Prompt): Embeds the store policies from the FAQ document and gives clear instructions to answer covered questions accurately and escalate uncovered questions to the support phone line (1-800-555-0199).
- Other Requests Node (Other_Request_Prompt): Directs general inquiries, legal questions, and human escalation requests directly to support phone (1-800-555-0199).
- Lambda Node (LambdaFunctionNode_1): Integrates with the CloudFormation-deployed Lambda tool to parse ticket metadata and write items to DynamoDB.

3. Testing and Evaluation Observations
- Test Suite Design: Defined test cases in flow-tests.json covering all four operational scenarios: bug report submissions, covered FAQ inquiries, uncovered FAQ inquiries, and other general requests.
- Dataset Generation: Executed generate-eval-dataset.py to run all test prompts through the Bedrock Flow API and generate eval-dataset.jsonl containing inputs, flow outputs, and reference ground truth.
- Bedrock Model Evaluation:
  - Uploaded the JSONL dataset to S3 and configured an automated Bedrock Model Evaluation job using LLM-as-a-judge.
  - Evaluation Results: Achieved a Correctness Score of 1.0 across the test dataset.
  - Written Observations:
    * The Amazon Nova Lite classifier achieved 100% precision in category discrimination (A, B, C), producing clean single-token responses with zero extraneous conversational text, which prevented any routing failures at ConditionNode_1.
    * For covered platform questions (e.g. return policy and order cancellation windows), the FAQ prompt generated exact, policy-compliant answers directly matching reference criteria.
    * For uncovered platform questions (e.g. international shipping to unsupported regions) and other requests, the flow consistently provided the designated support phone number (1-800-555-0199) as required by the rubric.
    * For bug reports, the Lambda tool successfully parsed bug parameters and wrote valid ticket records with unique IDs into the BugReports DynamoDB table.

4. Screenshots Included
- flowdiagram.png: Full Bedrock flow diagram showing all connected nodes (Input, Classifier, Condition, Prompts, Lambda, and Outputs).
- classifierprompt.png: Configuration panel of Classifier_Prompt showing the prompt instructions and Amazon Nova Lite model.
- classifiercondition.png: Configuration panel of ConditionNode_1 showing the routing expressions (conditionInput == "A", conditionInput == "B").
- lambdabinding.png: Configuration panel of LambdaFunctionNode_1 showing the Lambda function tool integration.
- faqprompttemplate.png: Configuration panel of FAQ_Prompt showing the prompt template with embedded store FAQ policies.
- testflowbugreport.png: Flow Test console chat response for submitting a bug report.
- testflowcoveredfaq.png: Flow Test console chat response for a covered FAQ question.
- testflowuncoveredfaq.png: Flow Test console chat response for an uncovered FAQ question directing to phone support.
- testflowotherrequest.png: Flow Test console chat response for an other-request message directing to phone support.
- dynamodbrecord.png: DynamoDB BugReports table in AWS Console Item Explorer showing the created bug ticket item.
- evalresults.png: Bedrock Model Evaluation job results page displaying the completed job and correctness evaluation scores.
