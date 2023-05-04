
#ifndef DEFINES_H
#define DEFINES_H

//////////////////////////////////////////////////////////////

#include <stdio.h>
#include "pico/stdlib.h"
#include <utility>
#include <map>
#include <string>
#include <vector>
#include <algorithm>

using namespace std;

//////////////////////////////////////////////////////////////

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

//////////////////////////////////////////////////////////////

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

//////////////////////////////////////////////////////////////

#endif
