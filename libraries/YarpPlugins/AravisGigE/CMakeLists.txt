# Copyright: (C) 2017 Universidad Carlos III de Madrid
# Authors: Juan G. Victores & David Estevez
# CopyPolicy: Released under the terms of the LGPLv2.1 or later, see LGPL.TXT

# Find required packages FIRST
find_package(YARP REQUIRED)
find_package(OpenCV REQUIRED)
find_package(ARAVIS)

if(NOT ARAVIS_FOUND)
    message(WARNING "ARAVIS package not found, disabling AravisGigE")
    set(SKIP_AravisGigE ON)
endif()

# Define source files
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
        DEPENDS ARAVIS_FOUND
        EXTRA_CONFIG WRAPPER=frameGrabber_nws_yarp
    )

    yarp_add_plugin(AravisGigE ${ARAVISGIGE_SOURCES})

    # Target properties
    target_link_libraries(AravisGigE
        YARP::YARP_os
        YARP::YARP_dev
        ${ARAVIS_LIBRARIES}
        ${OpenCV_LIBS} # Link OpenCV here
    )

    target_include_directories(AravisGigE
        PUBLIC
            ${CMAKE_CURRENT_SOURCE_DIR}/src
            ${CMAKE_CURRENT_SOURCE_DIR}/src/Log
            ${CMAKE_CURRENT_SOURCE_DIR}/src/Frame
        PRIVATE
            ${ARAVIS_INCLUDE_DIRS}
    )

    yarp_install(TARGETS AravisGigE
        LIBRARY DESTINATION ${ROBOTICSLAB-YARP-DEVICES_DYNAMIC_PLUGINS_INSTALL_DIR}
        ARCHIVE DESTINATION ${ROBOTICSLAB-YARP-DEVICES_STATIC_PLUGINS_INSTALL_DIR}
        YARP_INI DESTINATION ${ROBOTICSLAB-YARP-DEVICES_PLUGIN_MANIFESTS_INSTALL_DIR}
    )

else()
    message(STATUS "AravisGigE plugin build skipped.")
endif()