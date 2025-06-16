/*
 * AravisGigE
 * ---------------------
 *
 * Middleware for industrial camera integration in YARP using the Aravis library.
 *
 * Author: Álvaro Santos García
 * Copyright: Universidad Carlos III de Madrid (C) 2025
 * CopyPolicy: Released under the terms of the GNU LGPL v2.1
 */

#ifndef __ARAVIS_GIGE_LOG_COMPONENT_HPP__
#define __ARAVIS_GIGE_LOG_COMPONENT_HPP__

#include <yarp/os/LogComponent.h>
#include <fstream>
#include <yarp/os/LogComponent.h>
#include <yarp/os/LogStream.h>

YARP_DECLARE_LOG_COMPONENT(ARV)

extern bool useLogFile;

void customLogCallback(yarp::os::Log::LogType type, const char* msg, const char* file, unsigned int line,
    const char* func, double systemtime, double networktime, double externaltime,
    const char* hostname, const char* process);

#endif // __ARAVIS_GIGE_LOG_COMPONENT_HPP__
