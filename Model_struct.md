## 数据处理

- 表格处理
- dict处理
- 和类进行联动
- 中间表格输出？

## 建模

利用工厂模式

### 建变量

- build_varsetattr(model, range, name, rule, init, within)

### 建约束

- build_constraintsetattr(model, range, name, rule)

### 建目标

- build_obj
  - set_objective, del_component

### 求解 

- solver_obj
  - parameters

### 建立目标约束

- add_obj_constraint
  - setattr(self.model, "{}Constr".format(i), Constraint(rule=obj_rule, name=i))
  - exec("""self.opt.add_constraint(self.model.{}Constr)""".format(i))

## 后处理 postprocessing

## 输出
