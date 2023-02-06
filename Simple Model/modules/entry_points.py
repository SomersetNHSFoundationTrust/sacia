import pandas as pd
import numpy as np


def get_new_patients(data, day, startup=False, start_up_n=0):
    """

    :param weekday:
    :return:
    """

    weekday = pd.to_datetime(day).strftime('%A')

    n = 0

    if weekday == "Monday":
        n = np.random.normal(data[0][0],
                             data[1][0],
                             size=1)
    elif weekday == "Tuesday":
        n = np.random.normal(data[0][1],
                             data[1][1],
                             size=1)
    elif weekday == "Wednesday":
        n = np.random.normal(data[0][2],
                             data[1][2],
                             size=1)
    elif weekday == "Thursday":
        n = np.random.normal(data[0][3],
                             data[1][3],
                             size=1)
    elif weekday == "Friday":
        n = np.random.normal(data[0][4],
                             data[1][4],
                             size=1)
    elif weekday == "Saturday":
        n = np.random.normal(data[0][5],
                             data[1][5],
                             size=1)
    elif weekday == "Sunday":
        n = np.random.normal(data[0][6],
                             data[1][6],
                             size=1)

    if startup:
        n = start_up_n

    if n < 1:
        new_patients = pd.DataFrame(columns=['los'])
    else:
        new_patients = pd.DataFrame(np.random.exponential(scale=data[2],
                                                          size=int(n)).astype(int),
                                    columns=['los'])

    return new_patients
