SquirrelLang
===

语法简介
----

诶，其实就是编译到C++没什么大不了的...
基本数据类型全是C++的。
语法很简单：

- 1.声明
.. code:: squirrel

      var : int [1];

      "[]"表示的是参数列表。

- 2.定义
.. code:: squirrel

      var := [arg:int=>int]{
          return arg+1;
      };

      表示一个类型为int -> int的函数

      类：
      var: [member1:int, member2:float, member3:char]
      {
        this.member1=member1;
        this.member2=member2;
        this.member3=member3;  //非定义语句会被编译到C++类的初始化函数中

        member4:=[x:int,y:int=>[int=>int]]{
            ret:=[arg:int=>int]{
                return arg+(x+member1)*(y+member2);
            };
            return ret;
        }; //一个接受两个参数，返回[int=>int]类型的成员函数
      };
      //这么设计虽然不能柯里化，但是可以字典传参啊（逃

- 3.导入包
.. code:: squirrel

      using <= (Squirrel的Package Name)
      #include <- (C++的头文件或源文件)

- 4.goto语句
.. code:: squirrel

      =>=>where_you_wanna_goto;
      &here_you_wanna_goto;
