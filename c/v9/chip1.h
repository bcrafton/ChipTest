
#ifndef CHIP1_H
#define CHIP1_H

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

class chip1_t {
  public:

  chip1_t() {
    this->reset();
    this->clear();
  }
  ~chip1_t() { }
  
  void reset() {
    gpio_put(CLK, 0); sleep_us(1);
    gpio_put(RST, 1); sleep_us(1);
    gpio_put(RST, 0); sleep_us(1);
    gpio_put(RST, 1); sleep_us(1);
  }
  
  void clear() {
    for (int sel=0; sel<4; sel++) {
      this->write_cam(0x5, 0, 0, 0, sel);
      this->write_cam(0x6, 0, 0, 0, sel);
      this->write_cam(0xb, 0, 0, 0, sel);
      this->write_cam(0x7, 0, 0, 0, sel);
      this->write_cam(0x9, 0, 0, 0, sel);
      this->write_cam(0xa, 0, 0, 0, sel);
    }
  }

  void write_32b(uint32_t mmap, uint32_t addr, uint32_t data) {
    vector<uint8_t> _wen{1};
    vector<uint8_t> _mmap = int_to_bits(mmap, 4);
    vector<uint8_t> _addr = int_to_bits(addr, 32);
    vector<uint8_t> _data = int_to_bits(data, 32);

    vector<uint8_t> scan = _wen;
    scan.insert(scan.end(), _mmap.begin(), _mmap.end());
    scan.insert(scan.end(), _addr.begin(), _addr.end());
    scan.insert(scan.end(), _data.begin(), _data.end());

    vector<uint8_t> _fill(377 - scan.size(), 0);
    scan.insert(scan.end(), _fill.begin(), _fill.end());

    this->write(scan);
  }

  void read_32b(uint32_t mmap, uint32_t addr) {
    vector<uint8_t> _wen{0};
    vector<uint8_t> _mmap = int_to_bits(mmap, 4);
    vector<uint8_t> _addr = int_to_bits(addr, 32);

    vector<uint8_t> scan = _wen;
    scan.insert(scan.end(), _mmap.begin(), _mmap.end());
    scan.insert(scan.end(), _addr.begin(), _addr.end());

    vector<uint8_t> _fill(377 - scan.size(), 0);
    scan.insert(scan.end(), _fill.begin(), _fill.end());

    vector<uint8_t> bits = this->read(scan);
    vector<uint8_t> dout = {bits.begin(), bits.begin() + 32};
    uint32_t word = bits_to_int(dout);
    printf("%x\n", word);
  }

  void write_reg(uint32_t reg, uint32_t addr, uint32_t val) {
    vector<uint8_t> _wen{1};
    vector<uint8_t> _mmap = int_to_bits(0xe, 4);
    vector<uint8_t> _reg  = int_to_bits(reg, 5);
    vector<uint8_t> _addr = int_to_bits(addr, 5);
    vector<uint8_t> _val  = int_to_bits(val, 32);

    vector<uint8_t> scan = _wen;
    scan.insert(scan.end(), _mmap.begin(), _mmap.end());
    scan.insert(scan.end(), _reg.begin(), _reg.end());
    scan.insert(scan.end(), _addr.begin(), _addr.end());
    scan.insert(scan.end(), _val.begin(), _val.end());

    vector<uint8_t> _fill(377 - scan.size(), 0);
    scan.insert(scan.end(), _fill.begin(), _fill.end());

    this->write(scan);
  }

  void read_reg(uint32_t reg, uint32_t addr) {
    vector<uint8_t> _wen{0};
    vector<uint8_t> _mmap = int_to_bits(0xe, 4);
    vector<uint8_t> _reg  = int_to_bits(reg, 5);
    vector<uint8_t> _addr = int_to_bits(addr, 5);

    vector<uint8_t> scan = _wen;
    scan.insert(scan.end(), _mmap.begin(), _mmap.end());
    scan.insert(scan.end(), _reg.begin(), _reg.end());
    scan.insert(scan.end(), _addr.begin(), _addr.end());

    vector<uint8_t> _fill(377 - scan.size(), 0);
    scan.insert(scan.end(), _fill.begin(), _fill.end());

    vector<uint8_t> bits = this->read(scan);
    vector<uint8_t> dout = {bits.begin(), bits.begin() + 32};
    uint32_t word = bits_to_int(dout);
    printf("%x\n", word);
  }

  void write_cam(uint32_t mmap, uint32_t addr, uint32_t data, uint32_t mux, uint32_t sel) {
    vector<uint8_t> _wen{1};
    vector<uint8_t> _mmap = int_to_bits(mmap, 4);
    vector<uint8_t> _WL(128, 0);
    vector<uint8_t> _WLB(128, 0);
    vector<uint8_t> _MUX(8, 0);
    vector<uint8_t> _DAC(6, 0);
    vector<uint8_t> _SEL = int_to_bits(sel, 2);
    vector<uint8_t> _DIN = int_to_bits(data, 32);
    vector<uint8_t> _DINB = int_to_bits(~data, 32);
    vector<uint8_t> _CIM(32, 0);
    vector<uint8_t> _RD{0};
    vector<uint8_t> _WR{1};
    vector<uint8_t> _MODE{1};
    vector<uint8_t> _CMP{1};

    _WL[addr] = 1;
    _WLB[addr] = 1;
    _MUX[mux] = 1;

    vector<uint8_t> scan = _wen;
    scan.insert(scan.end(), _mmap.begin(), _mmap.end());
    scan.insert(scan.end(), _WL.begin(), _WL.end());
    scan.insert(scan.end(), _WLB.begin(), _WLB.end());
    scan.insert(scan.end(), _MUX.begin(), _MUX.end());
    scan.insert(scan.end(), _DAC.begin(), _DAC.end());
    scan.insert(scan.end(), _SEL.begin(), _SEL.end());
    scan.insert(scan.end(), _DIN.begin(), _DIN.end());
    scan.insert(scan.end(), _DINB.begin(), _DINB.end());
    scan.insert(scan.end(), _CIM.begin(), _CIM.end());
    scan.insert(scan.end(), _RD.begin(), _RD.end());
    scan.insert(scan.end(), _WR.begin(), _WR.end());
    scan.insert(scan.end(), _MODE.begin(), _MODE.end());
    scan.insert(scan.end(), _CMP.begin(), _CMP.end());

    this->write(scan);
  }

  uint32_t read_cam(uint32_t mmap, uint32_t addr, uint32_t mux, uint32_t sel) {
    vector<uint8_t> _wen{0};
    vector<uint8_t> _mmap = int_to_bits(mmap, 4);
    vector<uint8_t> _WL(128, 0);
    vector<uint8_t> _WLB(128, 0);
    vector<uint8_t> _MUX(8, 0);
    vector<uint8_t> _DAC(6, 0);
    vector<uint8_t> _SEL = int_to_bits(sel, 2);
    vector<uint8_t> _DIN(32, 0);
    vector<uint8_t> _DINB(32, 0);
    vector<uint8_t> _CIM(32, 0);
    vector<uint8_t> _RD{1};
    vector<uint8_t> _WR{0};
    vector<uint8_t> _MODE{0};
    vector<uint8_t> _CMP{1};

    _WL[addr] = 1;
    _WLB[addr] = 1;
    _MUX[mux] = 1;

    vector<uint8_t> scan = _wen;
    scan.insert(scan.end(), _mmap.begin(), _mmap.end());
    scan.insert(scan.end(), _WL.begin(), _WL.end());
    scan.insert(scan.end(), _WLB.begin(), _WLB.end());
    scan.insert(scan.end(), _MUX.begin(), _MUX.end());
    scan.insert(scan.end(), _DAC.begin(), _DAC.end());
    scan.insert(scan.end(), _SEL.begin(), _SEL.end());
    scan.insert(scan.end(), _DIN.begin(), _DIN.end());
    scan.insert(scan.end(), _DINB.begin(), _DINB.end());
    scan.insert(scan.end(), _CIM.begin(), _CIM.end());
    scan.insert(scan.end(), _RD.begin(), _RD.end());
    scan.insert(scan.end(), _WR.begin(), _WR.end());
    scan.insert(scan.end(), _MODE.begin(), _MODE.end());
    scan.insert(scan.end(), _CMP.begin(), _CMP.end());

    vector<uint8_t> bits = this->read(scan);
    vector<uint8_t> dout;
    if (mmap == 0xa) dout = {bits.begin() + 8,  bits.begin() + 16};
    else             dout = {bits.begin() + 32, bits.begin() + 64};
    uint32_t word = bits_to_int(dout);
    return word;
  }

  uint32_t cam(uint32_t mmap, vector<uint8_t> WL, vector<uint8_t> WLB, uint32_t mux, uint32_t sel) {
    if (WL.size()  != 128) printf("WL not 128b");
    if (WLB.size() != 128) printf("WLB not 128b");
  
    vector<uint8_t> _wen{0};
    vector<uint8_t> _mmap = int_to_bits(mmap, 4);
    vector<uint8_t> _MUX(8, 0);
    vector<uint8_t> _DAC(6, 0);
    vector<uint8_t> _SEL = int_to_bits(sel, 2);
    vector<uint8_t> _DIN(32, 0);
    vector<uint8_t> _DINB(32, 0);
    vector<uint8_t> _CIM(32, 0);
    vector<uint8_t> _RD{1};
    vector<uint8_t> _WR{0};
    vector<uint8_t> _MODE{0};
    vector<uint8_t> _CMP{1};

    _MUX[mux] = 1;

    vector<uint8_t> scan = _wen;
    scan.insert(scan.end(), _mmap.begin(), _mmap.end());
    scan.insert(scan.end(), WL.begin(), WL.end());
    scan.insert(scan.end(), WLB.begin(), WLB.end());
    scan.insert(scan.end(), _MUX.begin(), _MUX.end());
    scan.insert(scan.end(), _DAC.begin(), _DAC.end());
    scan.insert(scan.end(), _SEL.begin(), _SEL.end());
    scan.insert(scan.end(), _DIN.begin(), _DIN.end());
    scan.insert(scan.end(), _DINB.begin(), _DINB.end());
    scan.insert(scan.end(), _CIM.begin(), _CIM.end());
    scan.insert(scan.end(), _RD.begin(), _RD.end());
    scan.insert(scan.end(), _WR.begin(), _WR.end());
    scan.insert(scan.end(), _MODE.begin(), _MODE.end());
    scan.insert(scan.end(), _CMP.begin(), _CMP.end());
    if (scan.size() != 377) printf("scan not 377b");

    vector<uint8_t> bits = this->read(scan);
    vector<uint8_t> dout1;
    vector<uint8_t> dout2;
    if (mmap == 0xa) {
      dout1 = {bits.begin() + 24, bits.begin() + 32};
      dout2 = {bits.begin() + 16, bits.begin() + 24};
    }
    else {
      dout1 = {bits.begin() + 96, bits.end()};
      dout2 = {bits.begin() + 64, bits.begin() + 96};
    }
    uint32_t word1 = bits_to_int(dout1);
    uint32_t word2 = bits_to_int(dout2);
    uint32_t word = word1 & word2;
    return word;
  }

  uint32_t cim(uint32_t mmap, vector<uint8_t> WL, vector<uint8_t> WLB, uint32_t mux, uint32_t sel) {
    if (WL.size()  != 128) printf("WL not 128b");
    if (WLB.size() != 128) printf("WLB not 128b");
  
    vector<uint8_t> _wen{0};
    vector<uint8_t> _mmap = int_to_bits(mmap, 4);
    vector<uint8_t> _MUX(8, 0);
    vector<uint8_t> _DAC(6, 0);
    vector<uint8_t> _SEL = int_to_bits(sel, 2);
    vector<uint8_t> _DIN(32, 0);
    vector<uint8_t> _DINB(32, 0);
    vector<uint8_t> _CIM(32, 1);
    vector<uint8_t> _RD{0};
    vector<uint8_t> _WR{0};
    vector<uint8_t> _MODE{0};
    vector<uint8_t> _CMP{1};

    _MUX[mux] = 1;

    vector<uint8_t> scan = _wen;
    scan.insert(scan.end(), _mmap.begin(), _mmap.end());
    scan.insert(scan.end(), WL.begin(), WL.end());
    scan.insert(scan.end(), WLB.begin(), WLB.end());
    scan.insert(scan.end(), _MUX.begin(), _MUX.end());
    scan.insert(scan.end(), _DAC.begin(), _DAC.end());
    scan.insert(scan.end(), _SEL.begin(), _SEL.end());
    scan.insert(scan.end(), _DIN.begin(), _DIN.end());
    scan.insert(scan.end(), _DINB.begin(), _DINB.end());
    scan.insert(scan.end(), _CIM.begin(), _CIM.end());
    scan.insert(scan.end(), _RD.begin(), _RD.end());
    scan.insert(scan.end(), _WR.begin(), _WR.end());
    scan.insert(scan.end(), _MODE.begin(), _MODE.end());
    scan.insert(scan.end(), _CMP.begin(), _CMP.end());
    if (scan.size() != 377) printf("scan not 377b");

    vector<uint8_t> bits = this->read(scan);
    vector<uint8_t> dout;
    if (mmap == 0xa) {
      dout = {bits.begin() + 0, bits.begin() + 8};
    }
    else {
      dout = {bits.begin() + 0, bits.begin() + 32};
    }
    uint32_t word = bits_to_int(dout);
    return word;
  }

  void flush(uint32_t mmap, uint32_t sel) {
    vector<uint8_t> _wen{0};
    vector<uint8_t> _mmap = int_to_bits(mmap, 4);
    vector<uint8_t> _WL(128, 0);
    vector<uint8_t> _WLB(128, 0);
    vector<uint8_t> _MUX(8, 0);
    vector<uint8_t> _DAC(6, 0);
    vector<uint8_t> _SEL = int_to_bits(sel, 4);
    vector<uint8_t> _DIN(32, 0);
    vector<uint8_t> _DINB(32, 0);
    vector<uint8_t> _CIM(32, 0);
    vector<uint8_t> _RD{1};
    vector<uint8_t> _WR{0};
    vector<uint8_t> _MODE{0};
    vector<uint8_t> _CMP{1};

    vector<uint8_t> scan = _wen;
    scan.insert(scan.end(), _mmap.begin(), _mmap.end());
    scan.insert(scan.end(), _WL.begin(), _WL.end());
    scan.insert(scan.end(), _WLB.begin(), _WLB.end());
    scan.insert(scan.end(), _MUX.begin(), _MUX.end());
    scan.insert(scan.end(), _DAC.begin(), _DAC.end());
    scan.insert(scan.end(), _SEL.begin(), _SEL.end());
    scan.insert(scan.end(), _DIN.begin(), _DIN.end());
    scan.insert(scan.end(), _DINB.begin(), _DINB.end());
    scan.insert(scan.end(), _CIM.begin(), _CIM.end());
    scan.insert(scan.end(), _RD.begin(), _RD.end());
    scan.insert(scan.end(), _WR.begin(), _WR.end());
    scan.insert(scan.end(), _MODE.begin(), _MODE.end());
    scan.insert(scan.end(), _CMP.begin(), _CMP.end());

    vector<uint8_t> bits = this->read(scan);
  }

  void write(vector<uint8_t> scan) {
    gpio_put(MCLK,  0); sleep_us(1);
    gpio_put(SCLK,  0); sleep_us(1);
    gpio_put(SIN,   0); sleep_us(1);
    gpio_put(CLK,   0); sleep_us(1);
    gpio_put(VLD,   0); sleep_us(1);
    gpio_put(CAP,   0); sleep_us(1);
    gpio_put(START, 0); sleep_us(1);

    for (int i=0; i<scan.size(); i++) {
      gpio_put(SIN, scan[i]); sleep_us(1);

      gpio_put(MCLK, 0); sleep_us(1);
      gpio_put(MCLK, 1); sleep_us(1);
      gpio_put(MCLK, 0); sleep_us(1);

      gpio_put(SCLK, 0); sleep_us(1);
      gpio_put(SCLK, 1); sleep_us(1);
      gpio_put(SCLK, 0); sleep_us(1);
    }

    gpio_put(VLD, 1); sleep_us(1);

    gpio_put(CLK, 1); sleep_us(1);
    gpio_put(CLK, 0); sleep_us(1);
    gpio_put(CLK, 1); sleep_us(1);
    gpio_put(CLK, 0); sleep_us(1);

    gpio_put(VLD, 0); sleep_us(1);

    gpio_put(CLK, 1); sleep_us(1);
    gpio_put(CLK, 0); sleep_us(1);
    gpio_put(CLK, 1); sleep_us(1);
    gpio_put(CLK, 0); sleep_us(1);
  }

  vector<uint8_t> read(vector<uint8_t> scan) {
    gpio_put(MCLK,  0); sleep_100ns();
    gpio_put(SCLK,  0); sleep_100ns();
    gpio_put(SIN,   0); sleep_100ns();
    gpio_put(CLK,   0); sleep_100ns();
    gpio_put(VLD,   0); sleep_100ns();
    gpio_put(CAP,   0); sleep_100ns();
    gpio_put(START, 0); sleep_100ns();
    gpio_put(CLK2,  1); sleep_100ns();

    for (int i=0; i<scan.size(); i++) {
      gpio_put(SIN, scan[i]); sleep_100ns();

      gpio_put(MCLK, 0); sleep_100ns();
      gpio_put(MCLK, 1); sleep_100ns();
      gpio_put(MCLK, 0); sleep_100ns();

      gpio_put(SCLK, 0); sleep_100ns();
      gpio_put(SCLK, 1); sleep_100ns();
      gpio_put(SCLK, 0); sleep_100ns();
    }

    gpio_put(VLD, 1); sleep_100ns();

    gpio_put(CLK, 1); sleep_100ns();
    gpio_put(CLK, 0); sleep_100ns();
    gpio_put(CLK, 1); sleep_100ns();
    sleep_us(8);
    gpio_put(CLK2, 0); sleep_100ns();
    gpio_put(CLK2, 1); sleep_100ns();
    gpio_put(CLK, 0); sleep_100ns();
    gpio_put(CLK, 1); sleep_100ns();
    gpio_put(CLK, 0); sleep_100ns();

    gpio_put(CAP, 1); sleep_100ns();

    gpio_put(MCLK, 1); sleep_100ns();
    gpio_put(MCLK, 0); sleep_100ns();

    gpio_put(CAP, 0); sleep_100ns();

    gpio_put(SCLK, 1); sleep_100ns();
    gpio_put(SCLK, 0); sleep_100ns();

    gpio_put(VLD, 0); sleep_100ns();

    gpio_put(CLK, 1); sleep_100ns();
    gpio_put(CLK, 0); sleep_100ns();
    gpio_put(CLK, 1); sleep_100ns();
    gpio_put(CLK, 0); sleep_100ns();

    vector<uint8_t> bits;
    for (int i=0; i<scan.size(); i++) {
      bits.push_back( gpio_get(SOUT) );
      gpio_put(SIN, 0); sleep_100ns();

      gpio_put(MCLK, 0); sleep_100ns();
      gpio_put(MCLK, 1); sleep_100ns();
      gpio_put(MCLK, 0); sleep_100ns();

      gpio_put(SCLK, 0); sleep_100ns();
      gpio_put(SCLK, 1); sleep_100ns();
      gpio_put(SCLK, 0); sleep_100ns();
    }

    return bits;
  }
};

#endif
