import streamlit as st
import pandas as pd
import altair as alt

st.title('📄State Legislation Topic Explorer🏛')

# read in data
probs_df = pd.read_csv('df_probs_cleaned.csv', converters={'Jurisdiction': str.strip})
topics_df = pd.read_csv('LDA_70_topics_labels.csv')
topics_df['category'] = topics_df['main_category'] + '/' + topics_df['sub_category']
# Prob column is probability of failure. Need to take the inverse
probs_df['Pass'] = 1.0 - probs_df['Prob']
columns = ['Jurisdiction', 'Pass', 'Topic', 'Accuracy', 'category']
probs_df = probs_df.merge(topics_df, how='left', left_on='Topic', right_on='topics')[columns]

jurisdictions = probs_df.Jurisdiction.unique()
topics = probs_df.category.unique()

with st.sidebar:
    view = st.selectbox('View by States or Topics?', ['States', 'Topics', 'Both'])
    facet = st.selectbox('View by Probability Bill Passes or Model Accuracy', ['Pass', 'Accuracy'])

# Topics view
if view == 'States':
    state = st.selectbox('Select state', jurisdictions)
    plot_df = probs_df.loc[probs_df.Jurisdiction == state, ['category', facet]]
    c = alt.Chart(plot_df).mark_bar().encode(x=facet, y='category').properties(width=200, height=700)
    #st.table(plot_df)
    st.altair_chart(c, use_container_width=True)

if view == 'Topics':
    topic = st.selectbox('Select topic', topics)
    plot_df = probs_df.loc[probs_df.category == topic, ['Jurisdiction', facet]]
    c = alt.Chart(plot_df).mark_bar().encode(x=facet, y='Jurisdiction').properties(width=200, height=700)
    # st.table(plot_df)
    st.altair_chart(c, use_container_width=True)

if view == 'Both':
    c = alt.Chart(probs_df).mark_rect().encode(x='Jurisdiction', y='category', color=facet).properties(width=400, height=800)
    st.altair_chart(c, use_container_width=True)



