import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt
import seaborn as sns
st.sidebar.title("WhatsApp Chat Analyser")

### upload file
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

  #  st.dataframe(df)

### unique users

    user_list = df['user'].unique().tolist()
    # user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Group Chat")

    selected_user = st.sidebar.selectbox("Select user",user_list)
##button
    if st.sidebar.button("Show Analysis"):
#######stats
        col1,col2,col3,col4=st.columns(4)

        no_messages,words,no_media_messages,links=helper.fetch_stats(selected_user,df) ## fetch  with help of helper file

        with col1:
            st.header('Total Messages')
            st.title(no_messages)
        with col2:
            st.header('Total Words')
            st.title(len(words))
        with col3:
            st.header('Total Media')
            st.title(no_media_messages)
        with col4:
            st.header('Total Links')
            st.title(links)

#### monthly timeline# monthly timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user,df)
        fig,ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'],color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

### weekday activity
    st.title("Weekday Activity")
    activity=helper.week_activity_map(selected_user,df)
    fig,ax=plt.subplots()
    ax.plot(activity.index,activity.values,color='orange')
    plt.xticks(rotation='vertical')
    st.pyplot(fig)

### Activity timings
    st.title("Weekly Activity Map")
    user_heatmap = helper.activity_heatmap(selected_user, df)
    fig, ax = plt.subplots()
    ax = sns.heatmap(user_heatmap)
    st.pyplot(fig)

    #### top 5 most active users and percentage of msg by every user

    if selected_user=='Group Chat':

        st.title('Active Users')
        x,df2=helper.most_busy_users(df)

        fig,ax=plt.subplots()
        col1,col2=st.columns(2)

        with col1:
            ax.bar(x.index,x.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.dataframe(df2)

### most common words
    most_common_df = helper.most_common_words(selected_user, df)

    fig, ax = plt.subplots()

    ax.barh(most_common_df[0], most_common_df[1],color='red')
    plt.xticks(rotation='vertical')

    st.title('Most commmon words')
    st.pyplot(fig)

#### emoji

    emoji_df = helper.emoji_helper(selected_user,df)
    st.title("Emoji Analysis")

    col1,col2 = st.columns(2)

    with col1:
        st.dataframe(emoji_df)
    with col2:
        fig, ax = plt.subplots()
        ax.pie(emoji_df['Count'].head(), labels=emoji_df['Emoji'].head(), autopct="%0.2f")
        st.pyplot(fig)


