from typing import Optional
from dataclasses import dataclass

@dataclass
class PlotData:
    x: list[float]
    y: list[float]
    additional_data: Optional[list] = None

    def get_index_data(self, idx) -> str:
        return f'x: {self.x[idx]:.2e}, y: {self.y[idx]:.2e}' + \
               f'\n{self.additional_data[idx].__repr__()}' if self.additional_data else ''
