import json
import boto3
import argparse
import sys
import os

# script to generate eval dataset from flow tests

def main():
    parser = argparse.ArgumentParser(description="run flow tests and make jsonl for evaluation")
    parser.add_argument('--tests-json', default="flow-tests.json", help="path to test cases json file")
    parser.add_argument('--flow-id', required=True, help="bedrock flow identifier")
    parser.add_argument('--flow-alias-id', default="TSTALIASID", help="flow alias id")
    parser.add_argument('--out-jsonl', default="eval-dataset.jsonl", help="output file path")
    parser.add_argument('--region', default="us-east-1", help="aws region")
    
    args = parser.parse_args()

    # load the tests file
    if not os.path.exists(args.tests_json):
        print("Error: Cant find tests file:", args.tests_json)
        sys.exit(1)

    print("Opening test file:", args.tests_json)
    with open(args.tests_json, 'r') as f:
        data = json.load(f)

    # get tests list
    test_cases = data.get('tests', [])
    print(f"Found {len(test_cases)} tests to run.")

    # connect to bedrock agent runtime client
    client = boto3.client('bedrock-agent-runtime', region_name=args.region)

    out_records = []

    for i, test in enumerate(test_cases):
        test_id = test.get('id', f'test_{i+1}')
        prompt = test.get('prompt', '')
        expected = test.get('expected', '')

        print(f"[{i+1}/{len(test_cases)}] Running: {test_id} ...")
        
        flow_response_text = ""

        try:
            # call invoke flow
            response = client.invoke_flow(
                flowIdentifier=args.flow_id,
                flowAliasIdentifier=args.flow_alias_id,
                inputs=[
                    {
                        "nodeName": "FlowInputNode",
                        "nodeOutputName": "document",
                        "content": {
                            "document": prompt
                        }
                    }
                ]
            )

            # process the streaming response
            for event in response.get('responseStream', []):
                if 'flowOutputEvent' in event:
                    out_content = event['flowOutputEvent'].get('content', {})
                    flow_response_text = out_content.get('document', '')
                    print("  Got output from flow:", flow_response_text[:40], "...")
                    break
        except Exception as e:
            print(f"  Failed to invoke flow for {test_id}: {e}")
            flow_response_text = f"Error: {e}"

        # create byoi record
        record = {
            "prompt": prompt,
            "referenceResponse": expected,
            "modelResponses": [
                {
                    "response": flow_response_text,
                    "modelIdentifier": "my-flow-app"
                }
            ]
        }
        out_records.append(record)

    # write to jsonl output
    print("Writing records to:", args.out_jsonl)
    with open(args.out_jsonl, 'w') as f_out:
        for r in out_records:
            f_out.write(json.dumps(r) + "\n")

    print("Done generating evaluation dataset!")

if __name__ == "__main__":
    main()
