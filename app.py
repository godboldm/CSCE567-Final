import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.figure_factory as ff
import numpy as np
import base64

import utils as ut

def get_data(filename):
    data = pd.read_csv(filename)
    return data

# Config

st.set_page_config(layout='centered', 
    initial_sidebar_state='expanded', 
    page_title='Data Fueled Insights',
    page_icon='icons/tab_logo.png',
    menu_items={
        'About': '# A Data Visualization Dashboard for Formula 1'
    })
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


home = st.container()
drivers = st.container()
constructors = st.container()
references = st.container()
data = st.container()

st.sidebar.image("icons/logo.png")

st.sidebar.markdown("---")

page = st.sidebar.selectbox("App Navigation", ["Home", "Drivers", "Constructors", "Data", "References"])

driver_data = get_data('data/drivers.csv')
constructor_data = get_data('data/constructors.csv')
grand_prix_data = get_data('data/grand_prix.csv')
pits_data = get_data('data/pits.csv')
position_data = get_data('data/net_positions.csv')
points_data = get_data('data/points.csv')
distrabution_data = get_data('data/distrabution.csv')

if page == "Home":
    with home:
            st.title("Data Fueled Insights: Analyzing Formula 1 Through Interactive Visualizations")
            st.markdown('''Formula 1 has been renowned as the pinnacle of motorsports for the past 70 years.
                Its single seat, open-wheel, open cockpit, high-tech race cars are a marvel of engineering, 
                both mechanically and aerodynamically. However, while many fans appreciate the speed and skill 
                of the drivers, few are aware of the incredible amount of data collected from the cars, tracks, 
                drivers, and pits. 
                In fact, the sheer amount of data collected is a masterful conduction of data collection and 
                correlation. By communicating this data to its audience, Formula 1 can offer fans a deeper understanding 
                of the sport, allowing them to explore their favorite drivers, constructors, and tracks in a way 
                incomparable to any other sport. With so much data available, it's no surprise that fans are eager 
                to get their hands on it. By creating a data visualization dashboard, fans can explore and analyze the data, 
                gaining valuable insights into the performance of their favorite drivers and constructors. From lap times and 
                tire wear to fuel consumption and engine performance, the possibilities are endless. By providing fans with this 
                level of insight, Formula 1 is not only enhancing the fan experience, but also providing valuable data that can be 
                used to improve the performance of the cars and drivers themselves.''')
            st.video('https://www.youtube.com/watch?v=mdnF9R-Bzpg')

elif page == "Drivers":
    with drivers:
            st.title("Drivers")
            st.markdown('''Formula 1 is a unique sport in that the competition is multifaceted. There are two main competition levels: the 
                driver and the constructor. On the driver level, there are twenty drivers that compete for points (earned based on finishing position) 
                that go towards winning the Driver’s Championship.''')
            st.markdown("### Driver Success")
            st.markdown("A bar chart comparing the driver vs. their wins and points per grand prix.")
            driver_bar_option = st.radio("Select if you want to view wins or points.", ['Points', 'Wins'])
            driver_bar_fig = go.Figure(data=[go.Bar(x=driver_data['Driver'], y=driver_data[driver_bar_option])])
            st.plotly_chart(driver_bar_fig)
            st.markdown("### Driver Conversions")
            st.markdown("A diverging bar chart showing the drivers conversions per grand prix.")
            driver_div_option = st.selectbox("Driver", position_data['Driver'].unique())
            filtered_driver_data = position_data[position_data['Driver'] == driver_div_option]
            driver_div_fig = go.Figure(go.Bar(y=filtered_driver_data['Grand Prix'], x=filtered_driver_data['Net Positions'], name='Positions Gained', orientation='h'))
            st.markdown("*Note: To see all Grand Prix's on the y-axis, use the expander located in the top right of the chart on hover.*")
            st.plotly_chart(driver_div_fig)
            st.markdown("### Pit Duration")
            st.markdown("A pie chart will be used to show the time the driver spent in the pit during the total duration of the race.")
            grand_prixs_1 = pits_data['Grand Prix'].unique().tolist()
            selected_grand_prix_1 = st.selectbox('Select a grand prix:', grand_prixs_1)
            filtered_df_1 = pits_data[pits_data['Grand Prix'] == selected_grand_prix_1]
            pull_list = filtered_df_1['Pit Time'].tolist()
            pull_list_max = pull_list.index(max(pull_list))
            for i in range(len(pull_list)):
                if i == pull_list_max:
                    pull_list[i] = 0.2
                else:
                    pull_list[i] = 0.0
            driver_pie_fig = go.Figure(data=[go.Pie(labels=filtered_df_1['Driver'], values=filtered_df_1['Pit Time'], pull=pull_list)])
            st.markdown("*Note: To see all driver's names in the ledgend, use the expander located in the top right of the chart on hover.*")
            st.plotly_chart(driver_pie_fig)

elif page == "Constructors":
    with constructors:
            st.title("Constructors")
            st.markdown('''Formula 1 is a unique sport in that the competition is multifaceted. There are two main
                competition levels: the driver and the constructor. On the constructor level, the ten constructors (comprised of two drivers each)
                compete for team points which are based on the points earned by your two drivers. For this
                reason, I plan to create a dashboard that is separated into two main pages, one for drivers and
                one for constructors.''')
            st.markdown("### Constructors Success")
            st.markdown("A bar chart comparing the constructor wins and points vs other constructors per grand prix or all time.")
            constructor_bar_option = st.radio("Select if you want to view wins or points.", ['Points', 'Wins'])
            constructor_bar_fig = go.Figure(data=[go.Bar(x=constructor_data['Constructor'], y=constructor_data[constructor_bar_option])]) 
            st.plotly_chart(constructor_bar_fig)
            st.markdown("### Mapping the Team")
            st.markdown("Map placing the nationality of each of its drivers.")
            constructor_map_fig = px.scatter_geo(driver_data,
                                                lat='Lat',
                                                lon='Long',
                                                hover_name='Driver',
                                                color=driver_data['Constructor'],
                                                color_continuous_scale=px.colors.qualitative.Pastel,
                                                projection='natural earth',
                                                size='Points',
                                                title='F1 Drivers Nationality and Points')
            st.plotly_chart(constructor_map_fig)
            st.markdown("### Points Garnered")
            st.markdown("A histogram showing which races garnered the most points for the team in a season or all time.")
            constructor_hist_option = st.selectbox("Select a constructor:", points_data['Constructor'].unique())
            filtered_constructor_hist_data = pd.DataFrame({'Grand Prix': distrabution_data['Grand Prix'], 'Total Points': distrabution_data[constructor_hist_option]})
            contructor_hist_fig = px.histogram(filtered_constructor_hist_data, x='Grand Prix', y='Total Points')
            st.plotly_chart(contructor_hist_fig)


elif page == "Data":
    with data:
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Drivers", "Constructors", "Grand Prix", "Pits", "Position", "Points"])
        tab1.dataframe(driver_data)
        tab2.dataframe(constructor_data)
        tab3.dataframe(grand_prix_data)
        tab4.dataframe(pits_data)
        tab5.dataframe(position_data)
        tab6.dataframe(points_data)


elif page == "References":
    with references:
        st.title("References")
        def show_pdf(file_path):
            with open(file_path,"rb") as f:
                base64_pdf = base64.b64encode(f.read()).decode('utf-8')
            pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="800" height="800" type="application/pdf"></iframe>'
            st.markdown(pdf_display, unsafe_allow_html=True)

        st.markdown("## Midterm")
        show_pdf('Midterm.pdf')
        
        st.markdown("## Final")
        show_pdf('FinalV2.pdf')

st.sidebar.write('Created by Matthew Godbold to satisfy the requirements of CSCE567 - Visualization Tools.')