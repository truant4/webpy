import datetime
import os
import sys
import tempfile
import unittest
import warnings

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import web  # noqa: E402


class SqliteDateTest(unittest.TestCase):
    def test_datetimes_round_trip_without_deprecation_warnings(self):
        path = os.path.join(tempfile.mkdtemp(), "dates.db")
        db = web.database(dbn="sqlite", db=path)
        db.query("create table t (id integer primary key, d timestamp, day date)")
        moment = datetime.datetime(2026, 10, 12, 9, 30, 15, 123000)
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            db.insert("t", d=moment, day=moment.date())
            row = list(db.select("t"))[0]
        self.assertEqual([w for w in caught if issubclass(w.category, DeprecationWarning)], [])
        self.assertEqual(row.d, moment)
        self.assertEqual(row.day, moment.date())


if __name__ == "__main__":
    unittest.main()
