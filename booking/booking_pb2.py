# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: booking.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\rbooking.proto\"\x07\n\x05\x45mpty\"\x10\n\x02Id\x12\n\n\x02id\x18\x01 \x01(\t\"0\n\x07\x42ooking\x12\x0e\n\x06userid\x18\x01 \x01(\t\x12\x15\n\x05\x64\x61tes\x18\x02 \x03(\x0b\x32\x06.Dates\"%\n\x05\x44\x61tes\x12\x0c\n\x04\x64\x61te\x18\x01 \x01(\t\x12\x0e\n\x06movies\x18\x02 \x03(\t\"<\n\x0bPostBooking\x12\x0e\n\x06userid\x18\x01 \x01(\t\x12\x0c\n\x04\x64\x61te\x18\x02 \x01(\t\x12\x0f\n\x07movieid\x18\x03 \x01(\t2\xa8\x01\n\x08\x42ookings\x12#\n\x0bGetBookings\x12\x06.Empty\x1a\x08.Booking\"\x00\x30\x01\x12$\n\x11GetBookingsByUser\x12\x03.Id\x1a\x08.Booking\"\x00\x12*\n\x0ePostNewBooking\x12\x0c.PostBooking\x1a\x08.Booking\"\x00\x12%\n\x12PostNewBookingUser\x12\x03.Id\x1a\x08.Booking\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'booking_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _globals['_EMPTY']._serialized_start=17
  _globals['_EMPTY']._serialized_end=24
  _globals['_ID']._serialized_start=26
  _globals['_ID']._serialized_end=42
  _globals['_BOOKING']._serialized_start=44
  _globals['_BOOKING']._serialized_end=92
  _globals['_DATES']._serialized_start=94
  _globals['_DATES']._serialized_end=131
  _globals['_POSTBOOKING']._serialized_start=133
  _globals['_POSTBOOKING']._serialized_end=193
  _globals['_BOOKINGS']._serialized_start=196
  _globals['_BOOKINGS']._serialized_end=364
# @@protoc_insertion_point(module_scope)