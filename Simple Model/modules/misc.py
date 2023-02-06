import pandas as pd
from datetime import timedelta


def prepare_graph_data(original_df, new_df):
    """

    :param df:
    :return:
    """

    new_df = new_df.groupby(by=['iter', 'ds']).agg({'avg_los': 'mean',
                                                    'admissions': 'sum',
                                                    'occupied': 'sum',
                                                    'discharges': 'sum'})

    new_df.reset_index(inplace=True)

    df_output = pd.DataFrame()
    df_output['ds'] = new_df['ds'].unique()

    ## 95th percentiles occupied for upper and lower bound

    df_output['occupied_mean'] = new_df[['ds', 'occupied']].groupby(by=['ds']).mean().values
    df_output['occupied_min'] = new_df[['ds', 'occupied']].groupby(by=['ds']).mean().values - \
                                1.96 * new_df[['ds', 'occupied']].groupby(by=['ds']).std().values
    df_output['occupied_max'] = new_df[['ds', 'occupied']].groupby(by=['ds']).mean().values + \
                                1.96 * new_df[['ds', 'occupied']].groupby(by=['ds']).std().values

    ## 95th percentiles for admissions upper and lower bound

    df_output['admissions_mean'] = new_df[['ds', 'admissions']].groupby(by=['ds']).mean().values
    df_output['admissions_min'] = new_df[['ds', 'admissions']].groupby(by=['ds']).mean().values - \
                                  1.96 * new_df[['ds', 'admissions']].groupby(by=['ds']).std().values
    df_output['admissions_max'] = new_df[['ds', 'admissions']].groupby(by=['ds']).mean().values + \
                                  1.96 * new_df[['ds', 'admissions']].groupby(by=['ds']).std().values

    ## 95th percentiles for discharges upper and lower bound

    df_output['discharges_mean'] = new_df[['ds', 'discharges']].groupby(by=['ds']).mean().values
    df_output['discharges_min'] = new_df[['ds', 'discharges']].groupby(by=['ds']).mean().values - \
                                  1.96 * new_df[['ds', 'discharges']].groupby(by=['ds']).std().values
    df_output['discharges_max'] = new_df[['ds', 'discharges']].groupby(by=['ds']).mean().values + \
                                  1.96 * new_df[['ds', 'discharges']].groupby(by=['ds']).std().values

    ## 95th percentiles for los upper and lower bound

    df_output['los_mean'] = new_df[['ds', 'avg_los']].groupby(by=['ds']).mean().values
    df_output['los_min'] = new_df[['ds', 'avg_los']].groupby(by=['ds']).mean().values - \
                           1.96 * new_df[['ds', 'avg_los']].groupby(by=['ds']).std().values
    df_output['los_max'] = new_df[['ds', 'avg_los']].groupby(by=['ds']).mean().values + \
                           1.96 * new_df[['ds', 'avg_los']].groupby(by=['ds']).std().values

    df_output['ds'] = pd.to_datetime(df_output['ds'], format='%d/%m/%Y')

    original_df['ds'] = pd.to_datetime(original_df['ds'],
                                       format='%d/%m/%Y')

    df_output = pd.merge(left=original_df,
                         right=df_output,
                         how='outer',
                         left_on=['ds'],
                         right_on=['ds'])

    return df_output


def data(original=False, limit=None):
    df = pd.read_excel('modules/data/rawdata.xlsx',
                       sheet_name='admissions')

    los_df = pd.read_excel('modules/data/rawdata.xlsx',
                           sheet_name='los')

    limit = pd.to_datetime(limit)

    df['ds'] = pd.to_datetime(df['ds'])
    los_df['ds'] = pd.to_datetime(los_df['ds'])

    if limit is not None:
        df = df[(df['ds'] < limit) & (df['ds'] >= (limit - timedelta(days=90)))]
        los_df = los_df[(los_df['ds'] < limit) & (los_df['ds'] >= (limit - timedelta(days=90)))]

    if original:
        metrics = df

    else:

        metrics = [[
            df[df['wd'] == 'Monday']['admissions'].mean(),
            df[df['wd'] == 'Tuesday']['admissions'].mean(),
            df[df['wd'] == 'Wednesday']['admissions'].mean(),
            df[df['wd'] == 'Thursday']['admissions'].mean(),
            df[df['wd'] == 'Friday']['admissions'].mean(),
            df[df['wd'] == 'Saturday']['admissions'].mean(),
            df[df['wd'] == 'Sunday']['admissions'].mean(),
        ],
            [
                df[df['wd'] == 'Monday']['admissions'].std(),
                df[df['wd'] == 'Tuesday']['admissions'].std(),
                df[df['wd'] == 'Wednesday']['admissions'].std(),
                df[df['wd'] == 'Thursday']['admissions'].std(),
                df[df['wd'] == 'Friday']['admissions'].std(),
                df[df['wd'] == 'Saturday']['admissions'].std(),
                df[df['wd'] == 'Sunday']['admissions'].std(),

            ],

            los_df['los'].mean(),
            df.tail(1)['admissions'],

        ]

    # Need to add in attrition metric (i.e deaths / transfers)

    return metrics

# %%
