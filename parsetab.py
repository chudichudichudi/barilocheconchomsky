
# parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.8'

_lr_method = 'LALR'

_lr_signature = '7FF3B9EEE8D9AEFB99D07ACE2E73536A'
    
_lr_action_items = {'SUPER':([4,6,9,11,13,18,20,21,22,23,24,27,28,],[-19,14,14,14,14,14,14,-13,-14,-11,-12,14,30,]),'LLAVEDER':([4,7,9,12,13,15,18,19,20,21,22,23,24,25,26,27,28,31,32,],[-19,-15,-17,23,24,-16,-18,-5,-6,-13,-14,-11,-12,-3,-7,-8,-4,-9,-10,]),'DIVISION':([1,4,6,7,9,10,11,12,13,15,18,19,20,21,22,23,24,25,26,27,28,31,32,],[8,-19,16,8,16,8,16,8,16,8,16,-5,-6,-13,-14,-11,-12,-3,-7,-8,-4,-9,-10,]),'PARENIZQ':([0,1,2,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,],[2,2,2,-19,2,2,2,2,2,2,2,2,2,2,2,2,2,2,-5,-6,-13,-14,-11,-12,-3,-7,-8,-4,2,2,-9,-10,]),'PARENDER':([4,7,9,10,11,15,18,19,20,21,22,23,24,25,26,27,28,31,32,],[-19,-15,-17,21,22,-16,-18,-5,-6,-13,-14,-11,-12,-3,-7,-8,-4,-9,-10,]),'CARACTER':([0,1,2,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,],[4,4,4,-19,4,4,4,4,4,4,4,4,4,4,4,4,4,4,-5,-6,-13,-14,-11,-12,-3,-7,-8,-4,4,4,-9,-10,]),'SUB':([4,6,9,11,13,18,20,21,22,23,24,25,27,],[-19,17,17,17,17,17,17,-13,-14,-11,-12,29,17,]),'LLAVEIZQ':([0,1,2,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,],[5,5,5,-19,5,5,5,5,5,5,5,5,5,5,5,5,5,5,-5,-6,-13,-14,-11,-12,-3,-7,-8,-4,5,5,-9,-10,]),'$end':([1,3,4,6,7,9,15,18,19,20,21,22,23,24,25,26,27,28,31,32,],[-2,0,-19,-1,-15,-17,-16,-18,-5,-6,-13,-14,-11,-12,-3,-7,-8,-4,-9,-10,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'statement':([0,],[3,]),'expression2':([0,1,2,5,6,7,8,9,10,11,12,13,15,16,18,19,20,26,27,],[1,7,10,12,15,7,19,15,7,15,7,15,7,26,15,7,15,7,15,]),'expression':([0,1,2,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,26,27,29,30,],[6,9,11,13,18,9,20,18,9,18,9,18,25,9,27,28,18,9,18,9,18,31,32,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> statement","S'",1,None,None,None),
  ('statement -> expression','statement',1,'p_statement_expr','parser.py',46),
  ('statement -> expression2','statement',1,'p_statement_expr','parser.py',47),
  ('expression2 -> expression SUPER expression','expression2',3,'p_expression_binop','parser.py',51),
  ('expression2 -> expression SUB expression','expression2',3,'p_expression_binop','parser.py',52),
  ('expression2 -> expression2 DIVISION expression2','expression2',3,'p_expression_binop','parser.py',53),
  ('expression2 -> expression2 DIVISION expression','expression2',3,'p_expression_binop','parser.py',54),
  ('expression2 -> expression DIVISION expression2','expression2',3,'p_expression_binop','parser.py',55),
  ('expression2 -> expression DIVISION expression','expression2',3,'p_expression_binop','parser.py',56),
  ('expression2 -> expression SUPER expression SUB expression','expression2',5,'p_expression_terop','parser.py',63),
  ('expression2 -> expression SUB expression SUPER expression','expression2',5,'p_expression_terop','parser.py',64),
  ('expression -> LLAVEIZQ expression2 LLAVEDER','expression',3,'p_expression_group','parser.py',69),
  ('expression -> LLAVEIZQ expression LLAVEDER','expression',3,'p_expression_group','parser.py',70),
  ('expression -> PARENIZQ expression2 PARENDER','expression',3,'p_expression_group','parser.py',71),
  ('expression -> PARENIZQ expression PARENDER','expression',3,'p_expression_group','parser.py',72),
  ('expression2 -> expression2 expression2','expression2',2,'p_expression_concat','parser.py',77),
  ('expression2 -> expression expression2','expression2',2,'p_expression_concat','parser.py',78),
  ('expression2 -> expression2 expression','expression2',2,'p_expression_concat','parser.py',79),
  ('expression2 -> expression expression','expression2',2,'p_expression_concat','parser.py',80),
  ('expression -> CARACTER','expression',1,'p_expression_caracter','parser.py',84),
]
