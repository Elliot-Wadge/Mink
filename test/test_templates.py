import unittest
import numpy as np
from plotly import graph_objects as go
from Mink.plotly_templates import science_template
from Mink.special_chars_dict import sc

class TemplateTester(unittest.TestCase):
    x = np.linspace(0, 10, 20)

    def test_science_template(self):
        '''check that the template doesn't produce any errors'''
        fig = go.Figure()
        fig.update_layout(template=science_template)
        fig.add_trace(go.Scatter(x=self.x, y=self.x))
        fig.add_trace(go.Scatter(x=self.x, y=2*self.x))
        fig.update_xaxes(title=f"this is the x title {sc.pi + sc.psi + sc.chi}")
        fig.show()


if __name__ == '__main__':
    unittest.main()
