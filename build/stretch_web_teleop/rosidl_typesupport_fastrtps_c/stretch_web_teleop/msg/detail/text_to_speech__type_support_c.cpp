// generated from rosidl_typesupport_fastrtps_c/resource/idl__type_support_c.cpp.em
// with input from stretch_web_teleop:msg/TextToSpeech.idl
// generated code does not contain a copyright notice
#include "stretch_web_teleop/msg/detail/text_to_speech__rosidl_typesupport_fastrtps_c.h"


#include <cassert>
#include <limits>
#include <string>
#include "rosidl_typesupport_fastrtps_c/identifier.h"
#include "rosidl_typesupport_fastrtps_c/wstring_conversion.hpp"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
#include "stretch_web_teleop/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
#include "stretch_web_teleop/msg/detail/text_to_speech__struct.h"
#include "stretch_web_teleop/msg/detail/text_to_speech__functions.h"
#include "fastcdr/Cdr.h"

#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-parameter"
# ifdef __clang__
#  pragma clang diagnostic ignored "-Wdeprecated-register"
#  pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
# endif
#endif
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif

// includes and forward declarations of message dependencies and their conversion functions

#if defined(__cplusplus)
extern "C"
{
#endif

#include "rosidl_runtime_c/string.h"  // text, voice
#include "rosidl_runtime_c/string_functions.h"  // text, voice

// forward declare type support functions


using _TextToSpeech__ros_msg_type = stretch_web_teleop__msg__TextToSpeech;

static bool _TextToSpeech__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  const _TextToSpeech__ros_msg_type * ros_message = static_cast<const _TextToSpeech__ros_msg_type *>(untyped_ros_message);
  // Field name: text
  {
    const rosidl_runtime_c__String * str = &ros_message->text;
    if (str->capacity == 0 || str->capacity <= str->size) {
      fprintf(stderr, "string capacity not greater than size\n");
      return false;
    }
    if (str->data[str->size] != '\0') {
      fprintf(stderr, "string not null-terminated\n");
      return false;
    }
    cdr << str->data;
  }

  // Field name: voice
  {
    const rosidl_runtime_c__String * str = &ros_message->voice;
    if (str->capacity == 0 || str->capacity <= str->size) {
      fprintf(stderr, "string capacity not greater than size\n");
      return false;
    }
    if (str->data[str->size] != '\0') {
      fprintf(stderr, "string not null-terminated\n");
      return false;
    }
    cdr << str->data;
  }

  // Field name: is_slow
  {
    cdr << (ros_message->is_slow ? true : false);
  }

  // Field name: override_behavior
  {
    cdr << ros_message->override_behavior;
  }

  return true;
}

static bool _TextToSpeech__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  _TextToSpeech__ros_msg_type * ros_message = static_cast<_TextToSpeech__ros_msg_type *>(untyped_ros_message);
  // Field name: text
  {
    std::string tmp;
    cdr >> tmp;
    if (!ros_message->text.data) {
      rosidl_runtime_c__String__init(&ros_message->text);
    }
    bool succeeded = rosidl_runtime_c__String__assign(
      &ros_message->text,
      tmp.c_str());
    if (!succeeded) {
      fprintf(stderr, "failed to assign string into field 'text'\n");
      return false;
    }
  }

  // Field name: voice
  {
    std::string tmp;
    cdr >> tmp;
    if (!ros_message->voice.data) {
      rosidl_runtime_c__String__init(&ros_message->voice);
    }
    bool succeeded = rosidl_runtime_c__String__assign(
      &ros_message->voice,
      tmp.c_str());
    if (!succeeded) {
      fprintf(stderr, "failed to assign string into field 'voice'\n");
      return false;
    }
  }

  // Field name: is_slow
  {
    uint8_t tmp;
    cdr >> tmp;
    ros_message->is_slow = tmp ? true : false;
  }

  // Field name: override_behavior
  {
    cdr >> ros_message->override_behavior;
  }

  return true;
}  // NOLINT(readability/fn_size)

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_stretch_web_teleop
size_t get_serialized_size_stretch_web_teleop__msg__TextToSpeech(
  const void * untyped_ros_message,
  size_t current_alignment)
{
  const _TextToSpeech__ros_msg_type * ros_message = static_cast<const _TextToSpeech__ros_msg_type *>(untyped_ros_message);
  (void)ros_message;
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // field.name text
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->text.size + 1);
  // field.name voice
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->voice.size + 1);
  // field.name is_slow
  {
    size_t item_size = sizeof(ros_message->is_slow);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name override_behavior
  {
    size_t item_size = sizeof(ros_message->override_behavior);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  return current_alignment - initial_alignment;
}

static uint32_t _TextToSpeech__get_serialized_size(const void * untyped_ros_message)
{
  return static_cast<uint32_t>(
    get_serialized_size_stretch_web_teleop__msg__TextToSpeech(
      untyped_ros_message, 0));
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_stretch_web_teleop
size_t max_serialized_size_stretch_web_teleop__msg__TextToSpeech(
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

  // member: text
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
  // member: voice
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
  // member: is_slow
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }
  // member: override_behavior
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
    using DataType = stretch_web_teleop__msg__TextToSpeech;
    is_plain =
      (
      offsetof(DataType, override_behavior) +
      last_member_size
      ) == ret_val;
  }

  return ret_val;
}

static size_t _TextToSpeech__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_stretch_web_teleop__msg__TextToSpeech(
    full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}


static message_type_support_callbacks_t __callbacks_TextToSpeech = {
  "stretch_web_teleop::msg",
  "TextToSpeech",
  _TextToSpeech__cdr_serialize,
  _TextToSpeech__cdr_deserialize,
  _TextToSpeech__get_serialized_size,
  _TextToSpeech__max_serialized_size
};

static rosidl_message_type_support_t _TextToSpeech__type_support = {
  rosidl_typesupport_fastrtps_c__identifier,
  &__callbacks_TextToSpeech,
  get_message_typesupport_handle_function,
};

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, stretch_web_teleop, msg, TextToSpeech)() {
  return &_TextToSpeech__type_support;
}

#if defined(__cplusplus)
}
#endif
