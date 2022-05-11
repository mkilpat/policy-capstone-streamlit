import streamlit as st
import pandas as pd
import altair as alt

st.title('📄State Legislation Topic Explorer🏛')

# read in data
probs_df = pd.read_csv('df_probs_cleaned.csv', converters={'Jurisdiction': str.strip})
topics_df = pd.read_csv('LDA_70_topics_labels.csv')
topics_df['category'] = topics_df['main_category'] + '/' + topics_df['sub_category']
columns = ['Jurisdiction', 'Prob', 'Topic', 'Accuracy', 'category']
probs_df = probs_df.merge(topics_df, how='left', left_on='Topic', right_on='topics')[columns]

jurisdictions = probs_df.Jurisdiction.unique()
topics = probs_df.category.unique()

with st.sidebar:
    view = st.selectbox('View by States or Topics?', ['states', 'topics'])
    facet = st.selectbox('View by Probability Bill Passes or Model Accuracy', ['Prob', 'Accuracy'])

# Topics view
if view == 'states':
    state = st.selectbox('Select state', jurisdictions)
    plot_df = probs_df.loc[probs_df.Jurisdiction == state, ['category', facet]]
    c = alt.Chart(plot_df).mark_bar().encode(x='category', y=facet).properties(width=200, height=500)
    #st.table(plot_df)
    st.altair_chart(c, use_container_width=True)

if view == 'topics':
    topic = st.selectbox('Select topic', topics)
    plot_df = probs_df.loc[probs_df.category == topic, ['Jurisdiction', facet]]
    c = alt.Chart(plot_df).mark_bar().encode(x='Jurisdiction', y=facet).properties(width=200, height=500)
    # st.table(plot_df)
    st.altair_chart(c, use_container_width=True)



