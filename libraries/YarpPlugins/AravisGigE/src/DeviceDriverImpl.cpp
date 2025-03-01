#include <string>
#include <unordered_set>
#include <yarp/os/LogStream.h>

#include "AravisGigE.hpp"
#include "LogComponent.hpp"

using namespace roboticslab;

//AravisQtWindow *qtWindow = nullptr;

bool AravisGigE::open(yarp::os::Searchable &config)
{
    //-- Configuration of Aravis GigE Camera device
    if (config.check("fake", "enable fake Aravis camera"))
    {
        yCInfo(ARV) << "Enabling fake Aravis camera";
        arv_enable_interface("Fake"); //-- Enables fake Aravis cameras (useful for debug / testing)
    }

    //-- Open Aravis device(s)
    //-------------------------------------------------------------------------------
    int index = config.check("index", yarp::os::Value(0), "camera index").asInt32();

    arv_update_device_list();

    if (index < 0 || index >= (int)arv_get_n_devices())
    {
        yCError(ARV) << "Invalid device index, should be 0 <" << index << "<" << arv_get_n_devices();
        return false;
    }

    const auto * deviceName = arv_get_device_id(index);

    //-- Create Aravis camera
    camera = arv_camera_new(deviceName, nullptr);

    if (camera != nullptr)
    {
        yCInfo(ARV) << "Created Aravis camera with index" << index << "and name" << deviceName;
    }
    else
    {
        yCError(ARV) << "Could not create Aravis camera with index" << index << "and name" << deviceName;
        return false;
    }

    //-- Once we have a camera, we obtain the camera properties limits and initial values
    std::unordered_set<std::string> availablePixelFormats;

    if (config.check("introspection", "print available pixel formats on device init"))
    {
        //-- List all  available formats
        guint n_pixel_formats;
        auto ** availableFormatsStrings = arv_camera_dup_available_pixel_formats_as_strings(camera, &n_pixel_formats, nullptr);
        auto ** availableFormatsNames = arv_camera_dup_available_pixel_formats_as_display_names(camera, &n_pixel_formats, nullptr);

        yCInfo(ARV) << "Available pixel formats:";

        for (int i = 0; i < n_pixel_formats; i++)
        {
            yCInfo(ARV, "- %s (setting: %s)", availableFormatsNames[i], availableFormatsStrings[i]);
            availablePixelFormats.emplace(availableFormatsStrings[i]);
        }
        
        // formats in availablePixelFormats
        yCInfo(ARV) << "Stored pixel formats in availablePixelFormats:";
        for (const auto& format : availablePixelFormats) {
            yCInfo(ARV) << format;
        }

        g_free(availableFormatsStrings);
        g_free(availableFormatsNames);
    }

    // ===================== Pruebas sobre pixel format ======================
    if (config.check("pixelFormat", "pixel format"))
    {   
        if (!config.check("introspection")) {
            yCError(ARV) << "Flag introspection required!";
            return false;
        }
    
        //-- Detener adquisición (para probar si se evitan errores)
        yCInfo(ARV) << "Stopping acquisition before changing pixel format...";
        arv_camera_stop_acquisition(camera, nullptr);
    
        //-- Limpiar de buffers
        if (stream) {
            g_object_unref(stream);
            stream = nullptr;
        }
    
        auto requestedPixelFormatString = config.find("pixelFormat").asString();
        
        yCInfo(ARV) << "Requested pixel format: " << requestedPixelFormatString;
    
        if (availablePixelFormats.find(requestedPixelFormatString) == availablePixelFormats.end())
        {
            yCError(ARV) << "Requested pixel format " << requestedPixelFormatString << " is not available";
            return false;
        }
    
        //-- Nuevo formato
        yCInfo(ARV) << "Setting pixel format to: " << requestedPixelFormatString;
        arv_camera_set_pixel_format_from_string(camera, requestedPixelFormatString.c_str(), nullptr);
    
        //-- Verificar si cambia (no cambia)
        pixelFormat = arv_camera_get_pixel_format(camera, nullptr);
        const char *appliedPixelFormatString = arv_camera_get_pixel_format_as_string(camera, nullptr);
    
        if (appliedPixelFormatString == nullptr || requestedPixelFormatString != appliedPixelFormatString) {
            yCError(ARV) << "Pixel format change failed! Expected: " << requestedPixelFormatString
                         << ", but got: " << (appliedPixelFormatString ? appliedPixelFormatString : "NULL");
            return false;
        }
    
        //-- Pequeña espera para ver si ayuda
        yarp::os::Time::delay(0.1);
    
        //-- Crear un nuevo stream 
        yCInfo(ARV) << "Creating new stream for the updated pixel format...";
        stream = arv_camera_create_stream(camera, nullptr, nullptr, nullptr);
    
        if (stream == nullptr)
        {
            yCError(ARV) << "Could not create Aravis stream";
            return false;
        }
    
        //-- Reconfigurar
        g_object_set(stream, "socket-buffer", ARV_GV_STREAM_SOCKET_BUFFER_AUTO, "socket-buffer-size", 0, nullptr);
        g_object_set(stream, "packet-resend", ARV_GV_STREAM_PACKET_RESEND_NEVER, nullptr);
        g_object_set(stream, "packet-timeout", (unsigned) 40000, "frame-retention", (unsigned) 200000, nullptr);
    
        guint payload = arv_camera_get_payload(camera, nullptr);
    
        //-- Añadir nuevos buffer
        yCInfo(ARV) << "Adding buffers for the new pixel format...";
        for (int i = 0; i < 10; i++) {
            arv_stream_push_buffer(stream, arv_buffer_new(payload, nullptr));
        }
    
        //-- Iniciar adquisición tras todo el cambio
        yCInfo(ARV) << "Restarting acquisition...";
        arv_camera_start_acquisition(camera, nullptr);
    }
    else
    {
        yCInfo(ARV) << "Using pixel format: " << arv_camera_get_pixel_format_as_string(camera, nullptr);
    }
    
    pixelFormat = arv_camera_get_pixel_format(camera, nullptr); 

    arv_camera_get_width_bounds(camera, &widthMin, &widthMax, nullptr);
    arv_camera_get_height_bounds(camera, &heightMin, &heightMax, nullptr);
    arv_camera_set_region(camera, 0, 0, widthMax, heightMax, nullptr);

    yCInfo(ARV, "Width range: min=%d max=%d", widthMin, widthMax);
    yCInfo(ARV, "Height range: min=%d max=%d", heightMin, heightMax);

    bool fpsAvailable = arv_camera_is_frame_rate_available(camera, nullptr);

    if (fpsAvailable)
    {
        arv_camera_get_frame_rate_bounds(camera, &fpsMin, &fpsMax, nullptr);
        yCInfo(ARV, "FPS range: min=%f max=%f", fpsMin, fpsMax);

        fps = arv_camera_get_frame_rate(camera, nullptr);
        yCInfo(ARV) << "Current FPS value:" << fps;
    }
    else
    {
        yCWarning(ARV) << "FPS property not available";
    }

    bool gainAvailable = arv_camera_is_gain_available(camera, nullptr);

    if (gainAvailable)
    {
        arv_camera_get_gain_bounds(camera, &gainMin, &gainMax, nullptr);
        yCInfo(ARV, "Gain range: min=%f max=%f", gainMin, gainMax);

        gain = arv_camera_get_gain(camera, nullptr);
        yCInfo(ARV) << "Current gain value:" << gain;
    }
    else
    {
        yCWarning(ARV) << "Gain property not available";
    }

    bool exposureAvailable = arv_camera_is_exposure_time_available(camera, nullptr);

    if (exposureAvailable)
    {
        arv_camera_get_exposure_time_bounds(camera, &exposureMin, &exposureMax, nullptr);
        yCInfo(ARV, "Exposure range: min=%f max=%f", exposureMin, exposureMax);

        exposure = arv_camera_get_exposure_time(camera, nullptr);
        yCInfo(ARV) << "Current exposure value:" << exposure;
    }
    else
    {
        yCWarning(ARV) << "Gain property not available";
    }

    //-- Lens controls availability
    yCInfo(ARV) << "Checking Lens Controls availability";

    if (gint64 zoomMin, zoomMax; arv_device_get_feature(arv_camera_get_device(camera), "Zoom") != nullptr)
    {
        arv_device_get_integer_feature_bounds(arv_camera_get_device(camera), "Zoom", &zoomMin, &zoomMax, nullptr);
        yCInfo(ARV, "Zoom range: min=%ld max=%ld", zoomMin, zoomMax);
    }
    else
    {
        yCWarning(ARV) << "Zoom property not available";
    }

    if (gint64 focusMin, focusMax; arv_device_get_feature(arv_camera_get_device(camera), "Focus") != nullptr)
    {
        arv_device_get_integer_feature_bounds(arv_camera_get_device(camera), "Focus", &focusMin, &focusMax, nullptr);
        yCInfo(ARV, "Focus range: min=%ld max=%ld", focusMin, focusMax);
    }
    else
    {
        yCWarning(ARV) << "Focus property not available";
    }

    //-- Start capturing images
    //-------------------------------------------------------------------------------

    //-- Initialization of buffer(s)
    if (stream)
    {
        g_object_unref(stream);
        stream = nullptr;
    }

    stream = arv_camera_create_stream(camera, nullptr, nullptr, nullptr);

    if (stream == nullptr)
    {
        yCError(ARV) << "Could not create Aravis stream";
        return false;
    }

    g_object_set(stream, "socket-buffer", ARV_GV_STREAM_SOCKET_BUFFER_AUTO, "socket-buffer-size", 0, nullptr);
    g_object_set(stream, "packet-resend", ARV_GV_STREAM_PACKET_RESEND_NEVER, nullptr);
    g_object_set(stream, "packet-timeout", (unsigned) 40000, "frame-retention", (unsigned) 200000, nullptr);

    payload = arv_camera_get_payload(camera, nullptr);

    for (int i = 0; i < num_buffers; i++)
    {
        arv_stream_push_buffer(stream, arv_buffer_new(payload, nullptr));
    }

    //-- Start continuous acquisition
    arv_camera_set_acquisition_mode(camera, ARV_ACQUISITION_MODE_CONTINUOUS, nullptr);
    arv_device_set_string_feature_value(arv_camera_get_device(camera), "TriggerMode" , "Off", nullptr);
    arv_camera_start_acquisition(camera, nullptr);

    /*
    if (!qtWindow) {
        qtWindow = new AravisQtWindow();
        qtWindow->start();  // Inicia el hilo de la ventana Qt
    }*/

    yCInfo(ARV) << "Aravis Camera acquisition started!";
    return true;
}

bool AravisGigE::close()
{
    if (camera == nullptr)
    {
        yCError(ARV) << "Camera was not started!";
        return false;
    }

    arv_camera_stop_acquisition(camera, nullptr);
    yCInfo(ARV) << "Aravis Camera acquisition stopped!";

    //-- Cleanup
    if (stream)
    {
        g_object_unref(stream);
        stream = nullptr;
    }

    g_object_unref(camera);
    camera = nullptr;

    return true;
}
