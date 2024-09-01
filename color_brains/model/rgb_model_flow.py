# python std library
import os
import sys
import subprocess
from typing import *

# analysis
import pandas as pd
import numpy as np

# metaflow
from metaflow import FlowSpec, Flow, step, Parameter


def run_rgb_feature_metaflow(flowfile: str):
    script_path = os.path.join(
        os.path.dirname(
            os.path.dirname(__file__)  # parent of __file__ dir
        ),
        "data_enrichment",
        flowfile        
    )

    try:
        # Use the correct Python executable for the system
        python_executable = sys.executable
        
        # Run the script using the subprocess module
        process = subprocess.Popen(
            [python_executable, script_path, "run"],
            stdout=subprocess.PIPE,  # Capture stdout
            stderr=subprocess.PIPE   # Capture stderr
        )
        
        # Wait for the process to complete
        stdout, stderr = process.communicate()
        
        # Check if the process ended successfully
        if process.returncode == 0:
            print("Script executed successfully:")
            print(stdout.decode('utf-8'))
        else:
            print("Script failed with return code", process.returncode)
            print(stderr.decode('utf-8'))
    
    except Exception as e:
        print(f"An error occurred: {e}")



class RGBModelFlow(FlowSpec):
    dependendent_variables: List[str] = ['next_red', 'next_green', 'next_blue']
    rgb_feature_file = Parameter("rgb_feature_file", default="rgb_feature_enrichment_flow.py")
    rgb_feature_flowname = Parameter("rgb_feature_flowname", default="RGBFeatureEnrichmentFlow")
    
    @step
    def start(self):
        print(f"Loading dataset from latest successful run of {self.rgb_feature_flowname}")
        try:
            latest_run = Flow(self.rgb_feature_flowname).latest_successful_run
        except Exception:
            print(f'No Previously Successful Run of {self.rgb_feature_flowname} Found...\nRunning')
            run_rgb_feature_metaflow(self.rgb_feature_file)
            latest_run = Flow(self.rgb_feature_flowname).latest_successful_run
        
        self.dataset = latest_run.data.dataset
        self.identifier_column_name = latest_run.data.cmap_column_name
        self.next(self.end)
    
    @step
    def end(self):
        ...

    
if __name__ == "__main__":
    RGBModelFlow()