import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import seaborn as sns
from pandas import Timestamp
from matplotlib import colors as mcolors
import matplotlib
import datetime
import math
import os
import database.connections.db_transact as db_transact

def plot_cycle(user, date): 
    '''
    Plots last 3 cycles
    '''

    end_date = date - datetime.timedelta(weeks=13)
    start_date = end_date - datetime.timedelta(weeks=6)
    
    columns=['cycle_day', 'date']
    table = 'period'
    # get data
    data = db_transact.query_data_between_dates_by_user(user, start_date, end_date, table=table, columns=columns)   #returns list of tuples
    data_values = [tup[0:-1] for tup in data]   #extract values from each tuple
    date = [tup[-1] for tup in data] 

    # create dataframe from data
    print(columns[:-1])
    df = pd.DataFrame(data=data_values, index=date, columns=columns[:-1])
    print(df)

    #find local maxima
    locMax = df['cycle_day'][(df['cycle_day'].shift(1) < df['cycle_day']) & (df['cycle_day'].shift(-1) < df['cycle_day'])]
    #get local maxima mean
    cycleLengthMean = locMax.mean()
    cycleLengthMedian = locMax.median()

    # # cycle length based on ONLY the last 4 periods ---> later for when more health tracker data is available
    # cycleLengthCurrent = locMax[-4:].mean()

    # ----- calculate fertile window based ONLY on last 4 periods ----- ---> later for when more health tracker data is available, NOW: only with available

    # ovulation - occurs 14 days before period start
    # ovulation = math.ceil(cycleLengthCurrent - 14)
    ovulation = math.ceil(cycleLengthMean - 14)
    # the fertile window starts 5- 6 days before ovulation
    fertile_start = ovulation - 5
    # the most fertile window start 2- 3 days before ovulation
    fertile_high = ovulation - 3
    # fertilization can occur up to 24 after ovulation
    fertile_trail = ovulation + 1

    # PLOT
    fig, ax = plt.subplots(figsize=(7,4))

    ax.bar(df.index, df['cycle_day'], width = 0.5, color ='#fc2647')
    # ax.scatter(df.index, parameter, color ='blue', s=1)   ## to add additional parameters later on

    # custom values
    big_fonts = 8
    small_fonts = 6

    #add cycle info, including mean lenght, ovulation and fertile window
    plt.axhline(y=cycleLengthMean,xmin=0,xmax=0.98,color='pink',ls='-.',lw=0.7)
    total_days = len(df.index)
    lastDate = df.index.max()+datetime.timedelta(days=total_days/20) #add days for readability
    plt.text(x=lastDate, y=cycleLengthMean-0.3, s= f'mean cycle length',color='pink',size=big_fonts)
    plt.axhline(y=ovulation,xmin=0.04,xmax=0.98,color='purple',lw=0.5)
    plt.text(x=lastDate, y=ovulation-0.6, s= f'Ovulation (Cycle Day {ovulation})',color='purple',size=big_fonts)
    plt.axhspan(ymin=fertile_start, ymax=fertile_trail, xmin=0.04, xmax=0.98,color='purple',alpha=0.1, zorder=-1)
    plt.text(x=lastDate, y=fertile_start-1, s= f'cycle day {fertile_start}',color='purple',size=small_fonts,alpha=0.25)
    plt.axhspan(ymin=fertile_high, ymax=ovulation, xmin=0.04, xmax=0.98,color='purple',alpha=0.2, zorder=-1)
    plt.text(x=lastDate, y=fertile_high-0.3, s= f'cycle day {fertile_high}',color='purple',size=small_fonts,alpha=0.5)

    ax.xaxis.set_major_locator(matplotlib.dates.YearLocator())
    ax.xaxis.set_minor_locator(matplotlib.dates.MonthLocator((1,3,5,7,9,11)))

    ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter("\n%Y"))
    ax.xaxis.set_minor_formatter(matplotlib.dates.DateFormatter("%b"))
    plt.setp(ax.get_xticklabels(), rotation=0, ha="center")
    # plt.legend()

    sns.despine(left=True, bottom = True)
    plt.tight_layout()

    return fig
    plt.close()
    quit()
