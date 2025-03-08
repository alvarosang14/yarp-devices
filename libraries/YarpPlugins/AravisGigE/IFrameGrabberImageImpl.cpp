#include "AravisGigE.hpp"
#include <yarp/os/LogStream.h>
#include <opencv2/imgproc.hpp>
#include <yarp/cv/Cv.h>
#include "LogComponent.hpp"

using namespace roboticslab;

bool AravisGigE::getImage(yarp::sig::ImageOf<yarp::sig::PixelRgb> &image) {
    framebuffer = nullptr;
    GError *error = nullptr;

    if (stream == nullptr) {
        yCError(ARV) << "Stream was not initialized";
        return false;
    }

    yCInfo(ARV) << "Starting acquisition...";
    arv_camera_start_acquisition(camera, &error);

    if (error) {
        yCError(ARV) << "Error starting acquisition: " << error->message;
        g_error_free(error);
        return false;
    }

    ArvPixelFormat currentPixelFormat = arv_camera_get_pixel_format(camera, &error);
    if (error) {
        yCError(ARV) << "Error getting pixel format: " << error->message;
        g_error_free(error);
        return false;
    }

    yCInfo(ARV) << "Current pixel format: " << currentPixelFormat;

    if (currentPixelFormat != pixelFormat) {
        yCWarning(ARV) << "Pixel format mismatch! Setting to requested format...";
        arv_camera_set_pixel_format(camera, pixelFormat, &error);

        if (error) {
            yCError(ARV) << "Error setting pixel format: " << error->message;
            g_error_free(error);
            return false;
        }
    }

    gint n_buffers_assigned, n_buffers_pushed;
    arv_stream_get_n_buffers(stream, &n_buffers_assigned, &n_buffers_pushed);

    yCInfo(ARV) << "Buffers in stream - Assigned: " << n_buffers_assigned << ", Pushed: " << n_buffers_pushed;

    if (n_buffers_pushed == 0) {
        yCWarning(ARV) << "No buffers in stream, adding buffer...";
        // ================ Esto nunca funciona ===================
        arv_stream_push_buffer(stream, arv_buffer_new_allocate(_width * _height * 3));
    }

    arv_stream_get_n_buffers(stream, &n_buffers_assigned, &n_buffers_pushed);
    if (n_buffers_pushed == 0) {
        yCError(ARV) << "No buffers were added to the stream!";
    } else {
        yCInfo(ARV) << "Buffers successfully added to the stream.";
    }
    
    ArvBuffer *arvBuffer = nullptr;
    int max_tries = 10;
    int tries = 0;
    bool success = false;

    while (!success && tries < max_tries) {
        yCInfo(ARV) << "Attempting to retrieve frame (attempt " << tries + 1 << " of " << max_tries << ")...";
        // ====================== Tocar tiempo por si acaso ==========================
        arvBuffer = arv_stream_timeout_pop_buffer(stream, 500);

        if (arvBuffer != nullptr) {
            ArvBufferStatus status = arv_buffer_get_status(arvBuffer);
            if (status == ARV_BUFFER_STATUS_SUCCESS) {
                success = true;
            } else {
                yCError(ARV) << "Buffer has an error! Status: " << status;
                arv_stream_push_buffer(stream, arvBuffer);
            }
        }
        tries++;
    }

    if (arvBuffer == nullptr || !success) {
        yCError(ARV) << "Timeout! Could not grab frame...";
        return false;
    }

    size_t buffer_size;
    framebuffer = (void *)arv_buffer_get_data(arvBuffer, &buffer_size);
    arv_buffer_get_image_region(arvBuffer, &xoffset, &yoffset, &_width, &_height);
    frameID = arv_buffer_get_frame_id(arvBuffer);

    if (framebuffer == nullptr) {
        yCError(ARV) << "Framebuffer is empty";
        return false;
    }

    arv_stream_push_buffer(stream, arvBuffer);

    // P=============== Procesamiento de imagen =============================
    image.zero();
    image.resize(_width, _height);
    auto *rgbData = reinterpret_cast<yarp::sig::PixelRgb *>(image.getRawImage());

    if (pixelFormat == ARV_PIXEL_FORMAT_BAYER_RG_8) {
        yCInfo(ARV) << "Processing Bayer RG8 image...";
        cv::Mat bayerImg(_height, _width, CV_8UC1, (void *)framebuffer);
        cv::Mat rgbImg;
        cv::cvtColor(bayerImg, rgbImg, cv::COLOR_BayerRG2BGR);

        std::memcpy(image.getRawImage(), rgbImg.data, _width * _height * 3);
    } else if (pixelFormat == ARV_PIXEL_FORMAT_RGB_8_PACKED) {
        yCInfo(ARV) << "Processing RGB8 image...";
        std::memcpy(rgbData, framebuffer, _width * _height * 3);
    } else {
        yCError(ARV) << "Unsupported pixel format";
        return false;
    }

    return true;
}
