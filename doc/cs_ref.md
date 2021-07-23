> 转行程序员的精雕细选、诚心推荐。
> 
> 文末付下载链接和课程链接。

# 自学计算机书籍和课程推荐

> ⚠️ 切记**不要**只读书、看视频，不动手做练习、写程序。
> 
> ⚠️ 切记**不要**求速度，不做练习、不写程序

这些课程和书籍是我食用后觉得良心且有帮助的资源，他们不仅仅可以帮助你学习计算机科学，也会帮助你领略一点点计算机的优雅和美丽。这些主题可能听起来没有大数据、云计算那么华丽，但却道出了真正理解这些技术的真正要素。计算机科学太年轻了（不到100年历史），学习技术的收益远没有学习基础高

## 计算机基础

计算机入门书籍，我只推荐三本，而这三本 SICP 和 HTDP 可以先选择其中一本必读, CSAPP 是必读的。但是个人建议如果计算机基础差一些，建议HTDP，SICP 可以以后再读。

### 《Structure and Interpretation of Computer Programs》（SICP）

>《计算机程序的构造和解释》

![SICP](https://i.imgur.com/rHsSNr8.png)

这是一本来自麻省理工大学，经历20多年仍然充满活力的好书。这是一本关于计算机程序设计的总体性观念的入门书，书本中采用一种lisp方言 - Scheme作为所有例子和练习的实现语言。作者从基础的程序设计一直讲道了解释器和编译器的实现，编程范式从过程式、函数式到面向对象、面向并发都有涉及，但是讲解非常清晰。小编读完（花了两年时间，期间放弃了无数次）后，只能说：我还想再读一遍。

> 小知识：Lisp诞生于1958年，是一个比C和Fortran更古老的函数式编程语言。

不过，小编的感觉此书当然可以一上来就读，不过如果有了几年的实战经验后重读效果更佳！因为你会有一种这本书中涉及到了你工作中会遇到的大多数事情，比如编程范式、抽象方法等等。

有的小伙伴可能会忧虑：Scheme是个什么鬼？Lisp还活着吗？我不想用这个古老的语言，我要用Python！！好的好的，福音来了：

来自伯克利的同名课程，但是所有课程资料和作业都是Python3！

**[CS61A: Structure and Interpretation of Computer Programs](https://inst.eecs.berkeley.edu/~cs61a/sp12/)**

如果你对Scheme情有独钟，这里是MIT的原版视频：

**[Structure and Interpretation of Computer Programs](https://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-001-structure-and-interpretation-of-computer-programs-spring-2005/)**

### 《How to Design Programs》
> 《如何设计程序》

![HTDP](https://i.imgur.com/VMju2ju.png)

这是同样是一本经典的计算机程序设计入门书，采用另一个更现代的Lisp方言 - Racket 作为实现语言（是的，又是Lisp，这门古老的语言拥有强大的生命力）。与 SICP 相比，HTDP 更加注重程序设计的基本原则，材料组织更加平易近人，更容易读，难度也更低。小编认为是一本非常好的编程入门书，书中有大量的实例和练习题，从最简单的数据结构、递归讲到各种程序设计的抽象方法。

这本书的在线版本：https://htdp.org

### 《Computer Systems: A Programmer's Perspective》
> 《深入理解计算机系统》


![CSAPP](https://i.imgur.com/NkjpmYJ.png)

这本书中文被翻译成：深入理解计算机系统，我觉得不妥。原文的意思是给程序员看的计算机系书。这本书与前两本大不相同，他是从计算机硬件的角度切入的；而前两本是从软件和程序设计的角度切入。因此，这本书会解释你写的程序是如何被翻译成指令，如何被计算机执行，读完此书，你会理解：进程、并发、编译、虚拟内存、缓存等等计算机概念。此书采用C语言作为实现语言，总体来说，这是一门很“底层”的计算机入门课。

如果你觉得只读书有点无趣，可以考虑这门课：

**[中文字幕的公开课！](https://www.bilibili.com/video/BV1XW411A7fB/)**


## 数据结构和算法

网上很多人推荐经典《Introduction to Algorithms》作为算法入门书，我觉得很不妥，特别对于无法进行全职科班教育的人群。这本书太过于理论了，我自己试了几次都放弃了。所以我推荐下面两本，任选其一。

### 《Algorithms》
> 《算法》

![](https://i.imgur.com/g8PPdyW.png)

此书算是两大算法经典的另一个了，但是内容更加具体和实际一些，Java实现的，全部读完也需要一定的时间和耐心。

可以配合这个Coursera课程：

[同名课程](https://www.coursera.org/learn/algorithms-part1)

### 《Data Structures and Algorithms in Python》
> 《数据结构和算法 - Python》

![Data Structures and Algorithms in Python](https://i.imgur.com/T7QHhmB.png)

这一本我觉得更加亲民，特别是如果你已经在使用Python了，这本读起来会非常舒服，而且内容覆盖也比较全面。

## 编程语言

编程语言书籍的推荐比较困难，因为各人的差异巨大。我的建议是根据自己的工作情况选择一个语言，然后再去选择书籍。

这里只推荐一门非常棒的课程，来自康奈尔的 CS3110。这是一门教你学会如何学会任何编程语言的课程，让你成为一个更好的程序员。

[CS3110 Data Structures and Functional Programming](https://www.cs.cornell.edu/courses/cs3110/2020sp/)

如果时间充裕，可以尝试学习以下几种语言来体验不同的编程体验：

- C
- Ocaml
- Go
- Lisp的一种：Scheme、Racket、Clojure等等

我没有列出Python、Java和C++，因为我猜你们一定已经在工作使用这些语言啦！

推荐他们的原因很简单：这些语言本身很简单，他们代表了不同的范式。我会在后续的文章中对不同的语言进行书籍和资源推荐。

## 进阶

有了计算机和算法基础，加上对编程语言的熟悉，我们就可以开始更加深入的计算机之旅了。计算机的几大浪漫：

- 操作系统
- 数据库
- 计算机网络
- 编译原理

编译原理参考书没有提及，初学计算机的人可以先跳过这门课，因为这门课需要太多其他基础，比如操作系统、计算机语言、词法分析等等，而且编译原理通常只有在特定的工作岗位才会需要，一般的知识在计算机基础中已经有足够的涉猎。

下面这些书籍和课程需要在计算基础、算法、编程语言三项学习完成后食用，否则可能会错过这些资源的精华。

### 操作系统

**《Operating Systems: Three Easy Pieces》**
> 《操作系统：三堂简单的课》

此书是我认为最适合初学者的操作系统书。课程方面，推荐MIT的经典6.S081，这门课程的Lab有一定难度，都做下来对操作系统的重要概念比如：虚拟内存、中断、并发、文件系统等有更加深刻的理解。这门课对 C 语言有要求。

**[MIT 6.S081](https://pdos.csail.mit.edu/6.828/2020/schedule.html)**

更妙的是：**这门课是有视频的**

### 数据库

数据库只推荐一个课程，CMU 15-445 包括了SQL原理和数据库底层实现，但是这门课需要良好的C++功底。

**[CMU 15-445](https://15445.courses.cs.cmu.edu/fall2019/schedule.html)**

更妙的是：**这门课是有视频的**

### 计算机网络

CMU 15-441 有不错的结构和合理的Lab。

**[CMU 15-441](https://computer-networks.github.io/sp19/index.html)**

## 再进阶

### 分布式系统

分布式系统近年来大火，但是这是一个交叉学科，学起来并不容易，需要操作系统、计算机网络和数据库等多种知识做背景。

好在这个领域MIT有一门神课，不仅内容充分，而且配有视频和lab，就是

[MIT 6.824: Distributed Systems](https://pdos.csail.mit.edu/6.824/schedule.html)

资源下载：搜索微信公众号：泛程序员 。选择：资源 - 计算机。