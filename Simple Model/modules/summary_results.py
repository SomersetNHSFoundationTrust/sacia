import pandas as pd
import scipy.stats as stats
import textwrap


def summary_results(df, output='summary'):
    """

    :param df:
    :param output:
    :return:
    """
    alpha = 0.05
    confidence = "{}%".format(int((1 - alpha) * 100))
    post_point_resp = df['q']
    post_point_pred = df["x"]
    post_point_upper = df['y']
    post_point_lower = df['z']

    mean_resp = post_point_resp.mean()
    mean_resp_fmt = int(mean_resp)
    cum_resp = post_point_resp.sum()
    cum_resp_fmt = int(cum_resp)
    mean_pred = post_point_pred.mean()
    mean_pred_fmt = int(post_point_pred.mean())
    cum_pred = post_point_pred.sum()
    cum_pred_fmt = int(cum_pred)
    mean_lower = post_point_lower.mean()
    mean_lower_fmt = int(mean_lower)
    mean_upper = post_point_upper.mean()
    mean_upper_fmt = int(mean_upper)
    mean_ci_fmt = [mean_lower_fmt, mean_upper_fmt]
    cum_lower = post_point_lower.sum()
    cum_lower_fmt = int(cum_lower)
    cum_upper = post_point_upper.sum()
    cum_upper_fmt = int(cum_upper)
    cum_ci_fmt = [cum_lower_fmt, cum_upper_fmt]

    abs_effect = (post_point_resp - post_point_pred).mean()
    abs_effect_fmt = int(abs_effect)
    cum_abs_effect = (post_point_resp - post_point_pred).sum()
    cum_abs_effect_fmt = int(cum_abs_effect)
    abs_effect_lower = (post_point_resp - post_point_lower).mean()
    abs_effect_lower_fmt = int(abs_effect_lower)
    abs_effect_upper = (post_point_resp - post_point_upper).mean()
    abs_effect_upper_fmt = int(abs_effect_upper)
    abs_effect_ci_fmt = [abs_effect_lower_fmt, abs_effect_upper_fmt]
    cum_abs_lower = (post_point_resp - post_point_lower).sum()
    cum_abs_lower_fmt = int(cum_abs_lower)
    cum_abs_upper = (post_point_resp - post_point_upper).sum()
    cum_abs_upper_fmt = int(cum_abs_upper)
    cum_abs_effect_ci_fmt = [cum_abs_lower_fmt, cum_abs_upper_fmt]

    rel_effect = abs_effect / mean_pred * 100
    rel_effect_fmt = "{:.1f}%".format(rel_effect)
    cum_rel_effect = cum_abs_effect / cum_pred * 100
    cum_rel_effect_fmt = "{:.1f}%".format(cum_rel_effect)
    rel_effect_lower = abs_effect_lower / mean_pred * 100
    rel_effect_lower_fmt = "{:.1f}%".format(rel_effect_lower)
    rel_effect_upper = abs_effect_upper / mean_pred * 100
    rel_effect_upper_fmt = "{:.1f}%".format(rel_effect_upper)
    rel_effect_ci_fmt = [rel_effect_lower_fmt, rel_effect_upper_fmt]
    cum_rel_effect_lower = cum_abs_lower / cum_pred * 100
    cum_rel_effect_lower_fmt = "{:.1f}%".format(cum_rel_effect_lower)
    cum_rel_effect_upper = cum_abs_upper / cum_pred * 100
    cum_rel_effect_upper_fmt = "{:.1f}%".format(cum_rel_effect_upper)
    cum_rel_effect_ci_fmt = [cum_rel_effect_lower_fmt,
                             cum_rel_effect_upper_fmt]

    std_pred = post_point_pred.std()
    z_score = (post_point_resp.mean()-mean_pred) / std_pred
    p_value = stats.norm.cdf(z_score)
    prob_causal = (1 - p_value)
    p_value_perc = p_value * 100
    prob_causal_perc = prob_causal * 100

    summary = [
        [str(mean_resp_fmt), str(cum_resp_fmt)],
        [str(mean_pred_fmt), str(cum_pred_fmt)],
        [str(mean_ci_fmt), str(cum_ci_fmt)],
        [str(abs_effect_fmt), str(cum_abs_effect_fmt)],
        [str(abs_effect_ci_fmt), str(cum_abs_effect_ci_fmt)],
        [str(rel_effect_fmt), str(cum_rel_effect_fmt)],
        [str(rel_effect_ci_fmt), str(cum_rel_effect_ci_fmt)],
        ["{:.1f}%".format(p_value_perc), ''],
        ["{:.1f}%".format(prob_causal_perc), '']
    ]
    summary = pd.DataFrame(summary, columns=["Average", "Cumulative"],
                           index=["Actual",
                                  "Predicted",
                                  "95% CI",
                                  "Absolute Effect",
                                  "95% CI",
                                  "Relative Effect",
                                  "95% CI",
                                  "P-value",
                                  "Prob. of Causal Effect"
                                  ])

    if output == "summary":
        # Posterior inference {CausalImpact}
        summary = [
            [str(mean_resp_fmt), str(cum_resp_fmt)],
            [str(mean_pred_fmt), str(cum_pred_fmt)],
            [str(mean_ci_fmt), str(cum_ci_fmt)],
            [str(abs_effect_fmt), str(cum_abs_effect_fmt)],
            [str(abs_effect_ci_fmt), str(cum_abs_effect_ci_fmt)],
            [str(rel_effect_fmt), str(cum_rel_effect_fmt)],
            [str(rel_effect_ci_fmt), str(cum_rel_effect_ci_fmt)],
            ["{:.1f}%".format(p_value_perc), ''],
            ["{:.1f}%".format(prob_causal_perc), '']
        ]
        summary = pd.DataFrame(summary, columns=["Average", "Cumulative"],
                               index=["Actual",
                                      "Predicted",
                                      "95% CI",
                                      "Absolute Effect",
                                      "95% CI",
                                      "Relative Effect",
                                      "95% CI",
                                      "P-value",
                                      "Prob. of Causal Effect"
                                      ])
        return summary

    elif output == "report":
        sig = (not ((cum_rel_effect_lower < 0) and
                    (cum_rel_effect_upper > 0)))
        pos = cum_rel_effect > 0
        # Summarize averages
        stmt = textwrap.dedent("""
                          During the post-intervention period, the response
                          variable had an average value of
                          approx. {mean_resp}.
                          """.format(mean_resp=mean_resp_fmt))
        if sig:
            stmt += " By contrast, in "
        else:
            stmt += " In "

        stmt += textwrap.dedent("""
                    the absence of an intervention, we would have
                    expected an average response of {mean_pred}. The
                    {confidence} interval of this counterfactual
                    prediction is [{mean_lower}, {mean_upper}].
                    Subtracting this prediction from the observed
                    response yields an estimate of the causal effect
                    the intervention had on the response variable.
                    This effect is {abs_effect} with a
                    {confidence} interval of [{abs_lower},
                    {abs_upper}]. For a discussion of the
                    significance of this effect,
                    see below.
                    """.format(mean_pred=mean_pred_fmt,
                               confidence=confidence,
                               mean_lower=mean_lower_fmt,
                               mean_upper=mean_upper_fmt,
                               abs_effect=abs_effect_fmt,
                               abs_upper=abs_effect_upper_fmt,
                               abs_lower=abs_effect_lower_fmt))
        # Summarize sums
        stmt2 = textwrap.dedent("""
                    Summing up the individual data points during the
                    post-intervention period (which can only sometimes be
                    meaningfully interpreted), the response variable had an
                    overall value of {cum_resp}.
                    """.format(cum_resp=cum_resp_fmt))
        if sig:
            stmt2 += " By contrast, had "
        else:
            stmt2 += " Had "

        stmt2 += textwrap.dedent("""
                    the intervention not taken place, we would have expected
                    a sum of {cum_resp}. The {confidence} interval of this
                    prediction is [{cum_pred_lower}, {cum_pred_upper}]
                    """.format(cum_resp=cum_resp_fmt,
                               confidence=confidence,
                               cum_pred_lower=cum_lower_fmt,
                               cum_pred_upper=cum_upper_fmt))

        # Summarize relative numbers (in which case row [1] = row [2])
        stmt3 = textwrap.dedent("""
                                    The above results are given in terms
                                    of absolute numbers. In relative terms, the
                                    response variable showed
                                    """)
        if pos:
            stmt3 += " an increase of "
        else:
            stmt3 += " a decrease of "

        stmt3 += textwrap.dedent("""
                            {rel_effect}. The {confidence} interval of this
                            percentage is [{rel_effect_lower},
                            {rel_effect_upper}]
                            """.format(confidence=confidence,
                                       rel_effect=rel_effect_fmt,
                                       rel_effect_lower=rel_effect_lower_fmt,
                                       rel_effect_upper=rel_effect_upper_fmt))

        # Comment on significance
        if sig and pos:
            stmt4 = textwrap.dedent("""
                            This means that the positive effect observed
                            during the intervention period is statistically
                            significant and unlikely to be due to random
                            fluctuations. It should be noted, however, that
                            the question of whether this increase also bears
                            substantive significance can only be answered by
                            comparing the absolute effect {abs_effect} to
                            the original goal of the underlying
                            intervention.
                            """.format(abs_effect=abs_effect_fmt))
        elif sig and not pos:
            stmt4 = textwrap.dedent("""
                            This  means that the negative effect observed
                            during the intervention period is statistically
                            significant. If the experimenter had expected a
                            positive effect, it is recommended to double-check
                            whether anomalies in the control variables may have
                            caused an overly optimistic expectation of what
                            should have happened in the response variable in the
                            absence of the intervention.
                            """)
        elif not sig and pos:
            stmt4 = textwrap.dedent("""
                            This means that, although the intervention
                            appears to have caused a positive effect, this
                            effect is not statistically significant when
                            considering the post-intervention period as a whole.
                            Individual days or shorter stretches within the
                            intervention period may of course still have had a
                            significant effect, as indicated whenever the lower
                            limit of the impact time series (lower plot) was
                            above zero.
                            """)
        elif not sig and not pos:
            stmt4 = textwrap.dedent("""
                            This means that, although it may look as though
                            the intervention has exerted a negative effect on
                            the response variable when considering the
                            intervention period as a whole, this effect is not
                            statistically significant, and so cannot be
                            meaningfully interpreted.
                            """)
        if not sig:
            stmt4 += textwrap.dedent("""
                           The apparent effect could be the result of random
                           fluctuations that are unrelated to the intervention.
                           This is often the case when the intervention period
                           is very long and includes much of the time when the
                           effect has already worn off. It can also be the case
                           when the intervention period is too short to
                           distinguish the signal from the noise. Finally,
                           failing to find a significant effect can happen when
                           there are not enough control variables or when these
                           variables do not correlate well with the response
                           variable during the learning period.""")

        s1, s2, s3, s4 = stmt, stmt2, stmt3, stmt4

        return s1, s2, s3, s4

    else:
        raise ValueError("Output argument must be either 'summary' " +
                         "or 'report'")
