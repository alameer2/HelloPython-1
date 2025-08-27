# Overview

This repository contains noVNC, an HTML5 VNC client that provides remote desktop access through web browsers. noVNC consists of both a JavaScript library for VNC protocol implementation and a complete web application with user interface. The project enables users to connect to VNC servers directly from modern web browsers without requiring plugins or additional software installations.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Frontend Architecture
The application uses a modular ES6 JavaScript architecture with the following key components:

- **RFB Core Library**: The main VNC protocol implementation (`core/rfb.js`) that handles WebSocket connections, authentication, and protocol messaging
- **Display System**: Canvas-based rendering engine (`core/display.js`) for efficient 2D graphics with viewport management and backbuffer optimization
- **Input Handling**: Comprehensive input system including keyboard (`core/input/keyboard.js`), gesture handler for touch devices, and mouse event processing
- **UI Framework**: Complete user interface (`app/ui.js`) with control panels, settings management, and responsive design
- **Encoding Support**: Multiple VNC encoding implementations (Raw, CopyRect, RRE, Hextile, Tight, ZRLE, JPEG, H264) for optimized data transmission

## Communication Protocol
- **WebSocket Transport**: Uses WebSocket connections with custom buffering wrapper (`core/websock.js`) for reliable data transmission
- **VNC Protocol**: Full RFB protocol implementation supporting various authentication methods including VNC, RSA-AES, and credential-based authentication
- **Data Compression**: Integrated zlib deflation/inflation support for bandwidth optimization

## Security Architecture
- **Authentication Systems**: Multiple authentication mechanisms including password-based, RSA-AES encryption, and credential workflows
- **Encryption Support**: Built-in cryptographic capabilities using Web Crypto API for secure connections
- **Input Validation**: Comprehensive input sanitization and protocol validation

## Internationalization
- **Multi-language Support**: Complete localization system supporting 16 languages with dynamic loading
- **Translation Management**: JSON-based translation files with fallback mechanisms

## Development Infrastructure
- **Testing Framework**: Comprehensive test suite using Karma, Mocha, and Chai with browser automation
- **Build System**: Node.js-based build pipeline with Babel transpilation for legacy browser support
- **Code Quality**: ESLint integration for code standards and quality assurance

# External Dependencies

## Core Libraries
- **Pako**: JavaScript implementation of zlib for data compression/decompression
- **Babel**: JavaScript transpiler for ES6+ to ES5 conversion supporting older browsers

## Development Dependencies
- **Testing**: Karma test runner, Mocha testing framework, Chai assertion library, Sinon for mocking
- **Build Tools**: Node.js, Browserify for bundling, Commander for CLI tools
- **Quality Assurance**: ESLint for code linting, JSDOM for server-side DOM testing

## Browser APIs
- **WebSocket**: For network communication with VNC servers
- **Canvas 2D**: For graphics rendering and display management
- **Web Crypto API**: For encryption and security features
- **WebCodecs**: For H.264 video decoding (when available)

## Optional Integrations
The architecture supports integration with various VNC servers including QEMU, TigerVNC, LibVNCServer, and cloud platforms like OpenStack and OpenNebula.