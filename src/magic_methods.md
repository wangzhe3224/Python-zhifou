Objects are Python’s abstraction for data. In a sense, and in conformance to Von Neumann’s model of a “stored program computer”, code is also represented by objects. Every object has an identity, a type and a value.

For CPython, id(x) is the memory address where x is stored.

Also note that catching an exception with a ‘try…except’ statement may keep objects alive.