# -*- coding: utf-8 -*-
"""
Created on Wed Nov 14 15:55:56 2018
Functions to access Billboard's weekly charts and extracting chart data
@author: PDP2600
"""
import requests
import pandas as pd
import datetime
import numpy as np
from time import sleep

def bb_get_weekly_chart(chart_route, chart_date):
    """Attempts to get data for the chart_route & chart date provided. There's
    a simple check for valid chart routes (more details in parameter 
    description), & the date is sent as is, as Billboard's site figures out 
    what specific weekly chart based on the date being in that week.

    Parameters: 
        chart_route (str): A string with the specific chart type to get data 
            from. Check bb_get_weekly_chart for current valid chart routes.
            Currently valid (others will likely work, but I've only tested & 
            created datasets from these, just have to modify the 
            valid_chart_routes list): 'r-b-hip-hop-albums', 
            'r-b-hip-hop-songs', 'hot-100', 'billboard-200', 'pop-songs', 
            'rock-songs', 'latin-songs', 'dance-electronic-songs', 
            'country-songs', 'youtube', & 'japan-hot-100'
        chart_date (str): Date to get a weekly chart for. It's in 
            the format 'YYYY-MM-DD'. 
    Output: 
        DataFrame: Contains data from the weekly chart for the given 
        date extracted & indexed by '<chart_date>_<chart_rank>'. It contains 
        the column names: ranking, artist, title, last_week_rank, 
        peak_position, weeks_on_chart, chart_date    
    """    
    billboard_url = 'https://www.billboard.com/charts/'
    valid_chart_routes = ['r-b-hip-hop-albums', 'r-b-hip-hop-songs', 'hot-100', 
                          'billboard-200', 'pop-songs', 'rock-songs', 
                          'latin-songs', 'dance-electronic-songs', 
                          'country-songs', 'youtube', 'japan-hot-100']
    retry_max = 4
    if chart_route in valid_chart_routes:
        request_url = billboard_url + chart_route + "/" + chart_date
        chart_request_data = _attempt_connections(request_url, retry_max)
        
        if chart_request_data.status_code == requests.codes.ok:
            chart_request_str = str(chart_request_data.content).replace('\\n', '')
            number_one_df = _bb_extract_number_one_data(chart_request_str, chart_date)
            rest_of_chart_df = _bb_extract_chart_data(chart_request_str, chart_date)
            chart_appended_df = number_one_df.append(rest_of_chart_df, sort=False)
            #chart_appended_df = _bb_format_columns(chart_appended_df)        
            return chart_appended_df
        else:
            print("Connection error on {}, {} times attempted."
                  .format(billboard_url, retry_max + 1))
            return pd.DataFrame(columns = ['ranking', 'artist', 'title', 
                                           'last_week_rank', 'peak_position', 
                                           'weeks_on_chart', 'chart_date'])
        
    else:
        print("{} is not a valid Billboard chart route".format(chart_route))
        return pd.DataFrame(columns = ['ranking', 'artist', 'title', 
                                       'last_week_rank', 'peak_position', 
                                       'weeks_on_chart', 'chart_date'])
    
def bb_get_multiple_charts(chart_route, chart_from_date, chart_to_date):
    """Main function to get weekly Billboard charts. Will attempt to attain
    weekly charts between chart_from_date to chart_to_date in increments of 7 
    days (first chart will be the from date, next will be that date + 7 days 
    until it exceeds the chart_to_date). Uses the function bb_get_weekly_chart.

    Parameters: 
        chart_route (str): A string with the specific chart type to get data 
            from. Check bb_get_weekly_chart for current valid chart routes.
        chart_from_date (str): Date to start gathering weekly charts. It's in 
            the format 'YYYY-MM-DD'. 
        chart_to_date (str): Date up to when you want to collect weekly charts. 
            It's in the format 'YYYY-MM-DD'. Last chart will be either this 
            date or 1 to 6 days earlier.
    Output: 
        DataFrame: Contains data from all the weekly charts between the given 
        dates extracted & indexed by '<chart_date>_<chart_rank>'. It contains 
        the column names: ranking, artist, title, last_week_rank, 
        peak_position, weeks_on_chart, chart_date    
    """    
    chart_data_collection_df = bb_get_weekly_chart(chart_route, chart_from_date)
    chart_date_index = datetime.datetime.strptime(
            chart_from_date, "%Y-%m-%d") + datetime.timedelta(days=7)
    chart_to_datetime  = datetime.datetime.strptime(chart_to_date, "%Y-%m-%d")
    while chart_date_index <= chart_to_datetime:
        #print("Chart Date: {}".format(chart_date_index.strftime('%Y-%m-%d')))
        chart_data_collection_df = chart_data_collection_df.append(
                bb_get_weekly_chart(chart_route, 
                                    chart_date_index.strftime('%Y-%m-%d')))
        chart_date_index = chart_date_index + datetime.timedelta(days=7)
        sleep(1)
    print("Finished gathering data from Billboard.com, formatting data...")
    chart_data_collection_df = _bb_format_columns(chart_data_collection_df)
    return chart_data_collection_df

def _attempt_connections(conn_url, retries):
    """Simple and general function I created to retry making a requests.get 
    connection attempt. When an error status code is returned it's retried the
    amount of times passed in.

    Parameters:
        conn_url (str): A string which is url to attempt the get request with.
        retries (int): The number of times to retry if the connection failed. 
        At least one connection is attempted, retries are the number of 
        attempts if the first fails
        
    Output:
        requests "request" object: Contains the content and meta information of 
        the last connection attempt (first success, or failure of the last retry).
    """
    chart_request_result = requests.get(conn_url)
    success_bool = chart_request_result.status_code == requests.codes.ok
    retry_num = 1
    while (success_bool == False) and (retry_num <= retries):
        print("{} retry number {}".format(conn_url, retry_num))
        chart_request_result = requests.get(conn_url)
        success_bool = chart_request_data.status_code == requests.codes.ok
        retry_num = retry_num + 1
    return chart_request_result

def _bb_format_columns(chart_df):
    """Converts escaped characters for the string values, stripping space 
    characters from "numeric" values (i.e. chart rank, number of weeks on chart), 
    and replacing any '' artist values with a missing artist token to make it 
    more explicit and easy to deal with in the results.

    Parameters:
        chart_df (DataFrame): DF of chart data, with the following columns
            being acted on: artist, title, ranking, last_week_rank, 
            peak_position, and weeks_on_chart
        
    Output:
        DataFrame: Contains the DF which was passed in with the stated formatting
            applied to the columns acted on.
    """
    formatting_chart = chart_df
    formatting_chart.last_week_rank = (formatting_chart.last_week_rank
                                       .map(lambda lw: (
                                               str(lw).replace('-', '0')
                                               .strip())))
    formatting_chart.title = (formatting_chart.title
                              .map(lambda t: (
                                      t.replace('&amp;', '&')
                                      .replace('&#039;', "'")
                                      .replace('&quot;', '"')
                                      .strip())))
    formatting_chart.artist = (formatting_chart.artist
                               .map(lambda a: (
                                       a.replace('&amp;', '&')
                                       .replace('&#039;', "'")
                                       .replace('&quot;', '"')
                                       .strip())))
    formatting_chart.ranking = (formatting_chart.ranking
                                .map(lambda r: str(r).strip()))
    formatting_chart.peak_position = (formatting_chart.peak_position
                                      .map(lambda p: str(p).strip()))
    formatting_chart.weeks_on_chart = (formatting_chart.weeks_on_chart
                                       .map(lambda wc: str(wc).strip()))
    formatting_chart.artist = (np.where(formatting_chart['artist'] == '',
                                        '===<Missing_Artist>===',
                                        formatting_chart.artist))
    return formatting_chart

def _bb_extract_number_one_data(content_str, chart_date):
    """Used for extracting the Number 1 ranked entity in the chart (since 
    there's different mark up for #1s)

    Parameters:
        content_str (str): A string coverted version of the contents of a 
            request Billboard Chart page
        chart_date (str): Date used to retrieve the chart, in the format 
            'YYYY-MM-DD'.
    Output:
        DataFrame: contains chart data extracted and indexed by 
            '<chart_date>_<chart_rank>' with the column names: ranking, 
            artist, title, last_week_rank, peak_position, weeks_on_chart, 
            chart_date
    """
    
    try:
        start_index = content_str.index('<div class="chart-number-one__info ">')
    except ValueError:
        print("Missing opening Number 1 HTML tag for chart requested on date {}"
              .format(chart_date))
        return pd.DataFrame(columns = ['ranking', 'artist', 'title', 
                                       'last_week_rank', 'peak_position', 
                                       'weeks_on_chart', 'chart_date'])
    try:
        end_index = content_str.index('<div class="chart-details ">')
    except ValueError:
        print("Missing closing Number 1 HTML tag for chart requested on date {}\n"
              .format(chart_date))
        return pd.DataFrame(columns = ['ranking', 'artist', 'title', 
                                       'last_week_rank', 'peak_position', 
                                       'weeks_on_chart', 'chart_date'])
    number_one_data = content_str[start_index:end_index]
    print("Number One process success {}".format(chart_date))
    #Portion to extract out the values of interest
    this_week_position = '1'
    peak_position = '1'
    last_week_position = '0'
    if '<div class="chart-number-one__last-week">' in number_one_data:
        number_one_data = number_one_data[number_one_data
                                          .index('<div class="chart-number-one__last-week">'):]
        last_week_position = number_one_data[
                len('<div class="chart-number-one__last-week">'):number_one_data
                .index('</div>')]
    weeks_on_chart = '1'
    if '<div class="chart-number-one__weeks-on-chart">' in number_one_data: 
        number_one_data = number_one_data[
                number_one_data
                .index('<div class="chart-number-one__weeks-on-chart">'):]
        weeks_on_chart = number_one_data[
                len('<div class="chart-number-one__weeks-on-chart">'):number_one_data
                .index('</div>')]
    number_one_data = number_one_data[
            number_one_data.index('<div class="chart-number-one__title">'):]
    title = number_one_data[
            len('<div class="chart-number-one__title">'):number_one_data
            .index('</div>')]
    artist = '===<Missing_Artist>==='
    if '<div class="chart-number-one__artist">' in number_one_data:
        number_one_data = number_one_data[
                number_one_data.index('<div class="chart-number-one__artist">'):]
        number_one_data = number_one_data[
                len('<div class="chart-number-one__artist">'):] 
        artist =  number_one_data[:number_one_data.index('</div>')]
    if '</a>' in artist:
        artist = number_one_data[number_one_data
                                 .index('>')+1:number_one_data.index('</a>')]
    return pd.DataFrame({'ranking':this_week_position, 
                         'artist':artist, 'title':title, 
                         'last_week_rank':last_week_position, 
                         'peak_position':peak_position, 
                         'weeks_on_chart':weeks_on_chart, 
                         'chart_date':chart_date
                         }, index=[str(chart_date)+"_"+this_week_position.strip()])

def _bb_extract_chart_element(chart_str, chart_date):
    """For extracting data for a single non-number one chart entry

    Parameters: 
        content_str (str): A string coverted version of the contents of a 
            request Billboard Chart page
        chart_date (str): Date used to retrieve the chart, in the format 
            'YYYY-MM-DD'.
    
    Output:
        DataFrame: contains chart data extracted and indexed by 
            '<chart_date>_<chart_rank>' with the column names: ranking, 
            artist, title, last_week_rank, peak_position, weeks_on_chart, 
            chart_date
    """    

    title = chart_str[
            chart_str.index('data-title="')+len('data-title="'):chart_str
            .index('" data-has-content=')]
    if '<div class="chart-list-item__rank chart-list-item__rank--long">' in chart_str:
        chart_str = chart_str[
                chart_str
                .index('<div class="chart-list-item__rank chart-list-item__rank--long">'):]
        this_week_position = chart_str[
                len('<div class="chart-list-item__rank chart-list-item__rank--long">'):chart_str
                .index('</div>')]    
    else:
        chart_str = chart_str[chart_str.index('<div class="chart-list-item__rank ">'):]
        this_week_position = chart_str[
                len('<div class="chart-list-item__rank ">'):chart_str
                .index('</div>')]
    
    chart_str = chart_str[chart_str.index('<div class="chart-list-item__title">'):]
    #title = chart_str[len('<div class="chart-list-item__title">'):chart_str.index('</div>')]
    #if '<span class="chart-list-item__title-text">' in title:
    #    title = chart_str[chart_str.index('>')+1:chart_str.index('</span>')]
    artist = '===<Missing_Artist>==='
    if '<div class="chart-list-item__artist">' in chart_str:
        chart_str = chart_str[chart_str
                              .index('<div class="chart-list-item__artist">'):]
        chart_str = chart_str[len('<div class="chart-list-item__artist">'):]
        artist = chart_str[:chart_str.index('</div>')]
    if '</a>' in artist:
        artist = chart_str[chart_str.index('>')+1:chart_str.index('</a>')]
    last_week_position = '0'
    if '<div class="chart-list-item__last-week">' in chart_str:
        chart_str = chart_str[chart_str
                              .index('<div class="chart-list-item__last-week">'):]
        last_week_position = chart_str[
                len('<div class="chart-list-item__last-week">'):chart_str
                .index('</div>')]
    peak_position = this_week_position
    if '<div class="chart-list-item__weeks-at-one">' in chart_str:
        chart_str = chart_str[
                chart_str.index('<div class="chart-list-item__weeks-at-one">'):]
        peak_position = chart_str[
                len('<div class="chart-list-item__weeks-at-one">'):chart_str
                .index('</div>')]
    weeks_on_chart = '1'
    if '<div class="chart-list-item__weeks-on-chart">' in chart_str:
        chart_str = chart_str[
                chart_str.index('<div class="chart-list-item__weeks-on-chart">'):]
        weeks_on_chart = chart_str[
                len('<div class="chart-list-item__weeks-on-chart">'):chart_str
                .index('</div>')]
    return pd.DataFrame({'ranking':this_week_position, 
                         'artist':artist, 'title':title, 
                         'last_week_rank':last_week_position, 
                         'peak_position':peak_position, 
                         'weeks_on_chart':weeks_on_chart, 
                         'chart_date':chart_date
                         }, index=[str(chart_date)+"_"+this_week_position.strip()])

def _bb_extract_chart_data(content_str, chart_date):
    """Takes chart data, removes the number one entry data, slices the chart 
    data up into a list per chart entry & then calls the chart data extraction 
    function on each chart entry chunk.

    Parameters: 
        content_str (str): A string coverted version of the contents of a 
            request Billboard Chart page
        chart_date (str): date used to retrieve the chart, in the format 
            'YYYY-MM-DD'.
    Output: 
        DataFrame: contains chart data extracted and indexed by 
            '<chart_date>_<chart_rank>' with the column names: ranking, 
            artist, title, last_week_rank, peak_position, weeks_on_chart, 
            chart_date    
    """
    number_1_data_end = content_str.index('<div class="chart-details ">')
    try:
        end_index = content_str.index('</main>') + len('</main>')
    except ValueError:
        print("Missing closing Chart HTML tag for chart requested on date {}\n"
              .format(chart_date))
        return pd.DataFrame(columns = ['ranking', 'artist', 'title', 
                                       'last_week_rank', 'peak_position', 
                                       'weeks_on_chart', 'chart_date'])
    lower_chart_data = content_str[number_1_data_end:end_index]
    try:
        start_index = lower_chart_data.index('data-rank')
    except ValueError:
        print("Missing opening Chart HTML tag for chart requested on date {}\n"
              .format(chart_date))
        return pd.DataFrame(columns = ['ranking', 'artist', 'title', 
                                       'last_week_rank', 'peak_position', 
                                       'weeks_on_chart', 'chart_date'])
    end_index = lower_chart_data.index('</main>')
    
    lower_chart_data = lower_chart_data[start_index:end_index]
    lower_chart_list = lower_chart_data.split(
            sep='<div class="chart-list-item  " data-rank=')
    chart_parsed_data = pd.DataFrame(columns = ['ranking', 'artist', 'title', 
                                                'last_week_rank', 
                                                'peak_position', 
                                                'weeks_on_chart', 'chart_date'])
    #count = 2
    for chart_data in lower_chart_list:
        #print("{} rank\n".format(count))
        #print("{}".format(chart_data))
        chart_entry_data = _bb_extract_chart_element(chart_data, chart_date)
        chart_parsed_data = chart_parsed_data.append(chart_entry_data, sort=False)
        #count = count + 1        
    return chart_parsed_data
