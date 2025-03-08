#include "AravisGigE.hpp"
#include <yarp/os/LogStream.h>
#include <opencv2/imgproc.hpp>
#include <yarp/cv/Cv.h>
#include "LogComponent.hpp"

using namespace roboticslab;

bool AravisGigE::getImage(yarp::sig::ImageOf<yarp::sig::PixelRgb> &image)
{
    if (!stream)
    {
        yCError(ARV) << "Stream was not initialized";
        return false;
    }

    ArvBuffer *arvBuffer = nullptr;
    int max_tries = 10;
    int tries = 0;
    bool success = false;

    while (!success && tries < max_tries)
    {
        arvBuffer = arv_stream_timeout_pop_buffer(stream, 200000);
        if (arvBuffer && arv_buffer_get_status(arvBuffer) == ARV_BUFFER_STATUS_SUCCESS)
        {
            success = true;
        }
        else if (arvBuffer)
        {
            arv_stream_push_buffer(stream, arvBuffer);
        }
        tries++;
    }

    if (!success || !arvBuffer)
    {
        yCError(ARV) << "Timeout! Could not grab frame...";
        return false;
    }

    size_t buffer_size;
    framebuffer = (void *)arv_buffer_get_data(arvBuffer, &buffer_size);
    arv_buffer_get_image_region(arvBuffer, &xoffset, &yoffset, &_width, &_height);
    frameID = arv_buffer_get_frame_id(arvBuffer);
    arv_stream_push_buffer(stream, arvBuffer);

    if (!framebuffer)
    {
        yCError(ARV) << "Framebuffer is empty";
        return false;
    }

    image.resize(_width, _height);

    if (pixelFormat == ARV_PIXEL_FORMAT_BAYER_RG_8 ||
        pixelFormat == ARV_PIXEL_FORMAT_BAYER_RG_12P ||
        pixelFormat == ARV_PIXEL_FORMAT_BAYER_RG_16)
    {
        yCInfo(ARV) << "Processing Bayer image...";
        cv::Mat bayerImg(_height, _width, CV_8UC1, framebuffer);
        cv::Mat rgbImg;
        cv::cvtColor(bayerImg, rgbImg, cv::COLOR_BayerRG2BGR);
        std::memcpy(image.getRawImage(), rgbImg.data, _width * _height * 3);
    }
    else if (pixelFormat == ARV_PIXEL_FORMAT_YUV_422_PACKED ||
             pixelFormat == ARV_PIXEL_FORMAT_YUV_411_PACKED)
    {
        yCInfo(ARV) << "Processing YUV image...";
        cv::Mat ycbcrImg(_height, _width, CV_8UC2, framebuffer);
        cv::Mat rgbImg;
        cv::cvtColor(ycbcrImg, rgbImg, cv::COLOR_YUV2BGR_YUYV);
        std::memcpy(image.getRawImage(), rgbImg.data, _width * _height * 3);
    }
    else if (pixelFormat == ARV_PIXEL_FORMAT_RGB_8_PLANAR)
    {
        yCInfo(ARV) << "Processing RGB8 image...";
        std::memcpy(image.getRawImage(), framebuffer, _width * _height * 3);
    }
    else if (pixelFormat == ARV_PIXEL_FORMAT_MONO_8 ||
             pixelFormat == ARV_PIXEL_FORMAT_MONO_12 ||
             pixelFormat == ARV_PIXEL_FORMAT_MONO_16)
    {
        yCInfo(ARV) << "Processing Mono image...";
        cv::Mat monoImg(_height, _width, CV_8UC1, framebuffer);
        cv::Mat rgbImg;
        cv::cvtColor(monoImg, rgbImg, cv::COLOR_GRAY2BGR);
        std::memcpy(image.getRawImage(), rgbImg.data, _width * _height * 3);
    }
    else
    {
        yCError(ARV) << "Unsupported pixel format";
        return false;
    }

    return true;
}
