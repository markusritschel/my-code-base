# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Author: Markus Ritschel
# eMail:  git@markusritschel.de
# Date:   2024-08-15
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#
import logging

import numpy as np
import scipy.stats


log = logging.getLogger(__name__)


def t_statistic(r, dof):
    """
    Calculate the t-statistic for a given correlation coefficient and number of effective samples.

    The formula is given by:

    .. math::
        t_\\text{score} = r \\cdot \\frac{ \\sqrt{dof} }{ \\sqrt{1 - r^2} } 
                        = r \\cdot \\frac{ \\sqrt{n_\\text{eff}-2} }{ \\sqrt{1 - r^2} }

    where $r$ is the Pearson correlation coefficient, $dof$ is the number of degrees of freedom, 
    typicallyt he number of effective sample size - 2.

    Source: https://en.wikipedia.org/wiki/Student%27s_t-test

    Parameters
    ----------
    r : float
        The correlation coefficient.
    dof : float
        The degrees of freedom. Typically the number of effective samples - 2.

    Returns
    -------
    float
        The t-statistic.
    """
    return r * np.sqrt(dof) / np.sqrt(1 - r**2)


def tstats_p_value(t, dof):
    """
    Calculate the p-value for a given t-statistic and number of degrees of freedom.

    The formula is given by:

    .. math::
        f_p &= 2 \\cdot (1 - \\text{cdf}(t, dof)) \\\\
            &= 2 \\cdot \\text{sf}(t, dof)

    ``sf`` is the survival function of the t-distribution from :obj:`scipy.stats.t` 
    and is equivalent to ``1-cdf``.
    The number of degrees of freedom (dof) is typically the number of effective samples - 2.


    Parameters
    ----------
    t : float
        The t-statistic.
    dof : float
        The number of effective samples.

    Returns
    -------
    float
        The p-value.
    """
    return 2 * scipy.stats.t.sf(t, dof)
