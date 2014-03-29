"""
An interface class for performing and debugging optimization problems.
"""

from distutils.version import StrictVersion
import numpy as np
import scipy

scipy_version = scipy.__version__
scipy_version = StrictVersion(scipy_version.split('.dev')[0])
minimize_version = StrictVersion('0.11')

if scipy_version >= minimize_version:

    scipy_less_0_11 = False
    from scipy.optimize import minimize


else:

    scipy_less_0_11 = True
    from scipy.optimize import fmin_l_bfgs_b


class Optimizer(object):

    def __init__(self, fun,  x0, args=(), method='BFGS', jac=None, hess=None,
                 hessp=None, bounds=None, constraints=(), tol=None,
                 callback=None, options=None, history=False):
        """ A class for handling minimization of scalar function of one or more
        variables.

        Parameters
        ----------
        fun : callable
            Objective function.

        x0 : ndarray
            Initial guess.

        args : tuple, optional
            Extra arguments passed to the objective function and its
            derivatives (Jacobian, Hessian).

        method : str, optional
            Type of solver.  Should be one of

                - 'Nelder-Mead'
                - 'Powell'
                - 'CG'
                - 'BFGS'
                - 'Newton-CG'
                - 'Anneal'
                - 'L-BFGS-B'
                - 'TNC'
                - 'COBYLA'
                - 'SLSQP'
                - 'dogleg'
                - 'trust-ncg'

        jac : bool or callable, optional
            Jacobian of objective function. Only for CG, BFGS, Newton-CG,
            dogleg, trust-ncg.
            If `jac` is a Boolean and is True, `fun` is assumed to return the
            value of Jacobian along with the objective function. If False, the
            Jacobian will be estimated numerically.
            `jac` can also be a callable returning the Jacobian of the
            objective. In this case, it must accept the same arguments as `fun`.

        hess, hessp : callable, optional
            Hessian of objective function or Hessian of objective function
            times an arbitrary vector p.  Only for Newton-CG,
            dogleg, trust-ncg.
            Only one of `hessp` or `hess` needs to be given.  If `hess` is
            provided, then `hessp` will be ignored.  If neither `hess` nor
            `hessp` is provided, then the hessian product will be approximated
            using finite differences on `jac`. `hessp` must compute the Hessian
            times an arbitrary vector.

        bounds : sequence, optional
            Bounds for variables (only for L-BFGS-B, TNC and SLSQP).
            ``(min, max)`` pairs for each element in ``x``, defining
            the bounds on that parameter. Use None for one of ``min`` or
            ``max`` when there is no bound in that direction.

        constraints : dict or sequence of dict, optional
            Constraints definition (only for COBYLA and SLSQP).
            Each constraint is defined in a dictionary with fields:
                type : str
                    Constraint type: 'eq' for equality, 'ineq' for inequality.
                fun : callable
                    The function defining the constraint.
                jac : callable, optional
                    The Jacobian of `fun` (only for SLSQP).
                args : sequence, optional
                    Extra arguments to be passed to the function and Jacobian.
            Equality constraint means that the constraint function result is to
            be zero whereas inequality means that it is to be non-negative.
            Note that COBYLA only supports inequality constraints.

        tol : float, optional
            Tolerance for termination. For detailed control, use solver-specific
            options.

        callback : callable, optional
            Called after each iteration, as ``callback(xk)``, where ``xk`` is
            the current parameter vector.

        options : dict, optional
            A dictionary of solver options. All methods accept the following
            generic options:
                maxiter : int
                    Maximum number of iterations to perform.
                disp : bool
                    Set to True to print convergence messages.
            For method-specific options, see `show_options('minimize', method)`.

        history : bool, optional
            save history of x

        See also
        ---------
        scipy.optimize.minimize
        """

        if scipy_less_0_11:

            if method == 'L-BFGS-B':

                out = fmin_l_bfgs_b(fun, x0, None,
                                    approx_grad=True,
                                    bounds=bounds,
                                    m=options['maxcor'],
                                    factr=options['ftol'] / np.finfo(float).eps,
                                    pgtol=options['gtol'],
                                    epsilon=options['eps'])

                res = {'x':out[0], 'fun':out[1]}

            else:

                msg = 'Only L-BFGS-B is supported in this class for versions'
                msg += 'Scipy < 0.11.'
                raise ValueError(msg)

        if not scipy_less_0_11:

            if history is True:

                def hist(kx):
                    print(kx)

                res = minimize(fun, x0, args, method, jac, hess, hessp, bounds,
                               constraints, tol, callback=hist, options=options)

            else:

                res = minimize(fun, x0, args, method, jac, hess, hessp, bounds,
                               constraints, tol, callback, options)



        self.res = res

    @property
    def xopt(self):

        return self.res['x']

    @property
    def fopt(self):

        return self.res['fun']

    @property
    def nit(self):

        return self.res['nit']

    @property
    def nfev(self):

        return self.res['nfev']

    @property
    def message(self):

        return self.res['message']

    @property
    def info(self):

        print(self.res)









