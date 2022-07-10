import streamlit as st 
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
plt.style.use('seaborn-dark')
import os
import plotly.graph_objs as go
import plotly.express as px
st.set_option('deprecation.showPyplotGlobalUse', False)

#Loading the data
@st.cache
def get_matches_data():
     return pd.read_csv(os.path.join(os.getcwd(),'matches.csv'))
@st.cache
def get_deliveries_data():
     return pd.read_csv(os.path.join(os.getcwd(),'deliveries.csv'))

#configuration of the page
st.set_page_config(layout="wide")
#load dataframes
df = get_matches_data()
df2 = get_deliveries_data()
st.title('IPL Data Vizualisation Web App')


col1, col2 = st.columns([2, 2])
col3, col4 = st.columns([2, 2])
col5, col6 = st.columns([2, 2])

with col1:
    st.markdown('Total runs across the season')
    batsmen = df[['id','season']].merge(df2, left_on = 'id', right_on = 'match_id', how = 'left').drop('id', axis = 1)
    #merging the matches and delivery dataframe by referencing the id and match_id columns respectively
    top_runs=batsmen.groupby(['season'])['total_runs'].sum().reset_index()
    top_runs.set_index('season')
    fig = px.line(top_runs,x='season',y='total_runs')
    st.plotly_chart(fig)
    


with col2:
    st.markdown('Average runs per match across seasons')
    avgruns_each_season=df.groupby(['season']).count().id.reset_index()
    avgruns_each_season.rename(columns={'id':'matches'},inplace=1)
    avgruns_each_season['total_runs']=top_runs['total_runs']
    avgruns_each_season['average_runs_per_match']=avgruns_each_season['total_runs']/avgruns_each_season['matches']
    avgruns_each_season.set_index('season')['average_runs_per_match'].plot(marker='o')
    fig2 = px.line(avgruns_each_season,x='season',y='average_runs_per_match')
    st.plotly_chart(fig2)


with col3:
    st.markdown('Is winning toss impactful?')
    df_n=df[df['toss_winner']==df['winner']]
    slices=[len(df_n),(577-len(df_n))]
    label=['yes','no']
    fig3 = go.Figure(data=[go.Pie(labels=label, values=slices)])
    st.plotly_chart(fig3)


high_scores=df2.groupby(['match_id', 'inning','batting_team','bowling_team'])['total_runs'].sum().reset_index()
high_scores1=high_scores[high_scores['inning']==1]
high_scores2=high_scores[high_scores['inning']==2]
high_scores1=high_scores1.merge(high_scores2[['match_id','inning', 'total_runs']], on='match_id')
high_scores1.rename(columns={'inning_x':'inning_1','inning_y':'inning_2','total_runs_x':'inning1_runs','total_runs_y':'inning2_runs'},inplace=True)
high_scores1=high_scores1[high_scores1['inning1_runs']>=200]
high_scores1['is_score_chased']=1
high_scores1['is_score_chased'] = np.where(high_scores1['inning1_runs']<=high_scores1['inning2_runs'], 
                                           'yes', 'no')

with col4:
    st.markdown('Chances of chasing 200+ Target')
    slices=high_scores1['is_score_chased'].value_counts().reset_index().is_score_chased
    slices = list(slices)
    labels=['target not chased','target chased']
    fig4 = go.Figure(data=[go.Pie(labels=labels, values=slices)])
    st.plotly_chart(fig4)

with col5:
    st.markdown('Top 10 Batsmen')
    max_runs=df2.groupby(['batsman'])['batsman_runs'].sum()
    ax=max_runs.sort_values(ascending=False)[:10]
    st.bar_chart(ax)

with col6:
    st.markdown('Maximum Man of the match')
    ax2 = df['player_of_match'].value_counts().head(10)
    # to each batsman and then filters out the top 10 batsman and then plots a bargraph 
    st.bar_chart(ax2)

