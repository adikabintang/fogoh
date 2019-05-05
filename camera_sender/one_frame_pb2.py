# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: one_frame.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='one_frame.proto',
  package='',
  syntax='proto3',
  serialized_pb=_b('\n\x0fone_frame.proto\"i\n\x08OneFrame\x12\x1b\n\x13\x66rame_jpg_in_base64\x18\x01 \x01(\t\x12\x17\n\x0fvideo_source_id\x18\x02 \x01(\t\x12\x0e\n\x06millis\x18\x03 \x01(\x05\x12\x17\n\x0f\x66rame_order_nth\x18\x04 \x01(\x04\x62\x06proto3')
)




_ONEFRAME = _descriptor.Descriptor(
  name='OneFrame',
  full_name='OneFrame',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='frame_jpg_in_base64', full_name='OneFrame.frame_jpg_in_base64', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='video_source_id', full_name='OneFrame.video_source_id', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='millis', full_name='OneFrame.millis', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='frame_order_nth', full_name='OneFrame.frame_order_nth', index=3,
      number=4, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=19,
  serialized_end=124,
)

DESCRIPTOR.message_types_by_name['OneFrame'] = _ONEFRAME
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

OneFrame = _reflection.GeneratedProtocolMessageType('OneFrame', (_message.Message,), dict(
  DESCRIPTOR = _ONEFRAME,
  __module__ = 'one_frame_pb2'
  # @@protoc_insertion_point(class_scope:OneFrame)
  ))
_sym_db.RegisterMessage(OneFrame)


# @@protoc_insertion_point(module_scope)
