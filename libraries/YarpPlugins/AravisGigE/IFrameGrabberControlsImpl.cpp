#include <iostream>
#include <yarp/os/LogStream.h>

#include "AravisGigE.hpp"
#include "LogComponent.hpp"

using namespace roboticslab;

bool AravisGigE::getCameraDescription(CameraDescriptor * camera)
{
    if (arv_camera_is_uv_device(this->camera))
    {
        camera->busType = BUS_USB;
    }
    else
    {
        camera->busType = BUS_UNKNOWN; //-- Temporary until we add a BUS_GIGE in YARP
    }

    camera->deviceDescription = std::string(arv_camera_get_device_id(this->camera, nullptr)) + ": " + arv_camera_get_model_name(this->camera, nullptr);
    return true;
}

bool AravisGigE::hasFeature(int feature, bool * hasFeature) {
    yCDebug(ARV) << "Checking feature availability: " << feature;

    auto f = static_cast<cameraFeature_id_t>(feature);

    if (f < YARP_FEATURE_BRIGHTNESS || f > YARP_FEATURE_NUMBER_OF - 1) {
        yCError(ARV) << "Feature" << feature << "not supported by YARP";
        return false;
    }

    //-- Check if device supports this feature
    ArvDevice *device = arv_camera_get_device(camera);
    const char *feature_name = feature_names.count(f) ?
                                feature_names[f] : nullptr;

    if (feature_name && arv_device_get_feature(device, feature_name)) {
        *hasFeature = true;
    } else {
        *hasFeature = false;
        yCWarning(ARV) << "Feature" << feature << "not found in camera";
    }

    return true;
}

/* ========================================================================================
============================================ Set =======================================
========================================================================================== */
bool AravisGigE::setFeature(int feature, double value)
{
    yCDebug(ARV) << "Requested to set feature" << feature;

    //-- Check if YARP supports this feature
    auto f = static_cast<cameraFeature_id_t>(feature);

    if (f < YARP_FEATURE_BRIGHTNESS || f > YARP_FEATURE_NUMBER_OF - 1)
    {
        yCError(ARV) << "Feature not supported by YARP";
        return false;
    }

    if (auto yarp_int_feature = yarp_arv_int_feature_map.find(f); yarp_int_feature != yarp_arv_int_feature_map.end())
    {
        //-- Check {here} that value is within range here (when you can inspect ranges)
        setActive(yarp_int_feature->first, true);
        GError *error = nullptr;
        arv_device_set_integer_feature_value(arv_camera_get_device(camera), yarp_int_feature->second.featureName, value, &error);

        if (error) {
            yCError(ARV) << "Error setting feature " << yarp_int_feature->second.featureName << ": " << error->message;
            g_error_free(error);
            return false;
        }
    }
    else if (auto yarp_float_feature = yarp_arv_float_feat_map.find(f); yarp_float_feature != yarp_arv_float_feat_map.end())
    {
        //-- Check {here} that value is within range here (when you can inspect ranges)
        setActive(yarp_float_feature->first, true);
        GError *error = nullptr;
        arv_device_set_float_feature_value(arv_camera_get_device(camera), yarp_float_feature->second.featureName, value, &error);

        if (error) {
            yCError(ARV) << "Error setting feature " << yarp_float_feature->second.featureName << ": " << error->message;
            g_error_free(error);
            return false;
        }


    }
    else
    {
        yCError(ARV) << "Property with yarp id" << f << "not available";
        return false;
    }

    return true;
}

bool AravisGigE::getFeature(int feature, double * value)
{
    yCDebug(ARV) << "Property with yarp id" << feature << "requested";

    //-- Check if YARP supports this feature
    auto f = static_cast<cameraFeature_id_t>(feature);

    if (f < YARP_FEATURE_BRIGHTNESS || f > YARP_FEATURE_NUMBER_OF - 1)
    {
        yCError(ARV) << "Feature not supported by YARP";
        return false;
    }

    if (auto yarp_int_feature = yarp_arv_int_feature_map.find(f); yarp_int_feature != yarp_arv_int_feature_map.end())
    {
        *value = arv_device_get_integer_feature_value(arv_camera_get_device(camera), yarp_int_feature->second.featureName, nullptr);
    }
    else if (auto yarp_float_feature = yarp_arv_float_feat_map.find(f); yarp_float_feature != yarp_arv_float_feat_map.end())
    {
        *value = arv_device_get_float_feature_value(arv_camera_get_device(camera), yarp_float_feature->second.featureName, nullptr);
    }
    else
    {
        yCError(ARV) << "Property with yarp id" << f << "not available";
        return false;
    }

    yCDebug(ARV) << "Value:" << *value;
    return true;
}

bool AravisGigE::setFeature(int feature, double value1, double value2)
{
    yCError(ARV) << "No features with 2 values supported!";
    return false;
}

bool AravisGigE::getFeature(int feature, double * value1, double * value2)
{
    return getFeatureLimits(feature, value1, value2);
}

/* ========================================================================================
============================================ On/Off =======================================
========================================================================================== */

bool AravisGigE::hasOnOff(int feature, bool * hasOnOff)
{
    yCDebug(ARV) << "Request to know if feature" << feature << "has on/off mode";

    //-- Check if YARP supports this feature
    auto f = static_cast<cameraFeature_id_t>(feature);

    if (f < YARP_FEATURE_BRIGHTNESS || f > YARP_FEATURE_NUMBER_OF - 1)
    {
        yCError(ARV) << "Feature not supported by YARP";
        return false;
    }

    //-- Check if device supports this feature and if it is a binary on/off type
    const char* feature_name = feature_names.count(f) ? feature_names[f] : nullptr;

    if (feature_name) {
        // Check if the feature is a boolean or on/off feature
        if (arv_device_get_feature(arv_camera_get_device(camera), feature_name)) {
            // This might require querying a property or checking the feature value.
            *hasOnOff = true;
            return true;
        }
    }

    //-- If no on/off support, return false
    *hasOnOff = false;
    return true;
}

bool AravisGigE::setActive(int feature, bool onoff)
{
    yCDebug(ARV) << "Requested to set on/off mode for feature" << feature;

    //-- Check if YARP supports this feature
    auto f = static_cast<cameraFeature_id_t>(feature);

    if (f < YARP_FEATURE_BRIGHTNESS || f > YARP_FEATURE_NUMBER_OF - 1)
    {
        yCError(ARV) << "Feature not supported by YARP";
        return false;
    }

    bool hasOnOffFlag = false;
    if (!hasFeature(f, &hasOnOffFlag) || !hasOnOffFlag) {
        yCError(ARV) << "Feature is not available or does not support on/off mode";
        return false;
    }

    FeatureInfo feature_name = 
        (yarp_arv_int_feature_map.count(f) ? yarp_arv_int_feature_map[f] : 
        (yarp_arv_float_feat_map.count(f) ? yarp_arv_float_feat_map[f] : FeatureInfo{nullptr}));

    if (feature_name.featureName != nullptr) {
        int current_value = arv_device_get_integer_feature_value(arv_camera_get_device(camera), feature_name.enabledName, nullptr);
        if (current_value != (onoff ? 1 : 0)) {
            arv_device_set_boolean_feature_value(arv_camera_get_device(camera), feature_name.enabledName, true, nullptr);
            yCInfo(ARV) << "Feature " << feature_name.enabledName << " set to " << (onoff ? "ON" : "OFF");
            return true;
        } else {
            yCWarning(ARV) << "Feature " << feature_name.enabledName << " is already in the requested state.";
            return true;
        }
    }

    yCError(ARV) << "Feature " << feature << " could not be set to on/off mode.";
    return false;
}


bool AravisGigE::getActive(int feature, bool * isActive)
{
    yCDebug(ARV) << "Requested to get on/off mode for feature" << feature;

    //-- Check if YARP supports this feature
    auto f = static_cast<cameraFeature_id_t>(feature);

    if (f < YARP_FEATURE_BRIGHTNESS || f > YARP_FEATURE_NUMBER_OF - 1)
    {
        yCError(ARV) << "Feature not supported by YARP";
        return false;
    }

    bool hasOnOffFlag = false;
    if (!hasFeature(f, &hasOnOffFlag) || !hasOnOffFlag) {
        yCError(ARV) << "Feature is not available or does not support on/off mode";
        return false;
    }

    FeatureInfo feature_name = 
        (yarp_arv_int_feature_map.count(f) ? yarp_arv_int_feature_map[f] : 
        (yarp_arv_float_feat_map.count(f) ? yarp_arv_float_feat_map[f] : FeatureInfo{nullptr}));

    if (feature_name.featureName != nullptr) {
        int current_value = arv_device_get_integer_feature_value(arv_camera_get_device(camera), feature_name.enabledName, nullptr);
        *isActive = (current_value > 0);
        yCInfo(ARV) << "Feature " << feature_name.enabledName << " is " << (*isActive ? "ON" : "OFF");
        return true;
    }

    yCError(ARV) << "Feature " << feature << " could not be read.";
    return false;
}

/* =======================================================================================================================================
============================================ Auto (sin terminar porque de momneto no es necesario) =======================================
========================================================================================================================================== */

bool AravisGigE::hasAuto(int feature, bool * hasAuto)
{
    yCDebug(ARV) << "Request to know if feature" << feature << "has auto mode";

    //-- Check if YARP supports this feature
    auto f = static_cast<cameraFeature_id_t>(feature);

    if (f < YARP_FEATURE_BRIGHTNESS || f > YARP_FEATURE_NUMBER_OF - 1)
    {
        yCError(ARV) << "Feature not supported by YARP";
        return false;
    }

    //-- Check if device supports this feature
    //-- (No feature supports auto mode currently. If any did, the code to discover that would go here)
    *hasAuto = false;
    return true;
}

bool AravisGigE::hasManual(int feature, bool * hasManual)
{
    yCDebug(ARV) << "Request to know if feature" << feature << "has manual mode";

    //-- Check if YARP supports this feature
    auto f = static_cast<cameraFeature_id_t>(feature);

    if (f < YARP_FEATURE_BRIGHTNESS || f > YARP_FEATURE_NUMBER_OF - 1)
    {
        yCError(ARV) << "Feature not supported by YARP";
        return false;
    }

    //-- Check if device supports this feature
    //-- (No feature supports manual mode currently. If any did, the code to discover that would go here)
    *hasManual = false;
    return true;
}

bool AravisGigE::hasOnePush(int feature, bool * hasOnePush)
{
    yCDebug(ARV) << "Request to know if feature" << feature << "has one push mode";

    //-- Check if YARP supports this feature
    auto f = static_cast<cameraFeature_id_t>(feature);

    if (f < YARP_FEATURE_BRIGHTNESS || f > YARP_FEATURE_NUMBER_OF - 1)
    {
        yCError(ARV) << "Feature not supported by YARP";
        return false;
    }

    //-- Check if device supports this feature
    //-- (No feature supports one push mode currently. If any did, the code to discover that would go here)
    *hasOnePush = false;
    return true;
}

bool AravisGigE::setMode(int feature, FeatureMode mode)
{
    yCDebug(ARV) << "Requested to set auto/manual mode for feature" << feature;

    if (bool b; !hasFeature(feature, &b) || !b || (!hasAuto(feature, &b) || !b) && (!hasManual(feature, &b) || !b))
    {
        yCError(ARV) << "Feature is not available or does not support auto/manual mode";
        return false;
    }

    //-- Check if device supports this feature
    //-- (No feature supports auto/manual mode currently. If any did, the code to discover that would go here)
    return true;
}

bool AravisGigE::getMode(int feature, FeatureMode * mode)
{
    yCDebug(ARV) << "Requested to get auto/manual mode for feature" << feature;

    if (bool b; !hasFeature(feature, &b) || !b || (!hasAuto(feature, &b) || !b) && (!hasManual(feature, &b) || !b))
    {
        yCError(ARV) << "Feature is not available or does not support auto/manual mode";
        return false;
    }

    //-- Check if device supports this feature
    //-- (No feature supports auto/manual mode currently. If any did, the code to discover that would go here)
    *mode = MODE_UNKNOWN;

    return true;
}


bool AravisGigE::setOnePush(int feature)
{
    yCDebug(ARV) << "Requested to set one push mode for feature" << feature;

    if (bool b; !hasFeature(feature, &b) || !b || !hasOnePush(feature, &b) || !b)
    {
        yCError(ARV) << "Feature is not available or does not support one push mode";
        return false;
    }

    //-- Check if device supports this feature
    //-- (No feature supports one push mode currently. If any did, the code to discover that would go here)
    return true;
}

/* ========================================================================================
============================================ Min/Max =======================================
========================================================================================== */
bool AravisGigE::getFeatureLimits(int feature, double *min, double *max)
{
    auto f = static_cast<cameraFeature_id_t>(feature);

    if (f < YARP_FEATURE_BRIGHTNESS || f > YARP_FEATURE_NUMBER_OF - 1)
    {
        yCError(ARV) << "Feature not supported by YARP";
        return false;
    }

    FeatureInfo featureName = 
        (yarp_arv_int_feature_map.count(f) ? yarp_arv_int_feature_map[f] : 
        (yarp_arv_float_feat_map.count(f) ? yarp_arv_float_feat_map[f] : FeatureInfo{nullptr}));

    if (featureName.enabledName == nullptr) {
        return false;
    }

    if (!arv_device_get_feature(arv_camera_get_device(camera), featureName.featureName)) {
        yWarning() << "Feature" << featureName.featureName << "not available on this device";
        return false;
    }

    gint64 min_int = 0, max_int = 0;
    arv_device_get_integer_feature_bounds(arv_camera_get_device(camera), featureName.featureName, &min_int, &max_int, nullptr);
    if (min_int != max_int && min_int > std::numeric_limits<gint64>::min() && max_int < std::numeric_limits<gint64>::max()) {
        *min = static_cast<double>(min_int);
        *max = static_cast<double>(max_int);
        return true;
    }

    gdouble min_float = 0.0, max_float = 0.0;
    arv_device_get_float_feature_bounds(arv_camera_get_device(camera), featureName.featureName, &min_float, &max_float, nullptr);
    if (min_float != max_float && min_float > -std::numeric_limits<gdouble>::max() && max_float < std::numeric_limits<gdouble>::max()) {
        *min = static_cast<double>(min_float);
        *max = static_cast<double>(max_float);
        return true;
    }

    yWarning() << "Could not retrieve valid range for feature" << featureName.featureName;
    return false;
}


/* ========================================================================================
============================================ List =======================================
========================================================================================== */

void AravisGigE::listAvailableFeatures()
{
    std::cout << "Listing available features:\n";

    ArvDevice *device = arv_camera_get_device(camera);

    for (const auto &feature : feature_names)
    {
        bool available = false;
        if (hasFeature(feature.first, &available) && available) {
            FeatureMode mode = MODE_UNKNOWN;
            bool modeSuccess = getMode(feature.first, &mode);

            bool isActive = false;
            bool activeSuccess = getActive(feature.first, &isActive);

            bool onOff = false;
            bool onOffSuccess = hasOnOff(feature.first, &onOff);

            double value = 0.0;
            bool valueSuccess = getFeature(feature.first, &value);

            std::cout << "- " << feature.second << " (ID " << feature.first << ") is available. "
                    << "Mode: " << (modeSuccess ? std::to_string(mode) : "No mode") << ". "
                    << "IsActive: " << (activeSuccess ? (isActive ? "ON" : "OFF") : "No active") << ". "
                    << "Has On/Off: " << (onOffSuccess ? (onOff ? "Yes" : "No") : "No on/off") << ". "
                    << "Value: " << (valueSuccess ? std::to_string(value) : "No value") << "\n";


            if (!arv_device_get_feature(device, feature.second)) {
                std::cout << "  -- " << feature.second << " No soported range values." << std::endl;
                continue;
            }

            double min, max;
            if (getFeatureLimits(feature.first, &min, &max)) {
                std::cout << "\t- Range: " << min << " - " << max << std::endl;
            }            
        }
    }
}
