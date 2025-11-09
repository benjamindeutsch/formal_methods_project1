// DO NOT MODIFY THE IMPLEMENTATION OR THE METHOD SIGNATURE
method bezout(a: int, b: int) returns (g: int, x: int, y: int)
    requires a >= 0
    requires b >= 0
    ensures g >= 0
    ensures a * x + b * y == g
{
    if a == 0 {
        return b, 0, 1;
    }
    if b == 0 {
        return a, 1, 0;
    }

    var x0, x1 := 1, 0;
    var y0, y1 := 0, 1;
    var a', b' := a, b;

    while b' != a'
        invariant a' > 0
        invariant b' > 0
        invariant a * x0 + b * y0 == a'
        invariant a * x1 + b * y1 == b'
        decreases (a' + b') + (if a' < b' then 1 else 0) // If a' < b', they are swapped
    {
        var q: int := 0;
        var r: int := a';

        while r > b'
            invariant r > 0
            invariant a' == q * b' + r
            decreases r
        {
            r := r - b';
            q := q + 1;
        }

        a', b' := b', r;
        x0, x1 := x1, x0 - q * x1;
        y0, y1 := y1, y0 - q * y1;
    }

    g := a';
    x := x0;
    y := y0;
}
