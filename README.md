Zeller
------

FirstJeudi detector based on Zeller's congruence.

Install dependencies:

    pip install --user -r requirements.txt

Then:

    make examples

Lack a bunch of countries support and fail to recognize First Jeudi occuring
after the 7 of a month.

Better implementation
=====================

See BSD ncal for a nice calendar. A valid Julian calendar for France:

	$ ncal -J -s FR 12 1582
		December 1582
	Mo     3 20 27
	Tu     4 21 28
	We     5 22 29
	Th     6 23 30
	Fr     7 24 31
	Sa  1  8 25
	Su  2  9 26

In Great Britain:

	$ ncal -J -s GB 09 1752
		September 1752
	Mo    18 25
	Tu  1 19 26
	We  2 20 27
	Th 14 21 28
	Fr 15 22 29
	Sa 16 23 30
	Su 17 24

References
==========

https://en.wikipedia.org/wiki/Zeller%27s_congruence
https://en.wikipedia.org/wiki/Inter_gravissimas
https://en.wikipedia.org/wiki/Gregorian_calendar
https://en.wikipedia.org/wiki/Old_Style_and_New_Style_dates
