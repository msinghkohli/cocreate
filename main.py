#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from crew import Cocreate
from crewai import LLM
import os


# from langfuse import Langfuse
# from langfuse import get_client
# from openinference.instrumentation.crewai import CrewAIInstrumentor
# from openinference.instrumentation.litellm import LiteLLMInstrumentor

from bedrock_agentcore.runtime import BedrockAgentCoreApp
import argparse
import json
app = BedrockAgentCoreApp()

# langfuse = get_client()
 
# Verify connection
# if langfuse.auth_check():
#     print("Langfuse client is authenticated and ready!")
# else:
#     print("Authentication failed. Please check your credentials and host.")

# CrewAIInstrumentor().instrument(skip_dep_check=True)
# LiteLLMInstrumentor().instrument()

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

# Finally write your entrypoint
@app.entrypoint
def crewai_bedrock(payload):
    """
    Invoke the crew with a payload
    """
    user_input = payload.get("prompt")
    inputs = {
        'topic': user_input
    }
    llm = LLM(
        model="us.amazon.nova-pro-v1:0"
    )
    
    # Run the crew
    result = Cocreate(llm).crew().kickoff(inputs=inputs)
    
    # Return the result
    return result.raw

def run():
    # with langfuse.start_as_current_span(
    # name="cocreate-trace",
    # ) as span:
        
    inputs = {
        'topic': 'Quantum Computing'
    }

    llm = LLM(
        model="us.amazon.nova-pro-v1:0",
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        aws_region_name=os.getenv('AWS_DEFAULT_REGION')
    )
    
    try:
        result=Cocreate(llm).crew().kickoff(inputs=inputs)
        print(result.raw)
        # print("-------Structured Output-------")
        # print(result.pydantic)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

    # langfuse.flush()


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs",
        'current_year': str(datetime.now().year)
    }
    try:
        Cocreate().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        Cocreate().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs",
        "current_year": str(datetime.now().year)
    }
    
    try:
        Cocreate().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

if __name__ == "__main__":
    app.run()