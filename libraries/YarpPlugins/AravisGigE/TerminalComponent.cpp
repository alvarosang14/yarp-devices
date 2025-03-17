#include <yarp/os/LogStream.h>
#include <iostream>

#include "AravisGigE.hpp"
#include "LogComponent.hpp"

using namespace roboticslab;

void get_command(const std::string &command, std::vector<std::string> &tokens) {
    std::stringstream ss(command);
    std::string token;
    while (ss >> token) {
        tokens.push_back(token);
    }
}

cameraFeature_id_t AravisGigE::id_find(const std::string &feature_name) {
    for (const auto &pair : feature_names) {
        if (pair.second == feature_name) {
            return pair.first;  // Devuelve el ID encontrado
        }
    }
}

void AravisGigE::runInteractiveTerminal() {
    std::string command;

    while (true) {
        std::cout << "\n> ";
        std::getline(std::cin, command);

        std::vector<std::string> tokens;
        get_command(command, tokens);

        if (tokens.empty()) continue;

        std::string cmd = tokens[0];

        if (cmd == "exit") {
            std::cout << "Exiting interactive mode...\n";
            close();
            std::this_thread::sleep_for(std::chrono::seconds(1));
            std::exit(0);
        } else if (cmd == "list_features") {
            listAvailableFeatures();

        } else if (cmd == "get_feature") {
            if (tokens.size() != 2) {
                std::cout << "Usage: get_feature <FeatureName>\n";
                continue;
            }

            cameraFeature_id_t id = id_find(tokens[1]);
            if (!id) {
                std::cout << "Feature not found: " << tokens[1] << "\n";
                continue;
            }

            double value;
            if (getFeature(id, &value)) {
                std::cout << "Feature " << tokens[1] << " (ID " << id << ") value: " << value << std::endl;
            } else {
                std::cout << "Failed to get feature " << tokens[1] << std::endl;
            }

        } else if (cmd == "set_feature") {
            if (tokens.size() != 3) {
                std::cout << "Usage: set_feature <FeatureName> <value>\n";
                continue;
            }

            cameraFeature_id_t id = id_find(tokens[1]);
            if (!id) {
                std::cout << "Feature not found: " << tokens[1] << "\n";
                continue;
            }

            try {
                double value = std::stod(tokens[2]); // Convertir a número
                if (setFeature(id, value)) {
                    std::cout << "Feature " << tokens[1] << " (ID " << id << ") set to: " << value << std::endl;
                } else {
                    std::cout << "Failed to set feature " << tokens[1] << std::endl;
                }
            } catch (const std::exception &e) {
                std::cout << "Invalid value format.\n";
            }

        } else if (cmd == "help") {
            std::cout << "Available commands:\n"
                      << "  list_features\n"
                      << "  get_feature <FeatureName>\n"
                      << "  set_feature <FeatureName> <value>\n"
                      << "  exit\n";
        } 
        else {
            std::cout << "Unknown command. Type 'help' for available commands.\n";
        }
    }
}

/*
[INFO] |rl.AravisGigE| Using pixel format: BayerRG8
[INFO] |rl.AravisGigE| Width range: min=16 max=4096
[INFO] |rl.AravisGigE| Height range: min=2 max=2160
[INFO] |rl.AravisGigE| FPS range: min=1.000000 max=21.847353
[INFO] |rl.AravisGigE| Current FPS value: 21
[INFO] |rl.AravisGigE| Gain range: min=0.000000 max=24.082386
[INFO] |rl.AravisGigE| Current gain value: 0
[INFO] |rl.AravisGigE| Exposure range: min=20.742416 max=47573.566437
[INFO] |rl.AravisGigE| Current exposure value: 45411.1
[INFO] |rl.AravisGigE| Checking Lens Controls availability
[WARNING] |rl.AravisGigE| Zoom property not available
[WARNING] |rl.AravisGigE| Focus property not available

*/