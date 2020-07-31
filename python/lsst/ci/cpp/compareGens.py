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
import lsst.afw.math as afwMath
import lsst.pipe.base as pipeBase


__all__ = ["compareExposures"]


def compareExposures(exp1, exp2):
    """Compare two images for equivalence.

    Parameters
    ----------
    exp1 : `lsst.afw.image.Exposure`
        First image to compare.
    exp2 : `lsst.afw.image.Exposure`
        Second image to compare.

    Returns
    -------
    result : `lsst.pipe.base.Struct`
        Struct containing results.
    """
    mi1 = exp1.getMaskedImage()
    mi2 = exp2.getMaskedImage()
    diff = mi1
    diff -= mi2

    statsIm = afwMath.makeStatistics(diff.getImage(), afwMath.MEAN | afwMath.MEDIAN
                                     | afwMath.VARIANCE | afwMath.IQRANGE)
    statsMask = afwMath.makeStatistics(diff.getMask(), afwMath.SUM)
    statsVar = afwMath.makeStatistics(diff.getVariance(), afwMath.MEAN | afwMath.MEDIAN
                                      | afwMath.VARIANCE | afwMath.IQRANGE)
    imageStats = (statsIm.getValue(afwMath.MEAN),
                  statsIm.getValue(afwMath.MEDIAN),
                  statsIm.getValue(afwMath.VARIANCE),
                  statsIm.getValue(afwMath.IQRANGE))
    maskStats = (statsMask.getValue(afwMath.SUM))
    varianceStats = (statsVar.getValue(afwMath.MEAN),
                     statsVar.getValue(afwMath.MEDIAN),
                     statsVar.getValue(afwMath.VARIANCE),
                     statsVar.getValue(afwMath.IQRANGE))

    return pipeBase.Struct(
        mi1=mi1,
        mi2=mi2,
        diff=diff,
        imageStats=imageStats,
        maskStats=maskStats,
        varianceStats=varianceStats
    )
