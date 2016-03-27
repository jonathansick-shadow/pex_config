#/usr/bin/env python

#
# LSST Data Management System
# Copyright 2008-2015 AURA/LSST.
#
# This product includes software developed by the
# LSST Project (http://www.lsst.org/).
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
# You should have received a copy of the LSST License Statement and
# the GNU General Public License along with this program.  If not,
# see <http://www.lsstcorp.org/LegalNotices/>.
#

import unittest
import lsst.utils.tests as utilsTests
import lsst.pex.config as pexConfig
import lsst.pex.config.history as pexConfigHistory


class TestConfig(pexConfig.Config):
    a = pexConfig.Field('Parameter A', float, default=1.0)


class HistoryTest(unittest.TestCase):

    def testHistory(self):
        b = TestConfig()
        b.update(a=4.0)
        pexConfigHistory.Color.colorize(False)
        output = b.formatHistory("a", writeSourceLine=False)
        comparison = """a
1.0 run(True)
    utilsTests.run(suite(), exit)
    if unittest.TextTestRunner().run(suite).wasSuccessful():
    test(result)
    return self.run(*args, **kwds)
    test(result)
    return self.run(*args, **kwds)
    testMethod()
    b = TestConfig()
    a = pexConfig.Field('Parameter A', float, default=1.0)
4.0 run(True)
    utilsTests.run(suite(), exit)
    if unittest.TextTestRunner().run(suite).wasSuccessful():
    test(result)
    return self.run(*args, **kwds)
    test(result)
    return self.run(*args, **kwds)
    testMethod()
    b.update(a=4.0)"""
        self.assertEqual(output, comparison)


def suite():
    utilsTests.init()
    suites = []
    suites += unittest.makeSuite(HistoryTest)
    return unittest.TestSuite(suites)


def run(exit=False):
    utilsTests.run(suite(), exit)

if __name__ == '__main__':
    run(True)
