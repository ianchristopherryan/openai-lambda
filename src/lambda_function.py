import json
import openai
import boto3
import os

dynamodb = boto3.client('dynamodb')

def lambda_handler(event, context):
    # Retrieve the prompt key and input from the user's request
    function_name = event['functionName']
    user_input = event['input']
    
    # Retrieve the stored prompt from DynamoDB
    stored_prompt = dynamodb.get_item(
        TableName='openai_prompt_library',
        Key={
            'functionName': {
                'S': function_name
            }
        }
    )['Item']['prompt']['S']
    
    # Insert the user input into the prompt
    if not user_input:
        chat_input = stored_prompt
    else:
        chat_input = stored_prompt.format(input=user_input)
    
    
    openai.api_key = os.environ.get('openai_api_key')
    
    # Call the ChatGPT API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", 
        messages=[
            {"role": "system", "content": "You only respond with the answer, no additional dialog"},
            {"role": "user", "content": chat_input}
        ]
    )
    
    # Format and return the response
    chat_output = response['choices'][0]['message']['content']
    
    return chat_output
