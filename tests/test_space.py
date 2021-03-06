import unittest
from sklearn.datasets import make_sparse_spd_matrix
from nitk import methods
import numpy as np
from nitk.space import *
import rpy2.robjects as robjects
from rpy2.robjects.packages import importr
import rpy2.robjects.numpy2ri
import rpy2.rinterface as rinterface
from sklearn.utils.testing import assert_array_almost_equal
from sklearn.utils.testing import assert_array_less

class TestSPACE(unittest.TestCase):
    def _estimate_precision_matrix_using_r(self, X, l):
        """
        Estimates the precision matrix using the R
        implementation provided by the authors
        """
        rpy2.robjects.numpy2ri.activate()
        space = importr('space')
        prec = space.space_joint(X, np.array([l]))
        prec = np.array(prec[0])

        return prec
    def test_space(self):
        """
        Generates a distribution with a sparse precision matrix and sees if the non-zero values are correctly picked up
        by SPACE
        """
        p = 5
        n = 10
        K = make_sparse_spd_matrix(p, 0.7)
        C = np.linalg.inv(K)
        X = np.random.multivariate_normal(np.zeros(p), C, n)
        l = 0.5
        r_prec = self._estimate_precision_matrix_using_r(X, l)
        sp = SPACE(l)
        sp.fit(X)
        assert_array_almost_equal(r_prec, sp.partial_correlation_, decimal=2)


    def test_space_cv(self):
        """
        Sees how SPACE performs when we use cross validation to select lambda
        """
        p = 50
        n = 10
        K = make_sparse_spd_matrix(p, 0.7)
        C = np.linalg.inv(K)
        X = np.random.multivariate_normal(np.zeros(p), C, n)
        l = 0.5
        sp = SPACECV()
        sp.fit(X)
        print(sp.precision_)

if __name__ == '__main__':
    unittest.main()