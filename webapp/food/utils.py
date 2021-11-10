from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.models import (HoverTool, FactorRange, LinearAxis, Grid,
                          Range1d)
from bokeh.models.glyphs import VBar
from bokeh.models.sources import ColumnDataSource

from datetime import date, timedelta
from flask_login import current_user

from webapp.food.models import DailyConsumption


def daily_counter(today):
    daily_consumption = DailyConsumption.query.filter(
        DailyConsumption.user_cons == current_user.id,
        DailyConsumption.cons_day == today
    ).all()
    daily_consumption_cals = 0
    daily_consumption_prots = 0
    daily_consumption_fats = 0
    daily_consumption_carbos = 0
    for i in daily_consumption:
        daily_consumption_cals += i.cons_calories
        daily_consumption_prots += i.cons_prots
        daily_consumption_fats += i.cons_fats
        daily_consumption_carbos += i.cons_carbos

    return daily_consumption_cals, daily_consumption_prots, daily_consumption_fats, daily_consumption_carbos



def graph_maker():
    data = {"days": [], "calories": [], "prots": [], "fats": [], "carbos": []}
    data_check = False
    for i in range(0, 3):
        day = date.today() - timedelta(days=i)
        day = day.strftime("%d/%m/%Y")
        consumption_data = daily_counter(day)
        if consumption_data[0] != 0:
            data_check = True
        data['days'].append(day)
        data['calories'].append(consumption_data[0])
        data['prots'].append(consumption_data[1])
        data['fats'].append(consumption_data[2])
        data['carbos'].append(consumption_data[3])

    hover = create_hover_tool()
    plot = create_bar_chart(data, "days",
                            "calories", hover)
    script, div = components(plot)

    return script, div, data_check


def create_bar_chart(data, x_name, y_name, hover_tool=None,
                     width=300, height=150):

    source = ColumnDataSource(data)
    xdr = FactorRange(factors=data[x_name])
    ydr = Range1d(start=0,end=max(data[y_name])*1.5)

    tools = []
    if hover_tool:
        tools = [hover_tool,]

    plot = figure(x_range=xdr, y_range=ydr, plot_width=width,
                  plot_height=height, h_symmetry=False, v_symmetry=False,
                  min_border=0, toolbar_location="above", tools=tools,
                  responsive=True, outline_line_color="#666666")

    glyph = VBar(x=x_name, top=y_name, bottom=0, width=.3,
                 fill_color="#e12127")
    plot.add_glyph(source, glyph)

    xaxis = LinearAxis()
    yaxis = LinearAxis()

    plot.add_layout(Grid(dimension=0, ticker=xaxis.ticker))
    plot.add_layout(Grid(dimension=1, ticker=yaxis.ticker))
    plot.toolbar.logo = None
    plot.min_border_top = 0
    plot.xgrid.grid_line_color = None
    plot.ygrid.grid_line_color = "#999999"
    plot.yaxis.axis_label = "Каллорий потреблено"
    plot.ygrid.grid_line_alpha = 0.1
    plot.xaxis.axis_label = "Дата"
    plot.xaxis.major_label_orientation = 1
    return plot



def create_hover_tool():

    hover_html = """
        <div>
            <span class="hover-tooltip">$x</span>
        </div>
        <div>
            <span class="hover-tooltip">Потреблено @calories калорий из 2000 </span>
        </div>
        <div>
            <span class="hover-tooltip">Белки: @prots г</span>
        </div>
        <div>
            <span class="hover-tooltip">Жиры: @fats г</span>
        </div>
        <div>
            <span class="hover-tooltip">Углеводы: @carbos г</span>
        </div>
    """
    return HoverTool(tooltips=hover_html)