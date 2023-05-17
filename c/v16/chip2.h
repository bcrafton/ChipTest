
#ifndef CHIP2_H
#define CHIP2_H

#include <stdio.h>
#include "pico/stdlib.h"
#include <utility>
#include <map>
#include <string>
#include <vector>
#include <algorithm>

#include "util.h"
#include "defines.h"

using namespace std;

class chip2_t {
  public:

  chip2_t() {
    gpio_init(SPI_CLK);   gpio_set_dir(SPI_CLK,   GPIO_OUT);
    gpio_init(SPI_RST);   gpio_set_dir(SPI_RST,   GPIO_OUT);

    gpio_init(SPI_CS);    gpio_set_dir(SPI_CS,    GPIO_OUT);
    gpio_init(SPI_SCLK);  gpio_set_dir(SPI_SCLK,  GPIO_OUT);
    gpio_init(SPI_MOSI);  gpio_set_dir(SPI_MOSI,  GPIO_OUT);
    gpio_init(SPI_MISO);  gpio_set_dir(SPI_MISO,  GPIO_IN);

    gpio_init(SPI_START); gpio_set_dir(SPI_START, GPIO_OUT);

    this->reset();
  }
  ~chip2_t() { }
  
  void reset() {
    gpio_put(SPI_CLK,   0); sleep_us(1);
    gpio_put(SPI_RST,   1); sleep_us(1);
    gpio_put(SPI_CS,    1); sleep_us(1);
    gpio_put(SPI_SCLK,  0); sleep_us(1);
    gpio_put(SPI_MOSI,  0); sleep_us(1);
    gpio_put(SPI_START, 0); sleep_us(1);

    gpio_put(SPI_RST, 0); sleep_us(1);
    gpio_put(SPI_RST, 1); sleep_us(1);
  }

  void write(uint32_t mmap, uint32_t addr, uint32_t data) {
    vector<uint8_t> _wen{1};
    vector<uint8_t> _mmap = int_to_bits(mmap, 4);
    vector<uint8_t> _addr = int_to_bits(addr, 28);
    vector<uint8_t> _data = int_to_bits(data, 32);

    vector<uint8_t> scan = _data;
    scan.insert(scan.end(), _addr.begin(), _addr.end());
    scan.insert(scan.end(), _mmap.begin(), _mmap.end());
    scan.insert(scan.end(), _wen.begin(), _wen.end());

    gpio_put(SPI_CLK,  0); sleep_us(1);
    gpio_put(SPI_MOSI, 0); sleep_us(1);
    gpio_put(SPI_SCLK, 0); sleep_us(1);

    gpio_put(SPI_CS,   0); sleep_us(1);
    this->send(scan);
    gpio_put(SPI_CS,   1); sleep_us(1);

    gpio_put(SPI_CLK,  1); sleep_us(1);
    gpio_put(SPI_CLK,  0); sleep_us(1);
    gpio_put(SPI_CLK,  1); sleep_us(1);
    gpio_put(SPI_CLK,  0); sleep_us(1);

    gpio_put(SPI_SCLK, 1); sleep_us(1);
    gpio_put(SPI_SCLK, 0); sleep_us(1);    
  }

  uint32_t read(uint32_t mmap, uint32_t addr) {
    vector<uint8_t> _wen{0};
    vector<uint8_t> _mmap = int_to_bits(mmap, 4);
    vector<uint8_t> _addr = int_to_bits(addr, 28);
    vector<uint8_t> _data = int_to_bits(0, 32);

    vector<uint8_t> scan = _data;
    scan.insert(scan.end(), _addr.begin(), _addr.end());
    scan.insert(scan.end(), _mmap.begin(), _mmap.end());
    scan.insert(scan.end(), _wen.begin(), _wen.end());

    gpio_put(SPI_CLK,  0); sleep_us(1);
    gpio_put(SPI_MOSI, 0); sleep_us(1);
    gpio_put(SPI_SCLK, 0); sleep_us(1);

    gpio_put(SPI_CS,   0); sleep_us(1);
    this->send(scan);
    gpio_put(SPI_CS,   1); sleep_us(1);

    gpio_put(SPI_CLK,  1); sleep_us(1);
    gpio_put(SPI_CLK,  0); sleep_us(1);
    gpio_put(SPI_CLK,  1); sleep_us(1);
    gpio_put(SPI_CLK,  0); sleep_us(1);

    gpio_put(SPI_SCLK, 1); sleep_us(1);
    gpio_put(SPI_SCLK, 0); sleep_us(1);
    //////////////////////////////////////
    //fill(scan.begin(), scan.end(), 0);
    scan = vector<uint8_t>(65, 0);

    gpio_put(SPI_CLK,  0); sleep_us(1);
    gpio_put(SPI_MOSI, 0); sleep_us(1);
    gpio_put(SPI_SCLK, 0); sleep_us(1);

    gpio_put(SPI_CS,   0); sleep_us(1);
    vector<uint8_t> bits = this->send(scan);
    gpio_put(SPI_CS,   1); sleep_us(1);

    gpio_put(SPI_CLK,  1); sleep_us(1);
    gpio_put(SPI_CLK,  0); sleep_us(1);
    gpio_put(SPI_CLK,  1); sleep_us(1);
    gpio_put(SPI_CLK,  0); sleep_us(1);

    gpio_put(SPI_SCLK, 1); sleep_us(1);
    gpio_put(SPI_SCLK, 0); sleep_us(1);
    //////////////////////////////////////
    vector<uint8_t> dout = {bits.begin() + 0, bits.begin() + 32};
    uint32_t word = bits_to_int(dout);
    return word;
  }

  vector<uint8_t> send(vector<uint8_t> bits) {
    vector<uint8_t> out;
    for (int i=0; i<bits.size(); i++) {
      out.push_back( gpio_get(SPI_MISO) ); sleep_us(1);
      gpio_put(SPI_MOSI, bits[i]); sleep_us(1);
      gpio_put(SPI_SCLK, 1); sleep_us(1);
      gpio_put(SPI_SCLK, 0); sleep_us(1);
    }
    return out;
  }

  void run(uint32_t N) {
    gpio_put(SPI_START, 0); sleep_us(1);
    gpio_put(SPI_CLK,   0); sleep_us(1);

    gpio_put(SPI_START, 1); sleep_us(1);
    gpio_put(SPI_CLK,   1); sleep_us(1);
    gpio_put(SPI_CLK,   0); sleep_us(1);
    gpio_put(SPI_START, 0); sleep_us(1);

    for (int i=0; i<N; i++) {
      gpio_put(SPI_CLK,   1);
      gpio_put(SPI_CLK,   0);
    }
    //printf("done\n");
  }

  void run_us(uint32_t N) {
    gpio_put(SPI_START, 0); sleep_us(1);
    gpio_put(SPI_CLK,   0); sleep_us(1);

    gpio_put(SPI_START, 1); sleep_us(1);
    gpio_put(SPI_CLK,   1); sleep_us(1);
    gpio_put(SPI_CLK,   0); sleep_us(1);
    gpio_put(SPI_START, 0); sleep_us(1);

    for (int i=0; i<N; i++) {
      gpio_put(SPI_CLK,   1); sleep_us(1);
      gpio_put(SPI_CLK,   0); sleep_us(1);
    }
    printf("done\n");
  }

};

#endif
