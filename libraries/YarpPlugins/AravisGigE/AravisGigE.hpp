#ifndef __ARAVIS_GIGE_HPP__
#define __ARAVIS_GIGE_HPP__

#include <map>
#include <thread>

#include <yarp/dev/DeviceDriver.h>
#include <yarp/dev/IFrameGrabberControls.h>
#include <yarp/dev/IFrameGrabberImage.h>
#include <arv.h>

namespace roboticslab
{

/**
 * @ingroup YarpPlugins
 * @defgroup AravisGigE
 * @brief Contains roboticslab::AravisGigE.
 */

 /**
  * @ingroup AravisGigE
  * @brief Implementation for GigE cameras using Aravis as driver.
  */
class AravisGigE : public yarp::dev::DeviceDriver,
                   public yarp::dev::IFrameGrabberImageRaw,
                   public yarp::dev::IFrameGrabberControls,
                   public yarp::dev::IFrameGrabberImage
{
public:

    ~AravisGigE() override { close(); }

    //  --------- DeviceDriver Declarations. Implementation in DeviceDriverImpl.cpp ---------
    bool open(yarp::os::Searchable & config) override;
    bool close() override;

    //  --------- IFrameGrabberImageRaw Declarations. Implementation in IFrameGrabberImageRawImpl.cpp ---------
    bool getImage(yarp::sig::ImageOf<yarp::sig::PixelMono> & image) override;
    bool getImage(yarp::sig::ImageOf<yarp::sig::PixelRgb> &image) override;
    int height() const override;
    int width() const override;

    // ---------- Terminal ----------------------
    void runInteractiveTerminal();

    // ---------- IFrameGrabberControls Declarations. Implementation in IFrameGrabberControlsImpl.cpp ---------
    bool getCameraDescription(CameraDescriptor * camera) override; // descripcion de la camara.
    bool hasFeature(int feature, bool * hasFeature) override; // Tiene característica??
    bool setFeature(int feature, double value) override; // Establece valor
    bool getFeature(int feature, double * value) override; //Obtiene valor
    bool setFeature(int feature, double value1, double value2) override;
    bool getFeature(int feature, double * value1, double * value2) override;
    bool hasOnOff(int feature, bool * hasOnOff) override; // Se puede activar o desactiavr??
    bool setActive(int feature, bool onoff) override; // Activamos
    bool getActive(int feature, bool * isActive) override; // Vemos si activada??
    bool hasAuto(int feature, bool * hasAuto) override; // Tiene auto ??
    bool hasManual(int feature, bool * hasManual) override; // Tiene manual ??
    bool hasOnePush(int feature, bool * hasOnePush) override; // admite ajuste automatico al presionar un boton ??
    bool setMode(int feature, FeatureMode mode) override; // ponemos automatico o manual
    bool getMode(int feature, FeatureMode * mode) override; // esta en automatico o manual
    bool setOnePush(int feature) override; // activamos este modod

    void listAvailableFeatures();
    bool checkFeatureExistenceAndGetValue(const std::string &featureName, double &value);
    cameraFeature_id_t id_find(const std::string &feature_name);

private:
    ArvCamera       * camera {nullptr};      // camera to control
    ArvStream       * stream {nullptr};      // object for video stream reception
    void            * framebuffer {nullptr}; //

    unsigned int    payload {0};            // width x height x pixel width

    int             widthMin {0};           // camera sensor minium width
    int             widthMax {0};           // camera sensor maximum width
    int             heightMin {0};          // camera sensor minium height
    int             heightMax {0};          // camera sensor maximum height
    double          fpsMin {0.0};           // camera minimum fps
    double          fpsMax {0.0};           // camera maximum fps
    double          gainMin {0.0};          // camera minimum gain
    double          gainMax {0.0};          // camera maximum gain
    double          exposureMin {0.0};      // camera's minimum exposure time
    double          exposureMax {0.0};      // camera's maximum exposure time

    bool            controlExposure {false}; // flag if automatic exposure shall be done by this SW

    guint           pixelFormatsCnt;


    int             num_buffers {50};       // number of payload transmission buffers

    ArvPixelFormat  pixelFormat;            // pixel format

    int             xoffset {0};            // current frame region x offset
    int             yoffset {0};            // current frame region y offset
    int             _width {0};             // current frame width of frame
    int             _height {0};            // current frame height of image

    double          fps {0.0};              // current value of fps
    double          exposure {0.0};         // current value of exposure time
    double          gain {0.0};             // current value of gain

    unsigned        frameID {0};            // current frame id
    unsigned        prevFrameID {0};

    struct FeatureInfo {
        const char* featureName;
        const char* enabledName;
    };

    std::map<cameraFeature_id_t, FeatureInfo> yarp_arv_int_feature_map {
        {YARP_FEATURE_BRIGHTNESS, {"Brightness", "BrightnessEnabled"} },
        {YARP_FEATURE_SHUTTER, {"Shutter", "ShutterEnabled"}},
        {YARP_FEATURE_IRIS, {"Iris", "IrisEnabled"}},
        {YARP_FEATURE_FOCUS,  {"Focus", "FocusEnabled"}},
        {YARP_FEATURE_TEMPERATURE, {"Temperature", "TemperatureEnabled"}},
        {YARP_FEATURE_TRIGGER, {"Trigger", "TriggerEnabled"}},
        {YARP_FEATURE_TRIGGER_DELAY, {"TriggerDelay", "TriggerDelayEnabled"}},
        {YARP_FEATURE_WHITE_SHADING, {"WhiteShading", "WhiteShadingEnabled"}},
        {YARP_FEATURE_ZOOM, {"Zoom", "ZoomEnabled"}},
        {YARP_FEATURE_PAN, {"Pan", "PanEnabled"}},
        {YARP_FEATURE_TILT, {"Tilt", "TiltEnabled"}},
        {YARP_FEATURE_OPTICAL_FILTER, {"OpticalFilter", "OpticalFilterEnabled"}},
        {YARP_FEATURE_CAPTURE_SIZE, {"CaptureSize", "CaptureSizeEnabled"}},
        {YARP_FEATURE_CAPTURE_QUALITY, {"CaptureQuality", "CaptureQualityEnabled"}},
        {YARP_FEATURE_MIRROR, {"Mirror", "MirrorEnabled"}}
    };
    
    std::map<cameraFeature_id_t, FeatureInfo> yarp_arv_float_feat_map {
        {YARP_FEATURE_EXPOSURE, {"ExposureTime", "ExposureEnabled"}},
        {YARP_FEATURE_GAIN, {"Gain", "GainEnabled"}},
        {YARP_FEATURE_FRAME_RATE, {"FPS", "FPSEnabled"}},
        {YARP_FEATURE_SHARPNESS, {"Sharpness", "SharpnessEnabled"}},
        {YARP_FEATURE_WHITE_BALANCE, {"WhiteBalance", "WhiteBalanceEnabled"}},
        {YARP_FEATURE_HUE, {"Hue", "HueEnabled"}},
        {YARP_FEATURE_SATURATION, {"Saturation", "SaturationEnabled"}},
        {YARP_FEATURE_GAMMA, {"Gamma", "GammaEnabled"}}
    };

    std::map<cameraFeature_id_t, const char *> feature_names = {
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
        {YARP_FEATURE_MIRROR, "Mirror"},
        {YARP_FEATURE_FRAME_RATE, "FPS"},
    };
};

} // namespace roboticslab

#endif // __ARAVIS_GIGE_HPP__

/*
[DEBUG] Requested to set feature 8 (/home/alvaro/repos/yarp-devices/libraries/YarpPlugins/AravisGigE/IFrameGrabberControlsImpl.cpp:54, virtual bool roboticslab::AravisGigE::setFeature(int, double))
[DEBUG] Requested to set on/off mode for feature 8 (/home/alvaro/repos/yarp-devices/libraries/YarpPlugins/AravisGigE/IFrameGrabberControlsImpl.cpp:176, virtual bool roboticslab::AravisGigE::setActive(int, bool))
[DEBUG] Checking feature availability:  8 (/home/alvaro/repos/yarp-devices/libraries/YarpPlugins/AravisGigE/IFrameGrabberControlsImpl.cpp:25, virtual bool roboticslab::AravisGigE::hasFeature(int, bool*))
[INFO] Feature  GainEnabled  set to  ON (/home/alvaro/repos/yarp-devices/libraries/YarpPlugins/AravisGigE/IFrameGrabberControlsImpl.cpp:201, virtual bool roboticslab::AravisGigE::setActive(int, bool))

*/