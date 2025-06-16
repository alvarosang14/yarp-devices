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

#include "LogComponent.hpp"

bool useLogFile = false;

void customLogCallback(yarp::os::Log::LogType type, const char* msg, const char* file, unsigned int line,
                       const char* func, double systemtime, double networktime, double externaltime,
                       const char* hostname, const char* process) {

    if (!useLogFile) return;

    std::ofstream logFile("log_output.txt", std::ios::app);
    if (logFile.is_open()) {
        logFile << "[" << (type == yarp::os::Log::ErrorType ? "ERROR" :
                           type == yarp::os::Log::WarningType ? "WARNING" :
                           type == yarp::os::Log::InfoType ? "INFO" :
                           type == yarp::os::Log::DebugType ? "DEBUG" : "UNKNOWN")
                << "] " << msg << " (" << file << ":" << line << ", " << func << ")" << std::endl;
    }
}

YARP_LOG_COMPONENT(ARV, "rl.AravisGigE")
