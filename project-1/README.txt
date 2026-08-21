Project: Customer Support Chatbot with Amazon Bedrock Flows
Student: Ali Malik

1. Overview
In this project, I built a customer support routing workflow in Amazon Bedrock Flows. Incoming customer messages are categorized and sent down three paths:
- Bug Reports: Calls the create-bug-report Lambda function to save the bug details, steps, and system info into the BugReports DynamoDB table.
- Platform Questions: Answers shopping questions (shipping, returns, cancellations) using the FAQ content. If something is not in the FAQ, it gives the support number 1-800-555-0199.
- Other Requests: Handles manager escalations or general questions by giving the 1-800-555-0199 phone number.

2. Flow Design
- Classifier Node: Uses Amazon Nova Lite (amazon.nova-lite-v1:0). The prompt tells it to only return A, B, or C so the condition node can route without breaking.
- Condition Node: Checks the letter output:
  * conditionInput == "A" goes to the Lambda tool node
  * conditionInput == "B" goes to the FAQ prompt
  * fallback goes to the other request prompt
- FAQ Prompt: Contains the online shop FAQ rules. It answers known topics and tells users to call support for anything outside the list.
- Lambda Node: Connected to the Lambda function created by CloudFormation to store tickets in DynamoDB.

3. Testing and Evaluation Observations
- Wrote test cases in flow-tests.json for bug reports, covered questions, uncovered questions, and other inquiries.
- Used generate-eval-dataset.py to run the test cases through the flow and export eval-dataset.jsonl.
- Created and ran a Bedrock Model Evaluation job using LLM-as-a-judge.
- The evaluation scored 1.0 on correctness across the dataset.
- Observations:
  * Nova Lite consistently outputs single characters (A/B/C) with no extra text, so every test message went to the right branch.
  * Covered questions pulled accurate answers directly from the FAQ text.
  * Uncovered questions and general requests correctly returned 1-800-555-0199 as expected.
  * Bug reports created clean records in the DynamoDB table with unique IDs and timestamp data.

4. Screenshots
- flowdiagram.png: Full flow canvas with all connected nodes and endpoints.
- classifierprompt.png: Classifier prompt setup and Nova Lite model selection in the drawer.
- classifiercondition.png: Condition node routing rules for A and B.
- lambdabinding.png: Lambda tool configuration pointing to create-bug-report.
- faqprompttemplate.png: FAQ prompt template containing the store policies text.
- testflowbugreport.png: Chat test submitting a crash report ticket.
- testflowcoveredfaq.png: Testing return policy question with policy answer.
- testflowuncoveredfaq.png: Asking about Antarctica shipping and getting the support phone number.
- testflowotherrequest.png: Manager escalation request routing to the phone number.
- dynamodbrecord.png: DynamoDB table showing the saved bug ticket record.
- evalresults.png: Bedrock Model Evaluation job report showing the completed run and scores.
