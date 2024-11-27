% Declare predicates as dynamic
:- dynamic male/1.
:- dynamic female/1.
:- dynamic parent/2.
:- dynamic sibling/2.
:- dynamic pibling/2.
:- dynamic grandparent/2.
:- dynamic grandchild/2.
:- dynamic nibling/2.

% Rules for family relationships
father(X, Y) :- parent(X, Y), male(X), X \= Y.

mother(X, Y) :- parent(X, Y), female(X), X \= Y.

sibling(X, Y) :- 
    parent(Z, X), parent(Z, Y), 
    parent(T, X), 
    (parent(T, Y) ; \+ parent(T, Y), parent(Z, Y)),
    Z \= T, 
    X \= Y.

brother(X, Y) :- sibling(X, Y), male(X), X \= Y.
sister(X, Y) :- sibling(X, Y), female(X), X \= Y.

grandparent(X, Y) :- parent(X, Z), parent(Z, Y), X \= Y.
grandmother(X, Y) :- grandparent(X, Y), female(X), X \= Y.
grandfather(X, Y) :- grandparent(X, Y), male(X), X \= Y.
grandchild(X, Y) :- grandparent(Y, X), X \= Y.

pibling(X, Y) :- parent(Z, Y), sibling(X, Z), X \= Y.
uncle(X, Y) :- pibling(X, Y), male(X), X \= Y.
aunt(X, Y) :- pibling(X, Y), female(X), X \= Y.

nibling :- sibling(Z, Y), parent(Z, X), X \= Y.
nephew(X, Y) :- sibling(Z, Y), parent(Z, X), male(X), X \= Y.
niece(X, Y) :- sibling(Z, Y), parent(Z, X), female(X), X \= Y.


relationship(X, Y, father) :- father(X, Y).
relationship(X, Y, mother) :- mother(X, Y).
relationship(X, Y, sibling) :- sibling(X, Y).
relationship(X, Y, brother) :- brother(X, Y).
relationship(X, Y, sister) :- sister(X, Y).
relationship(X, Y, grandparent) :- grandparent(X, Y).
relationship(X, Y, grandmother) :- grandmother(X, Y).
relationship(X, Y, grandfather) :- grandfather(X, Y).
relationship(X, Y, grandchild) :- grandchild(X, Y).
relationship(X, Y, uncle) :- uncle(X, Y).
relationship(X, Y, aunt) :- aunt(X, Y).
relationship(X, Y, nephew) :- nephew(X, Y).
relationship(X, Y, niece) :- niece(X, Y).

% Validation rule: prevent contradictions
impossible :- fail.
