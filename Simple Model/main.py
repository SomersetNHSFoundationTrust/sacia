
import streamlit as st
from modules.graphs import *
from modules.simulation import *
from modules.summary_results import *
from modules.misc import *
from streamlit import session_state as ss
import datetime

st.set_page_config(page_title='SACIA',
                   layout='wide',
                   page_icon='📈'
                   )

st.markdown('### Simulated Asynchronous Causal Impact Analysis')

st.image('images/ascia.png')


st.markdown('*Simulated Asynchronous Causal Impact Analysis (SACIA) is a proof-of-concept tool to test the validity '
            'of using a Stochastic Simulation Model in place of Bayesian structural time-series when measuring change '
            'in an inpatient system. The aim of this methodology is three-fold. Firstly we attempt to allow the '
            'influence of confounders to be considered (admissions, los, discharges, occupancy). Secondly the '
            'unpredictability of admissions and LOS. Lastly we want to be able to measure asynchronous changes which '
            'may not be consecutive. Like with all non-experiment based Causal Impact Analysis a strong understanding '
            'of the data is required for interpretation.*')

if 'date_s' not in ss:
    ss.date_s = 0

if 'date_e' not in ss:
    ss.date_e = 0

small_view = st.columns(6)

for i in range(ss.date_s):
    with small_view[i % 6]:
        st.date_input('Change ' + str(i + 1) + ' Begin Date', value=datetime.date(2021, 1, 1), key=f'date_s{i}')
        st.date_input('Change ' + str(i + 1) + ' End Date', value=datetime.date(2021, 1, 1), key=f'date_e{i}')


def add_date():
    """

    :return:
    """
    ss.date_s += 1
    ss.date_e += 1


def remove_date():
    """

    :return:
    """
    ss.date_s -= 1
    ss.date_e -= 1


st.button('Add Change Date',
          on_click=add_date)

st.button('Remove Change Date',
          on_click=remove_date)

s_d, e_d = [], []

for i in range(ss.date_s):
    s_d.append(ss[f'date_s{i}'])
    e_d.append(ss[f'date_e{i}'])

number_of_sims = st.number_input(label='Number of Iterations',
                                 value=10)

ex = st.button('Run')

if ex and not s_d:

    st.warning("You have not entered any dates for querying")

elif ex and s_d:

    final_results = simulation(number_of_sims, s_d, e_d)

    df_plot = prepare_graph_data(data(True), final_results)

    st.info('Simulation vs Actual')
    occupancy, los, admissions, discharges = st.columns((1, 1, 1, 1))

    occupancy.markdown('**Beds Occupied (Actual Rolling 7 Day Mean)**')
    occupancy.plotly_chart(counter_actual(
        df_plot[['ds', 'occupied', 'occupied_mean', 'occupied_max', 'occupied_min']].rename(
            columns={"occupied": "q", "occupied_mean": "x", "occupied_max": "y", "occupied_min": "z"}), s_d, e_d),
        use_container_width=True)
    los.markdown('**Length of Stay (Actual Rolling 7 Day Mean)**')
    los.plotly_chart(counter_actual(df_plot[['ds', 'los', 'los_mean', 'los_max', 'los_min']].rename(
        columns={"los": "q", "los_mean": "x", "los_max": "y", "los_min": "z"}), s_d, e_d),
        use_container_width=True)
    admissions.markdown('**Admissions (Actual Rolling 7 Day Mean)**')
    admissions.plotly_chart(counter_actual(
        df_plot[['ds', 'admissions', 'admissions_mean', 'admissions_max', 'admissions_min']].rename(
            columns={"admissions": "q", "admissions_mean": "x", "admissions_max": "y", "admissions_min": "z"}), s_d,
        e_d),
        use_container_width=True)
    discharges.markdown('**Discharges (Actual Rolling 7 Day Mean)**')
    discharges.plotly_chart(counter_actual(
        df_plot[['ds', 'discharges', 'discharges_mean', 'discharges_max', 'discharges_min']].rename(
            columns={"discharges": "q", "discharges_mean": "x", "discharges_max": "y", "discharges_min": "z"}), s_d,
        e_d),
        use_container_width=True)

    st.info('Point Effects')
    p_occupancy, p_los, p_admissions, p_discharges = st.columns((1, 1, 1, 1))

    df_plot = df_plot.dropna()

    p_occupancy.plotly_chart(
        point_effect(df_plot[['ds', 'occupied', 'occupied_mean', 'occupied_min', 'occupied_max']].rename(
            columns={"occupied": "q", "occupied_mean": "x", "occupied_max": "y", "occupied_min": "z"}), s_d, e_d),
        use_container_width=True)

    p_los.plotly_chart(point_effect(df_plot[['ds', 'los', 'los_mean', 'los_max', 'los_min']].rename(
        columns={"los": "q", "los_mean": "x", "los_max": "y", "los_min": "z"}), s_d, e_d),
        use_container_width=True)

    p_admissions.plotly_chart(
        point_effect(df_plot[['ds', 'admissions', 'admissions_mean', 'admissions_max', 'admissions_min']].rename(
            columns={"admissions": "q", "admissions_mean": "x", "admissions_max": "y", "admissions_min": "z"}), s_d,
            e_d),
        use_container_width=True)

    p_discharges.plotly_chart(
        point_effect(df_plot[['ds', 'discharges', 'discharges_mean', 'discharges_max', 'discharges_min']].rename(
            columns={"discharges": "q", "discharges_mean": "x", "discharges_max": "y", "discharges_min": "z"}), s_d,
            e_d),
        use_container_width=True)

    # Cumulative Section

    st.info('Cumulative')

    c_occupancy, c_los, c_admissions, c_discharges = st.columns((1, 1, 1, 1))

    df_final = df_plot[['ds', 'occupied', 'occupied_mean', 'occupied_min', 'occupied_max']].rename(
        columns={"occupied": "q", "occupied_mean": "x", "occupied_max": "y", "occupied_min": "z"})

    c_occupancy.plotly_chart(cumulative_pointwise(df_final,
                                                  s_d,
                                                  e_d),
                             use_container_width=True)

    c_occupancy.markdown('**Occupied Bed Results**')

    c_occupancy.table(summary_results(df_final))

    s1, s2, s3, s4 = summary_results(df_final,
                                     output='report')

    c_occupancy.markdown(s1 + '  \n ' + s2 + '  \n ' + s3 + '  \n ' + s4)

    df_final = df_plot[['ds', 'los', 'los_mean', 'los_max', 'los_min']].rename(
        columns={"los": "q", "los_mean": "x", "los_max": "y", "los_min": "z"})

    c_los.plotly_chart(cumulative_pointwise(df_final,
                                            s_d,
                                            e_d),
                       use_container_width=True)

    c_los.markdown('**LOS Results**')

    c_los.table(summary_results(df_final))

    s1, s2, s3, s4 = summary_results(df_final,
                                     output='report')

    c_los.markdown('**LOS is not a normal distribution so these results may not** '
                   '**be useful**' + '  \n ' + s1 + '  \n ' + s2 + '  \n ' + s3 + '  \n ' + s4)

    df_final = df_plot[['ds', 'admissions', 'admissions_mean', 'admissions_max', 'admissions_min']].rename(
        columns={"admissions": "q", "admissions_mean": "x", "admissions_max": "y", "admissions_min": "z"})

    c_admissions.plotly_chart(cumulative_pointwise(df_final,
                                                   s_d,
                                                   e_d),
                              use_container_width=True)

    c_admissions.markdown('**Admissions Results**')

    c_admissions.table(summary_results(df_final))

    s1, s2, s3, s4 = summary_results(df_final,
                                     output='report')

    c_admissions.markdown(s1 + '  \n ' + s2 + '  \n ' + s3 + '  \n ' + s4)

    df_final = df_plot[['ds', 'discharges', 'discharges_mean', 'discharges_max', 'discharges_min']].rename(
        columns={"discharges": "q", "discharges_mean": "x", "discharges_max": "y", "discharges_min": "z"})

    c_discharges.plotly_chart(cumulative_pointwise(df_final,
                                                   s_d,
                                                   e_d),
                              use_container_width=True)

    c_discharges.markdown('**Discharges Results**')

    c_discharges.table(summary_results(df_final))

    s1, s2, s3, s4 = summary_results(df_final,
                                     output='report')

    c_discharges.markdown(s1 + '  \n ' + s2 + '  \n ' + s3 + '  \n ' + s4)



    df_final = df_final.to_csv().encode('utf-8')

    st.download_button('Download Results',
                       df_final,
                       file_name='CausalImpactAnalysis.csv')
