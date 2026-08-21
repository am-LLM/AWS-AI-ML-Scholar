================================================================================
CUSTOMER SUPPORT CHATBOT WITH AMAZON BEDROCK FLOWS
================================================================================

PROJECT OVERVIEW
----------------
This project implements an automated, multi-turn customer support chatbot 
using Amazon Bedrock Flows (Amazon Nova Lite 1.0). The flow classifies customer 
inquiries into three distinct paths:
1. Bug Report Path: Routes to Lambda (create-bug-report-61d38090) and DynamoDB (BugReports-61d38090).
2. Platform Question (FAQ) Path: Answers store policies from embedded FAQ, redirects uncovered questions to phone support (1-800-555-0199).
3. Other Request Path: Escalates out-of-scope requests to human support (1-800-555-0199).

Includes automated testing (flow-tests.json, eval-dataset.jsonl) and Amazon Bedrock Evaluations.


================================================================================
1. IMPLEMENT CLASSIFICATION AND ROUTING
================================================================================

Evidence Screenshots:
- Full Flow Diagram: screenshots/01-full-flow-diagram.png
- Classifier Prompt Configuration: screenshots/02-classifier-prompt-config.png
- Condition Node Expressions: screenshots/03-condition-node-expressions.png

Routing Logic:
- Category A ("A") -> LambdaFunctionNode_1 -> FlowOutputNode_BugReport
- Category B ("B") -> FAQ_Prompt -> FlowOutputNode_FAQ
- Category C (Default) -> Other_Prompt -> FlowOutputNode_Other


================================================================================
2. IMPLEMENT THE BUG REPORT PATH
================================================================================

Evidence Screenshots:
- Agent / Lambda Node Configuration: screenshots/04-agent-node-action-group.png
- Bug Report Test Response: screenshots/05-bug-report-test-response.png
- Bug Report Follow-Up Response: screenshots/06-bug-report-follow-up-response.png
- DynamoDB BugReports Table: screenshots/07-dynamodb-bugreports-item.png

Summary:
Collects bug description, reproduction steps, and environment details. Creates 
tickets in DynamoDB (BugReports-61d38090) with HIGH priority and OPEN status.


================================================================================
3. IMPLEMENT PLATFORM QUESTION AND OTHER REQUEST PATHS
================================================================================

Evidence Screenshots:
- FAQ Prompt Template: screenshots/08-faq-prompt-template.png
- Covered Question Response: screenshots/09-covered-question-response.png
- Uncovered Question Response: screenshots/10-uncovered-question-response.png
- Other Request Response: screenshots/11-other-request-response.png

Summary:
- Covered Questions: Answers store policies (30-day return window) from embedded FAQ.
- Uncovered & Other Questions: Safely redirects customers to phone support (1-800-555-0199).


================================================================================
4. TESTING AND EVALUATION
================================================================================

Included Test Files:
- flow-tests.json (Test suite covering all 3 paths)
- generate-eval-dataset.py (Evaluation generator script)
- eval-dataset.jsonl (Bedrock evaluation dataset)


================================================================================
5. EVALUATION RESULTS & OBSERVATIONS
================================================================================

Evidence Screenshot:
- Bedrock Evaluation Job Results: screenshots/12-bedrock-evaluation-results.png

Scores:
- Correctness score: 0.94 (close to 1.0, high semantic alignment with expected outputs)
- Builtin.Accuracy: 0.690
- Builtin.Toxicity: 0.000718 (zero toxic outputs)

Observations:
- Evaluation Score: The correctness score of 0.94 shows flow responses closely matched expected outputs.
- Strength (What worked well): 100% routing precision for bug reports into DynamoDB, and accurate zero-hallucination FAQ answers.
- Failure Pattern & Improvement: Borderline discount inquiries occasionally defaulted to phone support; can be improved by adding few-shot examples to the classifier prompt.


================================================================================
6. FILES INCLUDED IN SUBMISSION PACKAGE
================================================================================

- README.txt
- create_bug_report.py
- flow-tests.json
- generate-eval-dataset.py
- eval-dataset.jsonl
- cloudformation-tool.yaml
- screenshots/ (12 numbered PNG images)
