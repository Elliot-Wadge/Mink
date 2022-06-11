import plotly.graph_objects as go
import plotly.io as pio


science_template = go.layout.Template()
scatter_lst = []
colors = ["rgb(20,20,20)", "rgb(169,2,235)", "rgb(6,96,214)", "rgb(20,156,5)",
          "rgb(242,135,5)", "rgb(58,184,189)", "rgb(211,148,242)"]

for color in colors:
    scatter_lst.append(go.Scatter(marker=dict(color=color),
                                  line=dict(color=color),
                                  hovertemplate="x = %{x}<br>y = %{y}"))

science_template.data.scatter = scatter_lst
science_template.layout = pio.templates["simple_white"].layout
science_template.layout["margin"] = go.layout.Margin(autoexpand=True,
                                                     l=30, r=30, t=30, b=30)
