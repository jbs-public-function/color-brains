# python std library
from typing import *

# analysis
import pandas as pd
import numpy as np

# metaflow
from metaflow import FlowSpec, Flow, step, Parameter

# internal modules
from color_brains.model.utils import run_rgb_feature_metaflow, DATA_ENRICHMENT_METAFLOW_FILEPATH, DATA_ENRICHMENT_METAFLOW_NAME


class RGBModelFlow(FlowSpec):
    dependendent_variables: List[str] = ['next_red', 'next_green', 'next_blue']
    rgb_feature_file = Parameter("rgb_feature_file", default=DATA_ENRICHMENT_METAFLOW_FILEPATH)
    rgb_feature_flowname = Parameter("rgb_feature_flowname", default=DATA_ENRICHMENT_METAFLOW_NAME)
    
    @step
    def start(self):
        print(f"Loading dataset from latest successful run of {self.rgb_feature_flowname}")
        try:
            latest_run = Flow(self.rgb_feature_flowname).latest_successful_run
        except Exception:
            print(f'No Previously Successful Run of {self.rgb_feature_flowname} Found...\nRunning')
            run_rgb_feature_metaflow(DATA_ENRICHMENT_METAFLOW_FILEPATH)
            latest_run = Flow(self.rgb_feature_flowname).latest_successful_run
        
        self.latest_run = latest_run
        self.next(self.end)
    
    @step
    def end(self):
        ...

    
if __name__ == "__main__":
    RGBModelFlow()