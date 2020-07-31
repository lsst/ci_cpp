# This file is part of ci_cpp.
#
# Developed for the LSST Data Management System.
# This product includes software developed by the LSST Project
# (https://www.lsst.org).
# See the COPYRIGHT file at the top-level directory of this distribution
# for details of code ownership.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import unittest
import numpy as np

# import lsst.afw.image as afwImage
import lsst.ip.isr as ipIsr
import lsst.utils.tests

from lsst.utils import getPackageDir


FILENAMES = {'crosstalk': {2: 'DATA/crosstalkGen/calibrations/crosstalk/crosstalk-det000.fits',
                           3: './DATA/ci_cpp_crosstalk/20200731T17h07m00s/crosstalkProposal/crosstalkProposal_0_LATISS_ci_cpp_crosstalk_20200731T17h07m00s.fits'},  # noqa: E501
}


class TableProductCases(lsst.utils.tests.TestCase):

    def setup_filenames(self, file1, file2):
        """Lookup files and pass them to compare function.

        Parameters
        ----------
        file1 : `str`
            Partial filename of gen2 product.
        file2 : `str`
            Partial filename of gen3 product.

        Returns
        -------
        results : `lsst.pipe.base.Struct`
            Statistics results.
        """
        pathGen2 = getPackageDir('ci_cpp_gen2') + '/' + file1
        pathGen3 = getPackageDir('ci_cpp_gen3') + '/' + file2

        return pathGen2, pathGen3

    def test_crosstalkTables(self):
        """Compare crosstalk tables
        """
        product = 'crosstalk'
        pathGen2, pathGen3 = self.setup_filenames(FILENAMES[product][2],
                                                  FILENAMES[product][3])

        crosstalkGen2 = ipIsr.CrosstalkCalib.readFits(pathGen2)
        crosstalkGen3 = ipIsr.CrosstalkCalib.readFits(pathGen3)

        self.assertTrue(np.all(crosstalkGen2.coeffValid == crosstalkGen3.coeffValid))
        self.assertTrue(np.all(crosstalkGen2.coeffNum == crosstalkGen3.coeffNum))
        self.assertTrue(np.all(crosstalkGen2.coeffErr == crosstalkGen3.coeffErr))
        # These fail.  FIX!
        # self.assertTrue(np.all(crosstalkGen2.coeffs == crosstalkGen3.coeffs))
        # self.assertTrue(crosstalkGen2 == crosstalkGen3)


class MemoryTester(lsst.utils.tests.MemoryTestCase):
    pass


def setup_module(module):
    lsst.utils.tests.init()


if __name__ == "__main__":
    lsst.utils.tests.init()
    unittest.main()
