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

bool AravisGigE::hasFeature(int feature, bool * hasFeature)
{
    yCDebug(ARV) << "Request to know if camera has feature" << feature;

    //-- Check if YARP supports this feature
    auto f = static_cast<cameraFeature_id_t>(feature);

    if (f < YARP_FEATURE_BRIGHTNESS || f > YARP_FEATURE_NUMBER_OF - 1)
    {
        yCError(ARV) << "Feature" << feature << "not supported by YARP";
        return false;
    }

    //-- Check if device supports this feature
    *hasFeature =
        yarp_arv_int_feature_map.find(f) != yarp_arv_int_feature_map.end() ||
        yarp_arv_float_feat_map.find(f) != yarp_arv_float_feat_map.end();

    return true;
}

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
        arv_device_set_integer_feature_value(arv_camera_get_device(camera), yarp_int_feature->second, value, nullptr);
    }
    else if (auto yarp_float_feature = yarp_arv_float_feat_map.find(f); yarp_float_feature != yarp_arv_float_feat_map.end())
    {
        //-- Check {here} that value is within range here (when you can inspect ranges)
        arv_device_set_float_feature_value(arv_camera_get_device(camera), yarp_float_feature->second, value, nullptr);
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
        *value = arv_device_get_integer_feature_value(arv_camera_get_device(camera), yarp_int_feature->second, nullptr);
    }
    else if (auto yarp_float_feature = yarp_arv_float_feat_map.find(f); yarp_float_feature != yarp_arv_float_feat_map.end())
    {
        *value = arv_device_get_float_feature_value(arv_camera_get_device(camera), yarp_float_feature->second, nullptr);
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
    yCError(ARV) << "No features with 2 values supported!";
    return false;
}

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

    //-- Check if device supports this feature
    //-- (No feature supports on/off mode currently. If any did, the code to discover that would go here)
    *hasOnOff = false;
    return true;
}

bool AravisGigE::setActive(int feature, bool onoff)
{
    yCDebug(ARV) << "Requested to set on/of mode for feature" << feature;

    if (bool b; !hasFeature(feature, &b) || !b || !hasOnOff(feature, &b) || !b)
    {
        yCError(ARV) << "Feature is not available or does not support on/off mode";
        return false;
    }

    //-- Check if device supports this feature
    //-- (No feature supports on/off mode currently. If any did, the code to discover that would go here)
    return true;
}

bool AravisGigE::getActive(int feature, bool * isActive)
{
    yCDebug(ARV) << "Requested to get on/of mode for feature" << feature;

    if (bool b; !hasFeature(feature, &b) || !b || !hasOnOff(feature, &b) || !b)
    {
        yCError(ARV) << "Feature is not available or does not support on/off mode";
        return false;
    }

    //-- Check if device supports this feature
    //-- (No feature supports on/off mode currently. If any did, the code to discover that would go here)
    *isActive = false;
    return true;
}

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

    if (bool b; !hasFeature(feature, &b) || !b || (!hasAuto(feature, &b) || !b) && (!hasManual(feature, &b) || !b) && (!hasOnePush(feature, &b) || !b))
    {
        yCError(ARV) << "Feature is not available or does not support auto/manual/OnePush mode";
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

void AravisGigE::listAvailableFeatures()
{
    std::cout << "Listing available features:\n";

    // Map of IDs
    std::map<int, std::string> feature_names = {
        {YARP_FEATURE_BRIGHTNESS, "Brightness"},
        {YARP_FEATURE_EXPOSURE, "Exposure"},
        {YARP_FEATURE_SHARPNESS, "Sharpness"},
        {YARP_FEATURE_WHITE_BALANCE, "White Balance"},
        {YARP_FEATURE_HUE, "Hue"},
        {YARP_FEATURE_SATURATION, "Saturation"},
        {YARP_FEATURE_GAMMA, "Gamma"},
        {YARP_FEATURE_SHUTTER, "Shutter"},
        {YARP_FEATURE_GAIN, "Gain"},
        {YARP_FEATURE_IRIS, "Iris"},
        {YARP_FEATURE_FOCUS, "Focus"},
        {YARP_FEATURE_TEMPERATURE, "Temperature"},
        {YARP_FEATURE_TRIGGER, "Trigger"},
        {YARP_FEATURE_TRIGGER_DELAY, "Trigger Delay"},
        {YARP_FEATURE_WHITE_SHADING, "White Shading"},
        {YARP_FEATURE_FRAME_RATE, "Frame Rate"},
        {YARP_FEATURE_ZOOM, "Zoom"},
        {YARP_FEATURE_PAN, "Pan"},
        {YARP_FEATURE_TILT, "Tilt"},
        {YARP_FEATURE_OPTICAL_FILTER, "Optical Filter"},
        {YARP_FEATURE_CAPTURE_SIZE, "Capture Size"},
        {YARP_FEATURE_CAPTURE_QUALITY, "Capture Quality"},
        {YARP_FEATURE_MIRROR, "Mirror"}
    };

    for (const auto &feature : feature_names)
    {
        bool available = false;
        if (hasFeature(feature.first, &available) && available) {
            FeatureMode mode;
            getMode(feature.first, &mode);
            
            bool isActive;
            getActive(feature.first, &isActive);

            bool onOff;
            hasOnOff(feature.first, &onOff);

            std::cout << "- " << feature.second << " (ID " << feature.first << ") is available. Mode: " << mode << ". Isactive: " 
            << isActive << ". Has OnOff: " << onOff << "\n";

            ArvDevice *device = arv_camera_get_device(camera);

            gint64 min_val = 0, max_val = 0;
            arv_device_get_integer_feature_bounds(device, feature.second.c_str(), &min_val, &max_val, nullptr);

            std::cout << "  → Rango de " << feature.second << ": " << min_val << " - " << max_val << std::endl;

        }
    }
}
