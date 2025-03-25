#include <yarp/os/LogStream.h>
#include <iostream>
#include <sstream>
#include <vector>
#include <stdexcept>
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
            return pair.first;
        }
    }
    return YARP_FEATURE_INVALID;
}

bool AravisGigE::checkFeatureExistenceAndGetValue(const std::string &featureName, double &value) {
    cameraFeature_id_t id = id_find(featureName);
    if (id == YARP_FEATURE_INVALID) {
        std::cout << "Feature not found: " << featureName << "\n";
        return false;
    }
    
    return getFeature(id, &value);
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
        } 
        else if (cmd == "list_features") {
            listAvailableFeatures();
        } 
        else if (cmd == "get_feature") {
            if (tokens.size() != 2) {
                std::cout << "Usage: get_feature <FeatureName>\n";
                continue;
            }

            double value;
            if (checkFeatureExistenceAndGetValue(tokens[1], value)) {
                std::cout << "Feature " << tokens[1] << " value: " << value << "\n";
            } else {
                std::cout << "Failed to get feature " << tokens[1] << "\n";
            }
        } 
        else if (cmd == "set_feature") {
            if (tokens.size() != 3) {
                std::cout << "Usage: set_feature <FeatureName> <value>\n";
                continue;
            }

            double value;
            try {
                value = std::stod(tokens[2]); // Convertir a número
            } catch (const std::exception &e) {
                std::cout << "Invalid value format.\n";
                continue;
            }

            cameraFeature_id_t id = id_find(tokens[1]);
            if (id == YARP_FEATURE_INVALID) {
                std::cout << "Feature not found: " << tokens[1] << "\n";
                continue;
            }

            if (setFeature(id, value)) {
                std::cout << "Feature " << tokens[1] << " set to: " << value << "\n";
            } else {
                std::cout << "Failed to set feature " << tokens[1] << "\n";
            }
        } 
        else if (cmd == "help") {
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
