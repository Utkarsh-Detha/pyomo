#  ___________________________________________________________________________
#
#  Pyomo: Python Optimization Modeling Objects
#  Copyright (c) 2008-2025
#  National Technology and Engineering Solutions of Sandia, LLC
#  Under the terms of Contract DE-NA0003525 with National Technology and
#  Engineering Solutions of Sandia, LLC, the U.S. Government retains certain
#  rights in this software.
#  This software is distributed under the 3-clause BSD License.
#  ___________________________________________________________________________

"""Re-implementation of example 1 of Quesada and Grossmann.

Re-implementation of Quesada example 2 MINLP test problem in Pyomo
Author: David Bernal <https://github.com/bernalde>.

The expected optimal solution value is -5.512.

Ref:
    Quesada, Ignacio, and Ignacio E. Grossmann.
    'An LP/NLP based branch and bound algorithm
    for convex MINLP optimization problems.'
    Computers & chemical engineering 16.10-11 (1992): 937-947.

    Problem type:    convex MINLP
            size:    1  binary variable
                     2  continuous variables
                     4  constraints


"""

from pyomo.environ import (
    Binary,
    ConcreteModel,
    Constraint,
    Reals,
    Objective,
    RangeSet,
    Var,
    minimize,
    log,
)
from pyomo.common.collections import ComponentMap


class SimpleMINLP(ConcreteModel):
    def __init__(self, *args, **kwargs):
        """Create the problem."""
        kwargs.setdefault('name', 'SimpleMINLP3')
        super(SimpleMINLP, self).__init__(*args, **kwargs)
        m = self

        """Set declarations"""
        I = m.I = RangeSet(1, 2, doc='continuous variables')
        J = m.J = RangeSet(1, 1, doc='discrete variables')

        # initial point information for discrete variables
        initY = {1: 1}
        # initial point information for continuous variables
        initX = {1: 0, 2: 0}

        """Variable declarations"""
        # DISCRETE VARIABLES
        Y = m.Y = Var(J, domain=Binary, initialize=initY)
        # CONTINUOUS VARIABLES
        X = m.X = Var(I, domain=Reals, initialize=initX, bounds=(-0.9, 50))

        """Constraint definitions"""
        # CONSTRAINTS
        m.const1 = Constraint(expr=-X[2] + 5 * log(X[1] + 1) + 3 * Y[1] >= 0)
        m.const2 = Constraint(expr=-X[2] + X[1] ** 2 - Y[1] <= 1)
        m.const3 = Constraint(expr=X[1] + X[2] + 20 * Y[1] <= 24)
        m.const4 = Constraint(expr=2 * X[2] + 3 * X[1] <= 10)

        """Cost (objective) function definition"""
        m.objective = Objective(
            expr=10 * X[1] ** 2 - X[2] + 5 * (Y[1] - 1), sense=minimize
        )
        m.optimal_value = -5.512
        m.optimal_solution = ComponentMap()
        m.optimal_solution[m.X[1]] = 0.20710677582302733
        m.optimal_solution[m.X[2]] = 0.9411320859243828
        m.optimal_solution[m.Y[1]] = 0.0
