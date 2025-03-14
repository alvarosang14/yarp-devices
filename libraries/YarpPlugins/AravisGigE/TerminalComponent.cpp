#include <yarp/os/LogStream.h>
#include <iostream>

#include "AravisGigE.hpp"
#include "LogComponent.hpp"

using namespace roboticslab;

void AravisGigE::runInteractiveTerminal() {
    std::string command;
    while (true)
    {
        std::cout << "\n[AravisGigE Terminal] Enter command ('help' for list, 'exit' to quit): ";
        std::getline(std::cin, command);

        if (command == "exit")
        {
            std::cout << "Exiting interactive mode...\n";
            AravisGigE::close();
            break;
        }
        else if (command == "list_features")
        {
            listAvailableFeatures();
        }
        else if (command.rfind("get_feature", 0) == 0)
        {
            //getFeatureValue(command);
        }
        else if (command.rfind("set_feature", 0) == 0)
        {
            //setFeatureValue(command);
        }
        else if (command == "help")
        {
            std::cout << "Available commands:\n"
                      << "  list_features        - List available camera features\n"
                      << "  get_feature <id>     - Get the value of a feature\n"
                      << "  set_feature <id> <value> - Set a new value for a feature\n"
                      << "  exit                 - Quit interactive mode\n";
        }
        else
        {
            std::cout << "Unknown command. Type 'help' for a list of commands.\n";
        }
    }
}

/*
[ERROR] Feature is not available or does not support auto/manual/OnePush mode (/home/alvaro/repos/yarp-devices/libraries/YarpPlugins/AravisGigE/IFrameGrabberControlsImpl.cpp:248, virtual bool roboticslab::AravisGigE::getMode(int, FeatureMode*))
[ERROR] Feature is not available or does not support on/off mode (/home/alvaro/repos/yarp-devices/libraries/YarpPlugins/AravisGigE/IFrameGrabberControlsImpl.cpp:160, virtual bool roboticslab::AravisGigE::getActive(int, bool*))
[ERROR] Feature is not available or does not support auto/manual/OnePush mode (/home/alvaro/repos/yarp-devices/libraries/YarpPlugins/AravisGigE/IFrameGrabberControlsImpl.cpp:248, virtual bool roboticslab::AravisGigE::getMode(int, FeatureMode*))
[ERROR] Feature is not available or does not support on/off mode (/home/alvaro/repos/yarp-devices/libraries/YarpPlugins/AravisGigE/IFrameGrabberControlsImpl.cpp:160, virtual bool roboticslab::AravisGigE::getActive(int, bool*))
[ERROR] Feature is not available or does not support auto/manual/OnePush mode (/home/alvaro/repos/yarp-devices/libraries/YarpPlugins/AravisGigE/IFrameGrabberControlsImpl.cpp:248, virtual bool roboticslab::AravisGigE::getMode(int, FeatureMode*))
[ERROR] Feature is not available or does not support on/off mode (/home/alvaro/repos/yarp-devices/libraries/YarpPlugins/AravisGigE/IFrameGrabberControlsImpl.cpp:160, virtual bool roboticslab::AravisGigE::getActive(int, bool*))
[ERROR] Feature is not available or does not support auto/manual/OnePush mode (/home/alvaro/repos/yarp-devices/libraries/YarpPlugins/AravisGigE/IFrameGrabberControlsImpl.cpp:248, virtual bool roboticslab::AravisGigE::getMode(int, FeatureMode*))
[ERROR] Feature is not available or does not support on/off mode (/home/alvaro/repos/yarp-devices/libraries/YarpPlugins/AravisGigE/IFrameGrabberControlsImpl.cpp:160, virtual bool roboticslab::AravisGigE::getActive(int, bool*))
[ERROR] Feature is not available or does not support auto/manual/OnePush mode (/home/alvaro/repos/yarp-devices/libraries/YarpPlugins/AravisGigE/IFrameGrabberControlsImpl.cpp:248, virtual bool roboticslab::AravisGigE::getMode(int, FeatureMode*))
[ERROR] Feature is not available or does not support on/off mode (/home/alvaro/repos/yarp-devices/libraries/YarpPlugins/AravisGigE/IFrameGrabberControlsImpl.cpp:160, virtual bool roboticslab::AravisGigE::getActive(int, bool*))

*/