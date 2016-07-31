drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  device_ID text not null,
  sensor_ID text not null,
  sensor_type text,
  sensor_value real,
  units text,
  timestamp DATE DEFAULT (datetime('now','localtime'))
);
-- To do:
-- - change table name. something like readings or data
-- - add message type ? (like in xbee system - some messages are poll results)


-- Reference:
-- - for reading datetimes back out see: http://stackoverflow.com/questions/1829872/how-to-read-datetime-back-from-sqlite-as-a-datetime-instead-of-string-in-python
