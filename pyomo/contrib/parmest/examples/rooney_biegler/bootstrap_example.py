#  ___________________________________________________________________________
#
#  Pyomo: Python Optimization Modeling Objects
#  Copyright (c) 2008-2024
#  National Technology and Engineering Solutions of Sandia, LLC
#  Under the terms of Contract DE-NA0003525 with National Technology and
#  Engineering Solutions of Sandia, LLC, the U.S. Government retains certain
#  rights in this software.
#  This software is distributed under the 3-clause BSD License.
#  ___________________________________________________________________________

from pyomo.common.dependencies import pandas as pd
import pyomo.contrib.parmest.parmest as parmest
from pyomo.contrib.parmest.examples.rooney_biegler.rooney_biegler import (
    RooneyBieglerExperiment,
)


def main():

    # Data
    data = pd.DataFrame(
        data=[[1, 8.3], [2, 10.3], [3, 19.0], [4, 16.0], [5, 15.6], [7, 19.8]],
        columns=['hour', 'y'],
    )

    # Sum of squared error function
    def SSE(model):
        expr = (
            model.experiment_outputs[model.y]
            - model.response_function[model.experiment_outputs[model.hour]]
        ) ** 2
        return expr

    # Create an experiment list
    exp_list = []
    for i in range(data.shape[0]):
        exp_list.append(RooneyBieglerExperiment(data.loc[i, :].to_frame().transpose()))

    # View one model
    # exp0_model = exp_list[0].get_labeled_model()
    # print(exp0_model.pprint())

    # Create an instance of the parmest estimator
    pest = parmest.Estimator(exp_list, obj_function=SSE)

    # Parameter estimation
    obj, theta = pest.theta_est()

    # Parameter estimation with bootstrap resampling
    bootstrap_theta = pest.theta_est_bootstrap(50, seed=4581)

    # Plot results
    parmest.graphics.pairwise_plot(bootstrap_theta, title='Bootstrap theta')
    parmest.graphics.pairwise_plot(
        bootstrap_theta,
        theta,
        0.8,
        ['MVN', 'KDE', 'Rect'],
        title='Bootstrap theta with confidence regions',
    )


if __name__ == "__main__":
    main()
