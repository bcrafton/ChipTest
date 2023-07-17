
#ifndef UTIL_H
#define UTIL_H

#include "defines.h"

using namespace std;

inline void sleep_100ns() {
  // https://forums.raspberrypi.com/viewtopic.php?t=304922

  // grep -r "nop" IO.dis | wc 
  // 648    4328   26332
  __asm volatile ("nop\nnop\nnop\nnop\nnop\nnop\nnop\nnop\n":);

  // grep -r "nop" IO.dis | wc 
  // 308    1948   12052
  // sleep_us(1);
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

class bits_t {
  public:
  uint32_t ROW;
  uint32_t COL;
  uint32_t* mat;

  bits_t(uint32_t row, uint32_t col) {
    this->ROW = row;
    this->COL = col;
    this->mat = new uint32_t[this->ROW * this->COL];
    this->randomize();
    while( this->unique() == 0 ) {
      this->randomize();
    }
  }

  bits_t(uint32_t row, uint32_t col, uint32_t flag) {
    this->ROW = row;
    this->COL = col;
    this->mat = new uint32_t[this->ROW * this->COL];
    this->randomize();
    /*
    if (flag) {
      while( this->unique() == 0 ) {
        this->randomize();
      }
    }
    */
  }

  ~bits_t() {
    delete this->mat;
  }

  void randomize() {
    for (uint32_t r=0; r<this->ROW; r++) {
      for (uint32_t c=0; c<this->COL; c++) {
        uint32_t val = rand() % 2;
        this->set(r, c, val);
      }
    }
  }

  uint8_t unique() {
    vector<uint8_t> flags(this->COL * this->COL, 0);
    for (uint32_t c1=0; c1<this->COL; c1++) {
    for (uint32_t c2=0; c2<this->COL; c2++) {
    for (uint32_t r=0; r<this->ROW; r++) {
      flags[c1 * this->COL + c2] |= (this->get(r, c1) != this->get(r, c2));
    }
    }
    }
    uint8_t ret = 1;
    for (uint32_t c1=0; c1<this->COL; c1++) {
    for (uint32_t c2=0; c2<this->COL; c2++) {
      if (c1 != c2) {
        ret &= flags[c1 * this->COL + c2];
      }
    }
    }
    return ret;
  }

  void set(int r, int c, int val) {
    this->mat[ r * this->COL + c ] = val;
  }

  uint32_t get(int r, int c) {
    return this->mat[ r * this->COL + c ];
  }

  uint32_t word(uint32_t r) {
    uint32_t ret = 0;
    for (uint32_t c=0; c<this->COL; c++) {
      ret += (this->get(r, c) << c);
    }
    return ret;
  }

  vector<uint8_t> WL(uint32_t c) {
    vector<uint8_t> ret;
    for (uint32_t r=0; r<this->ROW; r++) {
      ret.push_back( this->get(r, c) );
    }
    return ret;
  }

  vector<uint8_t> WLB(uint32_t c) {
    vector<uint8_t> ret;
    for (uint32_t r=0; r<this->ROW; r++) {
      ret.push_back( 1 - this->get(r, c) );
    }
    return ret;
  }

};

#endif
