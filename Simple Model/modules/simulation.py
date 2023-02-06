import pandas as pd
from modules.misc import *
from modules.entry_points import *


def simulation(number_of_sims, s_d, e_d):
    """

    :param number_of_sims:
    :param s_d:
    :param e_d:
    :return:
    """

    final_results = pd.DataFrame(columns=['iter', 'ds', 'avg_los', 'admissions', 'occupied', 'discharges'])

    for q in range(0, len(s_d)):

        df = data(limit=s_d[q])

        for e in range(0, number_of_sims):

            sim_dates = pd.date_range(start=s_d[q],
                                      end=e_d[q],
                                      freq='d')

            sim_dates = [i_.strftime('%d/%m/%Y') for i_ in sim_dates]

            inpatient_list = pd.DataFrame(columns=['los'])

            for i in range(0, len(sim_dates)):

                if i == 0:

                    inpatient_list = get_new_patients(df, i, startup=True, start_up_n=514)
                    admissions = int(df[3].values)
                    discharges = len(inpatient_list[inpatient_list['los'] == 0])
                    inpatient_list['los'] = inpatient_list['los']-1

                else:

                    xy = get_new_patients(df, i)
                    admissions = len(xy[xy['los'] > 0])

                    inpatient_list = pd.concat([inpatient_list, xy])

                    discharges = len(inpatient_list[inpatient_list['los'] < 1])
                    inpatient_list = inpatient_list[inpatient_list['los'] > 0]
                    inpatient_list['los'] = inpatient_list['los']-1

                if inpatient_list.empty:
                    newdata = {
                        "iter": e,
                        "ds": sim_dates[i],
                        "avg_los": int(inpatient_list.los.mean()),
                        "admissions": admissions,
                        "occupied": len(inpatient_list),
                        "discharges": discharges,
                    }
                else:

                    newdata = {
                        "iter": e,
                        "ds": sim_dates[i],
                        "avg_los": int(inpatient_list.los.mean()),
                        "admissions": admissions,
                        "occupied": len(inpatient_list),
                        "discharges": discharges,
                    }

                final_results = final_results.append(newdata, ignore_index=True)

    return final_results
