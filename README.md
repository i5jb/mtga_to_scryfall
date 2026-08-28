MTG:Arena -> Scryfall
---------------------

Small tool to extract Alchemy cards from the MTG:Arena database and
format it the format scryfall uses.

Built to help them keep their database up to data with the latest
oracle text.

To build, run ``./build``.

It downloads the latest Arean datafile, the latest scryfall oracle file,
does some preprocessing and computing, then outputs ``arena_digital.json``
and ``scryfall_digital.json``. You can diff those to files to see what
changed.
