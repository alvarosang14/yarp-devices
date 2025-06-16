#include <iostream>
#include <yarp/os/LogStream.h>

#include "AravisGigE.hpp"
#include "LogComponent.hpp"

using namespace roboticslab;

// Helper function to get feature info
const FeatureInfo* AravisGigE::getFeatureInfo(cameraFeature_id_t feature) {
    if (yarp_arv_int_feature_map.count(feature)) {
        return &yarp_arv_int_feature_map.at(feature);
    } else if (yarp_arv_float_feat_map.count(feature)) {
        return &yarp_arv_float_feat_map.at(feature);
    }
    return nullptr;
}

bool AravisGigE::getCameraDescription(CameraDescriptor * camera) {
    if (arv_camera_is_uv_device(this->camera)) {
        camera->busType = BUS_USB;
    } else {
        camera->busType = BUS_UNKNOWN;
    }

    camera->deviceDescription = std::string(arv_camera_get_device_id(this->camera, nullptr)) + ": " + 
                               arv_camera_get_model_name(this->camera, nullptr);
    return true;
}

bool AravisGigE::hasFeature(int feature, bool * hasFeature) {
    yCDebug(ARV) << "Checking feature availability:" << feature;

    auto f = static_cast<cameraFeature_id_t>(feature);

    if (f < YARP_FEATURE_BRIGHTNESS || f > YARP_FEATURE_NUMBER_OF - 1) {
        yCError(ARV) << "Feature" << feature << "not supported by YARP";
        return false;
    }

    const FeatureInfo* info = getFeatureInfo(f);
    if (!info || !info->featureName) {
        *hasFeature = false;
        return true;
    }

    ArvDevice *device = arv_camera_get_device(camera);
    if (!device) {
        yCError(ARV) << "Camera device not available";
        return false;
    }

    *hasFeature = (arv_device_get_feature(device, info->featureName) != nullptr);
    if (!*hasFeature) {
        yCWarning(ARV) << "Feature" << info->featureName << "not found in camera";
        return true;
    }

    bool compatible;
    checkEnabled(f, &compatible);
    if (!compatible){
        *hasFeature = false;
        return true;
        yCWarning(ARV) << "Feature" << info->featureName << "not in camera but not compatible for pixelFormat.";
    }

    return true;
}

/* ============================================
 * Set Feature Implementation
 * ============================================ */
bool AravisGigE::setFeature(int feature, double value) {
    auto f = static_cast<cameraFeature_id_t>(feature);
    const FeatureInfo* info = getFeatureInfo(f);
    
    // Basic verifications
    if (!info || !info->featureName) {
        yCError(ARV) << "Feature" << feature << "not supported";
        return false;
    }

    yCDebug(ARV) << "Setting feature" << info->featureName << "to value" << value;

    // 1. Check feature compatibility with current pixel format
    bool compatible;
    if (!checkEnabled(f, &compatible)) {
        return false;
    }
    
    if (!compatible) {
        yCError(ARV) << "Feature" << info->featureName << "not compatible with current pixel format";
        return false;
    }

    // 2. Check if feature is in auto mode
    if (info->autoName) {
        FeatureMode currentMode;
        if (getMode(f, &currentMode) && currentMode == MODE_AUTO) {
            yCWarning(ARV) << "Feature" << info->featureName << "is in auto mode, manual change ignored";
            return false;
        }
    }

    // 3. Activate feature if disabled
    bool hasauto = false;
    hasAuto(f, &hasauto);
    if (info->enabledName && !hasauto) {
        bool isActive;
        if (!getActive(f, &isActive)) {
            return false;
        }
        
        if (!isActive) {
            yCInfo(ARV) << "Auto-enabling feature" << info->featureName;
            if (!setActive(f, true)) {
                yCError(ARV) << "Failed to enable feature" << info->featureName;
                return false;
            }
        }
    }

    // 4. Set the value
    ArvDevice* device = arv_camera_get_device(camera);
    GError* error = nullptr;
    
    if (yarp_arv_int_feature_map.count(f)) {
        arv_device_set_integer_feature_value(device, info->featureName, static_cast<gint64>(value), &error);
    } else if (yarp_arv_float_feat_map.count(f)) {
        arv_device_set_float_feature_value(device, info->featureName, static_cast<gdouble>(value), &error);
    } else {
        yCError(ARV) << "Feature type not recognized";
        return false;
    }

    if (error) {
        yCError(ARV) << "Error setting feature" << info->featureName << ":" << error->message;
        g_error_free(error);
        return false;
    }

    return true;
}

bool AravisGigE::getFeature(int feature, double * value) {
    yCDebug(ARV) << "Getting value for feature" << feature;

    auto f = static_cast<cameraFeature_id_t>(feature);
    const FeatureInfo* info = getFeatureInfo(f);
    
    if (!info || !info->featureName) {
        yCError(ARV) << "Feature" << feature << "not supported";
        return false;
    }

    ArvDevice* device = arv_camera_get_device(camera);
    if (!device) {
        yCError(ARV) << "Camera device not available";
        return false;
    }

    GError* error = nullptr;
    if (yarp_arv_int_feature_map.count(f)) {
        *value = arv_device_get_integer_feature_value(device, info->featureName, &error);
    } else if (yarp_arv_float_feat_map.count(f)) {
        *value = arv_device_get_float_feature_value(device, info->featureName, &error);
    } else {
        yCError(ARV) << "Feature type not recognized";
        return false;
    }

    if (error) {
        yCError(ARV) << "Error getting feature" << info->featureName << ":" << error->message;
        g_error_free(error);
        return false;
    }

    yCDebug(ARV) << "Feature" << info->featureName << "value:" << *value;
    return true;
}

bool AravisGigE::setFeature(int feature, double value1, double value2) {
    yCError(ARV) << "No features with 2 values supported!";
    return false;
}

bool AravisGigE::getFeature(int feature, double * value1, double * value2) {
    return getFeatureLimits(feature, value1, value2);
}

/* ============================================
 * On/Off Feature Implementation
 * ============================================ */
bool AravisGigE::hasOnOff(int feature, bool * hasOnOff) {
    auto f = static_cast<cameraFeature_id_t>(feature);
    const FeatureInfo* info = getFeatureInfo(f);
    
    if (!info) {
        yCError(ARV) << "Feature" << feature << "not supported";
        return false;
    }

    *hasOnOff = (info->enabledName != nullptr);
    return true;
}

bool AravisGigE::setActive(int feature, bool onoff) {
    auto f = static_cast<cameraFeature_id_t>(feature);
    const FeatureInfo* info = getFeatureInfo(f);
    
    if (!info || !info->enabledName) {
        yCError(ARV) << "Feature" << feature << "does not support on/off";
        return false;
    }

    yCDebug(ARV) << "Setting feature" << info->featureName << (onoff ? "ON" : "OFF");

    ArvDevice* device = arv_camera_get_device(camera);
    if (!device) {
        yCError(ARV) << "Camera device not available";
        return false;
    }

    GError* error = nullptr;
    arv_device_set_boolean_feature_value(device, info->enabledName, onoff, &error);
    
    if (error) {
        yCError(ARV) << "Error setting on/off for" << info->featureName << ":" << error->message;
        g_error_free(error);
        return false;
    }

    return true;
}

bool AravisGigE::getActive(int feature, bool * isActive) {
    auto f = static_cast<cameraFeature_id_t>(feature);
    const FeatureInfo* info = getFeatureInfo(f);
    
    if (!info || !info->enabledName) {
        yCError(ARV) << "Feature" << feature << "does not support on/off";
        return false;
    }

    ArvDevice* device = arv_camera_get_device(camera);
    if (!device) {
        yCError(ARV) << "Camera device not available";
        return false;
    }

    GError* error = nullptr;
    *isActive = arv_device_get_boolean_feature_value(device, info->enabledName, &error);
    
    if (error) {
        yCError(ARV) << "Error getting on/off for" << info->featureName << ":" << error->message;
        g_error_free(error);
        return false;
    }

    yCDebug(ARV) << "Feature" << info->featureName << "is" << (*isActive ? "ON" : "OFF");
    return true;
}

/* ============================================
 * Auto/Manual Mode Implementation
 * ============================================ */
bool AravisGigE::hasAuto(int feature, bool* hasAuto) {
    auto f = static_cast<cameraFeature_id_t>(feature);
    const FeatureInfo* info = getFeatureInfo(f);
    
    if (!info) {
        yCError(ARV) << "Feature" << feature << "not supported";
        return false;
    }

    ArvDevice *device = arv_camera_get_device(camera);
    if (!device) {
        yCError(ARV) << "Camera device not available";
        return false;
    }

    GError* error = nullptr;
    if (arv_camera_is_feature_available(camera, info->autoName, &error)==1 && arv_device_get_feature(device, info->autoName)!=0){
        *hasAuto = true;
        return true;
    }

    if (error) {
        g_error_free(error);
        *hasAuto = false;
        return false;
    }

    *hasAuto = false;
    return true;
}

bool AravisGigE::hasManual(int feature, bool* hasManual) {
    // All numeric features support manual mode by default
    auto f = static_cast<cameraFeature_id_t>(feature);
    *hasManual = (yarp_arv_int_feature_map.count(f) || yarp_arv_float_feat_map.count(f));
    return true;
}

bool AravisGigE::hasOnePush(int feature, bool* hasOnePush) {
    auto f = static_cast<cameraFeature_id_t>(feature);
    const FeatureInfo* info = getFeatureInfo(f);
    
    if (!info) {
        yCError(ARV) << "Feature" << feature << "not supported";
        return false;
    }

    *hasOnePush = info->supportsOnePush;
    return true;
}

bool AravisGigE::setMode(int feature, FeatureMode mode) {
    auto f = static_cast<cameraFeature_id_t>(feature);
    const FeatureInfo* info = getFeatureInfo(f);
    
    if (!info || !info->autoName) {
        yCError(ARV) << "Feature" << feature << "does not support auto modes";
        return false;
    }

    yCDebug(ARV) << "Setting mode" << mode << "for feature" << info->featureName;

    ArvDevice* device = arv_camera_get_device(camera);
    if (!device) {
        yCError(ARV) << "Camera device not available";
        return false;
    }

    const char* mode_str = nullptr;
    switch (mode) {
        case MODE_AUTO:     mode_str = "Continuous"; break;
        case MODE_MANUAL:   mode_str = "Off"; break;
        default:
            yCError(ARV) << "Invalid mode specified";
            return false;
    }

    GError* error = nullptr;
    arv_device_set_string_feature_value(device, info->autoName, mode_str, &error);
    
    if (error) {
        yCError(ARV) << "Failed to set mode for" << info->featureName << ":" << error->message;
        g_error_free(error);
        return false;
    }

    return true;
}

bool AravisGigE::getMode(int feature, FeatureMode* mode) {
    auto f = static_cast<cameraFeature_id_t>(feature);
    const FeatureInfo* info = getFeatureInfo(f);
    
    if (!info) {
        yCError(ARV) << "Feature" << feature << "not supported";
        return false;
    }

    // If no auto mode, it's manual by default
    if (!info->autoName) {
        *mode = MODE_MANUAL;
        return true;
    }

    ArvDevice* device = arv_camera_get_device(camera);
    if (!device) {
        yCError(ARV) << "Camera device not available";
        return false;
    }

    GError* error = nullptr;
    const char* current_mode = arv_device_get_string_feature_value(device, info->autoName, &error);
    
    if (error) {
        yCError(ARV) << "Failed to get mode for" << info->featureName << ":" << error->message;
        g_error_free(error);
        return false;
    }

    if (!current_mode) {
        *mode = MODE_MANUAL;
        return true;
    }

    if (strcmp(current_mode, "Continuous") == 0) {
        *mode = MODE_AUTO;
    } else if (strcmp(current_mode, "Once") == 0) {
        *mode = MODE_AUTO;
    } else if (strcmp(current_mode, "Off") == 0) {
        *mode = MODE_MANUAL;
    } else {
        *mode = MODE_UNKNOWN;
    }

    return true;
}

bool AravisGigE::setOnePush(int feature) {
    if (!setMode(feature, MODE_AUTO)) {
        return false;
    }
    return setMode(feature, MODE_MANUAL);
}

/* ============================================
 * Feature Compatibility Check
 * ============================================ */
bool AravisGigE::checkEnabled(cameraFeature_id_t feature, bool* compatible) {
    if (!compatible) {
        return false;
    }

    const FeatureInfo* info = getFeatureInfo(feature);
    if (!info) {
        *compatible = false;
        return true;
    }
    ArvDevice* device = arv_camera_get_device(camera);

    GError* error = nullptr;
    if (arv_camera_is_feature_available(camera, info->enabledName, &error)==0 && arv_device_get_feature(device, info->enabledName)!=0){
        *compatible = false;
        return true;
    }

    if (error) {
        g_error_free(error);
        *compatible = false;
        return false;
    }

    *compatible =true;
    return true;
}

/* ============================================
 * Feature Limits Implementation
 * ============================================ */
bool AravisGigE::getFeatureLimits(int feature, double *min, double *max) {
    auto f = static_cast<cameraFeature_id_t>(feature);
    const FeatureInfo* info = getFeatureInfo(f);
    
    if (!info || !info->featureName) {
        yCError(ARV) << "Feature" << feature << "not supported";
        return false;
    }

    ArvDevice* device = arv_camera_get_device(camera);
    if (!device) {
        yCError(ARV) << "Camera device not available";
        return false;
    }

    if (!arv_device_get_feature(device, info->featureName)) {
        yCWarning(ARV) << "Feature" << info->featureName << "not available on this device";
        return false;
    }

    GError* error = nullptr;
    
    // Try integer bounds first
    gint64 min_int = 0, max_int = 0;
    arv_device_get_integer_feature_bounds(device, info->featureName, &min_int, &max_int, &error);
    
    if (!error && min_int != max_int) {
        *min = static_cast<double>(min_int);
        *max = static_cast<double>(max_int);
        return true;
    }
    
    if (error) {
        g_error_free(error);
        error = nullptr;
    }

    // Try float bounds if integer failed
    gdouble min_float = 0.0, max_float = 0.0;
    arv_device_get_float_feature_bounds(device, info->featureName, &min_float, &max_float, &error);
    
    if (!error && min_float != max_float) {
        *min = static_cast<double>(min_float);
        *max = static_cast<double>(max_float);
        return true;
    }
    
    if (error) {
        ArvDevice* device = arv_camera_get_device(camera);
        yCError(ARV) << "Error getting bounds for" << info->featureName << ":" << error->message;
        g_error_free(error);
    }

    yCWarning(ARV) << "Could not retrieve valid range for feature" << info->featureName;
    return false;
}

/* ============================================
 * Feature Listing Implementation
 * ============================================ */
void AravisGigE::listAvailableFeatures() {
    std::cout << "Listing available features:\n";

    for (const auto& entry : yarp_arv_int_feature_map) {
        printFeatureInfo(entry.first, entry.second);
    }

    for (const auto& entry : yarp_arv_float_feat_map) {
        printFeatureInfo(entry.first, entry.second);
    }
}

void AravisGigE::printFeatureInfo(cameraFeature_id_t featureId, const FeatureInfo& info) {
    bool available = false;
    if (!hasFeature(featureId, &available) || !available) {
        return;
    }

    std::cout << "- " << info.featureName << " (ID " << featureId << "):\n";
    
    // Print mode information if available
    if (info.autoName) {
        FeatureMode mode;
        if (getMode(featureId, &mode)) {
            std::cout << "  Mode: ";
            switch (mode) {
                case MODE_AUTO: std::cout << "Auto"; break;
                case MODE_MANUAL: std::cout << "Manual"; break;
                default: std::cout << "Unknown";
            }
            std::cout << "\n";
        }
    }

    // Print active status if available
    if (info.enabledName) {
        bool isActive;
        if (getActive(featureId, &isActive)) {
            std::cout << "  Status: " << (isActive ? "Enabled" : "Disabled") << "\n";
        }
    }

    // Print current value
    double value;
    if (getFeature(featureId, &value)) {
        std::cout << "  Current value: " << value << "\n";
    }

    // Print limits
    double min, max;
    if (getFeatureLimits(featureId, &min, &max)) {
        std::cout << "  Range: " << min << " to " << max << "\n";
    }

    // Print compatibility
    bool compatible;
    if (checkEnabled(featureId, &compatible)) {
        std::cout << "  Compatible with current format: " << (compatible ? "Yes" : "No") << "\n";
    }

    bool jauto;
    if (hasAuto(featureId, &jauto)) {
        std::cout << "  auto: " << (jauto ? "Yes" : "No") << "\n";
    }

}