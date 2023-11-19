# LokiMusic

**Warning:** This is a learning project only, I am not responsible for any damage caused by this project, use this project at your own risk.

## Description
**LokiMusic** is a simple HTTP server made using *Pytube*. This server can download audio from any YouTube video.This web server can be configured using configuration file. Server has a very nice **custom** logging system with color.

## Requirements
- **pytube** is used to extract audio and metadata from video
- **colorama** is used to highlight error/warn/log messages

### File Structure
- **data/index.html** is where you store your website
- **data/cache.json** is used to store metadata related to audio that are already downloaded
- **configuration.ini** is where all configuration options are stored

### Issues
- **The server uses *latin-1* as its encoder and decoder which means, it removes any unsupported characters from file name**
- **The custom logging system is very simple compare to python inbuilt logging module**
- **No type hinting in configuration file**
- **No type checking in configuration parser**

### What I Have Learned
- **HTTP Status Codes**
- **HTTP Structure**
- **File Formats**
- **Advance String Manipulation**
- **separation of code**
