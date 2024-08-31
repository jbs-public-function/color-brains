# python std library
from typing import List, Iterable

# metaflow
from metaflow import FlowSpec, step

# internal modules
from color_brains.data.sequential_data import SequentialData


class RGBFeatureFlow(FlowSpec):
    @step
    def start(self):
        self.next(self.rgb_features)
    
    @step
    def rgb_features(self):
        # self.datset = 
        self.next(self.end)
    
    @step
    def end(self):
        ...
    
    @classmethod
    def mangle_rgb_names(cls, tag: str, include_columns: Iterable[str], exclude_column: str) -> List[str]:
        return [f"{tag}_{column}" for column in include_columns]


if __name__ == "__main__":
    RGBFeatureFlow()
