import streamlit as st
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import RendererAgg
st.title('Wissend Data Vizualisation')
uploaded_file = st.file_uploader("Choose the file to upload...", type="csv")
if uploaded_file is not None:
    if st.button("Submit"):
        print('CSV File::', uploaded_file)
        df_dep = pd.read_csv(uploaded_file)
        st.markdown("""
        This app performs simple visualization from the open data!
        """)
        st.write(df_dep)
        # st.write(df_pol_par)
        print(df_dep)
        st.sidebar.header('Select what to display')
        status_list = df_dep['Status'].unique().tolist()
        status_list_selected = st.sidebar.multiselect('Description Status', status_list, status_list)
        status_value = df_dep['Status'].value_counts()
        nb_mbrs = st.sidebar.slider("Number of Status", int(status_value.min()), int(status_value.max()), (int(status_value.min()), int(status_value.max())), 1)

        #creates masks from the sidebar selection widgets
        mask_status = df_dep['Status'].isin(status_list_selected)
        #get the parties with a number of members in the range of nb_mbrs
        mask_mbrs = df_dep['Status'].value_counts().between(nb_mbrs[0], nb_mbrs[1]).to_frame()
        mask_mbrs= mask_mbrs[mask_mbrs['Status'] == 1].index.to_list()
        mask_mbrs= df_dep['Status'].isin(mask_mbrs)

        df_dep_filtered = df_dep[mask_status & mask_mbrs]
        # st.title('Filtered Data')
        # st.write(df_dep_filtered)

        matplotlib.use("agg")
        _lock = RendererAgg.lock

        pol_par = df_dep_filtered['Status'].value_counts()
        try:
            DataType_ct = df_dep_filtered['DataType'].value_counts()
        except:
            DataType_ct = df_dep_filtered['Data Type'].value_counts()
        #merge the two dataframe to get a column with the color
        df = pd.DataFrame(pol_par)
        df_datatype = pd.DataFrame(DataType_ct)
        # colors = df['color'].tolist()

        row0_spacer1, row0_1, row0_spacer2, row0_2, row0_spacer3 = st.columns((0.2, 1, .2, 1, .2))
        with row0_1, _lock:
            st.header("Status Coverage")
            fig, ax = plt.subplots(figsize=(5, 5))
            ax.pie(pol_par, labels=(pol_par.index + ' (' + pol_par.map(str)
            + ')'), wedgeprops = { 'linewidth' : 7, 'edgecolor' : 'white'
            })
            p = plt.gcf()
            p.gca().add_artist(plt.Circle( (0,0), 0.7, color='white'))
            st.pyplot(fig)
        with row0_1, _lock:
            st.header("\nData Type Coverage")
            fig, ax = plt.subplots(figsize=(5, 5))
            ax.pie(DataType_ct, labels=(DataType_ct.index + ' (' + DataType_ct.map(str)
            + ')'), wedgeprops = { 'linewidth' : 7, 'edgecolor' : 'white'
            })
            p = plt.gcf()
            p.gca().add_artist(plt.Circle( (0,0), 0.7, color='white'))
            st.pyplot(fig)