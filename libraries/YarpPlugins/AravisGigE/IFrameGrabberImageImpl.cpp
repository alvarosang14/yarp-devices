#include "AravisGigE.hpp"
#include <yarp/os/LogStream.h>
#include <opencv2/imgproc.hpp>
#include <yarp/cv/Cv.h>
#include "LogComponent.hpp"

using namespace roboticslab;

bool AravisGigE::getImage(yarp::sig::ImageOf<yarp::sig::PixelRgb> &image) {
    framebuffer = nullptr;

    if (stream == nullptr) {
        yCError(ARV) << "Stream was not initialized";
        return false;
    }

    ArvBuffer *arvBuffer = nullptr;
    int max_tries = 10;
    int tries = 0;
    int success = false;
    while (!success && tries < max_tries) {
        arvBuffer = arv_stream_timeout_pop_buffer(stream, 200000);
        if (arvBuffer != nullptr && arv_buffer_get_status(arvBuffer) != ARV_BUFFER_STATUS_SUCCESS) {
            arv_stream_push_buffer(stream, arvBuffer);
        } else {
            success = true;
        }
    }

    if (arvBuffer != nullptr && success) {
        size_t buffer_size;
        framebuffer = (void *)arv_buffer_get_data(arvBuffer, &buffer_size);
        arv_buffer_get_image_region(arvBuffer, &xoffset, &yoffset, &_width, &_height);
        frameID = arv_buffer_get_frame_id(arvBuffer);
        arv_stream_push_buffer(stream, arvBuffer);
    } else {
        yCError(ARV) << "Timeout! Could not grab frame...";
        return false;
    }

    //-- Retrieve frame (convert and send as yarp image)
    //--------------------------------------------------------------------------------
    if (framebuffer==nullptr) {
        yCError(ARV) << "Framebuffer is empty";
        return false;
    }

    //-- Write data
    image.zero();
    image.resize(_width, _height);
    const unsigned char *bayerData = static_cast<const unsigned char *>(framebuffer);

    auto *rgbData = reinterpret_cast<yarp::sig::PixelRgb *>(image.getRawImage());

    /*
    if (pixelFormat == ARV_PIXEL_FORMAT_BAYER_RG_8 || pixelFormat == ARV_PIXEL_FORMAT_MONO_8)
    
      */
    if (pixelFormat == ARV_PIXEL_FORMAT_BAYER_RG_8) {
        cv::Mat bayerImg(_height, _width, CV_8UC1, (void *)framebuffer);
        cv::Mat rgbImg;
        cv::cvtColor(bayerImg, rgbImg, cv::COLOR_BayerRG2RGB);

        std::memcpy(image.getRawImage(), rgbImg.data, _width * _height * 3);
    } else if (pixelFormat == ARV_PIXEL_FORMAT_RGB_8_PACKED) {
        std::memcpy(rgbData, framebuffer, _width * _height * 3);
    } else {
        yCError(ARV) << "Unsupported pixel format";
        return false;
    }

    return true;
}