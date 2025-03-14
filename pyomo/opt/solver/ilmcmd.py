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

import re
import sys
import os
import subprocess

import pyomo.common
from pyomo.common.errors import ApplicationError

import pyomo.opt.solver.shellcmd
from pyomo.opt.solver.shellcmd import SystemCallSolver


class ILMLicensedSystemCallSolver(SystemCallSolver):
    """A command line solver that launches executables licensed with ILM"""

    def __init__(self, **kwds):
        """Constructor"""
        pyomo.opt.solver.shellcmd.SystemCallSolver.__init__(self, **kwds)

    def available(self, exception_flag=False):
        """True if the solver is available"""
        if self._assert_available:
            return True
        if not pyomo.opt.solver.shellcmd.SystemCallSolver.available(
            self, exception_flag
        ):
            return False
        executable = pyomo.common.Executable("ilmlist")
        if executable:
            try:
                cmd = [executable.path()]
                if sys.platform[0:3] == "win":
                    # on windows, the ilm license manager by default
                    # pauses after displaying the token status, so that
                    # the window doesn't disappear and the user can
                    # actually read it. however, if we don't suppress
                    # this behavior, this command will stall until the
                    # user hits Ctrl-C.
                    cmd.append("-batch")
                result = subprocess.run(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    universal_newlines=True,
                )
            except OSError:
                msg = sys.exc_info()[1]
                raise ApplicationError(
                    "Could not execute the command: ilmtest\n\tError message: " + msg
                )
            sys.stdout.flush()
            for line in result.stdout.split("\n"):
                tokens = re.split('[\t ]+', line.strip())
                if (
                    len(tokens) == 5
                    and tokens[0] == 'tokens'
                    and tokens[1] == 'reserved:'
                    and tokens[4] == os.environ.get('USER', None)
                ):
                    if not (tokens[2] == 'none' or tokens[2] == '0'):
                        return True
                    return False
                elif (
                    len(tokens) == 3
                    and tokens[0] == 'available'
                    and tokens[1] == 'tokens:'
                ):
                    if tokens[2] == '0':
                        return False
                    break
                elif (
                    len(tokens) == 6 and tokens[1] == 'server' and tokens[5] == 'DOWN.'
                ):
                    return False
        return True
