# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: nlu.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\tnlu.proto\x12\x03nlu\" \n\nNLURequest\x12\x12\n\ntranscript\x18\x01 \x01(\t\"3\n\x0bNLUResponse\x12\x11\n\tsentiment\x18\x01 \x01(\t\x12\x11\n\tintention\x18\x02 \x01(\t2E\n\nNLUService\x12\x37\n\x0eStreamAnalysis\x12\x0f.nlu.NLURequest\x1a\x10.nlu.NLUResponse(\x01\x30\x01\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'nlu_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_NLUREQUEST']._serialized_start=18
  _globals['_NLUREQUEST']._serialized_end=50
  _globals['_NLURESPONSE']._serialized_start=52
  _globals['_NLURESPONSE']._serialized_end=103
  _globals['_NLUSERVICE']._serialized_start=105
  _globals['_NLUSERVICE']._serialized_end=174
# @@protoc_insertion_point(module_scope)
