#!/usr/bin/env python

#
# LSST Data Management System
# Copyright 2008, 2009, 2010 LSST Corporation.
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
import os
import unittest
import lsst.utils.tests as utilsTests
import lsst.pex.config as pexConfig


class Config1(pexConfig.Config):
    f = pexConfig.Field("f", float, default=3.0)


class Config2(pexConfig.Config):
    d1 = pexConfig.ConfigDictField("d1", keytype=str, itemtype=Config1, itemCheck=lambda x: x.f > 0)


class ConfigDictFieldTest(unittest.TestCase):

    def testConstructor(self):
        try:
            class BadKeytype(pexConfig.Config):
                d = pexConfig.ConfigDictField("...", keytype=list, itemtype=Config1)
        except:
            pass
        else:
            raise SyntaxError("Unsupported keytypes should not be allowed")

        try:
            class BadItemtype(pexConfig.Config):
                d = pexConfig.ConfigDictField("...", keytype=int, itemtype=dict)
        except:
            pass
        else:
            raise SyntaxError("Unsupported itemtypes should not be allowed")

        try:
            class BadItemCheck(pexConfig.Config):
                d = pexConfig.ConfigDictField("...", keytype=str, itemtype=Config1, itemCheck=4)
        except:
            pass
        else:
            raise SyntaxError("Non-callable itemCheck should not be allowed")

        try:
            class BadDictCheck(pexConfig.Config):
                d = pexConfig.DictField("...", keytype=int, itemtype=Config1, dictCheck=4)
        except:
            pass
        else:
            raise SyntaxError("Non-callable dictCheck should not be allowed")

    def testAssignment(self):
        c = Config2()
        self.assertRaises(pexConfig.FieldValidationError, setattr, c, "d1", {3: 3})
        self.assertRaises(pexConfig.FieldValidationError, setattr, c, "d1", {"a": 0})
        self.assertRaises(pexConfig.FieldValidationError, setattr, c, "d1", [1.2, 3, 4])
        c.d1 = None
        c.d1 = {"a": Config1, "b": Config1()}

    def testValidate(self):
        c = Config2()
        self.assertRaises(pexConfig.FieldValidationError, Config2.validate, c)

        c.d1 = {"a": Config1(f=0)}
        self.assertRaises(pexConfig.FieldValidationError, Config2.validate, c)

        c.d1["a"].f = 5
        c.validate()

    def testInPlaceModification(self):
        c = Config2(d1={})
        self.assertRaises(pexConfig.FieldValidationError, c.d1.__setitem__, 1, 0)
        self.assertRaises(pexConfig.FieldValidationError, c.d1.__setitem__, "a", 0)
        c.d1["a"] = Config1(f=4)
        self.assertEqual(c.d1["a"].f, 4)

    def testSave(self):
        c = Config2(d1={"a": Config1(f=4)})
        c.save("configDictTest.py")

        rt = Config2()
        rt.load("configDictTest.py")

        os.remove("configDictTest.py")
        self.assertEqual(rt.d1["a"].f, c.d1["a"].f)

        c = Config2()
        c.save("emptyConfigDictTest.py")
        rt.load("emptyConfigDictTest.py")
        os.remove("emptyConfigDictTest.py")

        self.assertEqual(rt.d1, None)

    def testToDict(self):
        c = Config2(d1={"a": Config1(f=4), "b": Config1})
        dict_ = c.toDict()
        self.assertEqual(dict_, {"d1": {"a": {"f": 4.0}, "b": {"f": 3.0}}})

    def testFreeze(self):
        c = Config2(d1={"a": Config1(f=4), "b": Config1})
        c.freeze()

        self.assertRaises(pexConfig.FieldValidationError, setattr, c.d1["a"], "f", 0)

    def testNoArbitraryAttributes(self):
        c = Config2(d1={})
        self.assertRaises(pexConfig.FieldValidationError, setattr, c.d1, "should", "fail")


def suite():
    utilsTests.init()
    suites = []
    suites += unittest.makeSuite(ConfigDictFieldTest)
    suites += unittest.makeSuite(utilsTests.MemoryTestCase)
    return unittest.TestSuite(suites)


def run(exit=False):
    utilsTests.run(suite(), exit)

if __name__ == '__main__':
    run(True)
