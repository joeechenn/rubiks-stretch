// generated from rosidl_typesupport_cpp/resource/idl__type_support.cpp.em
// with input from stretch_web_teleop:action/MoveToPregrasp.idl
// generated code does not contain a copyright notice

#include "cstddef"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "stretch_web_teleop/action/detail/move_to_pregrasp__struct.hpp"
#include "rosidl_typesupport_cpp/identifier.hpp"
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_c/type_support_map.h"
#include "rosidl_typesupport_cpp/message_type_support_dispatch.hpp"
#include "rosidl_typesupport_cpp/visibility_control.h"
#include "rosidl_typesupport_interface/macros.h"

namespace stretch_web_teleop
{

namespace action
{

namespace rosidl_typesupport_cpp
{

typedef struct _MoveToPregrasp_Goal_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _MoveToPregrasp_Goal_type_support_ids_t;

static const _MoveToPregrasp_Goal_type_support_ids_t _MoveToPregrasp_Goal_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _MoveToPregrasp_Goal_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _MoveToPregrasp_Goal_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _MoveToPregrasp_Goal_type_support_symbol_names_t _MoveToPregrasp_Goal_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, stretch_web_teleop, action, MoveToPregrasp_Goal)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, stretch_web_teleop, action, MoveToPregrasp_Goal)),
  }
};

typedef struct _MoveToPregrasp_Goal_type_support_data_t
{
  void * data[2];
} _MoveToPregrasp_Goal_type_support_data_t;

static _MoveToPregrasp_Goal_type_support_data_t _MoveToPregrasp_Goal_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _MoveToPregrasp_Goal_message_typesupport_map = {
  2,
  "stretch_web_teleop",
  &_MoveToPregrasp_Goal_message_typesupport_ids.typesupport_identifier[0],
  &_MoveToPregrasp_Goal_message_typesupport_symbol_names.symbol_name[0],
  &_MoveToPregrasp_Goal_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t MoveToPregrasp_Goal_message_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_MoveToPregrasp_Goal_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace action

}  // namespace stretch_web_teleop

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<stretch_web_teleop::action::MoveToPregrasp_Goal>()
{
  return &::stretch_web_teleop::action::rosidl_typesupport_cpp::MoveToPregrasp_Goal_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, stretch_web_teleop, action, MoveToPregrasp_Goal)() {
  return get_message_type_support_handle<stretch_web_teleop::action::MoveToPregrasp_Goal>();
}

#ifdef __cplusplus
}
#endif
}  // namespace rosidl_typesupport_cpp

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "stretch_web_teleop/action/detail/move_to_pregrasp__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support_dispatch.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace stretch_web_teleop
{

namespace action
{

namespace rosidl_typesupport_cpp
{

typedef struct _MoveToPregrasp_Result_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _MoveToPregrasp_Result_type_support_ids_t;

static const _MoveToPregrasp_Result_type_support_ids_t _MoveToPregrasp_Result_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _MoveToPregrasp_Result_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _MoveToPregrasp_Result_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _MoveToPregrasp_Result_type_support_symbol_names_t _MoveToPregrasp_Result_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, stretch_web_teleop, action, MoveToPregrasp_Result)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, stretch_web_teleop, action, MoveToPregrasp_Result)),
  }
};

typedef struct _MoveToPregrasp_Result_type_support_data_t
{
  void * data[2];
} _MoveToPregrasp_Result_type_support_data_t;

static _MoveToPregrasp_Result_type_support_data_t _MoveToPregrasp_Result_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _MoveToPregrasp_Result_message_typesupport_map = {
  2,
  "stretch_web_teleop",
  &_MoveToPregrasp_Result_message_typesupport_ids.typesupport_identifier[0],
  &_MoveToPregrasp_Result_message_typesupport_symbol_names.symbol_name[0],
  &_MoveToPregrasp_Result_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t MoveToPregrasp_Result_message_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_MoveToPregrasp_Result_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace action

}  // namespace stretch_web_teleop

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<stretch_web_teleop::action::MoveToPregrasp_Result>()
{
  return &::stretch_web_teleop::action::rosidl_typesupport_cpp::MoveToPregrasp_Result_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, stretch_web_teleop, action, MoveToPregrasp_Result)() {
  return get_message_type_support_handle<stretch_web_teleop::action::MoveToPregrasp_Result>();
}

#ifdef __cplusplus
}
#endif
}  // namespace rosidl_typesupport_cpp

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "stretch_web_teleop/action/detail/move_to_pregrasp__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support_dispatch.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace stretch_web_teleop
{

namespace action
{

namespace rosidl_typesupport_cpp
{

typedef struct _MoveToPregrasp_Feedback_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _MoveToPregrasp_Feedback_type_support_ids_t;

static const _MoveToPregrasp_Feedback_type_support_ids_t _MoveToPregrasp_Feedback_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _MoveToPregrasp_Feedback_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _MoveToPregrasp_Feedback_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _MoveToPregrasp_Feedback_type_support_symbol_names_t _MoveToPregrasp_Feedback_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, stretch_web_teleop, action, MoveToPregrasp_Feedback)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, stretch_web_teleop, action, MoveToPregrasp_Feedback)),
  }
};

typedef struct _MoveToPregrasp_Feedback_type_support_data_t
{
  void * data[2];
} _MoveToPregrasp_Feedback_type_support_data_t;

static _MoveToPregrasp_Feedback_type_support_data_t _MoveToPregrasp_Feedback_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _MoveToPregrasp_Feedback_message_typesupport_map = {
  2,
  "stretch_web_teleop",
  &_MoveToPregrasp_Feedback_message_typesupport_ids.typesupport_identifier[0],
  &_MoveToPregrasp_Feedback_message_typesupport_symbol_names.symbol_name[0],
  &_MoveToPregrasp_Feedback_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t MoveToPregrasp_Feedback_message_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_MoveToPregrasp_Feedback_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace action

}  // namespace stretch_web_teleop

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<stretch_web_teleop::action::MoveToPregrasp_Feedback>()
{
  return &::stretch_web_teleop::action::rosidl_typesupport_cpp::MoveToPregrasp_Feedback_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, stretch_web_teleop, action, MoveToPregrasp_Feedback)() {
  return get_message_type_support_handle<stretch_web_teleop::action::MoveToPregrasp_Feedback>();
}

#ifdef __cplusplus
}
#endif
}  // namespace rosidl_typesupport_cpp

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "stretch_web_teleop/action/detail/move_to_pregrasp__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support_dispatch.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace stretch_web_teleop
{

namespace action
{

namespace rosidl_typesupport_cpp
{

typedef struct _MoveToPregrasp_SendGoal_Request_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _MoveToPregrasp_SendGoal_Request_type_support_ids_t;

static const _MoveToPregrasp_SendGoal_Request_type_support_ids_t _MoveToPregrasp_SendGoal_Request_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _MoveToPregrasp_SendGoal_Request_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _MoveToPregrasp_SendGoal_Request_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _MoveToPregrasp_SendGoal_Request_type_support_symbol_names_t _MoveToPregrasp_SendGoal_Request_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, stretch_web_teleop, action, MoveToPregrasp_SendGoal_Request)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, stretch_web_teleop, action, MoveToPregrasp_SendGoal_Request)),
  }
};

typedef struct _MoveToPregrasp_SendGoal_Request_type_support_data_t
{
  void * data[2];
} _MoveToPregrasp_SendGoal_Request_type_support_data_t;

static _MoveToPregrasp_SendGoal_Request_type_support_data_t _MoveToPregrasp_SendGoal_Request_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _MoveToPregrasp_SendGoal_Request_message_typesupport_map = {
  2,
  "stretch_web_teleop",
  &_MoveToPregrasp_SendGoal_Request_message_typesupport_ids.typesupport_identifier[0],
  &_MoveToPregrasp_SendGoal_Request_message_typesupport_symbol_names.symbol_name[0],
  &_MoveToPregrasp_SendGoal_Request_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t MoveToPregrasp_SendGoal_Request_message_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_MoveToPregrasp_SendGoal_Request_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace action

}  // namespace stretch_web_teleop

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<stretch_web_teleop::action::MoveToPregrasp_SendGoal_Request>()
{
  return &::stretch_web_teleop::action::rosidl_typesupport_cpp::MoveToPregrasp_SendGoal_Request_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, stretch_web_teleop, action, MoveToPregrasp_SendGoal_Request)() {
  return get_message_type_support_handle<stretch_web_teleop::action::MoveToPregrasp_SendGoal_Request>();
}

#ifdef __cplusplus
}
#endif
}  // namespace rosidl_typesupport_cpp

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "stretch_web_teleop/action/detail/move_to_pregrasp__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support_dispatch.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace stretch_web_teleop
{

namespace action
{

namespace rosidl_typesupport_cpp
{

typedef struct _MoveToPregrasp_SendGoal_Response_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _MoveToPregrasp_SendGoal_Response_type_support_ids_t;

static const _MoveToPregrasp_SendGoal_Response_type_support_ids_t _MoveToPregrasp_SendGoal_Response_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _MoveToPregrasp_SendGoal_Response_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _MoveToPregrasp_SendGoal_Response_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _MoveToPregrasp_SendGoal_Response_type_support_symbol_names_t _MoveToPregrasp_SendGoal_Response_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, stretch_web_teleop, action, MoveToPregrasp_SendGoal_Response)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, stretch_web_teleop, action, MoveToPregrasp_SendGoal_Response)),
  }
};

typedef struct _MoveToPregrasp_SendGoal_Response_type_support_data_t
{
  void * data[2];
} _MoveToPregrasp_SendGoal_Response_type_support_data_t;

static _MoveToPregrasp_SendGoal_Response_type_support_data_t _MoveToPregrasp_SendGoal_Response_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _MoveToPregrasp_SendGoal_Response_message_typesupport_map = {
  2,
  "stretch_web_teleop",
  &_MoveToPregrasp_SendGoal_Response_message_typesupport_ids.typesupport_identifier[0],
  &_MoveToPregrasp_SendGoal_Response_message_typesupport_symbol_names.symbol_name[0],
  &_MoveToPregrasp_SendGoal_Response_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t MoveToPregrasp_SendGoal_Response_message_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_MoveToPregrasp_SendGoal_Response_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace action

}  // namespace stretch_web_teleop

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<stretch_web_teleop::action::MoveToPregrasp_SendGoal_Response>()
{
  return &::stretch_web_teleop::action::rosidl_typesupport_cpp::MoveToPregrasp_SendGoal_Response_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, stretch_web_teleop, action, MoveToPregrasp_SendGoal_Response)() {
  return get_message_type_support_handle<stretch_web_teleop::action::MoveToPregrasp_SendGoal_Response>();
}

#ifdef __cplusplus
}
#endif
}  // namespace rosidl_typesupport_cpp

// already included above
// #include "cstddef"
#include "rosidl_runtime_c/service_type_support_struct.h"
// already included above
// #include "stretch_web_teleop/action/detail/move_to_pregrasp__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/identifier.hpp"
#include "rosidl_typesupport_cpp/service_type_support.hpp"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
#include "rosidl_typesupport_cpp/service_type_support_dispatch.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace stretch_web_teleop
{

namespace action
{

namespace rosidl_typesupport_cpp
{

typedef struct _MoveToPregrasp_SendGoal_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _MoveToPregrasp_SendGoal_type_support_ids_t;

static const _MoveToPregrasp_SendGoal_type_support_ids_t _MoveToPregrasp_SendGoal_service_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _MoveToPregrasp_SendGoal_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _MoveToPregrasp_SendGoal_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _MoveToPregrasp_SendGoal_type_support_symbol_names_t _MoveToPregrasp_SendGoal_service_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, stretch_web_teleop, action, MoveToPregrasp_SendGoal)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, stretch_web_teleop, action, MoveToPregrasp_SendGoal)),
  }
};

typedef struct _MoveToPregrasp_SendGoal_type_support_data_t
{
  void * data[2];
} _MoveToPregrasp_SendGoal_type_support_data_t;

static _MoveToPregrasp_SendGoal_type_support_data_t _MoveToPregrasp_SendGoal_service_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _MoveToPregrasp_SendGoal_service_typesupport_map = {
  2,
  "stretch_web_teleop",
  &_MoveToPregrasp_SendGoal_service_typesupport_ids.typesupport_identifier[0],
  &_MoveToPregrasp_SendGoal_service_typesupport_symbol_names.symbol_name[0],
  &_MoveToPregrasp_SendGoal_service_typesupport_data.data[0],
};

static const rosidl_service_type_support_t MoveToPregrasp_SendGoal_service_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_MoveToPregrasp_SendGoal_service_typesupport_map),
  ::rosidl_typesupport_cpp::get_service_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace action

}  // namespace stretch_web_teleop

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_service_type_support_t *
get_service_type_support_handle<stretch_web_teleop::action::MoveToPregrasp_SendGoal>()
{
  return &::stretch_web_teleop::action::rosidl_typesupport_cpp::MoveToPregrasp_SendGoal_service_type_support_handle;
}

}  // namespace rosidl_typesupport_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_cpp, stretch_web_teleop, action, MoveToPregrasp_SendGoal)() {
  return ::rosidl_typesupport_cpp::get_service_type_support_handle<stretch_web_teleop::action::MoveToPregrasp_SendGoal>();
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "stretch_web_teleop/action/detail/move_to_pregrasp__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support_dispatch.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace stretch_web_teleop
{

namespace action
{

namespace rosidl_typesupport_cpp
{

typedef struct _MoveToPregrasp_GetResult_Request_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _MoveToPregrasp_GetResult_Request_type_support_ids_t;

static const _MoveToPregrasp_GetResult_Request_type_support_ids_t _MoveToPregrasp_GetResult_Request_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _MoveToPregrasp_GetResult_Request_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _MoveToPregrasp_GetResult_Request_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _MoveToPregrasp_GetResult_Request_type_support_symbol_names_t _MoveToPregrasp_GetResult_Request_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, stretch_web_teleop, action, MoveToPregrasp_GetResult_Request)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, stretch_web_teleop, action, MoveToPregrasp_GetResult_Request)),
  }
};

typedef struct _MoveToPregrasp_GetResult_Request_type_support_data_t
{
  void * data[2];
} _MoveToPregrasp_GetResult_Request_type_support_data_t;

static _MoveToPregrasp_GetResult_Request_type_support_data_t _MoveToPregrasp_GetResult_Request_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _MoveToPregrasp_GetResult_Request_message_typesupport_map = {
  2,
  "stretch_web_teleop",
  &_MoveToPregrasp_GetResult_Request_message_typesupport_ids.typesupport_identifier[0],
  &_MoveToPregrasp_GetResult_Request_message_typesupport_symbol_names.symbol_name[0],
  &_MoveToPregrasp_GetResult_Request_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t MoveToPregrasp_GetResult_Request_message_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_MoveToPregrasp_GetResult_Request_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace action

}  // namespace stretch_web_teleop

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<stretch_web_teleop::action::MoveToPregrasp_GetResult_Request>()
{
  return &::stretch_web_teleop::action::rosidl_typesupport_cpp::MoveToPregrasp_GetResult_Request_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, stretch_web_teleop, action, MoveToPregrasp_GetResult_Request)() {
  return get_message_type_support_handle<stretch_web_teleop::action::MoveToPregrasp_GetResult_Request>();
}

#ifdef __cplusplus
}
#endif
}  // namespace rosidl_typesupport_cpp

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "stretch_web_teleop/action/detail/move_to_pregrasp__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support_dispatch.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace stretch_web_teleop
{

namespace action
{

namespace rosidl_typesupport_cpp
{

typedef struct _MoveToPregrasp_GetResult_Response_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _MoveToPregrasp_GetResult_Response_type_support_ids_t;

static const _MoveToPregrasp_GetResult_Response_type_support_ids_t _MoveToPregrasp_GetResult_Response_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _MoveToPregrasp_GetResult_Response_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _MoveToPregrasp_GetResult_Response_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _MoveToPregrasp_GetResult_Response_type_support_symbol_names_t _MoveToPregrasp_GetResult_Response_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, stretch_web_teleop, action, MoveToPregrasp_GetResult_Response)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, stretch_web_teleop, action, MoveToPregrasp_GetResult_Response)),
  }
};

typedef struct _MoveToPregrasp_GetResult_Response_type_support_data_t
{
  void * data[2];
} _MoveToPregrasp_GetResult_Response_type_support_data_t;

static _MoveToPregrasp_GetResult_Response_type_support_data_t _MoveToPregrasp_GetResult_Response_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _MoveToPregrasp_GetResult_Response_message_typesupport_map = {
  2,
  "stretch_web_teleop",
  &_MoveToPregrasp_GetResult_Response_message_typesupport_ids.typesupport_identifier[0],
  &_MoveToPregrasp_GetResult_Response_message_typesupport_symbol_names.symbol_name[0],
  &_MoveToPregrasp_GetResult_Response_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t MoveToPregrasp_GetResult_Response_message_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_MoveToPregrasp_GetResult_Response_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace action

}  // namespace stretch_web_teleop

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<stretch_web_teleop::action::MoveToPregrasp_GetResult_Response>()
{
  return &::stretch_web_teleop::action::rosidl_typesupport_cpp::MoveToPregrasp_GetResult_Response_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, stretch_web_teleop, action, MoveToPregrasp_GetResult_Response)() {
  return get_message_type_support_handle<stretch_web_teleop::action::MoveToPregrasp_GetResult_Response>();
}

#ifdef __cplusplus
}
#endif
}  // namespace rosidl_typesupport_cpp

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/service_type_support_struct.h"
// already included above
// #include "stretch_web_teleop/action/detail/move_to_pregrasp__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_cpp/service_type_support.hpp"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_cpp/service_type_support_dispatch.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace stretch_web_teleop
{

namespace action
{

namespace rosidl_typesupport_cpp
{

typedef struct _MoveToPregrasp_GetResult_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _MoveToPregrasp_GetResult_type_support_ids_t;

static const _MoveToPregrasp_GetResult_type_support_ids_t _MoveToPregrasp_GetResult_service_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _MoveToPregrasp_GetResult_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _MoveToPregrasp_GetResult_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _MoveToPregrasp_GetResult_type_support_symbol_names_t _MoveToPregrasp_GetResult_service_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, stretch_web_teleop, action, MoveToPregrasp_GetResult)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, stretch_web_teleop, action, MoveToPregrasp_GetResult)),
  }
};

typedef struct _MoveToPregrasp_GetResult_type_support_data_t
{
  void * data[2];
} _MoveToPregrasp_GetResult_type_support_data_t;

static _MoveToPregrasp_GetResult_type_support_data_t _MoveToPregrasp_GetResult_service_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _MoveToPregrasp_GetResult_service_typesupport_map = {
  2,
  "stretch_web_teleop",
  &_MoveToPregrasp_GetResult_service_typesupport_ids.typesupport_identifier[0],
  &_MoveToPregrasp_GetResult_service_typesupport_symbol_names.symbol_name[0],
  &_MoveToPregrasp_GetResult_service_typesupport_data.data[0],
};

static const rosidl_service_type_support_t MoveToPregrasp_GetResult_service_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_MoveToPregrasp_GetResult_service_typesupport_map),
  ::rosidl_typesupport_cpp::get_service_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace action

}  // namespace stretch_web_teleop

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_service_type_support_t *
get_service_type_support_handle<stretch_web_teleop::action::MoveToPregrasp_GetResult>()
{
  return &::stretch_web_teleop::action::rosidl_typesupport_cpp::MoveToPregrasp_GetResult_service_type_support_handle;
}

}  // namespace rosidl_typesupport_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_cpp, stretch_web_teleop, action, MoveToPregrasp_GetResult)() {
  return ::rosidl_typesupport_cpp::get_service_type_support_handle<stretch_web_teleop::action::MoveToPregrasp_GetResult>();
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "stretch_web_teleop/action/detail/move_to_pregrasp__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support_dispatch.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace stretch_web_teleop
{

namespace action
{

namespace rosidl_typesupport_cpp
{

typedef struct _MoveToPregrasp_FeedbackMessage_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _MoveToPregrasp_FeedbackMessage_type_support_ids_t;

static const _MoveToPregrasp_FeedbackMessage_type_support_ids_t _MoveToPregrasp_FeedbackMessage_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _MoveToPregrasp_FeedbackMessage_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _MoveToPregrasp_FeedbackMessage_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _MoveToPregrasp_FeedbackMessage_type_support_symbol_names_t _MoveToPregrasp_FeedbackMessage_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, stretch_web_teleop, action, MoveToPregrasp_FeedbackMessage)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, stretch_web_teleop, action, MoveToPregrasp_FeedbackMessage)),
  }
};

typedef struct _MoveToPregrasp_FeedbackMessage_type_support_data_t
{
  void * data[2];
} _MoveToPregrasp_FeedbackMessage_type_support_data_t;

static _MoveToPregrasp_FeedbackMessage_type_support_data_t _MoveToPregrasp_FeedbackMessage_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _MoveToPregrasp_FeedbackMessage_message_typesupport_map = {
  2,
  "stretch_web_teleop",
  &_MoveToPregrasp_FeedbackMessage_message_typesupport_ids.typesupport_identifier[0],
  &_MoveToPregrasp_FeedbackMessage_message_typesupport_symbol_names.symbol_name[0],
  &_MoveToPregrasp_FeedbackMessage_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t MoveToPregrasp_FeedbackMessage_message_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_MoveToPregrasp_FeedbackMessage_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace action

}  // namespace stretch_web_teleop

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<stretch_web_teleop::action::MoveToPregrasp_FeedbackMessage>()
{
  return &::stretch_web_teleop::action::rosidl_typesupport_cpp::MoveToPregrasp_FeedbackMessage_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, stretch_web_teleop, action, MoveToPregrasp_FeedbackMessage)() {
  return get_message_type_support_handle<stretch_web_teleop::action::MoveToPregrasp_FeedbackMessage>();
}

#ifdef __cplusplus
}
#endif
}  // namespace rosidl_typesupport_cpp

#include "action_msgs/msg/goal_status_array.hpp"
#include "action_msgs/srv/cancel_goal.hpp"
// already included above
// #include "stretch_web_teleop/action/detail/move_to_pregrasp__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
#include "rosidl_runtime_c/action_type_support_struct.h"
#include "rosidl_typesupport_cpp/action_type_support.hpp"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
// already included above
// #include "rosidl_typesupport_cpp/service_type_support.hpp"

namespace stretch_web_teleop
{

namespace action
{

namespace rosidl_typesupport_cpp
{

static rosidl_action_type_support_t MoveToPregrasp_action_type_support_handle = {
  NULL, NULL, NULL, NULL, NULL};

}  // namespace rosidl_typesupport_cpp

}  // namespace action

}  // namespace stretch_web_teleop

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_action_type_support_t *
get_action_type_support_handle<stretch_web_teleop::action::MoveToPregrasp>()
{
  using ::stretch_web_teleop::action::rosidl_typesupport_cpp::MoveToPregrasp_action_type_support_handle;
  // Thread-safe by always writing the same values to the static struct
  MoveToPregrasp_action_type_support_handle.goal_service_type_support = get_service_type_support_handle<::stretch_web_teleop::action::MoveToPregrasp::Impl::SendGoalService>();
  MoveToPregrasp_action_type_support_handle.result_service_type_support = get_service_type_support_handle<::stretch_web_teleop::action::MoveToPregrasp::Impl::GetResultService>();
  MoveToPregrasp_action_type_support_handle.cancel_service_type_support = get_service_type_support_handle<::stretch_web_teleop::action::MoveToPregrasp::Impl::CancelGoalService>();
  MoveToPregrasp_action_type_support_handle.feedback_message_type_support = get_message_type_support_handle<::stretch_web_teleop::action::MoveToPregrasp::Impl::FeedbackMessage>();
  MoveToPregrasp_action_type_support_handle.status_message_type_support = get_message_type_support_handle<::stretch_web_teleop::action::MoveToPregrasp::Impl::GoalStatusMessage>();
  return &MoveToPregrasp_action_type_support_handle;
}

}  // namespace rosidl_typesupport_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_action_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__ACTION_SYMBOL_NAME(rosidl_typesupport_cpp, stretch_web_teleop, action, MoveToPregrasp)() {
  return ::rosidl_typesupport_cpp::get_action_type_support_handle<stretch_web_teleop::action::MoveToPregrasp>();
}

#ifdef __cplusplus
}
#endif
