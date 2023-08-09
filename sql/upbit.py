
SQL_DAILY_CREATE = """
    CREATE TABLE DailyData (
    시장_종목 TEXT NOT NULL,
    시각_UTC TEXT NOT NULL,
    시각_KST TEXT NOT NULL,
    시가 REAL NOT NULL,
    고가 REAL NOT NULL,
    저가 REAL NOT NULL,
    종가 REAL NOT NULL,
    누적거래금액 REAL NOT NULL,
    누적거래량 REAL NOT NULL);
"""
SQL_DAILY_INSERT = """
    INSERT INTO DailyData
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
"""
SQL_DAILY_UPDATE = """
"""
SQL_DAILY_DELETE = """
"""

SQL_MINUTELY_CREATE = """
    CREATE TABLE DailyData (
    시장_종목 TEXT NOT NULL,
    시각_UTC TEXT NOT NULL,
    시각_KST TEXT NOT NULL,
    시가 REAL NOT NULL,
    고가 REAL NOT NULL,
    저가 REAL NOT NULL,
    종가 REAL NOT NULL,
    누적거래금액 REAL NOT NULL,
    누적거래량 REAL NOT NULL);
"""
SQL_MINUTELY_INSERT = """
    INSERT INTO DailyData
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
"""
SQL_MINUTELY_UPDATE = """
"""
SQL_MINUTELY_DELETE = """
"""