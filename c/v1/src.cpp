
#include <stdio.h>
#include "pico/stdlib.h"
#include <utility>
#include <map>
#include <string>
#include <vector>

using namespace std;

#define CLK     14
#define RST     15

#define MCLK    10
#define SCLK    9
#define SIN     13
#define SOUT    16

#define DONE    17
#define VLD     12
#define CAP     8
#define START   11
#define CLK2    18

#define SCK     2
#define MOSI    3
#define CS_LDO  0
#define CS_AVDD 1
#define CS_BIAS 6
#define CS_EN   7

///////////////////////////////////////////////////////////////////////////

class bus_expander_t {
  public:

  bus_expander_t() {
    this->init();
  }
  ~bus_expander_t() { }

  void init() {
    this->write(0, 0);
    this->write(9, 0xff);
  }
  
  void write(int address, int data) {
    // opcode = 01000
    // A1 = 0
    // A0 = 0
    // rw = 0
    // opcode | A1 | A0 | rw = 0x40
    
    gpio_put(CS_EN, 0); sleep_ms(1);
    this->send(0x40);
    this->send(address);
    this->send(data);
    gpio_put(CS_EN, 1); sleep_ms(1);
  }
  
  void send(int bits) {
    for (int i=7; i>=0; i--) {
      uint32_t bit = (bits >> i) & 0x1;
      gpio_put(MOSI, bit); sleep_ms(1);
      gpio_put(SCK,  1);   sleep_ms(1);
      gpio_put(SCK,  0);   sleep_ms(1);
    }
  }
};

///////////////////////////////////////////////////////////////////////////

class dac_t {
  public:
  map<string, pair<int, int>> lut;

  dac_t() {
    this->lut["vdd"]       = pair<int, int>(0, CS_LDO);
    this->lut["avdd_cim"]  = pair<int, int>(1, CS_LDO);
    this->lut["avdd_sram"] = pair<int, int>(2, CS_LDO);

    this->lut["avdd_bl"]   = pair<int, int>(0, CS_AVDD);
    this->lut["avdd_wl"]   = pair<int, int>(1, CS_AVDD);
    this->lut["vref"]      = pair<int, int>(2, CS_AVDD);

    this->lut["vb1"]       = pair<int, int>(0, CS_BIAS);
    this->lut["vb0"]       = pair<int, int>(1, CS_BIAS);
    this->lut["vbl"]       = pair<int, int>(2, CS_BIAS);
    this->lut["vb_dac"]    = pair<int, int>(3, CS_BIAS);

    this->init();
  }
  ~dac_t() { }

  void init() {
    this->set_voltage("vdd",       790);
    this->set_voltage("vdd",       790);
    this->set_voltage("avdd_cim",  820);
    this->set_voltage("avdd_sram", 850);

    this->set_voltage("avdd_bl", 0);
    this->set_voltage("avdd_wl", 450);
    this->set_voltage("vref",    400);

    this->set_voltage("vb1",    700);
    this->set_voltage("vb0",    700);
    this->set_voltage("vbl",    0);
    this->set_voltage("vb_dac", 900);
  }

  void set_voltage(string name, uint32_t value) {
    uint32_t code = value * 256 / 1200;
    pair<int, int> id = this->lut[name];
    this->write(id.second, id.first, code);
  }

  void write(int sync, int address, int data) {
    // PD = 1
    // LDAC = 0
    // last = 0000
    // bits = address + PD + LDAC + data + last

    uint32_t PD = 1;
    uint32_t LDAC = 0;
    uint32_t last = 0;

    uint32_t bits = 0x0000;
    bits = bits | (last    << 0);
    bits = bits | (data    << 4);
    bits = bits | (LDAC    << 12);
    bits = bits | (PD      << 13);
    bits = bits | (address << 14);

    gpio_put(sync, 0); sleep_ms(1);
    for (int i=15; i>=0; i--) {
      uint32_t bit = (bits >> i) & 0x1;
      gpio_put(MOSI, bit); sleep_ms(1);
      gpio_put(SCK,  1);   sleep_ms(1);
      gpio_put(SCK,  0);   sleep_ms(1);
    }
    gpio_put(sync, 1); sleep_ms(1);
  }
};

///////////////////////////////////////////////////////////////////////////

vector<uint8_t> int_to_bits(uint32_t word, uint32_t N) {
  vector<uint8_t> bits;
  for (int i=0; i<N; i++) {
    bits.push_back( (word >> i) & 1 );
  }
  return bits;
}

uint32_t bits_to_int(vector<uint8_t> bits) {
  uint32_t word = 0;
  for (int i=0; i<bits.size(); i++) {
    word = word + (bits[i] << i);
  }
  return word;
}

///////////////////////////////////////////////////////////////////////////

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
    vector<uint8_t> _CMP{0};

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

  void read_cam(uint32_t mmap, uint32_t addr, uint32_t mux, uint32_t sel) {
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
    vector<uint8_t> _CMP{0};

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
    printf("%x\n", word);
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
    vector<uint8_t> _CMP{0};

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
    gpio_put(MCLK,  0); sleep_us(1);
    gpio_put(SCLK,  0); sleep_us(1);
    gpio_put(SIN,   0); sleep_us(1);
    gpio_put(CLK,   0); sleep_us(1);
    gpio_put(VLD,   0); sleep_us(1);
    gpio_put(CAP,   0); sleep_us(1);
    gpio_put(START, 0); sleep_us(1);
    gpio_put(CLK2,  1); sleep_us(1);

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

    gpio_put(CLK, 1);
    gpio_put(CLK, 0);
    gpio_put(CLK, 1);
    gpio_put(CLK2, 0);
    gpio_put(CLK2, 1);
    gpio_put(CLK, 0);
    gpio_put(CLK, 1);
    gpio_put(CLK, 0);
    gpio_put(CLK, 1);
    gpio_put(CLK, 0); sleep_us(1);

    gpio_put(CAP, 1); sleep_us(1);

    gpio_put(MCLK, 1); sleep_us(1);
    gpio_put(MCLK, 0); sleep_us(1);

    gpio_put(CAP, 0); sleep_us(1);

    gpio_put(SCLK, 1); sleep_us(1);
    gpio_put(SCLK, 0); sleep_us(1);

    gpio_put(VLD, 0); sleep_us(1);

    gpio_put(CLK, 1); sleep_us(1);
    gpio_put(CLK, 0); sleep_us(1);
    gpio_put(CLK, 1); sleep_us(1);
    gpio_put(CLK, 0); sleep_us(1);

    vector<uint8_t> bits;
    for (int i=0; i<scan.size(); i++) {
      bits.push_back( gpio_get(SOUT) );
      gpio_put(SIN, 0); sleep_us(1);

      gpio_put(MCLK, 0); sleep_us(1);
      gpio_put(MCLK, 1); sleep_us(1);
      gpio_put(MCLK, 0); sleep_us(1);

      gpio_put(SCLK, 0); sleep_us(1);
      gpio_put(SCLK, 1); sleep_us(1);
      gpio_put(SCLK, 0); sleep_us(1);
    }

    return bits;
  }
};

///////////////////////////////////////////////////////////////////////////

int main() {

  ///////////////////////////////////

  stdio_init_all();

  ///////////////////////////////////

  gpio_init(CLK); gpio_set_dir(CLK, GPIO_OUT);
  gpio_init(RST); gpio_set_dir(RST, GPIO_OUT);

  gpio_init(MCLK); gpio_set_dir(MCLK, GPIO_OUT);
  gpio_init(SCLK); gpio_set_dir(SCLK, GPIO_OUT);
  gpio_init(SIN);  gpio_set_dir(SIN,  GPIO_OUT);
  gpio_init(SOUT); gpio_set_dir(SOUT, GPIO_IN);

  gpio_init(DONE);  gpio_set_dir(DONE,  GPIO_IN);
  gpio_init(VLD);   gpio_set_dir(VLD,   GPIO_OUT);
  gpio_init(CAP);   gpio_set_dir(CAP,   GPIO_OUT);
  gpio_init(START); gpio_set_dir(START, GPIO_OUT);
  gpio_init(CLK2);  gpio_set_dir(CLK2,  GPIO_OUT);

  ///////////////////////////////////

  gpio_init(SCK);     gpio_set_dir(SCK, GPIO_OUT);
  gpio_init(MOSI);    gpio_set_dir(MOSI, GPIO_OUT);
  gpio_init(CS_LDO);  gpio_set_dir(CS_LDO, GPIO_OUT);
  gpio_init(CS_AVDD); gpio_set_dir(CS_AVDD, GPIO_OUT);
  gpio_init(CS_BIAS); gpio_set_dir(CS_BIAS, GPIO_OUT);
  gpio_init(CS_EN);   gpio_set_dir(CS_EN, GPIO_OUT);

  ///////////////////////////////////

  gpio_put(CS_EN, 1);   sleep_ms(1);
  gpio_put(CS_LDO, 1);  sleep_ms(1);
  gpio_put(CS_AVDD, 1); sleep_ms(1);
  gpio_put(CS_BIAS, 1); sleep_ms(1);
  gpio_put(SCK, 0);     sleep_ms(1);
  gpio_put(MOSI, 0);    sleep_ms(1);

  ///////////////////////////////////
  
  bus_expander_t* bus_expander = new bus_expander_t();
  dac_t* dac = new dac_t();
  chip1_t* chip = new chip1_t();

  ///////////////////////////////////

  dac->set_voltage("avdd_wl", 475);
  dac->set_voltage("vref",    500);

  ///////////////////////////////////

  uint32_t tgt = 0x7;
  uint32_t mux = 0;
  uint32_t sel = 0;

  uint32_t N = 16;

  ///////////////////////////////////

  while (1) {

    ///////////////////////////////////////////////////////////////////////////

    vector<uint32_t> words;
    for (int i=0; i<N; i++) {
      uint32_t word = rand() + rand();
      words.push_back( word );
    }

    vector<vector<uint8_t>> WLs(32, vector<uint8_t>(128, 0));
    vector<vector<uint8_t>> WLBs(32, vector<uint8_t>(128, 0));
    for (int i=0; i<N; i++) {
      for (int j=0; j<32; j++) {
        WLs[j][i] = (words[i] >> j) & 0x1;
        WLBs[j][i] = 1 - WLs[j][i];
      }
    }

    ///////////////////////////////////////////////////////////////////////////

    for (int i=0; i<N; i++) {
      printf("[write] %d: %x\n", i, words[i]);
      chip->write_cam(tgt, i, words[i], mux, sel);
    }

    for (int i=0; i<N; i++) {
      printf("[read] %d: ", i);
      chip->read_cam(tgt, i, mux, sel);
    }

    for (int i=0; i<32; i++) {
      printf("[cam] %d: ", i);
      uint32_t word = chip->cam(tgt, WLs[i], WLBs[i], mux, sel);
      printf("%x", word);
      if ( word != (1 << i) ) {
        printf(" | ERROR");
      }
      printf("\n");
    }

    for (int i=0; i<N; i++) {
      printf("[read] %d: ", i);
      chip->read_cam(tgt, i, mux, sel);
    }

    printf("------------------------\n");
    sleep_ms(5000);
  }

  ///////////////////////////////////////////////////////////////////////////
}
