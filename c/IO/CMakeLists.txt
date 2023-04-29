cmake_minimum_required(VERSION 3.12)

include(pico_sdk_import.cmake)

project(pico-projects)

pico_sdk_init()

add_executable(IO
    src.c
)

target_link_libraries(IO pico_stdlib)

pico_enable_stdio_usb(IO 1)
pico_enable_stdio_uart(IO 0)

pico_add_extra_outputs(IO)
