#include "AravisGigE.hpp"
#include <yarp/os/LogStream.h>
//#include <opencv2/imgproc.hpp>
//#include <yarp/cv/Cv.h>
#include "LogComponent.hpp"

using namespace roboticslab;

bool AravisGigE::getImage(yarp::sig::ImageOf<yarp::sig::PixelRgb> &image) {
    if (!stream)
    {
        yCError(ARV) << "Stream was not initialized";
        return false;
    }

    ArvBuffer *arvBuffer = nullptr;
    const int maxTries = 10;

    for (int i = 0; i < maxTries; i++)
    {
        arvBuffer = arv_stream_timeout_pop_buffer(stream, 200000);
        if (arvBuffer && arv_buffer_get_status(arvBuffer) == ARV_BUFFER_STATUS_SUCCESS)
            break;
        if (arvBuffer)
            arv_stream_push_buffer(stream, arvBuffer);
    }

    if (!arvBuffer)
    {
        yCError(ARV) << "Timeout! Could not grab frame...";
        return false;
    }

    size_t bufferSize = 0;
    const void *framebuffer = arv_buffer_get_data(arvBuffer, &bufferSize);
    arv_buffer_get_image_region(arvBuffer, &xoffset, &yoffset, &_width, &_height);
    frameID = arv_buffer_get_frame_id(arvBuffer);
    arv_stream_push_buffer(stream, arvBuffer);

    if (!framebuffer)
    {
        yCError(ARV) << "Framebuffer is empty";
        return false;
    }

    image.resize(_width, _height);
    const unsigned char *bayerData = static_cast<const unsigned char *>(framebuffer);

    auto *rgbData = reinterpret_cast<yarp::sig::PixelRgb *>(image.getRawImage());

    if (pixelFormat == ARV_PIXEL_FORMAT_BAYER_RG_8 || pixelFormat == ARV_PIXEL_FORMAT_MONO_8)
    {
        for (int y = 1; y < _height - 1; y++)
        {
            for (int x = 1; x < _width - 1; x++)
            {
                int i = y * _width + x;
                unsigned char r, g, b;

                if ((y & 1) == (x & 1))
                {
                    r = (y & 1) ? 0 : bayerData[i];
                    b = (y & 1) ? bayerData[i] : 0;
                    g = (bayerData[i - 1] + bayerData[i + 1] + bayerData[i - _width] + bayerData[i + _width]) / 4;
                }
                else
                {
                    g = bayerData[i];
                    r = (bayerData[i - _width] + bayerData[i + _width]) / 2;
                    b = (bayerData[i - 1] + bayerData[i + 1]) / 2;
                }

                rgbData[i] = {r, g, b};
            }
        }
    }
    else if (pixelFormat == ARV_PIXEL_FORMAT_RGB_8_PACKED)
    {
        std::memcpy(rgbData, framebuffer, _width * _height * 3);
    }
    else
    {
        yCError(ARV) << "Unsupported pixel format";
        return false;
    }

    return true;
}