// generated from rosidl_typesupport_fastrtps_cpp/resource/idl__type_support.cpp.em
// with input from stretch_web_teleop:msg/TextToSpeech.idl
// generated code does not contain a copyright notice
#include "stretch_web_teleop/msg/detail/text_to_speech__rosidl_typesupport_fastrtps_cpp.hpp"
#include "stretch_web_teleop/msg/detail/text_to_speech__struct.hpp"

#include <limits>
#include <stdexcept>
#include <string>
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_fastrtps_cpp/identifier.hpp"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support_decl.hpp"
#include "rosidl_typesupport_fastrtps_cpp/wstring_conversion.hpp"
#include "fastcdr/Cdr.h"


// forward declaration of message dependencies and their conversion functions

namespace stretch_web_teleop
{

namespace msg
{

namespace typesupport_fastrtps_cpp
{

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_stretch_web_teleop
cdr_serialize(
  const stretch_web_teleop::msg::TextToSpeech & ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  // Member: text
  cdr << ros_message.text;
  // Member: voice
  cdr << ros_message.voice;
  // Member: is_slow
  cdr << (ros_message.is_slow ? true : false);
  // Member: override_behavior
  cdr << ros_message.override_behavior;
  return true;
}

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_stretch_web_teleop
cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  stretch_web_teleop::msg::TextToSpeech & ros_message)
{
  // Member: text
  cdr >> ros_message.text;

  // Member: voice
  cdr >> ros_message.voice;

  // Member: is_slow
  {
    uint8_t tmp;
    cdr >> tmp;
    ros_message.is_slow = tmp ? true : false;
  }

  // Member: override_behavior
  cdr >> ros_message.override_behavior;

  return true;
}  // NOLINT(readability/fn_size)

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_stretch_web_teleop
get_serialized_size(
  const stretch_web_teleop::msg::TextToSpeech & ros_message,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // Member: text
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message.text.size() + 1);
  // Member: voice
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message.voice.size() + 1);
  // Member: is_slow
  {
    size_t item_size = sizeof(ros_message.is_slow);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: override_behavior
  {
    size_t item_size = sizeof(ros_message.override_behavior);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  return current_alignment - initial_alignment;
}

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_stretch_web_teleop
max_serialized_size_TextToSpeech(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  size_t last_member_size = 0;
  (void)last_member_size;
  (void)padding;
  (void)wchar_size;

  full_bounded = true;
  is_plain = true;


  // Member: text
  {
    size_t array_size = 1;

    full_bounded = false;
    is_plain = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }

  // Member: voice
  {
    size_t array_size = 1;

    full_bounded = false;
    is_plain = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }

  // Member: is_slow
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }

  // Member: override_behavior
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }

  size_t ret_val = current_alignment - initial_alignment;
  if (is_plain) {
    // All members are plain, and type is not empty.
    // We still need to check that the in-memory alignment
    // is the same as the CDR mandated alignment.
    using DataType = stretch_web_teleop::msg::TextToSpeech;
    is_plain =
      (
      offsetof(DataType, override_behavior) +
      last_member_size
      ) == ret_val;
  }

  return ret_val;
}

static bool _TextToSpeech__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  auto typed_message =
    static_cast<const stretch_web_teleop::msg::TextToSpeech *>(
    untyped_ros_message);
  return cdr_serialize(*typed_message, cdr);
}

static bool _TextToSpeech__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  auto typed_message =
    static_cast<stretch_web_teleop::msg::TextToSpeech *>(
    untyped_ros_message);
  return cdr_deserialize(cdr, *typed_message);
}

static uint32_t _TextToSpeech__get_serialized_size(
  const void * untyped_ros_message)
{
  auto typed_message =
    static_cast<const stretch_web_teleop::msg::TextToSpeech *>(
    untyped_ros_message);
  return static_cast<uint32_t>(get_serialized_size(*typed_message, 0));
}

static size_t _TextToSpeech__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_TextToSpeech(full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}

static message_type_support_callbacks_t _TextToSpeech__callbacks = {
  "stretch_web_teleop::msg",
  "TextToSpeech",
  _TextToSpeech__cdr_serialize,
  _TextToSpeech__cdr_deserialize,
  _TextToSpeech__get_serialized_size,
  _TextToSpeech__max_serialized_size
};

static rosidl_message_type_support_t _TextToSpeech__handle = {
  rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
  &_TextToSpeech__callbacks,
  get_message_typesupport_handle_function,
};

}  // namespace typesupport_fastrtps_cpp

}  // namespace msg

}  // namespace stretch_web_teleop

namespace rosidl_typesupport_fastrtps_cpp
{

template<>
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_EXPORT_stretch_web_teleop
const rosidl_message_type_support_t *
get_message_type_support_handle<stretch_web_teleop::msg::TextToSpeech>()
{
  return &stretch_web_teleop::msg::typesupport_fastrtps_cpp::_TextToSpeech__handle;
}

}  // namespace rosidl_typesupport_fastrtps_cpp

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, stretch_web_teleop, msg, TextToSpeech)() {
  return &stretch_web_teleop::msg::typesupport_fastrtps_cpp::_TextToSpeech__handle;
}

#ifdef __cplusplus
}
#endif
