
#include <stdio.h>
#include "pico/stdlib.h"
#include <utility>
#include <map>
#include <string>
#include <vector>
#include <algorithm>

#include "defines.h"
#include "bus_expander.h"
#include "dac.h"
#include "chip1.h"
#include "chip2.h"
#include "util.h"

using namespace std;

///////////////////////////////////////////////////////////////////////////

char command[1024];
uint64_t args[1024];

///////////////////////////////////////////////////////////////////////////

void read_input() {
  char byte;
  uint32_t i = 0;
  while((byte = getchar()) != '\n' && byte != EOF) {
    if (i < 1024) {
      command[i] = byte;
      i += 1;
    }
  }
  command[i] = '\0';
}

///////////////////////////////////////////////////////////////////////////

bus_expander_t* bus_expander;
dac_t* dac;
chip1_t* chip;
chip2_t* chip2;

///////////////////////////////////////////////////////////////////////////

void write_cam(uint32_t tgt, uint32_t addr, uint32_t data, uint32_t mux, uint32_t sel) {
  chip->write_cam(tgt, addr, data, mux, sel);
}

void read_cam(uint32_t tgt, uint32_t addr, uint32_t mux, uint32_t sel) {
  uint32_t word = chip->read_cam(tgt, addr, mux, sel);
  printf("%x\n", word);
}

void cim(uint32_t tgt, uint32_t mux, uint32_t sel, uint32_t N, uint32_t B) {
  matrix_t* raw = new matrix_t(150, N+1);

  int last = 0;
  for (int code=0; code<150; code++) {
    dac->set_dac("vref", code);
    sleep_ms(2);

    vector<uint8_t> WL(128, 0);
    vector<uint8_t> WLB(128, 0);

    // read (0) WL
    uint32_t word = chip->cim(tgt, WL, WLB, mux, sel);
    raw->set(code, 0, word);

    // read (1:N) WL
    for (int i=0; i<N; i++) {
      WLB[i] = 1;
      uint32_t word = chip->cim(tgt, WL, WLB, mux, sel);
      raw->set(code, i+1, word);
      if (word > 0) last = code;
    }

    if (code > (last + 5)) break;
  }

  matrix_t* data = raw->process(B);
  for (uint32_t bit=0; bit<B; bit++) {
    for (uint32_t wl=0; wl<N+1; wl++) {
      printf("%d ", data->get(bit, wl));
    }
    printf("\n");
  }

  delete raw;
  delete data;
}

void cim2(uint32_t tgt, uint32_t mux, uint32_t sel, uint32_t N, uint32_t B) {
  matrix_t* raw = new matrix_t(150, N+1);

  int last = 0;
  for (int code=0; code<150; code++) {
    dac->set_dac("vref", code);
    sleep_ms(2);

    for (int i=0; i<N+1; i++) {
      vector<uint8_t> WL(128, 0);
      vector<uint8_t> WLB(128, 0);
      for (int j=0; j<i; j++) {
        WLB[j] = 1;
      }
      for (int j=i; j<N; j++) {
        WL[j] = 1;
      }
      uint32_t word = chip->cim(tgt, WL, WLB, mux, sel);
      raw->set(code, i, word);
      if (word > 0) last = code;
    }

    if (code > (last + 5)) break;
  }

  matrix_t* data = raw->process(B);
  for (uint32_t bit=0; bit<B; bit++) {
    for (uint32_t wl=0; wl<N+1; wl++) {
      printf("%d ", data->get(bit, wl));
    }
    printf("\n");
  }

  delete raw;
  delete data;
}

uint32_t cam(uint32_t tgt, uint32_t WL, uint32_t WLB, uint32_t mux, uint32_t sel) {
  vector<uint8_t> _WL  = int_to_bits(WL,  32);
  vector<uint8_t> _WL_PAD(96, 0);
  _WL.insert(_WL.end(), _WL_PAD.begin(), _WL_PAD.end());

  vector<uint8_t> _WLB  = int_to_bits(WLB,  32);
  vector<uint8_t> _WLB_PAD(96, 0);
  _WLB.insert(_WLB.end(), _WLB_PAD.begin(), _WLB_PAD.end());

  return chip->cam(tgt, _WL, _WLB, mux, sel);
}

uint32_t cam2(uint32_t tgt, uint64_t WL, uint64_t WLB, uint32_t mux, uint32_t sel) {
  vector<uint8_t> _WL  = long_to_bits(WL,  64);
  vector<uint8_t> _WL_PAD(64, 0);
  _WL.insert(_WL.end(), _WL_PAD.begin(), _WL_PAD.end());

  vector<uint8_t> _WLB  = long_to_bits(WLB,  64);
  vector<uint8_t> _WLB_PAD(64, 0);
  _WLB.insert(_WLB.end(), _WLB_PAD.begin(), _WLB_PAD.end());

  return chip->cam(tgt, _WL, _WLB, mux, sel);
}

void write_reg() {
  chip->read_reg(9, 3);
  chip->write_reg(9, 3, 0x01);
  chip->read_reg(9, 3);

  chip->read_reg(9, 5);
  chip->write_reg(9, 5, 0x01);
  chip->read_reg(9, 5);
}

///////////////////////////////////////////////////////////////////////////

int main() {

  ///////////////////////////////////

  stdio_init_all();

  ///////////////////////////////////

  gpio_init(SCK);     gpio_set_dir(SCK, GPIO_OUT);
  gpio_init(MOSI);    gpio_set_dir(MOSI, GPIO_OUT);
  gpio_init(CS_LDO);  gpio_set_dir(CS_LDO, GPIO_OUT);
  gpio_init(CS_AVDD); gpio_set_dir(CS_AVDD, GPIO_OUT);
  gpio_init(CS_BIAS); gpio_set_dir(CS_BIAS, GPIO_OUT);
  gpio_init(CS_EN);   gpio_set_dir(CS_EN, GPIO_OUT);

  ///////////////////////////////////

  gpio_put(CS_EN, 1);   sleep_us(1);
  gpio_put(CS_LDO, 1);  sleep_us(1);
  gpio_put(CS_AVDD, 1); sleep_us(1);
  gpio_put(CS_BIAS, 1); sleep_us(1);
  gpio_put(SCK, 0);     sleep_us(1);
  gpio_put(MOSI, 0);    sleep_us(1);

  ///////////////////////////////////
  
  bus_expander = new bus_expander_t();
  dac = new dac_t();
  chip = new chip1_t();
  chip2 = new chip2_t();

  ///////////////////////////////////

  uint32_t tgt = 0xa;
  uint32_t mux = 0;
  uint32_t sel = 0;

  uint32_t N = 16;
  uint32_t B = 8;

  ///////////////////////////////////

  while (1) {

    read_input();
    sscanf(command, "%u", &args[0]);

    if (args[0] == 0) {
      sscanf(command, "%u %u %u", &args[0], &args[1], &args[2]);
      if      (args[1] == 0) dac->set_voltage("vdd",       args[2], 1);
      else if (args[1] == 1) dac->set_voltage("avdd_cim",  args[2], 1);
      else if (args[1] == 2) dac->set_voltage("avdd_sram", args[2], 1);
      else if (args[1] == 3) dac->set_voltage("avdd_bl",   args[2], 1);
      else if (args[1] == 4) dac->set_voltage("avdd_wl",   args[2], 1);
      else if (args[1] == 5) dac->set_voltage("vref",      args[2], 1);
      else if (args[1] == 6) dac->set_voltage("vb1",       args[2], 1);
      else if (args[1] == 7) dac->set_voltage("vb0",       args[2], 1);
      else if (args[1] == 8) dac->set_voltage("vbl",       args[2], 1);
      else if (args[1] == 9) dac->set_voltage("vb_dac",    args[2], 1);
      else printf("No such DAC");
    }
    else if (args[0] == 1) {
      sscanf(command, "%u %u %u", &args[0], &args[1], &args[2]);
      read_cam(args[1], args[2], mux, sel);
    }
    else if (args[0] == 2) {
      sscanf(command, "%u %u %u %u", &args[0], &args[1], &args[2], &args[3]);
      write_cam(args[1], args[2], args[3], mux, sel);
    }
    else if (args[0] == 3) {
      cim(tgt, mux, sel, N, B);
    }
    else if (args[0] == 4) {
      cim2(tgt, mux, sel, N, B);
    }
    else if (args[0] == 5) {
      write_reg();
    }
    else if (args[0] == 6) {
      sscanf(command, "%u %u %u %u", &args[0], &args[1], &args[2], &args[3]);
      chip2->write(args[1], args[2], args[3]);
    }
    else if (args[0] == 7) {
      sscanf(command, "%u %u %u", &args[0], &args[1], &args[2]);
      uint32_t word = chip2->read(args[1], args[2]);
      printf("%u %u: %x\n", args[1], args[2], word);
    }
    else if (args[0] == 8) {
      chip2->run(100000);
    }
    else if (args[0] == 9) {
      chip2->run_us(100000);
    }
    else if (args[0] == 10) {
      sscanf(command, "%u %u %x %x", &args[0], &args[1], &args[2], &args[3]);
      uint32_t word = cam(args[1], args[2], args[3], mux, sel);
      printf("%x\n", word);
    }
    else if (args[0] == 11) {
      sscanf(command, "%u %u %llx %llx", &args[0], &args[1], &args[2], &args[3]);
      uint32_t word = cam2(args[1], args[2], args[3], mux, sel);
      printf("%x\n", word);
    }
    else {
      printf("Invalid code: %u\n", args[0]);
    }

  }

  ///////////////////////////////////

}
