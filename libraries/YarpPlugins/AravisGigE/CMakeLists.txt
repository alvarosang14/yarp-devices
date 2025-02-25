# Copyright: (C) 2017 Universidad Carlos III de Madrid
# Authors: Juan G. Victores & David Estevez
# CopyPolicy: Released under the terms of the LGPLv2.1 or later, see LGPL.TXT

# Find required packages FIRST
find_package(YARP REQUIRED)  # Assuming YARP is a dependency
find_package(OpenCV REQUIRED)

# Check for Aravis - this should be done *before* any Aravis-related logic
find_package(ARAVIS) # No need for the custom ENABLE_AravisGigE variable, find_package handles this

if(NOT ARAVIS_FOUND)
    message(WARNING "ARAVIS package not found, disabling AravisGigE")
    set(SKIP_AravisGigE ON) # Set the skip flag directly
endif()

# Define source files - do this ONCE
file(GLOB ARAVISGIGE_SOURCES
    ${CMAKE_CURRENT_SOURCE_DIR}/src/*.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/src/Log/*.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/src/Frame/*.cpp
)

# Conditional logic for building the plugin
if(NOT SKIP_AravisGigE)

    yarp_prepare_plugin(AravisGigE
        CATEGORY device
        TYPE roboticslab::AravisGigE
        INCLUDE AravisGigE.hpp
        DEFAULT ON
        DEPENDS ARAVIS_FOUND  # This is usually implied by yarp_add_plugin below
        EXTRA_CONFIG WRAPPER=frameGrabber_nws_yarp
    )

    yarp_add_plugin(AravisGigE ${ARAVISGIGE_SOURCES})

    # Target properties - these should be set *after* yarp_add_plugin
    target_link_libraries(AravisGigE
        YARP::YARP_os
        YARP::YARP_dev
        ${ARAVIS_LIBRARIES}
        ${OpenCV_LIBS} # Link OpenCV here
    )

    target_include_directories(AravisGigE
        PUBLIC  # Use PUBLIC for headers that users of the plugin need
            ${CMAKE_CURRENT_SOURCE_DIR}/src
            ${CMAKE_CURRENT_SOURCE_DIR}/src/Log
            ${CMAKE_CURRENT_SOURCE_DIR}/src/Frame
        PRIVATE # Use PRIVATE for internal headers
            ${ARAVIS_INCLUDE_DIRS}
    )

    yarp_install(TARGETS AravisGigE
        LIBRARY DESTINATION ${ROBOTICSLAB-YARP-DEVICES_DYNAMIC_PLUGINS_INSTALL_DIR}
        ARCHIVE DESTINATION ${ROBOTICSLAB-YARP-DEVICES_STATIC_PLUGINS_INSTALL_DIR}
        YARP_INI DESTINATION ${ROBOTICSLAB-YARP-DEVICES_PLUGIN_MANIFESTS_INSTALL_DIR}
    )

else()
    # No need to set ENABLE_AravisGigE here if you're skipping the build
    message(STATUS "AravisGigE plugin build skipped.")
endif()