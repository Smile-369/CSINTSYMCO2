% Declare predicates as dynamic
:- dynamic male/1.
:- dynamic female/1.
:- dynamic parent/2.
:- dynamic sibling/2.



% Rules for family relationships
father(X, Y) :- parent(X, Y), male(X),
     X \= Y.

mother(X, Y) :- parent(X, Y), female(X), 
    X\= Y.

sibling(X, Y) :- 
    parent(Z, X), parent(Z, Y), 
    parent(T, X), 
    (parent(T, Y) ; \+ parent(T, Y), parent(Z, Y)),
    Z \= T, 
    X \= Y.

brother(X, Y) :- sibling(X, Y), male(X), X \= Y.
sister(X, Y) :- sibling(X, Y), female(X), X \= Y.

grandparent(X, Y) :- parent(X, Z), parent(Z, Y).
grandchild(X, Y) :- grandparent(Y, X).

uncle(X, Y) :- parent(Z, Y), sibling(X, Z), male(X).
aunt(X, Y) :- parent(Z, Y), sibling(X, Z), female(X).

nephew(X, Y) :- sibling(Z, Y), parent(Z, X), male(X).
niece(X, Y) :- sibling(Z, Y), parent(Z, X), female(X).



% Validation rule: prevent contradictions
impossible :- fail.
