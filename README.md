# readingjournal

## Toiminnot

* Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
* Käyttäjä pystyy lisäämään sovellukseen kirjoja. Lisäksi käyttäjä pystyy muokkaamaan ja poistamaan lisäämiään kirjoja.
* Käyttäjä pystyy lisäämään kuvia kirjoihin.
* Käyttäjä näkee sovellukseen lisätyt kirjat. Käyttäjä näkee sekä itse lisäämänsä että muiden käyttäjien lisäämät kirjat.
* Käyttäjä pystyy etsimään kirjoja hakusanalla tai muulla perusteella. Käyttäjä pystyy hakemaan sekä itse lisäämiään että muiden käyttäjien lisäämiä kirjoja.
* Sovelluksessa on käyttäjäsivut, jotka näyttävät jokaisesta käyttäjästä tilastoja ja käyttäjän lisäämät kirjat.
* Käyttäjä pystyy valitsemaan kirjalle yhden tai useamman luokittelun (esim. genre, kirjamuoto). Mahdolliset luokat ovat tietokannassa.
* Sovelluksessa on pääasiallisen tietokohteen lisäksi toissijainen tietokohde, joka täydentää pääasiallista tietokohdetta. Käyttäjä pystyy lisäämään kommentteja omiin ja muiden käyttäjien kirjoihin liittyen.

## Testaus

Lataa sovellus omalle koneelle

```
git clone git@github.com:shuy-fu/readingjournal.git
```

Siirry hakemistoon

```
cd readingjournal
```

Luo virtuaaliympäristö
```
python -m venv venv
```

Aktivoi virtuaaliympäristö
```
venv\Scripts\activate
```

Asenna flask kirjasto

```
pip install flask
```

Käynnistä sovellus

```
flask run
```