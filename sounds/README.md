Becky Sound Prompts
===================

This directory is a placeholder for all of becky's sound prompts. A prompt
is a short audio message explaining to the caller what actions he can do.

Unfortunately, due to copyright issues, I cannot freely redistribute the
original sound prompts from the show. However, there's nothing stopping you
from making your own.  You can even contribute your own prompts and help
make becky better ! Please read the section on contributions for more details.

Recording the prompts
=====================

Find yourself someone with a nice telephone-ish voice and start recording ! The
list of files that you need to record can be found towards the end of this
README. Ideally, the recordings should not contain any background noise. Also,
make sure to trim any silence at the beginning and end.

Sound files must be in a format that asterisk can use. The easiest is to create
16-bit WAV files, mono, 8000 Hz. If you have sox installed, you can convert files
with the following command:

    sox inputfile -c 1 -r 8000 outputfile.wav

Contributing
============

Becky does not have a set of default sound prompts, which is a bit of a shame
for anyone wanting to install becky on their own servers. So, anyone wanting to
contribute their own set of prompts is very welcome to do so :) I would also be
interested if anyone would like to record prompts in english, or any other
language for that matter. Becky could become international !

All that I ask is that you release your recordings using a license that is permissive
enough to let me redistribute the files alongside this project. I highly
encourage using a [Create Commons License](http://creativecommons.org/licenses/by/4.0/)
if you don't know which one to use.

List of propmts
===============

Here is a list of file names and the sentences they contain. I've also included
the original french sentences, since that's becky's native language ;)

* 10secs

    *This file is just becky counting from 1 to 10*

* confirm-message

    French: Si vous êtes satisfait de votre message faites le 1. Si vous
    voulez recommencer faites le 2.

    English: If you are satisfied with your message press 1. To start again
    press 2.

* confirm-more-time

    French : Faites le 5 si vous voulez 10 secondes à fin de faire le 3
    parce-que vous avez fait le 2 ou faites le 6 pour 10 secondes pour faire le
    4 si vous avez fait le 1 parce-que vous vouliez faire le 2. Faites le 7
    pour recommencer, le 8 pour ré-entendre ces choix de nouveau, ou le 9 pour
    ne pas reécouter ces choix.

    English: Press 5 if you would like 10 more seconds to go press 3 because
    you have pressed 2 or press 6 for 10 more seconds to go press 4 if you have
    pressed 1 because you wanted to press 2. Press 7 to start over again, 8 to
    hear these choices once more, or 9 to stop listening to these choices.

* confirm-name

    French: Pour choisir ce nom faites le carré. Pour recommencer faites
    l'étoile.

    English: To choose this name press pound. To start again press star.

* confirm-satisfied-press-1

    French: Si vous êtes satisfait d'avoir fait le 2, faites le 1

    English: If you are satisfied with having pressed 2, press 2.

* enter-name

    French : Entrez le nom complet via le téléphone

    English : Enter the full name using the keypad

* leave-message

    French: Ici Becky Walters. Je ne suis pas là pour l'instant laissez votre
    message.

    English: You've reached Becky Walters. I am not available for the moment
    please leave a message.

* pressed-1

    French: Vous avez fait le 1

    English : You have pressed 1

* pressed-2

    French: Vous avez fait le 2

    English : You have pressed 2

* pressed-9

    French: Vous avez fait le 9

    English : You have pressed 9

* press-number-complex

    French : Faites le 3 si vous avez fait le 1 parce-que vous êtes satisfait
    de votre message ou faites le 4 si vous avez fait le 1 parce-que vous étiez
    satisfait d'avoir fait le 2 parce-que vous n'étiez pas satisfait de votre
    message

    English: Press 3 if you have pressed 1 because you were satisfied with your
    message or press 4 if you have pressed 1 because you were satisfied with
    pressing 2 because you were not satisfied with your message

* press-star

    French: Faites l'étoile sur le clavier

    English: Press star on the keypad


* said-vignila

    French: Vous avez dit vignila

    English: You have said vignila

* say-name

    French: Dites le nom de la personne à qui vous désirez parler

    English: Say the name of the person you wish to speak with

* spelled-wakete

    French: Vous avez épelé wakete

    English: You have typed wakete

* time-out

    French: Votre temps est écoulé

    English: You have run out of time

* wakete-explanation

    French: Le wakete est un animal aquatique nocturne.

    English: The wakete is an aquatic night animal.
