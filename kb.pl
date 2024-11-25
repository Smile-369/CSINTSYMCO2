% Declare predicates as dynamic
:- dynamic male/1.
:- dynamic female/1.
:- dynamic parent/2.

% Rules for family relationships
father(X, Y) :- parent(X, Y), male(X).
mother(X, Y) :- parent(X, Y), female(X).

assume_second_parent(X, Y) :- 
    sibling(X, Y),
    parent(P, X), 
    parent(P, Y), 
    not(parent(P2, X)), 
    not(parent(P2, Y)),
    assert(parent(P2, X)), 
    assert(parent(P2, Y)).

sibling(X, Y) :- parent(Z, X), parent(Z, Y), X \= Y.
brother(X, Y) :- sibling(X, Y), male(X).
sister(X, Y) :- sibling(X, Y), female(X).

grandparent(X, Y) :- parent(X, Z), parent(Z, Y).
grandchild(X, Y) :- grandparent(Y, X).

uncle(X, Y) :- parent(Z, Y), sibling(X, Z), male(X).
aunt(X, Y) :- parent(Z, Y), sibling(X, Z), female(X).

nephew(X, Y) :- sibling(Z, Y), parent(Z, X), male(X).
niece(X, Y) :- sibling(Z, Y), parent(Z, X), female(X).

% Validation rule: prevent contradictions
impossible :- fail.
