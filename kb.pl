% Declare predicates as dynamic
:- dynamic male/1.
:- dynamic female/1.
:- dynamic parent/2.
:- dynamic sibling/2.
:- dynamic pibling/2.
:- dynamic grandparent/2.
:- dynamic grandchild/2.
:- dynamic nibling/2.
:- dynamic child/2.


% Rules for family relationships
child(X, Y) :- parent(Y, X).
father(X, Y) :- parent(X, Y), male(X), X \= Y.
mother(X, Y) :- parent(X, Y), female(X), X \= Y.

sibling(X, Y) :-
    parent(Z, X), parent(Z, Y),  
    X \= Y.

brother(X, Y) :- sibling(X, Y), male(X), X \= Y.
sister(X, Y) :- sibling(X, Y), female(X), X \= Y.


daughter(X,Y) :- parent(Y, X), female(X).
son(X,Y) :- parent(Y, X), male(X).

grandparent(X, Y) :- parent(X, Z), parent(Z, Y), X \= Y.
grandmother(X, Y) :- grandparent(X, Y), female(X), X \= Y.
grandfather(X, Y) :- grandparent(X, Y), male(X), X \= Y.

grandchild(X, Y) :- grandparent(Y, X), X \= Y.
grandson(X, Y) :- grandparent(X, Y), male(X), X \= Y.
granddaughter(X, Y) :- grandparent(X,Y), female(X),X \= Y.

pibling(X, Y) :- parent(Z, Y), sibling(X, Z).
uncle(X, Y) :- pibling(X, Y), male(X).
aunt(X, Y) :- pibling(X, Y), female(X).

nibling(X, Y) :- pibling(Y, X).
nephew(X, Y) :- nibling(X, Y), male(X).
niece(X, Y) :- nibling(X, Y), female(X).


related(X, Y) :-
    father(X, Y);
    mother(X, Y);
    parent(X, Y);
    sibling(X, Y);
    brother(X, Y);
    sister(X, Y);
    child(X, Y);
    son(X, Y);
    daughter(X, Y);
    grandparent(X, Y);
    grandfather(X, Y);
    grandmother(X, Y);
    grandchild(X, Y);
    grandson(X, Y);
    granddaughter(X, Y);
    pibling(X, Y);
    uncle(X, Y);
    aunt(X, Y);
    nibling(X, Y);
    nephew(X, Y);
    niece(X, Y).

relationship(X, Y, father) :- father(X, Y).
relationship(X, Y, mother) :- mother(X, Y).
relationship(X, Y, parent) :- parent(X, Y).
relationship(X, Y, sibling) :- sibling(X, Y).
relationship(X, Y, brother) :- brother(X, Y).
relationship(X, Y, sister) :- sister(X, Y).
relationship(X, Y, grandparent) :- grandparent(X, Y).
relationship(X, Y, grandmother) :- grandmother(X, Y).
relationship(X, Y, grandfather) :- grandfather(X, Y).
relationship(X, Y, grandchild) :- grandchild(X, Y).
relationship(X, Y, uncle/aunt) :- pibling(X, Y).
relationship(X, Y, uncle) :- uncle(X, Y).
relationship(X, Y, aunt) :- aunt(X, Y).
relationship(X, Y, niece/nephew) :- nibling(X, Y).
relationship(X, Y, nephew) :- nephew(X, Y).
relationship(X, Y, niece) :- niece(X, Y).
relationship(X, Y, child) :- child(X,Y).
relationship(X, Y, son) :- son(X, Y).
relationship(X, Y, daughter) :- daughter(X, Y).
relationship(X, Y, grandson) :- grandson(X, Y).
relationship(X, Y, granddaughter) :- granddaughter(X, Y).

% Validation rule: prevent contradictions
impossible :- fail.
