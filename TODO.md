1. Object by možno mal byť vlastný token (Základná nadtrieda [Superclass])

``` c++
class Shape : Object** {
int id;
void Shape(void) { print("constructor of Shape"); }
string toString(void) { return "instance of Shape " + (string)(this.id); }
}
```