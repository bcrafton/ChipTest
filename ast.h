
#ifndef AST_H
#define AST_H

#include "defines.h"
#include "instruction.h"
#include "util.h"
using namespace std;

typedef enum op_t {
  OP_PLUS,
  OP_LESS,
  OP_GREATER,
  OP_EQUAL,
  OP_MINUS,
  OP_ASSIGN,
  OP_SHIFT_LEFT,
  OP_AND,
  OP_SHIFT_RIGHT,
  OP_INV,
  OP_OR,
  OP_LESS_EQUAL,
  OP_GREATER_EQUAL,
  OP_MATMUL,
  OP_MUL,
  OP_DIV
} op_t;

class program_t;
class expr_t;
class while_expr_t;
class op_expr_t;
class function_decl_t;

static uint32_t label_counter;
static uint32_t expr_count;

// virtual != abstract
class expr_t {
  public:
  int id;
  expr_t() {
    this->id = expr_count;
    expr_count++;
  };
  virtual ~expr_t()                                                { assert(false); };
  virtual code_t compile(string space, map_t<Address>* memory_map) { assert(false); };
};

class expr_imm_t : public expr_t {
  public:
  int id;
  expr_imm_t() {};
  virtual code_t compile       (string space, map_t<Address>* memory_map) { assert(false); };
  virtual code_t compile_assign(string space, map_t<Address>* memory_map) { assert(false); };
  virtual ret_type_t ret_type() { assert(false); };
};

class num_expr_t : public expr_imm_t {
  public:
  int num;
  
  num_expr_t(int num) { this->num = num; }
  ~num_expr_t() { }
  
  // optimize: "is_imm()" member for expr
  // would allow us to merge this into other instruction
  code_t compile(string space, map_t<Address>* memory_map) {
    code_t code;
    if (abs(this->num) >= pow(2, 11)) {
      int MSB = (this->num & 0xFFFFF000) >> 12;
      code.add( new LUI(1, MSB) );

      if ((this->num & 0x00000800) == 0x00000800) {
        code.add( new ADDI(1, 1, 0x000007FF) );
        code.add( new ADDI(1, 1, 1) );
      }

      int LSB = this->num & 0x000007FF;
      code.add( new ADDI(1, 1, LSB) );
    }
    else {
      code.add( new ADDI(0, 1, num) );
    }
    return code;
  }
  code_t compile_assign(string space, map_t<Address>* memory_map) {
    assert(false); // cannot assign a value to a num
  }
  ret_type_t ret_type() {
    return RET_INT;
  }
};

class var_expr_t : public expr_imm_t {
  public:
  string var;
  
  var_expr_t(string var) { this->var = var; }
  ~var_expr_t() { }
  code_t compile(string space, map_t<Address>* memory_map) {
    /*
    code_t code;
    Address addr = memory_map.get(this->var);
    code.add( new LW(addr.reg, 1, addr.imm) );
    return code;
    */
    code_t code;
    code.add( new LW(space + "." + this->var, 1) );
    return code;
  }
  code_t compile_assign(string space, map_t<Address>* memory_map) {
    code_t code;
    code.add( new SW(space + "." + this->var, 2) );
    return code;
  }
  ret_type_t ret_type() {
    return RET_INT;
  }
};

class index_expr_t : public expr_imm_t {
  public:
  dtype_t dtype;
  expr_imm_t* index;

  index_expr_t(dtype_t dtype, expr_imm_t* index) {
    this->dtype = dtype;
    this->index = index;
  }

  code_t compile(string space, map_t<Address>* memory_map) {
    code_t code;

    // compile index
    code.add( this->index->compile(space, memory_map) );

    // load x1 -> x1
    if      (this->dtype == TYPE_INT)  code.add( new  LW(1, 1, 0)    );
    else if (this->dtype == TYPE_LONG) {
      code.add( new LL(1, 0, 0) );
      code.add( new ADDI(0, 0, 0) ); // added to avoid forwarding in RTL
      code.add( new ADDI(0, 0, 0) ); // added to avoid forwarding in RTL
    }
    else if (this->dtype == TYPE_CAM1) {
      ret_type_t type = this->index->ret_type();
      if (type == RET_LONG) {
        // $1 = CAM[MODULE, BL][WL]
        code.add( new CIM1(1) );
      }
      else if (type == RET_INT) {
        // clear
        code.add( new CLR() );
        // $2 = 1
        code.add( new ADDI(0, 2, 1) );
        // WL[ $1 ] = $2
        code.add( new WWL(1, 2) );
        code.add( new ADDI(0, 0, 0) );
        code.add( new ADDI(0, 0, 0) );
        // $1 = $1 + 128
        code.add( new ADDI(1, 1, 128) );
        // WLB[ $1 ] = $2
        code.add( new WWL(1, 2) );
        code.add( new ADDI(0, 0, 0) );
        code.add( new ADDI(0, 0, 0) );
        // $1 = CAM[MODULE, BL][WL]
        code.add( new RD1(1) );
      }
      else {
        assert(false);
      }
    }
    else if (this->dtype == TYPE_CAM2) {
      ret_type_t type = this->index->ret_type();
      if (type == RET_LONG) {
        // $1 = CAM[MODULE, BL][WL]
        code.add( new CIM2(1) );
      }
      else if (type == RET_INT) {
        // clear
        code.add( new CLR() );
        // $2 = 1
        code.add( new ADDI(0, 2, 1) );
        // WL[ $1 ] = $2
        code.add( new WWL(1, 2) );
        code.add( new ADDI(0, 0, 0) );
        code.add( new ADDI(0, 0, 0) );
        // $1 = $1 + 128
        code.add( new ADDI(1, 1, 128) );
        // WLB[ $1 ] = $2
        code.add( new WWL(1, 2) );
        code.add( new ADDI(0, 0, 0) );
        code.add( new ADDI(0, 0, 0) );
        // $1 = CAM[MODULE, BL][WL]
        code.add( new RD2(1) );
      }
      else {
        assert(false);
      }
    }
    else if (this->dtype == TYPE_CAM3) {
      ret_type_t type = this->index->ret_type();
      if (type == RET_LONG) {
        // $1 = CAM[MODULE, BL][WL]
        code.add( new CIM3(1) );
      }
      else if (type == RET_INT) {
        // clear
        code.add( new CLR() );
        // $2 = 1
        code.add( new ADDI(0, 2, 1) );
        // WL[ $1 ] = $2
        code.add( new WWL(1, 2) );
        code.add( new ADDI(0, 0, 0) );
        code.add( new ADDI(0, 0, 0) );
        // $1 = $1 + 128
        code.add( new ADDI(1, 1, 128) );
        // WLB[ $1 ] = $2
        code.add( new WWL(1, 2) );
        code.add( new ADDI(0, 0, 0) );
        code.add( new ADDI(0, 0, 0) );
        // $1 = CAM[MODULE, BL][WL]
        code.add( new RD3(1) );
      }
      else {
        assert(false);
      }
    }
    else if (this->dtype == TYPE_L2) {
      // instructions #1 & #3 are compiler fix to RTL bug. see l2.v & l2_FIX.v
      code.add( new ADDI(1, 2, 0) );
      code.add( new L2L(1, 1) );
      code.add( new L2L(2, 2) );
    }
    else assert(false);

    return code;
  }

  code_t compile_assign(string space, map_t<Address>* memory_map) {
    code_t code;

    // compile index
    code.add( this->index->compile(space, memory_map) );

    if      (this->dtype == TYPE_INT) code.add( new SW(1, 2, 0) );
    else if (this->dtype == TYPE_CAM1) {
      ret_type_t type = this->index->ret_type();
      if (type == RET_INT) {
        code.add( new INV(0, 4) );
        code.add( new ADDI(0, 3, 1) );
        code.add( new CLR() );
        code.add( new WWL(1, 3) );
        code.add( new ADDI(0, 0, 0) );
        code.add( new ADDI(0, 0, 0) );
        code.add( new WR1(2, 4) );
        code.add( new ADDI(0, 0, 0) );
      }
      else if (type == RET_LONG) {
        code.add( new INV(0, 4) );
        code.add( new ADDI(0, 0, 0)   );
        code.add( new WR1(2, 4) );
        code.add( new ADDI(0, 0, 0)   );
      }
      else {
        assert(false);
      }
    }
    else if (this->dtype == TYPE_CAM2) {
      ret_type_t type = this->index->ret_type();
      if (type == RET_INT) {
        code.add( new INV(0, 4) );
        code.add( new ADDI(0, 3, 1) );
        code.add( new CLR() );
        code.add( new WWL(1, 3) );
        code.add( new ADDI(0, 0, 0) );
        code.add( new ADDI(0, 0, 0) );
        code.add( new WR2(2, 4) );
        code.add( new ADDI(0, 0, 0) );
      }
      else if (type == RET_LONG) {
        code.add( new INV(0, 4) );
        code.add( new ADDI(0, 0, 0)   );
        code.add( new WR2(2, 4) );
        code.add( new ADDI(0, 0, 0)   );
      }
      else {
        assert(false);
      }
    }
    else if (this->dtype == TYPE_CAM3) {
      ret_type_t type = this->index->ret_type();
      if (type == RET_INT) {
        code.add( new INV(0, 4) );
        code.add( new ADDI(0, 3, 1) );
        code.add( new CLR() );
        code.add( new WWL(1, 3) );
        code.add( new ADDI(0, 0, 0) );
        code.add( new ADDI(0, 0, 0) );
        code.add( new WR3(2, 4) );
        code.add( new ADDI(0, 0, 0) );
      }
      else if (type == RET_LONG) {
        code.add( new INV(0, 4) );
        code.add( new ADDI(0, 0, 0)   );
        code.add( new WR3(2, 4) );
        code.add( new ADDI(0, 0, 0)   );
      }
      else {
        assert(false);
      }
    }
    else if (this->dtype == TYPE_L2) {
      code.add( new L2S(1, 2) );
    }
    else assert(false);

    return code;
  }

  ret_type_t ret_type() {
    if      (this->dtype == TYPE_INT)  return RET_INT;
    else if (this->dtype == TYPE_LONG) return RET_LONG;
    else assert(false);
  }
};

class index2_expr_t : public expr_imm_t {
  public:
  dtype_t dtype;
  expr_imm_t* index1;
  expr_imm_t* index2;

  index2_expr_t(dtype_t dtype, expr_imm_t* index1, expr_imm_t* index2) {
    this->dtype = dtype;
    this->index1 = index1;
    this->index2 = index2;
  }

  code_t compile(string space, map_t<Address>* memory_map) {
    code_t code;

    // compile index2
    code.add( this->index2->compile(space, memory_map) );
    code.add( new ADDI(1, 3, 0) );

    // compile index1
    code.add( this->index1->compile(space, memory_map) );

    if (this->dtype == TYPE_LONG) {
      code.add( new SLLI(1, 1, 3) );
      code.add( new ADD(1, 3, 1) );
      code.add( new ADDI(0, 0, 0) );
      code.add( new LLW(1, 1) );
      code.add( new ADDI(0, 0, 0) );
    }
    else assert(false);

    return code;
  }

  code_t compile_assign(string space, map_t<Address>* memory_map) {
    code_t code;

    // compile index2
    code.add( this->index2->compile(space, memory_map) );
    code.add( new ADDI(1, 3, 0) );

    // compile index1
    code.add( this->index1->compile(space, memory_map) );

    if (this->dtype == TYPE_LONG) {
      code.add( new SLLI(1, 1, 3) );
      code.add( new ADD(1, 3, 1) );
      code.add( new ADDI(0, 0, 0) );
      code.add( new SLW(1, 2) );
      code.add( new ADDI(0, 0, 0) );
    }
    else if (this->dtype == TYPE_CAM1) {
      code.add( new CLR() );
      code.add( new ADDI(0, 0, 0) );

      code.add( new WWL2(1, 3) );
      code.add( new ADDI(0, 0, 0) );

      code.add( new INV(0, 4) );
      code.add( new ADDI(0, 0, 0) );

      code.add( new WR1(2, 4) );
      code.add( new ADDI(0, 0, 0) );
    }
    else assert(false);

    return code;
  }

  ret_type_t ret_type() {
    if      (this->dtype == TYPE_INT)  return RET_INT;
    else if (this->dtype == TYPE_LONG) return RET_LONG;
    else assert(false);
  }
};

class index3_expr_t : public expr_imm_t {
  public:
  dtype_t dtype;
  expr_imm_t* index1;
  expr_imm_t* index2;
  expr_imm_t* index3;

  index3_expr_t(dtype_t dtype, expr_imm_t* index1, expr_imm_t* index2, expr_imm_t* index3) {
    this->dtype = dtype;
    this->index1 = index1;
    this->index2 = index2;
    this->index3 = index3;
  }

  code_t compile(string space, map_t<Address>* memory_map) {
    code_t code;

    // compile index3
    code.add( this->index3->compile(space, memory_map) );
    code.add( new ADDI(1, 3, 0) );

    // compile index2
    code.add( this->index2->compile(space, memory_map) );
    code.add( new ADDI(1, 2, 0) );

    // compile index1
    code.add( this->index1->compile(space, memory_map) );

    if (this->dtype == TYPE_CAM1) {
      // clear
      code.add( new CLR() );
      code.add( new ADDI(0, 0, 0) );

      // WL[ $1 ] = $2
      code.add( new WWL2(1, 2) );
      code.add( new ADDI(0, 0, 0) );

      // WL[ $1 + 4 ] = $3
      code.add( new ADDI(1, 1, 4) );
      code.add( new WWL2(1, 3) );
      code.add( new ADDI(0, 0, 0) );

      // RD
      code.add( new ADDI(0, 0, 0) );
      for (int i=0; i<300; i++) {
      code.add( new CIM1(1) );
      }     
      code.add( new ADDI(0, 0, 0) );
    }
    else if (this->dtype == TYPE_CAM2) {
      // clear
      code.add( new CLR() );
      code.add( new ADDI(0, 0, 0) );

      // WL[ $1 ] = $2
      code.add( new WWL2(1, 2) );
      code.add( new ADDI(0, 0, 0) );

      // WL[ $1 + 4 ] = $3
      code.add( new ADDI(1, 1, 4) );
      code.add( new WWL2(1, 3) );
      code.add( new ADDI(0, 0, 0) );

      // RD
      code.add( new ADDI(0, 0, 0) );
      code.add( new CIM2(1) );
      code.add( new ADDI(0, 0, 0) );
    }
    else if (this->dtype == TYPE_CAM3) {
      // clear
      code.add( new CLR() );
      code.add( new ADDI(0, 0, 0) );

      // WL[ $1 ] = $2
      code.add( new WWL2(1, 2) );
      code.add( new ADDI(0, 0, 0) );

      // WL[ $1 + 4 ] = $3
      code.add( new ADDI(1, 1, 4) );
      code.add( new WWL2(1, 3) );
      code.add( new ADDI(0, 0, 0) );

      // RD
      code.add( new ADDI(0, 0, 0) );
      code.add( new CIM3(1) );
      code.add( new ADDI(0, 0, 0) );
    }
    else assert(false);

    return code;
  }

  code_t compile_assign(string space, map_t<Address>* memory_map) {
    code_t code;

    // compile index3
    code.add( this->index3->compile(space, memory_map) );
    code.add( new ADDI(1, 4, 0) );

    // compile index2
    code.add( this->index2->compile(space, memory_map) );
    code.add( new ADDI(1, 3, 0) );

    // compile index1
    code.add( this->index1->compile(space, memory_map) );

    if (this->dtype == TYPE_CAM1) {
      code.add( new CLR() );
      code.add( new ADDI(0, 0, 0) );

      code.add( new WWL2(1, 3) );
      code.add( new ADDI(0, 0, 0) );
      code.add( new ADDI(0, 0, 0) );

      code.add( new WR1(2, 4) );
      code.add( new ADDI(0, 0, 0) );
    }
    else assert(false);

    return code;
  }

  ret_type_t ret_type() {
    if      (this->dtype == TYPE_INT)  return RET_INT;
    else if (this->dtype == TYPE_LONG) return RET_LONG;
    else assert(false);
  }
};

class bitsum_expr_t : public expr_t {
  public:
  expr_t* bits;

  bitsum_expr_t(expr_t* bits) {
    this->bits = bits;
  }

  code_t compile(string space, map_t<Address>* memory_map) {
    code_t code;

    // compile bits
    code.add( this->bits->compile(space, memory_map) );

    // sum(WL=1) -> x1
    code.add( new ADDI(0, 0, 0) );
    code.add( new BITSUM(0, 1) );
    code.add( new ADDI(0, 0, 0) );

    return code;
  }
};

class while_expr_t : public expr_t {
  public:
  expr_t* cond;
  vector<expr_t*> exprs;
  int label_id;
  string label;
  
  while_expr_t(expr_t* cond, vector<expr_t*> exprs) { 
    this->cond = cond;
    this->exprs = exprs;
    this->label_id = label_counter;
    label_counter++;
    this->label = "label_while_" + to_string(this->label_id);
  }
  ~while_expr_t() { }

  // LOOP:
  //   cond
  //   bne [END]
  //   while-block
  //   jump [LOOP]
  // END:

  code_t compile(string space, map_t<Address>* memory_map) {
    code_t code;
    // evaluate condition
    code_t code1 = cond->compile(space, memory_map);
    // evaluate code block
    code_t code3;
    for(int i=0; i<this->exprs.size(); i++) {
      code3.add(this->exprs.at(i)->compile(space, memory_map));
    }
    int offset = code1.count() + 2 + code3.count();
    code3.add( new JALR(0, 1, new Value("", -offset * 4, true)) );
    code3.add( new ADDI(0, 0, 0) ); // need a place to jump to if this is last instruction
    // branch if condition is not true
    code_t code2;
    code2.add( new ADDI(0, 2, 1) );
    code2.add( new BNE(1, 2, code3.count() * 4) ); // multiples of 2 ... see isa docs
    // concatenate them together
    code.add(code1);
    code.add(code2);
    code.add(code3);
    return code;
  }
};

class for_expr_t : public expr_t {
  public:
  expr_t* init;
  expr_t* cond;
  expr_t* post;
  vector<expr_t*> exprs;

  for_expr_t(expr_t* init, expr_t* cond, expr_t* post, vector<expr_t*> exprs) {
    this->init = init;
    this->cond = cond;
    this->post = post;
    this->exprs = exprs;
  }
  ~for_expr_t() { }

  // https://norasandler.com/2018/04/10/Write-a-Compiler-8.html
  // 1) Evaluate init.
  // 2) Evaluate condition.
  // 3) If it’s false, jump to step 7.
  // 4) Execute statement.
  // 5) Execute post-expression.
  // 6) Jump to step 2.
  // 7) Finish.

  code_t compile(string space, map_t<Address>* memory_map) {
    code_t code;

    // 1) evaluate init
    code_t code1 = this->init->compile(space, memory_map);

    // 2) evaluate cond
    code_t code2 = this->cond->compile(space, memory_map);

    // 3) branch if complete
    code_t code3;

    // 4) evaluate code block
    code_t code4;
    for(int i=0; i<this->exprs.size(); i++) {
      code4.add(this->exprs.at(i)->compile(space, memory_map));
    }

    // 5) evaluate post
    code_t code5 = this->post->compile(space, memory_map);

    // 6) jump to (2)
    code_t code6;
    int jump_offset = code2.count() + 2 + code4.count() + code5.count();
    code6.add( new JAL(0, -jump_offset * 4) );
    code6.add( new ADDI(0, 0, 0) ); // need a place to jump to if this is last instruction

    // [FILL IN (3)]
    int branch_offset = code4.count() + code5.count() + code6.count();
    code3.add( new ADDI(0, 2, 1) );
    code3.add( new BNE(1, 2, branch_offset * 4) ); // multiples of 2 ... see isa docs

    // concatenate them together
    code.add(code1);
    code.add(code2);
    code.add(code3);
    code.add(code4);
    code.add(code5);
    code.add(code6);

    return code;
  }
};

class op_expr_t : public expr_t {
  public:
  expr_t* arg1;
  expr_t* arg2;
  op_t op;

  op_expr_t(expr_t* arg1, expr_t* arg2, op_t op) { 
    this->arg1 = arg1;
    this->arg2 = arg2;
    this->op   = op;
  }

  ~op_expr_t() { }

  code_t compile(string space, map_t<Address>* memory_map) {
    code_t code;

    string tmp_var = space + "." + "binop_arg2_" + to_string(this->id);
    memory_map->add(tmp_var, Address());

    code.add(this->arg2->compile(space, memory_map));
    code.add( new SW(tmp_var, 1) );
    code.add(this->arg1->compile(space, memory_map));
    code.add( new LW(tmp_var, 2) );

    if      (op == OP_PLUS)    code.add( new ADD(1, 2, 1) );
    else if (op == OP_LESS)    code.add( new SLT(1, 2, 1) );
    else if (op == OP_GREATER) code.add( new SLT(2, 1, 1) );
    // https://github.com/bcrafton/processor/blob/master/compiler/compile.ml
    // CTRL+F "LessEq"
    else if (op == OP_EQUAL) {
      code.add( new  SLT(1, 2, 3) );
      code.add( new  SLT(2, 1, 4) );
      code.add( new  ADD(3, 4, 5) );
      code.add( new ADDI(0, 6, 1) );
      code.add( new  SLT(5, 6, 1) );
    }
    else if (op == OP_MINUS)         code.add( new SUB(1, 2, 1) );
    else if (op == OP_SHIFT_LEFT)    code.add( new SLL(1, 2, 1) );
    else if (op == OP_AND)           code.add( new AND(1, 2, 1) );
    else if (op == OP_SHIFT_RIGHT)   code.add( new SRL(1, 2, 1) );
    else if (op == OP_OR)            code.add( new  OR(1, 2, 1) );
    else if (op == OP_LESS_EQUAL) {
      code.add( new  SLT(2, 1, 2) );
      code.add( new SLTI(2, 1, 1) );
    }
    else if (op == OP_GREATER_EQUAL) {
      code.add( new  SLT(1, 2, 2) );
      code.add( new SLTI(2, 1, 1) );
    }
    else if (op == OP_MUL) code.add( new MUL(1, 2, 1) );
    else if (op == OP_DIV) code.add( new DIV(1, 2, 1) );
    else assert(false);

    return code;
  }
};

/////////////////////////////////////////////////////////////////////

class tensor_expr_t : public expr_t {
  public:
  expr_t* arg1;
  expr_t* arg2;
  op_t op;

  tensor_expr_t(expr_t* arg1, expr_t* arg2, op_t op) { 
    this->arg1 = arg1;
    this->arg2 = arg2;
    this->op   = op;
  }

  ~tensor_expr_t() { }

  code_t compile(string space, map_t<Address>* memory_map) {
    code_t code;

    code.add(this->arg2->compile(space, memory_map));
    code.add( new MV(1, 2) );
    code.add( new ADDI(0, 0, 0) );
    code.add( new ADDI(0, 0, 0) );
    code.add(this->arg1->compile(space, memory_map));
    code.add( new MM(1, 2, 0, 1) );
    code.add( new ADDI(0, 0, 0) );
    code.add( new ADDI(0, 0, 0) );

    return code;
  }
};

class mac_expr_t : public expr_t {
  public:
  expr_t* arg1;
  expr_t* arg2;
  expr_t* arg3;

  mac_expr_t(expr_t* arg1, expr_t* arg2, expr_t* arg3) { 
    this->arg1 = arg1;
    this->arg2 = arg2;
    this->arg3 = arg3;
  }

  ~mac_expr_t() { }

  code_t compile(string space, map_t<Address>* memory_map) {
    code_t code;

    code.add(this->arg3->compile(space, memory_map));
    code.add( new MV(1, 3) );
    code.add( new ADDI(0, 0, 0) );
    code.add( new ADDI(0, 0, 0) );
    code.add(this->arg2->compile(space, memory_map));
    code.add( new MV(1, 2) );
    code.add( new ADDI(0, 0, 0) );
    code.add( new ADDI(0, 0, 0) );
    code.add(this->arg1->compile(space, memory_map));
    code.add( new MM(1, 2, 3, 1) );
    code.add( new ADDI(0, 0, 0) );
    code.add( new ADDI(0, 0, 0) );

    return code;
  }
};

class tensor_index_t : public expr_imm_t {
  public:
  dtype_t dtype;
  expr_imm_t* index;

  tensor_index_t(dtype_t dtype, expr_imm_t* index) {
    this->dtype = dtype;
    this->index = index;
  }

  code_t compile(string space, map_t<Address>* memory_map) {
    code_t code;

    // compile index
    code.add(this->index->compile(space, memory_map));

    if (this->dtype == TYPE_REG) {
      code.add( new LR(1, 1) );
      code.add( new ADDI(0, 0, 0) );
      code.add( new ADDI(0, 0, 0) );
    }
    else if (this->dtype == TYPE_TENSOR) {
      code.add( new LT(1, 1) );
      code.add( new ADDI(0, 0, 0) );
      code.add( new ADDI(0, 0, 0) );
    }
    else if (this->dtype == TYPE_ECC) {
      code.add( new LE(1, 1, 0) );
      code.add( new ADDI(0, 0, 0) );
      code.add( new ADDI(0, 0, 0) );
    }
    else {
      assert (false);
    }

    return code;
  }

  code_t compile_assign(string space, map_t<Address>* memory_map) {
    code_t code;

    // compile index
    code.add(this->index->compile(space, memory_map));

    if (this->dtype == TYPE_REG) {
      code.add( new SR(1, 1) );
      code.add( new ADDI(0, 0, 0) );
      code.add( new ADDI(0, 0, 0) );
    }
    else if (this->dtype == TYPE_TENSOR) {
      code.add( new ST(1, 1) );
      code.add( new ADDI(0, 0, 0) );
      code.add( new ADDI(0, 0, 0) );
    }
    else if (this->dtype == TYPE_ECC) {
      code.add( new SE(1, 1) );
      code.add( new ADDI(0, 0, 0) );
      code.add( new ADDI(0, 0, 0) );
    }
    else {
      assert (false);
    }

    return code;
  }

  ret_type_t ret_type() {
    assert(false);
  }
};

class tensor_index2_t : public expr_imm_t {
  public:
  dtype_t dtype;
  int flags;
  expr_imm_t* index;

  tensor_index2_t(dtype_t dtype, int flags, expr_imm_t* index) {
    this->dtype = dtype;
    this->flags = flags;
    this->index = index;
  }

  code_t compile(string space, map_t<Address>* memory_map) {
    code_t code;

    // compile index
    code.add(this->index->compile(space, memory_map));

    if (this->dtype == TYPE_ECC) {
      code.add( new LE(1, 1, flags) );
      code.add( new ADDI(0, 0, 0) );
      code.add( new ADDI(0, 0, 0) );
    }
    else {
      assert (false);
    }

    return code;
  }

  code_t compile_assign(string space, map_t<Address>* memory_map) {
    code_t code;
    assert(false);
    return code;
  }

  ret_type_t ret_type() {
    assert(false);
  }
};

class tensor_assign_expr_t : public expr_t {
  public:
  expr_imm_t* arg1;
  expr_t*     arg2;

  tensor_assign_expr_t(expr_imm_t* arg1, expr_t* arg2) {
    this->arg1 = arg1;
    this->arg2 = arg2;
  }

  code_t compile(string space, map_t<Address>* memory_map) {
    code_t code;
    
    // compile arg2
    code.add(this->arg2->compile(space, memory_map));

    // compile assign arg1 = $1
    code.add(this->arg1->compile_assign(space, memory_map));

    return code;
  }
};

/////////////////////////////////////////////////////////////////////

class unary_expr_t : public expr_t {
  public:
  expr_t* arg;
  op_t op;

  unary_expr_t(expr_t* arg, op_t op) { 
    this->arg = arg;
    this->op   = op;
  }

  ~unary_expr_t() { }

  code_t compile(string space, map_t<Address>* memory_map) {
    code_t code;

    // compile arg
    code.add( this->arg->compile(space, memory_map) );

    // $1 = ~($1)
    if (op == OP_INV) code.add( new INV(1, 1) );
    else assert(false);

    return code;
  }
};

class assign_expr_t : public expr_t {
  public:
  expr_imm_t* arg1;
  expr_t*     arg2;

  assign_expr_t(expr_imm_t* arg1, expr_t* arg2) { 
    this->arg1 = arg1;
    this->arg2 = arg2;
  }

  code_t compile(string space, map_t<Address>* memory_map) {
    code_t code;
    
    // compile arg2
    code.add(this->arg2->compile(space, memory_map));

    // move arg2 -> x2
    code.add( new ADDI(1, 2, 0) );

    // compile arg1
    code.add(this->arg1->compile_assign(space, memory_map));

    return code;
  }
};

class config_index_t : public expr_imm_t {
  public:
  dtype_t     dtype;
  expr_imm_t* index;
  config_t    cfg;

  config_index_t(dtype_t dtype, config_t cfg, expr_imm_t* index) {
    this->dtype = dtype;
    this->index = index;
    this->cfg   = cfg;
  }

  code_t compile(string space, map_t<Address>* memory_map) {
    code_t code;

    // compile index
    code.add( this->index->compile(space, memory_map) );

    if (this->cfg == CONFIG_WL) {
      // $1 = WL[ $1 ]
      code.add( new RWL(1, 1) );
      code.add( new ADDI(0, 0, 0) );
    }
    else {
      assert(false);
    }

    return code;
  }

  code_t compile_assign(string space, map_t<Address>* memory_map) {
    code_t code;

    // $2 = [cam1 | cam2 | cam3]
    int addr;
    if      (this->dtype == TYPE_CAM1) addr = 0;
    else if (this->dtype == TYPE_CAM2) addr = 1;
    else if (this->dtype == TYPE_CAM3) addr = 2;
    else                               assert(false);
    code.add( new ADDI(0, 2, addr) );

    // cfg[cfg, $2] = $1
    code.add( new CFG(1, 2, cfg) );

    return code;
  }
};

class config_assign_expr_t : public expr_t {
  public:
  expr_imm_t* arg1;
  expr_t*     arg2;

  config_assign_expr_t(expr_imm_t* arg1, expr_t* arg2) {
    this->arg1 = arg1;
    this->arg2 = arg2;
  }

  code_t compile(string space, map_t<Address>* memory_map) {
    code_t code;

    // compile arg2
    code.add(this->arg2->compile(space, memory_map));

    // compile assign arg1 = $1
    code.add(this->arg1->compile_assign(space, memory_map));

    return code;
  }
};

class if_else_expr_t : public expr_t {
  public:
  expr_t* cond;
  vector<expr_t*> exprs_if;
  vector<expr_t*> exprs_else;
  bool has_else;
  int label_id;
  string label_if;
  string label_else;

  if_else_expr_t(expr_t* cond, vector<expr_t*> exprs_if, vector<expr_t*> exprs_else) { 
    this->cond = cond;
    this->exprs_if = exprs_if;
    this->exprs_else = exprs_else;
    this->has_else = true;
    this->labels();
  }

  if_else_expr_t(expr_t* cond, vector<expr_t*> exprs_if) { 
    this->cond = cond;
    this->exprs_if = exprs_if;
    this->has_else = false;
    this->labels();
  }

  void labels() {
    this->label_id = label_counter;
    label_counter++;
    this->label_if   = "label_if_"   + to_string(this->label_id);
    this->label_else = "label_else_" + to_string(this->label_id);
  }

  ~if_else_expr_t() { }

  //   cond
  //   bne [ELSE]
  //   if-block
  //   jump [IF]
  // ELSE:
  //   else-block
  // IF:

  code_t compile(string space, map_t<Address>* memory_map) {
    code_t code;

    // evaluate condition
    code_t code_cond = cond->compile(space, memory_map);

    // if code block
    code_t code_if;
    for(int i=0; i<this->exprs_if.size(); i++) {
      code_if.add(this->exprs_if.at(i)->compile(space, memory_map));
    }

    // else code block
    code_t code_else;
    for(int i=0; i<this->exprs_else.size(); i++) {
      code_else.add(this->exprs_else.at(i)->compile(space, memory_map));
    }

    // append branch instruction
    int branch_num = (code_if.count() + 2); // (+0)=code_if[-1] (+1)=jalr (+2)=code_else[0]
    code_cond.add( new ADDI(0, 2, 1) );
    code_cond.add( new BNE(1, 2, branch_num * 4) ); // multiples of 2 ... see isa docs

    // append jump instruction
    int jump_addr = code_else.count() + 1; // (+1) = jump ... want to land on dummy.
    code_if.add( new JALR(0, 1, new Value("", jump_addr * 4, true)) );

    code_t dummy = new ADDI(0, 0, 0); // dummy instruction to jump to

    // concatenate them together
    code.add(code_cond);
    code.add(code_if);
    code.add(code_else);
    code.add(dummy);

    return code;
  }
};

// (1) get [registers used, local vars (stack vars)]
// (2) define [return address, stack pointer] = [x30, x31] ?

class function_decl_t : public expr_t {
  public:
  string name;
  vector<string> args;
  vector<string> vars;
  vector<expr_t*> body;
  expr_t* ret;

  function_decl_t(string name, vector<string> args, vector<string> vars, vector<expr_t*> body, expr_t* ret) {
    this->name = name;
    this->args = args;
    this->vars = vars;
    this->body = body;
    this->ret  = ret;
  }

  // regs
  // vars
  // ra <- [stack pointer]
  // args

  code_t compile(string space, map_t<Address>* memory_map) {
    code_t code;

    /////////////////////////////////////////////////////

    string new_space = space + "." + this->name;
    map_t<Address>* new_memory_map = new map_t<Address>();

    /////////////////////////////////////////////////////

    // body
    code_t code_body;
    for(int i=0; i<this->body.size(); i++) {
      code_body.add(this->body.at(i)->compile(new_space, new_memory_map));
    }

    /////////////////////////////////////////////////////

    // 1) add args to namespace
    for(int i=0; i<this->args.size(); i++) {
      string name = this->args.at(i);
      Address addr(BP, (i - this->args.size()) * 4);
      new_memory_map->add(new_space + "." + name, addr);
    }
    // 2) add vars to namespace
    for(int i=0; i<this->vars.size(); i++) {
      string name = this->vars.at(i);
      Address addr(SP, (i - this->vars.size()) * 4);
      new_memory_map->add(new_space + "." + name, addr);
    }

    /////////////////////////////////////////////////////

    int tmp_vars_size = 0;
    for (int i=0; i<new_memory_map->size(); i++) {
      pair<string, Address> var = new_memory_map->at(i);
      if (! var.second.alloc) {
        tmp_vars_size += 1;
        var.second.alloc = true;
        var.second.reg = SP;
        var.second.imm = (-tmp_vars_size - 1 - vars.size()) * 4;
        new_memory_map->add(var.first, var.second);
      }
    }

    /////////////////////////////////////////////////////

    code_t code_ret;

    // compile return expr
    code_ret.add( this->ret->compile(new_space, new_memory_map) );

    // put return value in x1
    // [ implied ]

    /////////////////////////////////////////////////////

    // gather registers used
    set_t regs = code_body.regs();
    regs.remove(0);
    regs.remove(1);
    regs.remove(SP);
    regs.remove(BP);
    regs.remove(RA);

    // amount to move stack pointer
    int amt = regs.size() + vars.size() + 2 + tmp_vars_size;

    /////////////////////////////////////////////////////

    // prologue
    code_t prologue;

    // store old BP
    prologue.add( new   SW(SP, BP, 0) );

    // new BP = old SP
    prologue.add( new ADDI(SP, BP, 0) );

    // increment stack pointer
    prologue.add( new ADDI(SP, SP, amt * 4) );

    // push return address
    prologue.add( new SW(BP, RA, 1 * 4) );

    // push registers used
    for(int i=0; i<regs.size(); i++) {
      int reg = regs.at(i);
      int addr = i + 2;
      prologue.add( new SW(BP, reg, addr * 4) );
    }

    // push local vars -> [allocate local vars]

    /////////////////////////////////////////////////////

    // epilogue
    code_t epilogue;

    // pop registers used
    for(int i=0; i<regs.size(); i++) {
      int reg = regs.at(i);
      int addr = i + 2;
      epilogue.add( new LW(BP, reg, addr * 4) );
    }

    // pop return address
    epilogue.add( new LW(BP, RA, 1 * 4) );

    // decrement stack pointer
    epilogue.add( new ADDI(SP, SP, -amt * 4) );

    // load old BP
    epilogue.add( new   LW(SP, BP, 0) );

    /////////////////////////////////////////////////////

    // jump back to return address
    epilogue.add( new JALR(RA, 0, 0) );

    /////////////////////////////////////////////////////

    // concatenate them together
    // code.add( new Label(this->name) );
    code.add(prologue);
    code.add(code_body);
    code.add(code_ret);
    code.add(epilogue);

    memory_map->add(new_memory_map);

    return code;
  }
};

// caller save registers ?
// callee save registers ? [THIS]
//
// caller:
// [push] -> args push to stack
// [push] -> return address ... we will overwrite it with jalr
// [call] -> [jalr, ja] -> jump to function + save return address
// [pop] args from the stack ?
//
// callee 
// 
/*
def prologue ():
  decrement sp by num registers + local var space
  store any saved registers used
  store ra if a function call is made

def epilogue ():
  reload any saved registers used
  reload ra
  increment sp back to previous value
  jump back to return address
*/

//
// bc [CALLEE] saves registers
// we can do [prologue, epilogue] in either [decl, expr]
// does anything have to be done in [decl, expr] ?
// probably best off doing it inside decl to save code space.
//
// RISCV_Calling_Convention.pdf -- puts [prologue, epilogue] around function.
// "sum_squares" is a great example.
//
// so all "function_expr" will do is:
// 1) push arguments to stack.
// 2) call jalr
// 3) then pop them off afterwards.

/////////////////////////////////////////////////////

// (1) get [arguments]
// (2) define stack pointer
// (3) get function address

/////////////////////////////////////////////////////

// where to put functions ?
// [top / bottom] of code ?
//
// top = [need to jump to start program]
// bottom = [fill in actual address later, jump to end of program -- or exit instruction]
//
// compile every function ... instruction address = offset from 0.
// use main() as well
// then stick them all-together afterwards
//
// alternative = force function declaration at top, do test program fibonacci.
// use function_map_t to keep track of where to jump to.
// yeah this would be fastest/bad solution.
// still need to jump over first function decl.

class function_expr_t : public expr_t {
  public:
  string name;
  vector<expr_t*> args;

  function_expr_t(string name, vector<expr_t*> args) {
    this->name = name;
    this->args = args;
  }
  ~function_expr_t() { }
  code_t compile(string space, map_t<Address>* memory_map) {
    code_t code;

    /////////////////////////////////////////////////////

    // memory_map->add(space + "." + "app_" + to_string(this->id), Address());

    /////////////////////////////////////////////////////

    int sp_incr = this->args.size();

    // push arguments
    code_t code_args;
    for(int i=0; i<this->args.size(); i++) {
      code.add(this->args.at(i)->compile(space, memory_map));
      code.add( new SW(SP, 1, i * 4) );
    }

    // increment stack pointer
    code.add( new ADDI(SP, SP, sp_incr * 4) );

    // jump to function
    code.add( new JALR(0, RA, new Value(this->name, 0)) );

    /////////////////////////////////////////////////////

    // decrement stack pointer
    code.add( new ADDI(SP, SP, (-1) * sp_incr * 4) );

    /////////////////////////////////////////////////////

    return code;
  }
};

/////////////////////////////////////////////////////////////////////////////////////////////////////////

class program_t {
  public:
  vector<string> decls;
  vector<function_decl_t*> functions;
  vector<expr_t*> exprs;

  map_t<int>* function_map;
  map_t<Address>* memory_map;

  program_t(vector<string> decls, vector<function_decl_t*> functions, vector<expr_t*> exprs) {
    this->decls = decls;
    this->functions = functions;
    this->exprs = exprs;

    this->function_map = new map_t<int>();
    this->memory_map = new map_t<Address>();
  };

  code_t compile() {
    string space = "main";
    code_t code;

    /////////////////////////////////////////////////////

    // start the memory map
    for(int i=0; i<this->decls.size(); i++) {
      Address addr(HP, i * 4);
      this->memory_map->add(space + "." + this->decls.at(i), addr);
    }

    /////////////////////////////////////////////////////

    // exprs outside functions / blocks
    code_t code_main;
    for(int i=0; i<this->exprs.size(); i++) {
      code_main.add(this->exprs.at(i)->compile(space, memory_map));
    }

    /////////////////////////////////////////////////////

    uint32_t vars = 0;
    for (int i=0; i<memory_map->size(); i++) {
      pair<string, Address> var = memory_map->at(i);
      if (! var.second.alloc) {
        vars += 1;
        var.second.alloc = true;
        var.second.reg = SP;
        var.second.imm = -vars * 4;
        memory_map->add(var.first, var.second);
      }
    }

    /////////////////////////////////////////////////////

    code.add( new ADDI(0, 0, 0) );
    code.add( new ADDI(SP, SP, vars * 4) );

    code.add( new ADDI(0,  HP, 512) );
    code.add( new ADDI(HP, HP, 512) );
    code.add( new ADDI(HP, HP, 512) );
    code.add( new ADDI(HP, HP, 512) );

    code.add(code_main);
    code.add( new Exit() );

    /////////////////////////////////////////////////////

    uint32_t count = code.count();

    // compile all the functions
    vector<code_t> code_functions;
    for(int i=0; i<this->functions.size(); i++) {
      function_decl_t* f = this->functions.at(i);

      code_t code_function = f->compile(space, memory_map);
      code_functions.push_back(code_function);

      string name = f->name;
      int size = code_function.count();

      function_map->add(name, count * 4);
      count += size;
    }

    /////////////////////////////////////////////////////

    // concatenate them together
    for(int i=0; i<code_functions.size(); i++) {
      code.add(code_functions[i]);
    }

    /////////////////////////////////////////////////////

    return code;
  };
};

/////////////////////////////////////////////////////////////////////////////////////////////////////////

class matmul_expr_t : public expr_t {
  public:
  uint32_t X1;
  uint32_t Y1;
  uint32_t X2;
  uint32_t Y2;

  uint32_t A;
  uint32_t B;
  uint32_t C;

  matmul_expr_t(uint32_t X1, uint32_t Y1, uint32_t X2, uint32_t Y2) {
    this->X1 = X1;
    this->Y1 = Y1;
    this->X2 = X2;
    this->Y2 = Y2;

    assert(this->Y1 == this->X2);

    assert((this->X1 % 4) == 0);
    assert((this->Y1 % 4) == 0);
    assert((this->X2 % 4) == 0);

    this->A = this->X1 / 4;
    this->B = this->Y1 / 4;
    this->C = this->X2 / 4;
  }
  ~matmul_expr_t() { }

  code_t compile(string space, map_t<Address>* memory_map) {
    uint32_t total_op = this->A * this->B * this->C;
    uint32_t mod3 = this->C % 3;
    uint32_t mod2 = this->C % 2;

    if (total_op > 64) {
      if      (mod3 == 0) return this->compile_loop_fast_3(space, memory_map);
      else if (mod2 == 0) return this->compile_loop_fast_2(space, memory_map);
      else                return this->compile_loop(space, memory_map);
    }
    else {
      if      (mod3 == 0) return this->compile_unroll_fast_3(space, memory_map);
      else if (mod2 == 0) return this->compile_unroll_fast_2(space, memory_map);
      else                return this->compile_unroll(space, memory_map);
    }
  }

  code_t compile_unroll(string space, map_t<Address>* memory_map) {
    code_t code;

    uint32_t offset1 = 0;
    uint32_t offset2 = this->A * this->B;
    uint32_t offset3 = offset2 + this->B * this->C;

    for (int i=0; i<this->A; i++){
    for (int j=0; j<this->C; j++){

      code.add( new MV(0, 1) );

      for (int k=0; k<this->B; k++){
        int a = (i * this->B + k) + offset1;
        int b = (k * this->C + j) + offset2;

        code.add( new ADDI(0, 1, a) );
        code.add( new LT(1, 2) );
        code.add( new ADDI(0, 0, 0) );
        code.add( new ADDI(0, 0, 0) );

        code.add( new ADDI(0, 1, b) );
        code.add( new LT(1, 3) );
        code.add( new ADDI(0, 0, 0) );
        code.add( new ADDI(0, 0, 0) );

        code.add( new MM(2, 3, 1, 1) );
        code.add( new ADDI(0, 0, 0) );
        code.add( new ADDI(0, 0, 0) );
      }
      int c = (i * this->B + j) + offset3;

      code.add( new ADDI(0, 1, c) );
      code.add( new ST(1, 1) );
      code.add( new ADDI(0, 0, 0) );
      code.add( new ADDI(0, 0, 0) );
    }
    }

    return code;
  }

  code_t compile_loop(string space, map_t<Address>* memory_map) {
    code_t code;

    uint32_t offset1 = 0;
    uint32_t offset2 = this->A * this->B;
    uint32_t offset3 = offset2 + this->B * this->C;

    int i  = 8;
    int ix = 9;
    int j  = 10;

    int A = 11;
    int B = 12;
    int C = 13;

    int c = 14;

    //////////////////////////////////////////////////

    code.add( new ADDI(0, A, this->A) );
    code.add( new ADDI(0, B, this->B) );
    code.add( new ADDI(0, C, this->C) );

    code.add( new ADDI(0, c, offset3) );

    code.add( new ADDI(0, i, 0) );
    code.add( new ADDI(0, ix, 0) );

    code.add( new ADDI(0, j, 0) );

    //////////////////////////////////////////////////

    code.add( new MV(0, 1) );

    for (int k=0; k<this->B; k++){
      code.add( new ADDI(ix, 1, offset1 + k) );
      code.add( new LT(1, 2) );
      code.add( new ADDI(0, 0, 0) );
      code.add( new ADDI(0, 0, 0) );

      code.add( new ADDI(j, 1, offset2 + k * this->C) );
      code.add( new LT(1, 3) );
      code.add( new ADDI(0, 0, 0) );
      code.add( new ADDI(0, 0, 0) );

      code.add( new MM(2, 3, 1, 1) );
      code.add( new ADDI(0, 0, 0) );
      code.add( new ADDI(0, 0, 0) );
    }

    code.add( new ST(c, 1) );
    code.add( new ADDI(c, c, 1) );
    code.add( new ADDI(0, 0, 0) );
    code.add( new ADDI(0, 0, 0) );

    //////////////////////////////////////////////////

    int jmp1 = 1 + 4 + (this->B * 11) + 1;
    int jmp2 = 2 + 1 + jmp1 + 1;

    //////////////////////////////////////////////////

    code.add( new ADDI(j, j, 1) );
    code.add( new BNE(C, j, -jmp1*4) );

    //////////////////////////////////////////////////

    code.add( new ADDI(ix, ix, this->B) );
    code.add( new ADDI(i, i, 1) );
    code.add( new BNE(A, i, -jmp2*4) );

    //////////////////////////////////////////////////

    return code;
  }

  code_t compile_unroll_fast_2(string space, map_t<Address>* memory_map) {
    code_t code;

    uint32_t offset1 = 0;
    uint32_t offset2 = this->A * this->B;
    uint32_t offset3 = offset2 + this->B * this->C;

    for (int i=0; i<this->A; i++){
    for (int j=0; j<this->C; j+=2){

      for (int k=0; k<this->B; k++){
        int a = (i * this->B + k) + offset1;
        int b1 = (k * this->C + (j+0)) + offset2;
        int b2 = (k * this->C + (j+1)) + offset2;

        code.add( new ADDI(0, 1, a) );
        code.add( new LT(1, 2) );

        code.add( new ADDI(0, 1, b1) );
        code.add( new LT(1, 3) );

        code.add( new ADDI(0, 1, b2) );
        code.add( new LT(1, 4) );

        if (k == 0) code.add( new MM(2, 3, 0, 1) );
        else        code.add( new MM(2, 3, 1, 1) );

        code.add( new ADDI(0, 0, 0) );

        if (k == 0) code.add( new MM(2, 4, 0, 5) );
        else        code.add( new MM(2, 4, 5, 5) );
      }
      int c1 = (i * this->B + (j+0)) + offset3;
      int c2 = (i * this->B + (j+1)) + offset3;

      code.add( new ADDI(0, 1, c1) );
      code.add( new ADDI(0, 2, c2) );
      code.add( new ST(1, 1) );
      code.add( new ST(2, 5) );
    }
    }

    return code;
  }

  code_t compile_loop_fast_2(string space, map_t<Address>* memory_map) {
    code_t code;

    uint32_t offset1 = 0;
    uint32_t offset2 = this->A * this->B;
    uint32_t offset3 = offset2 + this->B * this->C;

    int i  = 8;
    int ix = 9;
    int j  = 10;

    int A = 11;
    int B = 12;
    int C = 13;

    int c = 14;

    //////////////////////////////////////////////////

    code.add( new ADDI(0, A, this->A) );
    code.add( new ADDI(0, B, this->B) );
    code.add( new ADDI(0, C, this->C) );

    code.add( new ADDI(0, c, offset3) );

    code.add( new ADDI(0, i, 0) );
    code.add( new ADDI(0, ix, 0) );

    code.add( new ADDI(0, j, 0) );

    //////////////////////////////////////////////////

    code.add( new MV(0, 1) );
    code.add( new MV(0, 2) );

    for (int k=0; k<this->B; k++){
      code.add( new ADDI(ix, 1, offset1 + k) );
      code.add( new LT(1, 3) );

      code.add( new ADDI(j, 1, offset2 + k * this->C) );
      code.add( new LT(1, 4) );

      code.add( new ADDI(j, 1, offset2 + k * this->C + 1) );
      code.add( new LT(1, 5) );

      code.add( new MM(3, 4, 1, 1) );
      code.add( new ADDI(0, 0, 0) );
      code.add( new MM(3, 5, 2, 2) );
    }

    code.add( new ST(c, 1) );
    code.add( new ADDI(c, c, 1) );
    code.add( new ST(c, 2) );
    code.add( new ADDI(c, c, 1) );

    //////////////////////////////////////////////////

    int jmp1 = 1 + 4 + (this->B * 9) + 2;
    int jmp2 = 2 + 1 + jmp1 + 1;

    //////////////////////////////////////////////////

    code.add( new ADDI(j, j, 2) );
    code.add( new BNE(C, j, -jmp1*4) );

    //////////////////////////////////////////////////

    code.add( new ADDI(ix, ix, this->B) );
    code.add( new ADDI(i, i, 1) );
    code.add( new BNE(A, i, -jmp2*4) );

    //////////////////////////////////////////////////

    return code;
  }

  code_t compile_unroll_fast_3(string space, map_t<Address>* memory_map) {
    code_t code;

    uint32_t offset1 = 0;
    uint32_t offset2 = this->A * this->B;
    uint32_t offset3 = offset2 + this->B * this->C;

    for (int i=0; i<this->A; i++){
    for (int j=0; j<this->C; j+=3){

      for (int k=0; k<this->B; k++){
        int a = (i * this->B + k) + offset1;
        int b1 = (k * this->C + (j+0)) + offset2;
        int b2 = (k * this->C + (j+1)) + offset2;
        int b3 = (k * this->C + (j+2)) + offset2;

        code.add( new ADDI(0, 1, a) );
        code.add( new LT(1, 4) );

        code.add( new ADDI(0, 1, b1) );
        code.add( new LT(1, 5) );

        code.add( new ADDI(0, 1, b2) );
        code.add( new LT(1, 6) );

        code.add( new ADDI(0, 1, b3) );
        code.add( new LT(1, 7) );

        if (k == 0) {
          code.add( new MM(4, 5, 0, 1) );
          code.add( new MM(4, 6, 0, 2) );
          code.add( new MM(4, 7, 0, 3) );
        }
        else {
          code.add( new MM(4, 5, 1, 1) );
          code.add( new MM(4, 6, 2, 2) );
          code.add( new MM(4, 7, 3, 3) );
        }
      }
      int c1 = (i * this->B + (j+0)) + offset3;
      int c2 = (i * this->B + (j+1)) + offset3;
      int c3 = (i * this->B + (j+2)) + offset3;

      code.add( new ADDI(0, 1, c1) );
      code.add( new ADDI(0, 2, c2) );
      code.add( new ADDI(0, 3, c3) );
      code.add( new ST(1, 1) );
      code.add( new ST(2, 2) );
      code.add( new ST(3, 3) );
    }
    }

    return code;
  }

  code_t compile_loop_fast_3(string space, map_t<Address>* memory_map) {
    code_t code;

    uint32_t offset1 = 0;
    uint32_t offset2 = this->A * this->B;
    uint32_t offset3 = offset2 + this->B * this->C;

    int i  = 8;
    int ix = 9;
    int j  = 10;

    int A = 11;
    int B = 12;
    int C = 13;

    int c = 14;

    //////////////////////////////////////////////////

    code.add( new ADDI(0, A, this->A) );
    code.add( new ADDI(0, B, this->B) );
    code.add( new ADDI(0, C, this->C) );

    code.add( new ADDI(0, c, offset3) );

    code.add( new ADDI(0, i, 0) );
    code.add( new ADDI(0, ix, 0) );

    code.add( new ADDI(0, j, 0) );

    //////////////////////////////////////////////////

    code.add( new MV(0, 1) );
    code.add( new MV(0, 2) );
    code.add( new MV(0, 3) );

    for (int k=0; k<this->B; k++){
      code.add( new ADDI(ix, 1, offset1 + k) );
      code.add( new LT(1, 4) );

      code.add( new ADDI(j, 1, offset2 + k * this->C) );
      code.add( new LT(1, 5) );

      code.add( new ADDI(j, 1, offset2 + k * this->C + 1) );
      code.add( new LT(1, 6) );

      code.add( new ADDI(j, 1, offset2 + k * this->C + 2) );
      code.add( new LT(1, 7) );

      code.add( new MM(4, 5, 1, 1) );
      code.add( new MM(4, 6, 2, 2) );
      code.add( new MM(4, 7, 3, 3) );
    }

    code.add( new ST(c, 1) );
    code.add( new ADDI(c, c, 1) );
    code.add( new ST(c, 2) );
    code.add( new ADDI(c, c, 1) );
    code.add( new ST(c, 3) );
    code.add( new ADDI(c, c, 1) );

    //////////////////////////////////////////////////

    int jmp1 = 1 + 6 + (this->B * 11) + 3;
    int jmp2 = 2 + 1 + jmp1 + 1;

    //////////////////////////////////////////////////

    code.add( new ADDI(j, j, 3) );
    code.add( new BNE(C, j, -jmp1*4) );

    //////////////////////////////////////////////////

    code.add( new ADDI(ix, ix, this->B) );
    code.add( new ADDI(i, i, 1) );
    code.add( new BNE(A, i, -jmp2*4) );

    //////////////////////////////////////////////////

    return code;
  }
};

#endif










