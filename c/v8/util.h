
#ifndef UTIL_H
#define UTIL_H

#include "defines.h"

using namespace std;

inline void sleep_16ns() {
  __asm volatile ("nop":);
  __asm volatile ("nop":);
}

class matrix_t {
  public:
  uint32_t ROW;
  uint32_t COL;
  uint32_t* mat;

  matrix_t(uint32_t row, uint32_t col) {
    this->ROW = row;
    this->COL = col;
    this->mat = new uint32_t[this->ROW * this->COL];
    for (uint32_t r=0; r<this->ROW; r++) {
      for (uint32_t c=0; c<this->COL; c++) {
        this->set(r, c, 0);
      }
    }
  }

  ~matrix_t() {
    delete this->mat;
  }

  void set(int r, int c, int val) {
    this->mat[ r * this->COL + c ] = val;
  }

  uint32_t get(int r, int c) {
    return this->mat[ r * this->COL + c ];
  }

  matrix_t* process(uint32_t BIT) {
    matrix_t* ret = new matrix_t(BIT, this->COL);
    for (uint32_t dac=0; dac<this->ROW; dac++) {
      for (uint32_t bit=0; bit<BIT; bit++) {
        for (uint32_t wl=0; wl<this->COL; wl++) {
          uint32_t val = (this->get(dac, wl) >> bit) & 0x1;
          if (val) {
            ret->set(bit, wl, dac);
          }
        }
      }
    }
    return ret;
  }

};

#endif
